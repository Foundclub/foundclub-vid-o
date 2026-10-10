"""Assemble index.html (vidéo « ach10 x Ergysport ») à partir de gabarits/ et de calage.json.
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html

DUREE_VIDEO = 30.97               # la vidéo d'ach10 (a-monter/ach10-ergysport.mov)
T = json.load(open("calage.json", encoding="utf-8"))
DEBUT_CARTON = round(T["ergysport2"] - 0.25, 2)
DUREE = round(DEBUT_CARTON + 3.2, 2)

SOUS_TITRES = [  # (début, fin, texte)
    (0.10, 2.50, "Mes petits potes, vous savez que le football"),
    (2.50, 4.25, "c'est pas seulement ce qui se passe sur le terrain."),
    (4.30, 6.75, "La préparation, l'hydratation et la récupération,"),
    (6.75, 8.35, "c'est aussi important."),
    (8.45, 10.85, "Aujourd'hui, je vais vous présenter Ergysport,"),
    (10.85, 12.50, "une gamme de nutrition sportive."),
    (12.55, 14.35, "On retrouve de la whey,"),
    (14.50, 16.15, "de la créatine, des gélules"),
    (16.15, 17.95, "pour accompagner la récupération sportive,"),
    (17.95, 20.25, "plus précisément les crampes et les courbatures,"),
    (20.30, 22.90, "mais aussi des multivitamines pour la vitalité."),
    (22.95, 24.95, "Et pendant l'effort, des barres céréales"),
    (24.95, 26.75, "et des boosts pour un plein d'énergie."),
    (26.90, 28.40, "Parce que la performance sur le terrain,"),
    (28.40, DEBUT_CARTON + 0.3, "ça se prépare aussi dehors, avec Ergysport."),
]

lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
src = lire("index.gabarit.html")
src = src.replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--SOUSTITRES-->", "\n".join(f'        <p id="st-{i}" class="st"><span>{html.escape(t)}</span></p>' for i, (_, _, t) in enumerate(SOUS_TITRES)))
src = src.replace("/*T*/", json.dumps(T)).replace("/*ST*/", json.dumps([[d, f] for d, f, _ in SOUS_TITRES]))
src = (src.replace("__DUREE_VIDEO__", f"{DUREE_VIDEO:.2f}").replace("__DEBUT_CARTON__", f"{DEBUT_CARTON:.2f}")
          .replace("__DUREE_CARTON__", f"{DUREE - DEBUT_CARTON:.2f}").replace("__DUREE__", f"{DUREE:.2f}"))
open("index.html", "w", encoding="utf-8").write(src)
print("index.html :", len(src), "caractères,", len(SOUS_TITRES), "sous-titres, durée", DUREE, "s")
