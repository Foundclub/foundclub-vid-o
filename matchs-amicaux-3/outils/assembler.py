"""Assemble index.html (vidéo « matchs amicaux 3 » : l'extrait « Dimanche prochain je vais jouer », le joueur au maillot
FoundClub, puis la navigation des matchs amicaux dans l'appli) à partir de gabarits/ et de calage.json, découpe les extraits
de l'enregistrement d'écran à la bonne vitesse, et écrit sons.json (bruitages).
calage.json est dans le temps de la vidéo d'Adel (a-monter/matchs-amicaux-ref.mp4) : le joueur y commence à 4,25 s,
il est placé ici juste après l'extrait, d'où le décalage DEC.
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html, subprocess, os

IPS = 30
DUREE_EXTRAIT = 112 / IPS          # medias/reference/extrait.mp4 : 3,733 s
MEDIA_JOUEUR = 4.25                # dans la vidéo d'Adel : la fin de son fondu au noir, 0,1 s avant « Si t'es coach »
FIN_JOUEUR = 11.4667               # fin de la vidéo d'Adel (la voix s'arrête à 10,85 s)
DEC = DUREE_EXTRAIT - MEDIA_JOUEUR
T0 = json.load(open("calage.json", encoding="utf-8"))
T = {k: round(v + DEC, 3) for k, v in T0.items()}
VOLET = 3.40                       # le volet bleu entre sur « que je vais jouer ! » et couvre la coupe (3,733 s)
TEL = round(T["toi"] - 0.05, 3)    # le téléphone arrive après « c'est fait pour toi »

# Extraits de l'enregistrement d'écran (secondes de l'enregistrement) et fenêtre visée dans la vidéo finale
EXTRAITS = [
    ("x-0", 0.0, 2.9, TEL + 0.3, T["trouver"] - 0.05),            # l'accueil, jusqu'à la carte « Matchs amicaux »
    ("x-1", 2.9, 3.4, T["trouver"] - 0.05, T["trouver"] + 0.45),  # « Rechercher » : « Trouver un adversaire », « + Créer un match amical » (puis figé)
    ("x-2", 3.75, 5.4, T["annonce"] + 0.25, T["annonce"] + 0.85),  # la liste : un club, « Proposer un match »
    ("x-3", 16.0, 21.25, T["annonce"] + 0.85, T["annonce"] + 2.05),  # le formulaire : Senior 1, « Je reçois », envoyer
    ("x-4", 21.25, 23.6, T["annonce"] + 2.05, T["annonce"] + 3.35),  # l'envoi, puis « Félicitations, proposition envoyée ! » (vers 22,6 s)
]
FIN = round(EXTRAITS[-1][4] + 0.05, 3)
DUREE_CARTON = 3.0
DUREE = round(FIN + DUREE_CARTON, 2)
SOURCE_ENREG = "medias/enregistrement/enregistrement-30ips.mp4"

# Où tombent les appuis (centre, en px de la vidéo) : l'écran du téléphone commence à (290, 364), à l'échelle 0,5 de l'enregistrement
APPUIS = {"__APPUI_AMICAUX__": (650, 1074), "__APPUI_CREER__": (540, 934), "__APPUI_PROPOSER__": (494, 1152)}

SOUS_TITRES = [  # (début, fin, texte), dans le temps final
    (0.05, 1.62, "« Et dimanche prochain, je vais jouer ! »"),
    (1.62, VOLET + 0.05, "« Je vais jouer, la tête de ma mère, que je vais jouer ! »"),
    (T["coach"] - 0.42, T["amicaux"] + 0.15, "Si t'es coach et que tu cherches des matchs amicaux,"),   # le volet bleu le cache, puis le découvre
    (T["amicaux"] + 0.15, T["toi"] + 0.05, "FoundClub, c'est fait pour toi."),
    (T["toi"] + 0.2, T["app"] + 0.12, "Télécharge l'app,"),
    (T["app"] + 0.12, T["amicaux2"] + 0.12, "et tu pourras trouver des matchs amicaux"),
    (T["amicaux2"] + 0.12, T["annonce"] + 0.1, "et publier ta propre annonce."),
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
    "__DUREE_EXTRAIT__": f"{DUREE_EXTRAIT:.4f}", "__DEBUT_JOUEUR__": f"{DUREE_EXTRAIT:.4f}", "__MEDIA_JOUEUR__": f"{MEDIA_JOUEUR:.4f}",
    "__DUREE_JOUEUR__": f"{FIN_JOUEUR - MEDIA_JOUEUR:.4f}", "__VOLET_DEBUT__": f"{VOLET:.3f}", "__VOLET_DUREE__": "0.9",
    "__TEL__": f"{TEL:.3f}", "__FIN__": f"{FIN:.3f}", "__DUREE_CARTON__": f"{DUREE_CARTON:.2f}", "__DUREE__": f"{DUREE:.2f}",
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
    (0.25, "pop", 0, 0), (1.15, "secousse", 0), (3.1, "pop", -2, 4),
    (VOLET, "whoosh", -2), (VOLET + 0.1, "pop", 0, 2), (VOLET + 0.15, "impact", -6), (VOLET + 0.62, "whoosh", -6),
    (T["cherches"] - 0.45, "swish", 0), (T["amicaux"] - 0.55, "zip", 0),
    (T["club"] - 0.75, "souffle", 0), (T["club"] - 0.6, "pop", 0, 0), (T["club"] - 0.35, "impact", -3), (T["club"] + 0.05, "scintille", 0),
    (TEL, "whoosh", -3), (TEL + 0.15, "swish", 0), (TEL + 0.45, "swish", -3), (TEL + 0.85, "swish", -4),
] + [(x["debut"], "tick", 0) for x in X[1:]] + [
    (T["trouver"] - 0.3, "tap", 0), (T["amicaux2"] - 0.45, "pop", 0, 0), (T["publier"] - 0.35, "pop", 0, 4), (T["publier"] - 0.05, "tap", 0),
    (X[2]["debut"] - 0.15, "souffle", 0), (X[2]["debut"] + 0.15, "pop", 0, 2), (X[3]["debut"] - 0.2, "tap", 0),
    (X[4]["debut"] + 0.75, "choix", 0),
    (FIN, "whoosh", -2), (FIN + 0.25, "impact", -3), (FIN + 0.9, "scintille", 0), (FIN + 1.05, "pop", -2, 4),
]
# La voix est enregistrée vers -17,8 LUFS, 6 dB sous celle d'ach10 sur laquelle les niveaux ont été validés
GAIN_SONS = -6.0
sons = [{"t": round(s[0], 3), "son": s[1], "db": s[2] + GAIN_SONS, **({"note": s[3]} if len(s) > 3 else {})} for s in sorted(S, key=lambda s: s[0])]
json.dump(sons, open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"index.html : {len(src)} caractères, {len(SOUS_TITRES)} sous-titres, {len(EXTRAITS)} extraits, {len(sons)} bruitages ; "
      f"téléphone à {TEL:.2f} s, carton à {FIN:.2f} s, durée {DUREE:.2f} s")
