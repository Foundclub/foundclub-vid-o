"""Monte l'épisode à partir de papier.json, séquence par séquence.

Pour chaque phrase : l'image et le son du rush entre ses deux instants, élargis d'une respiration prise dans le
silence (jamais sur le mot d'avant ou d'après), les plans de coupe posés par-dessus (la voix continue), le son
ramené à -16 LUFS par rush (le réglage fin à -14 LUFS se fait à la finition).
Les « images » sont un plan sans parole (drone), un extrait d'un fichier (« source », relatif à TRAVAIL) ou une
carte provisoire (« carte » : texte blanc sur l'image ou sur fond noir, remplacé à la finition).

Sortie : TRAVAIL/montage/seq-NN.mp4 (l'instant de l'épisode écrit en haut à droite), seq-NN.jpg (planche),
brouillon.mp4 (tout l'épisode) et montage.json (où commence chaque séquence).

Avec --final : depuis les rushs d'origine, en 1920×1080, dans TRAVAIL/final ; pas d'aperçu ni d'instant écrit,
seulement les séquences sNN.mkv et montage.json (où tombe chaque pièce), que outils/finir.py habille.

python -I outils/monter.py [--final] [numéros de séquences…]      (sans numéro : toutes)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parents[1]
TRAVAIL = Path(r"D:\App\video\rushs\interview\travail")
RUSHS = Path(r"D:\Foundclub média\ACh")
FINAL = "--final" in sys.argv
SORTIE = TRAVAIL / ("final" if FINAL else "montage")
PIECES = SORTIE / "pieces"
L, H, IPS = (1920, 1080, "30000/1001") if FINAL else (1280, 720, "30000/1001")
VIDEO = ["-c:v", "libx264", "-preset", "fast" if FINAL else "veryfast", "-crf", "17" if FINAL else "20",
         "-pix_fmt", "yuv420p", "-r", IPS]
NOIR_ET_BLANC = "hue=s=0,eq=contrast=1.12"
SON = ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"]
POLICE = "C\\:/Windows/Fonts/arialbd.ttf"
CIBLE_LUFS = -16.0
RESPIRE_AVANT, RESPIRE_APRES = 0.12, 0.25

papier = json.loads((ICI / "papier.json").read_text(encoding="utf-8"))


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", *args], check=True)


def duree(chemin):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(chemin)], capture_output=True, text=True, check=True).stdout)


def proxy(rush):
    return TRAVAIL / "proxies" / f"{rush}.mp4"


def source(rush):
    """Le fichier lu pour l'image et le son : la copie légère, ou le rush d'origine en --final."""
    return next(RUSHS.glob(f"{rush}.*")) if FINAL else proxy(rush)


def entree(rush, debut, longueur):
    decode = ["-hwaccel", "cuda"] if FINAL else []
    return [*decode, "-ss", f"{debut:.3f}", "-t", f"{longueur:.3f}", "-i", str(source(rush))]


def echappe(chemin):
    return str(chemin).replace("\\", "/").replace(":", "\\:")


_mots, _niveaux = {}, None


def bornes(rush, debut, fin):
    """Élargit la coupe d'une respiration, sans mordre sur le mot voisin."""
    if rush not in _mots:
        _mots[rush] = json.loads((TRAVAIL / "transcriptions" / f"{rush}-mots.json").read_text(encoding="utf-8"))
    avant = [m["fin"] for m in _mots[rush] if m["fin"] <= debut + 0.02]
    apres = [m["debut"] for m in _mots[rush] if m["debut"] >= fin - 0.02]
    d = max(debut - RESPIRE_AVANT, (max(avant) + 0.02) if avant else 0.0, 0.0)
    f = min(fin + RESPIRE_APRES, (min(apres) - 0.03) if apres else fin + RESPIRE_APRES, duree(proxy(rush)))
    return min(d, debut), max(f, fin)


def gain(rush):
    """dB à appliquer au rush pour l'amener vers -16 LUFS (mesure intégrée, gardée en cache)."""
    global _niveaux
    cache = TRAVAIL / "niveaux.json"
    if _niveaux is None:
        _niveaux = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
    if rush not in _niveaux:
        err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(TRAVAIL / "son48" / f"{rush}.wav"),
                              "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace").stderr
        _niveaux[rush] = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
        cache.write_text(json.dumps(_niveaux, indent=2) + "\n", encoding="utf-8")
    return max(-12.0, min(10.0, CIBLE_LUFS - _niveaux[rush]))


def carte_texte(texte, nom):
    f = PIECES / f"{nom}.txt"
    f.write_text(texte, encoding="utf-8")
    return (f"drawtext=fontfile='{POLICE}':textfile='{echappe(f)}':fontcolor=white:fontsize=64"
            ":x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.55:boxborderw=24")


# Zooms en tribune (plan fixe) : cadre serré 1,25× sur celui qui parle, coin haut-gauche en pixels 1920×1080
ZOOM = 1.25
CADRES = {"DJI_20261026185942_0009_D": {"moussa": (48, 130), "achraf": (384, 197)},
          "DJI_20261026190240_0010_D": {"moussa": (125, 169), "achraf": (384, 121)}}
PLAN_MIN, SERRE_MAX, LARGE_PAUSE = 2.0, 7.0, 4.0
_voix = {}


def plans_serres(rush, d, f):
    """[(début, fin, qui)] en temps de la pièce : serré sur qui parle ≥ 2 s ; une longue réponse respire en large."""
    if rush not in _voix:
        par_phrase = json.loads((TRAVAIL / "voix" / f"{rush}.json").read_text(encoding="utf-8"))
        _voix[rush] = {k: q for voix in par_phrase.values() for k, q in voix.items()}
    tours = []
    for k, m in enumerate(_mots[rush]):
        qui = _voix[rush].get(str(k))
        if qui in ("achraf", "moussa") and d <= m["debut"] < f:
            if tours and tours[-1][2] == qui and m["debut"] - tours[-1][1] < 1.0:
                tours[-1][1] = m["fin"]
            else:
                tours.append([m["debut"], m["fin"], qui])
    plans = []
    for a, b, qui in tours:
        t = a
        while b - t >= PLAN_MIN:
            fin = min(b, t + SERRE_MAX) if b - t > SERRE_MAX + PLAN_MIN else b
            plans.append((t - d, fin - d, qui))
            t = fin + LARGE_PAUSE
    return plans


def zooms(rush, d, f):
    """Morceau de graphe qui remplace [v0] par [v0z] avec les plans serrés ; « » s'il n'y a rien à zoomer."""
    plans = plans_serres(rush, d, f) if rush in CADRES else []
    if not plans:
        return [], "v0"
    k = L / 1920
    w, h = round(L / ZOOM / 2) * 2, round(H / ZOOM / 2) * 2
    g = ["[v0]split=3[zl][zm][za]"]
    avant = "zl"
    for qui in ("moussa", "achraf"):
        fen = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b, q in plans if q == qui)
        if not fen:
            g.append(f"[z{qui[0]}]nullsink")
            continue
        x, y = (round(v * k) for v in CADRES[rush][qui])
        g += [f"[z{qui[0]}]crop={w}:{h}:{x}:{y},scale={L}:{H},setsar=1[c{qui[0]}]",
              f"[{avant}][c{qui[0]}]overlay=enable='{fen}'[s{qui[0]}]"]
        avant = f"s{qui[0]}"
    g.append(f"[{avant}]null[v0z]")
    return g, "v0z"


def piece_parole(p, nom, effet=None):
    d, f = bornes(p["rush"], p["debut"], p["fin"])
    longueur = f - d
    entrees = entree(p["rush"], d, longueur)
    graphe = [f"[0:v]scale={L}:{H},setsar=1,setpts=PTS-STARTPTS[v0]"]
    g, base = zooms(p["rush"], d, f)
    graphe += g
    for i, c in enumerate(p.get("plans", []), 1):
        lc = c["fin"] - c["debut"]
        decal = c["a"] + (p["debut"] - d)
        quand = f"between(t,{decal:.3f},{decal + lc:.3f})"
        avant = base if i == 1 else f"v{i - 1}"
        if c.get("telephone"):  # vidéo verticale (TikTok) au milieu, sur l'image floutée, avec le compte à côté
            entrees += ["-ss", f"{c['debut']:.3f}", "-t", f"{lc:.3f}", "-i", str(TRAVAIL / c["source"])]
            hv = round(H * 0.84 / 2) * 2
            graphe += [f"[{i}:v]scale=-2:{hv},setsar=1,fps={IPS},pad=iw+12:ih+12:6:6:white,"
                       f"setpts=PTS-STARTPTS+{decal:.3f}/TB[c{i}]",
                       f"[{avant}]split[n{i}][b{i}]", f"[b{i}]gblur=sigma=30,eq=brightness=-0.15[f{i}]",
                       f"[n{i}][f{i}]overlay=enable='{quand}'[g{i}]",
                       f"[g{i}][c{i}]overlay=x=(W-w)/2:y=(H-h)/2-{round(H * 0.04)}:eof_action=pass:enable='{quand}',"
                       f"drawtext=fontfile='{POLICE}':text='TikTok @moussaldz34':fontcolor=white:fontsize={round(H / 24)}"
                       f":x=w/2+{round(hv * 9 / 32) + 40}:y=h*0.42:borderw=3:bordercolor=black:enable='{quand}'[v{i}]"]
            continue
        entrees += entree(c["rush"], c["debut"], lc)
        graphe += [f"[{i}:v]scale={L}:{H},setsar=1,fps={IPS},setpts=PTS-STARTPTS+{decal:.3f}/TB[c{i}]",
                   f"[{avant}][c{i}]overlay=eof_action=pass:enable='{quand}'[v{i}]"]
    n = len(p.get("plans", []))
    graphe.append(f"[{f'v{n}' if n else base}]{NOIR_ET_BLANC if effet == 'noir et blanc' else 'null'}[vo]")
    graphe.append(f"[0:a]aresample=48000,volume={gain(p['rush']):.1f}dB,afade=t=in:d=0.02,"
                  f"afade=t=out:st={longueur - 0.03:.3f}:d=0.03,alimiter=limit=0.89:level=0[a]")
    sortie = PIECES / f"{nom}.mkv"
    ffmpeg(*entrees, "-filter_complex", ";".join(graphe), "-map", "[vo]", "-map", "[a]",
           "-t", f"{longueur:.3f}", *VIDEO, *SON, str(sortie))
    return sortie, d


def piece_image(im, nom):
    longueur = im["fin"] - im["debut"]
    texte = f",{carte_texte(im['carte'], nom)}" if im.get("carte") else ""
    if "rush" in im:
        entrees = entree(im["rush"], im["debut"], longueur)
    elif "source" in im:
        entrees = ["-ss", f"{im['debut']:.3f}", "-t", f"{longueur:.3f}", "-i", str(TRAVAIL / im["source"])]
    else:
        entrees = ["-f", "lavfi", "-t", f"{longueur:.3f}", "-i", f"color=black:s={L}x{H}:r={IPS}"]
    a_son = "source" in im  # les drones et les cartes sont muets ; un extrait garde son son
    entrees += [] if a_son else ["-f", "lavfi", "-t", f"{longueur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    graphe = (f"[0:v]scale={L}:{H},setsar=1,fps={IPS},setpts=PTS-STARTPTS{texte}[v];"
              + ("[0:a]aresample=48000,afade=t=in:d=0.05[a]" if a_son else "[1:a]anull[a]"))
    sortie = PIECES / f"{nom}.mkv"
    ffmpeg(*entrees, "-filter_complex", graphe, "-map", "[v]", "-map", "[a]", "-t", f"{longueur:.3f}",
           *VIDEO, *SON, str(sortie))
    return sortie


def hms(s):
    return f"{int(s // 3600)}:{int(s // 60) % 60:02}:{s % 60:04.1f}"


SORTIE.mkdir(parents=True, exist_ok=True)
PIECES.mkdir(exist_ok=True)
choisies = {int(x) for x in sys.argv[1:] if x != "--final"}
journal_f = SORTIE / "montage.json"
journal = json.loads(journal_f.read_text(encoding="utf-8")) if journal_f.exists() else {}

# fabriquer les pièces des séquences demandées ; noter où tombe chaque phrase (pour les sous-titres et bandeaux)
for n, seq in enumerate(papier["sequences"]):
    if choisies and n not in choisies:
        continue
    pieces, faites = [], []
    for i, p in enumerate(seq["paroles"]):
        fichier, d = piece_parole(p, f"s{n:02}-p{i:02}", seq.get("effet"))
        pieces.append(fichier)
        faites.append({"parole": i, "rush": p["rush"], "coupe": round(d, 3), "duree": round(duree(fichier), 3)})
    for i, im in enumerate(seq.get("images", [])):
        pieces.append(piece_image(im, f"s{n:02}-i{i:02}"))
        faites.append({"image": i, "duree": round(duree(pieces[-1]), 3)})
    liste = PIECES / f"s{n:02}.txt"
    liste.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces), encoding="utf-8")
    ffmpeg("-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(PIECES / f"s{n:02}.mkv"))
    journal[str(n)] = {"titre": seq["titre"], "duree": round(duree(PIECES / f"s{n:02}.mkv"), 3), "pieces": faites}
    print(f"séquence {n} : {journal[str(n)]['duree']:.1f} s", flush=True)

# l'instant de chaque séquence dans l'épisode, puis les aperçus avec l'instant écrit dessus
t = 0.0
for n in range(len(papier["sequences"])):
    if str(n) not in journal:
        break
    journal[str(n)]["debut"] = round(t, 3)
    if not FINAL and (not choisies or n in choisies):
        src, apercu = PIECES / f"s{n:02}.mkv", SORTIE / f"seq-{n:02}.mp4"
        ffmpeg("-i", str(src), "-vf",
               f"drawtext=fontfile='{POLICE}':text='%{{pts\\:hms\\:{t:.3f}}}':x=w-text_w-16:y=12:fontsize=26"
               ":fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=6",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(apercu))
        pas = max(2.0, journal[str(n)]["duree"] / 40)
        lignes = max(1, -(-int(journal[str(n)]["duree"] // pas + 1) // 8))
        ffmpeg("-i", str(apercu), "-vf", f"fps=1/{pas:.3f},scale=320:-2,tile=8x{lignes}:padding=4",
               "-frames:v", "1", "-q:v", "4", str(SORTIE / f"seq-{n:02}.jpg"))
    t += journal[str(n)]["duree"]
journal_f.write_text(json.dumps(journal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

complet = [SORTIE / f"seq-{n:02}.mp4" for n in range(len(papier["sequences"])) if (SORTIE / f"seq-{n:02}.mp4").exists()]
if not FINAL and len(complet) == len(papier["sequences"]):
    liste = SORTIE / "brouillon.txt"
    liste.write_text("".join(f"file '{p.as_posix()}'\n" for p in complet), encoding="utf-8")
    ffmpeg("-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", "-movflags", "+faststart",
           str(SORTIE / "brouillon.mp4"))
    print(f"brouillon.mp4 : {hms(duree(SORTIE / 'brouillon.mp4'))}")
print(f"épisode : {hms(t)}")
