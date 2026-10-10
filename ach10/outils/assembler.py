"""Assemble index.html a partir de index.source.html : polices, tempete de messages, sous-titres.
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html, sys

DUREE = float(sys.argv[1]) if len(sys.argv) > 1 else 57.5    # duree rendue : 54,83 s de video + le carton final
FIN_ECRAN = 47.0                                              # fin du « mode ecran » (scenes 4 a 7)
DUREE_VIDEO = 54.83

# Instants (s) ou chaque mot-cle vient d'etre prononce — outils/caler_mots.py sur la voix d'ach10
T = json.load(open("calage.json", encoding="utf-8"))

SOUS_TITRES = [  # (debut, fin, texte) — cale sur la voix d'ach10 (transcription + calage mot a mot)
    (0.16, 2.40, "Toi aussi, dans ton club en 2026,"),
    (2.45, 5.05, "vous utilisez encore les groupes WhatsApp pour tout organiser ?"),
    (5.10, 7.80, "Les convocations, les entraînements, les matchs,"),
    (7.80, 9.30, "toutes les informations importantes :"),
    (9.30, 10.40, "tout passe par WhatsApp,"),
    (10.40, 11.85, "et au final, on s'y perd."),
    (11.87, T["presenter"] + 0.1, "Mais aujourd'hui, j'ai une application à vous présenter"),
    (T["presenter"] + 0.1, 16.70, "qui pourrait changer l'organisation de ton club."),
    (16.76, 18.85, "Cette application, c'est FoundClub."),
    (19.00, 20.75, "L'objectif est très simple :"),
    (20.95, 23.42, "faciliter la communication et l'organisation"),
    (23.48, 27.20, "entre le club, les joueurs, les dirigeants, et même les parents."),
    (27.55, T["whatsapp"] + 0.12, "Plutôt que de multiplier les groupes WhatsApp"),
    (T["whatsapp"] + 0.12, 31.25, "et de chercher les informations un peu partout,"),
    (31.45, 33.60, "vous pouvez tout centraliser au même endroit."),
    (33.65, 35.30, "Et ce qui est intéressant, c'est que FoundClub"),
    (35.30, 37.90, "ne s'arrête pas seulement à la gestion de ton équipe :"),
    (37.95, 39.45, "l'application a aussi pour ambition"),
    (39.45, 42.40, "de faciliter la connexion entre les joueurs et les clubs."),
    (42.45, 46.45, "Alors, que tu sois joueur, éducateur, président, dirigeant, parent…"),
    (46.55, 48.50, "C'est le moment de venir découvrir FoundClub."),
    (48.60, 51.80, "Et dis-moi en commentaire si vous utilisez encore les groupes WhatsApp,"),
    (52.00, 53.75, "ou si vous utilisez une application."),
    (53.89, 54.85, "Ciao mes petits potes !"),
]
SOUS_TITRES = [st for st in SOUS_TITRES if st[0] < DUREE]

# Scene 5 : messages eparpilles autour du telephone (cote g = ancre a gauche, d = ancre a droite)
EPARPILLES = [
    ("Yanis", "Qui est dispo samedi ?", "g", 30, 470, "c2"),
    ("Maman de Léo", "C'est à quelle heure ??", "d", 30, 600, "c3"),
    ("Coach Karim", "Le planning svp", "g", 40, 760, "c1"),
    ("Le président", "Cotisation avant vendredi", "d", 26, 920, "c4"),
    ("Nathan", "On joue où samedi ?", "g", 30, 1090, "c6"),
    ("Sofiane", "Entraînement annulé ?", "d", 34, 1240, "c5"),
]
def cible(texte, cote, marge, y):  # deplacement vers le centre de l'ecran du telephone (540, 845)
    w = len(texte) * 16 + 44
    cx = marge + w / 2 if cote == "g" else 1080 - marge - w / 2
    return round(540 - cx), round(845 - (y + 40))

# Messages fictifs (aucun vrai nom, aucun emoji) : x, y, rotation, couleur de l'expediteur
TEMPETE = [
    ("Yanis", "Qui est dispo samedi ?", 120, 360, -3, "c2"),
    ("Maman de Léo", "C'est à quelle heure la convoc ??", 470, 470, 2, "c3"),
    ("Sofiane", "Entraînement annulé ou pas ?", 40, 600, 2, "c4"),
    ("Papa d'Adam", "Quelqu'un a l'adresse du terrain ?", 500, 740, -2, "c1"),
    ("Ilyes", "Je peux pas venir mercredi", 120, 860, -2, "c5"),
    ("Nathan", "On joue contre qui ?", 600, 980, 3, "c6"),
    ("Coach Karim", "Vous avez vu mon message d'hier ?", 140, 1100, 1, "c1"),
    ("Maman d'Inès", "Le covoit part d'où ?", 560, 1220, -3, "c3"),
    ("Le président", "Cotisation avant vendredi svp", 120, 1340, 2, "c2"),
    ("Mehdi", "Le planning de la semaine svp", 470, 300, 2, "c4"),
    ("Hugo", "???", 780, 640, -4, "c6"),
    ("Lucas", "Je l'ai pas reçu", 650, 1650, -2, "c5"),
    ("Enzo", "C'est reporté ?", 130, 1700, 3, "c1"),
    ("Coach Karim", "Qui ramène les maillots ?", 380, 1040, -1, "c1"),
]
DEBUT, PAS = 7.95, 0.17

src = open("gabarits/index.gabarit.html", encoding="utf-8").read()
lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
for marque, ext in (("/*CSS-3-5*/", "css"), ("<!--HTML-3-5-->", "html"), ("/*JS-3-5*/", "js")):
    morceaux = [lire(f"scenes-3-5.{ext}")] + ([lire(f"scenes-6-9.{ext}")] if DUREE > 34 else [])
    src = src.replace(marque, "\n".join(morceaux))
src = src.replace('data-start="0" data-duration="__DUREE__" data-track-index="0" data-has-audio="true"', f'data-start="0" data-duration="{min(DUREE, DUREE_VIDEO):.2f}" data-track-index="0" data-has-audio="true"')
src = src.replace("__DUREE_CARTON__", f"{max(DUREE - 54.0, 0.1):.2f}")
src = src.replace("__DUREE_ECRAN__", f"{min(DUREE, FIN_ECRAN) - 18.9:.2f}").replace("__DUREE__", f"{DUREE:.2f}")
src = src.replace("<!--EPARPILLES-->", "\n".join(
    f'        <div id="e-{i}" class="eparpille" style="{"left" if c == "g" else "right"}:{m}px;top:{y}px;"><div class="qui {k}">{html.escape(q)}</div><div class="quoi">{html.escape(t)}</div></div>'
    for i, (q, t, c, m, y, k) in enumerate(EPARPILLES)))
src = src.replace("const TEMPETE = /*TP*/;", "const TEMPETE = /*TP*/;\n      const EPARPILLES = " + json.dumps([
    {"t": round(27.65 + i * 0.55, 2), "dx": cible(t, c, m, y)[0], "dy": cible(t, c, m, y)[1]} for i, (q, t, c, m, y, k) in enumerate(EPARPILLES)]) + ";")
src = src.replace("/*T*/", json.dumps(T))
src = src.replace("/*POLICES*/", open("gabarits/polices.css", encoding="utf-8").read())
src = src.replace("<!--TEMPETE-->", "\n".join(
    f'          <div id="m-{i}" class="mini" style="left:{x}px;top:{y}px;"><div class="qui {c}">{html.escape(q)}</div><div class="quoi">{html.escape(m)}</div></div>'
    for i, (q, m, x, y, r, c) in enumerate(TEMPETE)))
src = src.replace("<!--SOUSTITRES-->", "\n".join(
    f'        <p id="st-{i}" class="st">{html.escape(t)}</p>' for i, (_, _, t) in enumerate(SOUS_TITRES)))
src = src.replace("/*ST*/", json.dumps([[d, f] for d, f, _ in SOUS_TITRES]))
src = src.replace("/*TP*/", json.dumps([{"t": round(DEBUT + i * PAS, 2), "r": r} for i, (_, _, _, _, r, _) in enumerate(TEMPETE)]))
open("index.html", "w", encoding="utf-8").write(src)
print("index.html :", len(src), "caracteres,", len(TEMPETE), "messages,", len(SOUS_TITRES), "sous-titres")
