"""Assemble index.html (vidéo FoundClub 03/20 « Le week-end gâché » : ach10 sur son canapé,
l'appli des matchs amicaux dans le téléphone, le carton final ; l'ouverture en mème a été retirée le 28/10) à partir de gabarits/ et de calage.json, découpe les extraits
de l'enregistrement d'écran à la bonne vitesse, et écrit sons.json (bruitages).
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet, après outils/preparer-video.sh)"""
import json, html, subprocess, os

DUREE_VIDEO = 29.2667
T = json.load(open("calage.json", encoding="utf-8"))
TEL = T["d"]                 # le téléphone arrive sur « Sur FoundClub »
RETOUR = T["e"]              # retour à ach10 sur « Envoie-lui la vidéo »
FIN = T["fin_video"]         # après « … jouer un petit peu »
DUREE_CARTON = 3.0
DUREE = round(FIN + DUREE_CARTON, 2)

# Extraits de l'enregistrement d'écran (celui des vidéos matchs amicaux 3 et 4) et fenêtre visée dans la vidéo
EXTRAITS = [
    ("x-0", 0.0, 2.9, TEL + 0.3, TEL + 2.0),            # l'accueil, jusqu'à la carte « Matchs amicaux »
    ("x-1", 3.75, 5.4, TEL + 2.0, T["disponibles"] + 0.4),  # « visualiser les matchs disponibles » : la liste
    ("x-2", 2.9, 3.4, T["disponibles"] + 0.4, T["creer"] - 0.1),  # « créer son propre match » : « + Créer un match amical » (puis figé)
]
SOURCE_ENREG = "medias/enregistrement/enregistrement-30ips.mp4"
# Où tombent les appuis (centre, en px) : l'écran du téléphone commence à (290, 364), à l'échelle 0,5 de l'enregistrement
APPUIS = {"__APPUI_AMICAUX__": (650, 1074), "__APPUI_CREER__": (540, 934)}

SOUS_TITRES = [
    (T["a"], T["but"] + 0.05, "Toute la semaine, j'ai visualisé mon but,"),
    (T["but"] + 0.05, T["celebration"] + 0.1, "ma célébration,"),
    (T["celebration"] + 0.1, T["reseaux"] + 0.5, "le post que j'allais mettre sur les réseaux sociaux…"),
    (T["reseaux"] + 0.5, T["repos"] + 0.15, "Et là : repos."),
    (T["b"], T["encore"] + 0.15, "Encore."),
    (T["encore"] + 0.15, T["sac"] + 0.1, "Bientôt, je vais être meilleur à préparer mon sac de foot"),
    (T["sac"] + 0.1, T["frappes"] + 0.2, "qu'à faire des frappes !"),
    (T["c"], T["arreter"] + 0.15, "Mais on peut arrêter ça."),
    (T["arreter"] + 0.15, T["amical"] + 0.1, "On peut essayer de trouver un match amical"),
    (T["amical"] + 0.1, T["d"] - 0.05, "chaque week-end où il n'y a pas match."),
    (T["d"], T["club"] + 0.2, "Sur FoundClub,"),
    (T["club"] + 0.2, T["disponibles"] + 0.1, "ton coach peut visualiser les matchs disponibles"),
    (T["disponibles"] + 0.1, T["e"] - 0.05, "ou même créer son propre match."),
    (T["e"], T["video"] + 0.25, "Envoie-lui la vidéo, s'il te plaît,"),
    (T["video"] + 0.25, T["saigne"] + 0.15, "parce que ça y est, le canapé, je l'ai saigné…"),
    (T["saigne"] + 0.15, FIN, "J'ai envie de jouer un petit peu !"),
]

def couper(nom, deb, fin, duree):
    sortie = f"medias/enregistrement/{nom}.mp4"
    vitesse = (fin - deb) / duree
    attendu = f"{deb}-{fin}-{duree:.3f}"
    marque = sortie + ".info"
    if os.path.exists(sortie) and os.path.exists(marque) and open(marque).read() == attendu:
        return vitesse
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(deb), "-t", str(fin - deb), "-i", SOURCE_ENREG,
                    "-vf", f"setpts=PTS/{vitesse:.4f},fps=30", "-an", "-c:v", "libx264", "-crf", "16", "-g", "15",
                    "-pix_fmt", "yuv420p", "-t", f"{duree:.3f}", sortie], check=True)
    open(marque, "w").write(attendu)
    return vitesse

extraits_js, extraits_html = [], []
for nom, deb, fin, debut, fin_cible in EXTRAITS:
    debut, duree = round(debut, 3), round(fin_cible - debut, 3)
    v = couper(nom, deb, fin, duree)
    extraits_js.append({"debut": debut, "duree": duree})
    extraits_html.append(f'            <div id="{nom}" class="extrait"><video id="v-{nom}" src="medias/enregistrement/{nom}.mp4" muted playsinline '
                         f'data-start="{debut:.3f}" data-duration="{duree:.3f}" data-track-index="5"></video></div>')
    print(f"{nom} : {deb}-{fin} s de l'enregistrement -> {debut:.2f}-{debut + duree:.2f} s (vitesse x{v:.2f})")

# espaces insécables de la typographie française : « ! », « ? », « : » et les guillemets ne partent jamais seuls à la ligne
insecable = lambda t: t.replace(" !", " !").replace(" ?", " ?").replace(" :", " :").replace("« ", "« ").replace(" »", " »")
remplacements = {
    "__DUREE_VIDEO__": f"{DUREE_VIDEO:.4f}", "__TEL__": f"{TEL:.3f}", "__RETOUR__": f"{RETOUR:.3f}", "__FIN__": f"{FIN:.3f}",
    "__DUREE_CARTON__": f"{DUREE_CARTON:.2f}", "__DUREE__": f"{DUREE:.2f}",
    **{k: f"{x}px; top: {y}px" for k, (x, y) in APPUIS.items()},
}
lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
src = lire("index.gabarit.html")
src = src.replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--EXTRAITS-->", "\n".join(extraits_html))
src = src.replace("<!--SOUSTITRES-->", "\n".join(f'        <p id="st-{i}" class="st">{html.escape(insecable(t))}</p>' for i, (_, _, t) in enumerate(SOUS_TITRES)))
for i, (d, f, t) in enumerate(SOUS_TITRES):
    assert f > d + 0.3, f"sous-titre {i} trop court : {t}"
src = src.replace("/*T*/", json.dumps(T)).replace("/*ST*/", json.dumps([[round(d, 3), round(f, 3)] for d, f, _ in SOUS_TITRES]))
src = src.replace("/*EXTRAITS*/", json.dumps(extraits_js))
for k, v in remplacements.items():
    src = src.replace(k, v)
assert "__" not in src.replace("__timelines", ""), "repère non remplacé"
open("index.html", "w", encoding="utf-8").write(src)

# ── Bruitages (outils/sons.py), aux mêmes instants que scenes.js ──
X = extraits_js
# Peu de sons, et des bruits du monde réel (Adel, 28/10 : les mêmes pops et whooshs partout faisaient « IA ») :
# un sticker qui se plaque, le tampon et la bande qui s'arrête sur « repos », la vibration du téléphone, les clics de l'appli.
# Les titres n'ont pas de son.
S = [
    (T["but"] - 0.55, "sticker", 0), (T["celebration"] - 0.75, "sticker", -1), (T["reseaux"] - 1.4, "sticker", -2),
    (T["repos"] - 0.42, "arret", 0), (T["repos"] - 0.3, "tampon", 0), (T["encore"] - 0.15, "tampon", -2),
    (TEL - 0.05, "vibre", 0),
    (X[0]["debut"] + X[0]["duree"] - 0.45, "clic", 0), (X[1]["debut"] + 0.25, "sticker", -3), (X[2]["debut"], "sticker", -3),
    (T["creer"] - 0.3, "clic", 0),
    (T["video"] - 0.7, "sticker", 0),
    (FIN + 0.25, "tampon", -6),
]
# La voix est enregistrée à -21,5 LUFS, 9,8 dB sous celle d'ach10 sur laquelle les niveaux ont été validés
GAIN_SONS = -9.5
sons = [{"t": round(s[0], 3), "son": s[1], "db": s[2] + GAIN_SONS, **({"note": s[3]} if len(s) > 3 else {})} for s in sorted(S, key=lambda s: s[0])]
json.dump(sons, open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"index.html : {len(src)} caractères, {len(SOUS_TITRES)} sous-titres, {len(EXTRAITS)} extraits, {len(sons)} bruitages ; "
      f"téléphone {TEL:.2f}-{RETOUR:.2f} s, carton à {FIN:.2f} s, durée {DUREE:.2f} s")
