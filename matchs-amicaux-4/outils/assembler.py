"""Assemble index.html (vidéo « matchs amicaux 4 » : les vacances de la Toussaint et la nouvelle fonctionnalité, deux joueurs
en maillot FoundClub, l'appli en motion au milieu) à partir de gabarits/ et de calage.json, découpe les extraits de
l'enregistrement d'écran à la bonne vitesse, et écrit sons.json (bruitages).
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html, subprocess, os

DUREE_VIDEO = 21.6333
T = json.load(open("calage.json", encoding="utf-8"))
TEL = round(T["maintenant"] - 0.2, 3)          # le téléphone arrive sur « Maintenant »
RETOUR = round(T["adversaires"] + 0.25, 3)     # retour aux joueurs, sur la coupe de la vidéo d'Adel (15,7 s)
FIN = 21.45                                    # après « … à ton coach »
DUREE_CARTON = 3.0
DUREE = round(FIN + DUREE_CARTON, 2)

# Extraits de l'enregistrement d'écran (secondes de l'enregistrement) et fenêtre visée dans la vidéo
EXTRAITS = [
    ("x-0", 0.0, 2.9, TEL + 0.3, T["amicaux"] - 0.25),             # l'accueil, jusqu'à la carte « Matchs amicaux »
    ("x-1", 2.9, 3.4, T["amicaux"] - 0.25, T["amicaux"] + 0.25),   # « Rechercher » : « + Créer un match amical » (puis figé)
    ("x-2", 3.75, 5.4, T["annonce"] + 0.15, RETOUR),                # la liste : un club, « Proposer un match »
]
SOURCE_ENREG = "medias/enregistrement/enregistrement-30ips.mp4"
# Où tombent les appuis (centre, en px) : l'écran du téléphone commence à (290, 364), à l'échelle 0,5 de l'enregistrement
APPUIS = {"__APPUI_AMICAUX__": (650, 1074), "__APPUI_CREER__": (540, 934), "__APPUI_PROPOSER__": (494, 1152)}

SOUS_TITRES = [
    (0.15, T["2026"] + 0.15, "On est en 2026,"),
    (T["2026"] + 0.15, T["heures"] + 0.05, "et il y a encore des coachs qui galèrent pendant des heures"),
    (T["heures"] + 0.05, T["amical"] + 0.15, "à trouver un match amical."),
    (6.70, T["arrivent"] + 0.05, "Ça tombe bien : les vacances de la Toussaint arrivent,"),
    (T["arrivent"] + 0.05, T["club"] + 0.1, "et on vient d'ouvrir une nouvelle fonctionnalité sur FoundClub."),
    (T["club"] + 0.1, T["amicaux"] + 0.15, "Maintenant, tu peux directement trouver des matchs amicaux"),
    (T["amicaux"] + 0.15, T["adversaires"] + 0.15, "ou publier ta propre annonce pour trouver des adversaires."),
    (15.85, T["match"] + 0.15, "Donc si t'es coach, va sur FoundClub et trouve ton prochain match."),
    (T["match"] + 0.15, T["coach2"] + 0.35, "Et si t'es joueur, envoie cette vidéo à ton coach."),
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
insecable = lambda t: t.replace(" !", " !").replace(" ?", " ?").replace(" :", " :").replace("« ", "« ").replace(" »", " »")
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
src = src.replace("/*T*/", json.dumps(T)).replace("/*ST*/", json.dumps([[round(d, 3), round(f, 3)] for d, f, _ in SOUS_TITRES]))
src = src.replace("/*EXTRAITS*/", json.dumps(extraits_js))
for k, v in remplacements.items():
    src = src.replace(k, v)
assert "__" not in src.replace("__timelines", ""), "repère non remplacé"
open("index.html", "w", encoding="utf-8").write(src)

# ── Bruitages (outils/sons.py), aux mêmes instants que scenes.js ──
X = extraits_js
S = [
    (T["2026"] - 0.21, "impact", -7), (T["2026"] - 0.21, "secousse", -2),   # ouverture douce (« réduit le premier sound design », Adel, vidéo 2)
    (T["coachs"] - 0.7, "souffle", 0), (T["coachs"] - 0.6, "swish", 0), (T["heures"] - 0.55, "zip", 0), (T["amical"] - 0.3, "secousse", 0),
    (T["tombe"] - 0.65, "souffle", 0), (T["toussaint"] - 0.75, "pop", 0, 0), (T["arrivent"] + 0.45, "souffle", -2),
    (T["fonctionnalite"] - 0.75, "pop", 0, 4), (T["fonctionnalite"] - 0.35, "pop", 0, 0), (T["club"] - 0.45, "impact", -4), (T["club"] - 0.05, "scintille", 0),
    (TEL, "whoosh", -3), (TEL + 0.15, "swish", 0), (TEL + 0.45, "swish", -3), (TEL + 0.85, "swish", -4),
] + [(x["debut"], "tick", 0) for x in X[1:]] + [
    (T["amicaux"] - 0.5, "pop", 0, 0), (T["amicaux"] - 0.45, "tap", 0), (T["annonce"] - 0.6, "pop", 0, 4), (T["annonce"] - 0.25, "tap", 0),
    (X[2]["debut"] - 0.1, "souffle", 0), (X[2]["debut"] + 0.1, "pop", 0, 2), (X[2]["debut"] + X[2]["duree"] - 0.3, "tap", 0),
    (RETOUR, "whoosh", -4), (T["coach"] - 0.5, "swish", 0), (T["match"] - 0.6, "zip", 0),
    (T["joueur"] - 0.6, "souffle", 0), (T["video"] - 0.75, "pop", 0, 2), (T["coach2"] - 0.2, "secousse", 0),
    (FIN, "whoosh", -2), (FIN + 0.25, "impact", -3), (FIN + 0.9, "scintille", 0), (FIN + 1.05, "pop", -2, 4),
]
# La voix est enregistrée à -16,3 LUFS, 4,6 dB sous celle d'ach10 sur laquelle les niveaux ont été validés
GAIN_SONS = -4.5
sons = [{"t": round(s[0], 3), "son": s[1], "db": s[2] + GAIN_SONS, **({"note": s[3]} if len(s) > 3 else {})} for s in sorted(S, key=lambda s: s[0])]
json.dump(sons, open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"index.html : {len(src)} caractères, {len(SOUS_TITRES)} sous-titres, {len(EXTRAITS)} extraits, {len(sons)} bruitages ; "
      f"téléphone {TEL:.2f}-{RETOUR:.2f} s, carton à {FIN:.2f} s, durée {DUREE:.2f} s")
