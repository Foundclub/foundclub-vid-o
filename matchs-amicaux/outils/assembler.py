"""Assemble index.html (vidéo « matchs amicaux ») à partir de gabarits/ et de calage.json,
et découpe les extraits de l'enregistrement d'écran à la bonne vitesse pour tomber sur la voix.
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html, subprocess, os

DUREE_VIDEO = 49.78
DUREE = 52.6                      # la vidéo + le carton final
T = json.load(open("calage.json", encoding="utf-8"))

SOUS_TITRES = [  # (début, fin, texte)
    (0.61, 3.00, "On se plaint parce que les footballeurs professionnels jouent tous les trois jours."),
    (3.00, 7.26, "Mais nous, dans le football amateur, parfois, on peut passer un mois sans jouer un seul match."),
    (7.72, 11.64, "Entre les week-ends de coupe, les trêves, les matchs reportés… un mois sans match."),
    (12.20, 14.75, "Mais attendez, il y en a, ils paient leur licence jusqu'à 350 € !"),
    (14.75, 16.86, "« La tête de ma mère, je vais jouer ! »"),
    (17.25, 20.86, "Mais en fait, pourquoi on ne joue pas des matchs amicaux le week-end où on n'a pas de match de championnat ?"),
    (21.45, 25.37, "Les coachs font une réponse simple : il faut tout le temps trouver une équipe en face, et s'organiser."),
    (26.09, 28.70, "Justement, c'est là qu'un outil intervient : FoundClub."),
    (29.32, 31.40, "Ton coach va sur FoundClub,"),
    (31.40, 33.20, "il cherche une équipe disponible près de chez vous,"),
    (33.20, 34.97, "il organise un match amical : il se déplace, ou il reçoit."),
    (35.43, 36.38, "C'est tout."),
    (36.90, 40.30, "Que ce soit pendant une trêve, un week-end de coupe, un match annulé,"),
    (40.30, 43.61, "même en semaine pour préparer un match, vous pouvez continuer à jouer et garder le rythme."),
    (44.04, 46.85, "Donc maintenant, toi-même tu peux aller voir, mais envoie cette vidéo à ton coach."),
    (46.85, 49.76, "Parce que 350 €… la tête de ma mère, je vais jouer !"),
]

# Octobre 2026 : le 1er est un jeudi. Les pros : un match tous les 3 jours.
PROS = list(range(1, 32, 3))
TAMPONS = [("t-coupe", "Coupe", 0), ("t-treve", "Trêve", 1), ("t-reporte", "Reporté", 2)]  # week-ends des lignes 0, 1, 2

# Extraits de l'enregistrement d'écran (secondes de l'enregistrement) et fenêtre visée dans la vidéo
EXTRAITS = [
    ("x-0", 0.0, 3.0, T["coach8"] - 0.35, T["disponible"] - 0.75),        # l'accueil, puis la recherche
    ("x-1", 3.0, 5.4, T["disponible"] - 0.75, T["amical"] - 0.75),        # « Trouver un adversaire » près de chez toi
    ("x-2", 13.3, 16.0, T["amical"] - 0.75, T["deplace"] - 0.65),          # la fiche de l'équipe, « Proposer un match »
    ("x-3", 18.6, 21.25, T["deplace"] - 0.65, T["recoit"] + 0.35),         # Senior 1, « Je reçois »
    ("x-4", 21.25, 23.4, T["recoit"] + 0.35, T["tout"] + 0.55),            # « Félicitations, proposition envoyée ! »
]
SOURCE_ENREG = "medias/enregistrement/enregistrement-30ips.mp4"

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
    duree = round(fin_cible - debut, 3)
    v = couper(nom, deb, fin, duree)
    extraits_js.append({"debut": round(debut, 3), "duree": duree})
    extraits_html.append(f'            <div id="{nom}" class="extrait"><video id="v-{nom}" src="medias/enregistrement/{nom}.mp4" muted playsinline '
                         f'data-start="{debut:.3f}" data-duration="{duree:.3f}" data-track-index="3"></video></div>')
    print(f"{nom} : {deb}-{fin} s de l'enregistrement -> {debut:.2f}-{fin_cible:.2f} s (vitesse x{v:.2f})")

def cases():
    sortie = ['            <div class="case vide"></div>'] * 3  # lundi 28, mardi 29, mercredi 30 sept.
    for jour in range(1, 32):
        col = (jour + 2) % 7          # 0 = lundi
        classe = "case we" if col >= 5 else "case"
        ballon = f'<span id="b-{jour}" class="ballon"></span>' if jour in PROS else ""
        sortie.append(f'            <div class="{classe}"><span class="num">{jour}</span>{ballon}</div>')
    return "\n".join(sortie)

def tampons():  # centrés sur les colonnes samedi-dimanche des 3 premières semaines
    cx = 34 + 5 * 126 + 121           # bord du samedi + moitié des deux colonnes, dans le repère du calendrier
    y0 = 34 + 49 + 22 + 29 + 12       # haut de la grille dans le calendrier
    return "\n".join(f'          <div id="{i}" class="tampon" style="left:{cx}px;top:{y0 + r * 138 + 64}px;">{html.escape(t)}</div>'
                     for i, t, r in TAMPONS)

lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
src = lire("index.gabarit.html")
src = src.replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--CASES-->", cases()).replace("<!--TAMPONS-->", tampons()).replace("<!--EXTRAITS-->", "\n".join(extraits_html))
src = src.replace("<!--SOUSTITRES-->", "\n".join(f'        <p id="st-{i}" class="st">{html.escape(t)}</p>' for i, (_, _, t) in enumerate(SOUS_TITRES)))
src = src.replace("/*T*/", json.dumps(T)).replace("/*ST*/", json.dumps([[d, f] for d, f, _ in SOUS_TITRES]))
src = src.replace("/*PROS*/", json.dumps(PROS)).replace("/*EXTRAITS*/", json.dumps(extraits_js))
src = src.replace("__DUREE_VIDEO__", f"{DUREE_VIDEO:.2f}").replace("__DUREE_CARTON__", f"{DUREE - 49.5:.2f}").replace("__DUREE__", f"{DUREE:.2f}")
open("index.html", "w", encoding="utf-8").write(src)
print("index.html :", len(src), "caractères,", len(SOUS_TITRES), "sous-titres,", len(EXTRAITS), "extraits")
