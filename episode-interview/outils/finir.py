"""Habille et finit les séquences montées en --final : sous-titres, bandeaux, « Dans cet épisode.. », son à -14 LUFS.

Lit TRAVAIL/final/montage.json (où tombe chaque phrase), papier.json (bandeaux, effets) et sous-titres.json
(corrections). Les sous-titres viennent des transcriptions mot à mot : blancs en bas, sans fond, comme l'épisode #42 ;
une phrase s'éteint avant que la suivante arrive ; ils remontent quand un bandeau est à l'écran.
Le son : gain mesuré vers -14 LUFS, puis la chaîne de METHODE_MONTAGE.md §4 (limiteur à 192 kHz).

Sortie : TRAVAIL/final/<nom>.mp4 et <nom>.ass ; la liste des mots douteux s'affiche pour relecture.

python -I outils/finir.py <nom> [numéros de séquences consécutifs…]      (sans numéro : toutes)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parents[1]
TRAVAIL = Path(r"D:\App\video\rushs\interview\travail")
FINAL = TRAVAIL / "final"
HABILLAGE = TRAVAIL / "habillage"
IPS = "30000/1001"
CIBLE_LUFS = -14.0
LIMITEUR = ("afade=t=in:st=0:d=0.05,aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=0:latency=1,"
            "aresample=48000")
BANDEAU_DUREE, FONDU = 4.5, 0.25
SOUS_TITRE_MAX = 68  # caractères : deux lignes au plus

papier = json.loads((ICI / "papier.json").read_text(encoding="utf-8"))
corrections = json.loads((ICI / "sous-titres.json").read_text(encoding="utf-8"))
journal = json.loads((FINAL / "montage.json").read_text(encoding="utf-8"))
nom = sys.argv[1]
choisies = [int(x) for x in sys.argv[2:]] or list(range(len(papier["sequences"])))
t0 = journal[str(choisies[0])]["debut"]


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *args], check=True)


def echappe(chemin):
    return str(chemin).replace("\\", "/").replace(":", "\\:")


def insecable(texte):
    """Typographie française : espace insécable avant ! ? : ; » et après «."""
    texte = re.sub(r"\s*([!?:;»])", "\u00a0\\1", texte)
    return re.sub(r"«\s*", "«\u00a0", texte)


def deux_lignes(texte):
    """Retour à la ligne choisi : lignes équilibrées, de préférence après une virgule, jamais après « le », « d'un »…"""
    mots_ = texte.split(" ")
    if len(texte) <= 42 or len(mots_) < 2:
        return texte
    def cout(k):
        a, b = " ".join(mots_[:k]), " ".join(mots_[k:])
        fin = mots_[k - 1]
        return abs(len(a) - len(b)) - (15 if fin.endswith(",") else 0) + (40 if fin.lower() in FAIBLES else 0)
    k = min(range(1, len(mots_)), key=cout)
    return " ".join(mots_[:k]) + "\\N" + " ".join(mots_[k:])


def ass_temps(s):
    return f"{int(s // 3600)}:{int(s // 60) % 60:02}:{s % 60:05.2f}"


# 1. où tombe chaque mot dit, chaque bandeau et chaque passage en noir et blanc dans la sortie
mots, bandeaux, noir_et_blanc, _cache = [], [], [], {}
for n in choisies:
    seq, j = papier["sequences"][n], journal[str(n)]
    t = j["debut"] - t0
    fin_paroles = t
    for piece in j["pieces"]:
        if "parole" in piece:
            p = seq["paroles"][piece["parole"]]
            if p["rush"] not in _cache:
                _cache[p["rush"]] = json.loads((TRAVAIL / "transcriptions" / f"{p['rush']}-mots.json")
                                               .read_text(encoding="utf-8"))
            for m in _cache[p["rush"]]:
                if p["debut"] - 0.05 <= m["debut"] < p["fin"]:
                    mots.append({**m, "t": t + m["debut"] - piece["coupe"], "tf": t + m["fin"] - piece["coupe"],
                                 "piece": (n, piece["parole"]), "fin_piece": t + piece["duree"]})
            if p.get("bandeau"):
                debut = t + p["debut"] - piece["coupe"] + p["bandeau"]["a"]
                bandeaux.append((HABILLAGE / f"bandeau-{p['bandeau']['nom']}.png", debut, debut + BANDEAU_DUREE))
            fin_paroles = t + piece["duree"]
        t += piece["duree"]
    if seq.get("effet") == "noir et blanc":
        noir_et_blanc.append((HABILLAGE / "dans-cet-episode.png", j["debut"] - t0 + 0.3, fin_paroles - 0.1))

# 2. les sous-titres : une phrase par pause, coupure ou ponctuation forte, deux lignes au plus
def longueur(g):
    return len("".join(x["mot"] for x in g).strip())


FAIBLES = {"d'un", "d'une", "un", "une", "de", "du", "des", "la", "le", "les", "l'", "à", "au", "en", "et", "que",
           "qui", "tout", "ce", "cette", "mon", "ma", "son", "sa", "sous", "pour", "dans", "avec", "il", "je", "tu", "on"}


def decouper(g):
    """Coupe une phrase trop longue : de préférence après une virgule, jamais après un petit mot (« d'un »)."""
    if longueur(g) <= SOUS_TITRE_MAX:
        return [g]
    meilleur, cout = None, None
    for k in range(1, len(g)):
        a, b = longueur(g[:k]), longueur(g[k:])
        fin = g[k - 1]["mot"].strip()
        c = abs(a - b) - (25 if fin.endswith(",") else 0) + (40 if fin.lower() in FAIBLES or re.match(r"\d", fin) else 0)
        if min(a, b) >= 12 and (cout is None or c < cout):
            meilleur, cout = k, c
    if meilleur is None:
        return [g]
    return decouper(g[:meilleur]) + decouper(g[meilleur:])


phrases, cur = [], []
for m in mots:
    if cur and (m["piece"] != cur[-1]["piece"] or m["t"] - cur[-1]["tf"] > 0.6
                or (re.search(r"[.?!]$", cur[-1]["mot"].strip()) and longueur(cur) > 25)):
        phrases.append(cur)
        cur = []
    cur.append(m)
if cur:
    phrases.append(cur)
groupes = [morceau for g in phrases for morceau in decouper(g)]

utilisees = set()
lignes, douteux = [], []
for i, g in enumerate(groupes):
    texte = re.sub(r"\s+", " ", "".join(x["mot"] for x in g)).strip()
    for k, (de, en) in enumerate(corrections["remplacer"]):
        if de in texte:
            texte = texte.replace(de, en)
            utilisees.add(k)
    debut = max(0.0, g[0]["t"] - 0.05)
    fin = min(g[-1]["tf"] + 0.3, g[-1]["fin_piece"])
    if i + 1 < len(groupes):
        fin = min(fin, groupes[i + 1][0]["t"] - 0.09)
    haut = any(b < fin and debut < e for _, b, e in bandeaux)
    lignes.append(f"Dialogue: 0,{ass_temps(debut)},{ass_temps(fin)},Bas,,0,0,0,,"
                  + ("{\\pos(960,850)}" if haut else "") + deux_lignes(insecable(texte)))
    douteux += [f"{ass_temps(x['t'])} « {x['mot'].strip()} » ({x['probabilite']:.2f}) dans : {texte}"
                for x in g if x["probabilite"] < 0.5 and len(x["mot"].strip()) > 3]

ass = FINAL / f"{nom}.ass"
ass.write_text("\n".join([
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
    "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
    "MarginR, MarginV, Encoding",
    "Style: Bas,Segoe UI,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2.6,1.4,2,230,230,"
    "92,1", "",
    "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text", *lignes, ""]),
    encoding="utf-8-sig")

# 3. recoller les séquences, poser l'habillage, régler le son
liste = FINAL / f"{nom}.txt"
liste.write_text("".join(f"file '{(FINAL / 'pieces' / f's{n:02}.mkv').as_posix()}'\n" for n in choisies),
                 encoding="utf-8")
assemble = FINAL / f"{nom}-assemble.mkv"
ffmpeg("-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(assemble))


def niveau(chaine):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(assemble), "-map", "0:a", "-af",
                          f"{chaine}ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


# le limiteur mange une partie du gain : on remesure après lui (son seul, rapide) jusqu'à tomber à ±0,3 dB
gain = CIBLE_LUFS - niveau("")
for _ in range(4):
    ecart = CIBLE_LUFS - niveau(f"volume={gain:.2f}dB,{LIMITEUR},")
    if abs(ecart) < 0.3:
        break
    gain += ecart

calques = noir_et_blanc + bandeaux
entrees = ["-i", str(assemble)]
graphe, avant = [], "0:v"
for k, (png, debut, fin) in enumerate(calques, 1):
    entrees += ["-loop", "1", "-framerate", IPS, "-t", f"{fin + 0.1:.3f}", "-i", str(png)]
    graphe += [f"[{k}:v]format=rgba,fade=t=in:st={debut:.3f}:d={FONDU}:alpha=1,"
               f"fade=t=out:st={fin - FONDU:.3f}:d={FONDU}:alpha=1[c{k}]",
               f"[{avant}][c{k}]overlay=eof_action=pass:enable='between(t,{debut:.3f},{fin:.3f})'[v{k}]"]
    avant = f"v{k}"
graphe.append(f"[{avant}]ass='{echappe(ass)}':fontsdir='C\\:/Windows/Fonts'[v]")
graphe.append(f"[0:a]volume={gain:.2f}dB,{LIMITEUR}[a]")
sortie = FINAL / f"{nom}.mp4"
ffmpeg(*entrees, "-filter_complex", ";".join(graphe), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", IPS,
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(sortie))
assemble.unlink()

print(f"{sortie.name} : {len(lignes)} sous-titres, {len(bandeaux)} bandeau(x), gain {gain:+.1f} dB")
for k, (de, _) in enumerate(corrections["remplacer"]):
    if k not in utilisees:
        print(f"correction non trouvée ici : « {de} »")
print("mots douteux à relire :" if douteux else "aucun mot douteux")
print("\n".join(douteux))
