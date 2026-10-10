"""Assemble index.html (vidéo « World Cup ») à partir de gabarits/, de calage.json et de la carte en points.
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html, math

DUREE_VIDEO = 81.44               # après la coupe de la prise en double (outils/preparer-video.sh)
T = json.load(open("calage.json", encoding="utf-8"))
DEBUT_CARTON = round(T["jouer"] + 0.2, 2)
DUREE = round(DEBUT_CARTON + 3.0, 2)

SOUS_TITRES = [  # (début, fin, texte) sur la vidéo coupée
    (0.71, 3.30, "Dans pile un an, notre première Coupe du monde de football amateur"),
    (3.30, 5.24, "commence, et tu vas pouvoir y participer,"),
    (6.92, 8.76, "avec ton club, ou simplement avec tes potes."),
    (9.51, 10.97, "On s'est lancé un défi un peu fou :"),
    (11.14, 15.45, "organiser en un an un Mondial de football amateur, ouvert à tous, peu importe ton niveau."),
    (16.13, 17.56, "Le principe est simple."),
    (17.99, 20.60, "On va organiser des phases de qualification dans différents pays :"),
    (20.60, 24.43, "les équipes vont s'affronter, passer les tours, jusqu'à ce qu'il ne reste que les meilleures de chaque pays."),
    (24.82, 28.49, "Et ces équipes se retrouveront en France pour disputer les phases finales de ce Mondial."),
    (29.34, 31.85, "Et bonne nouvelle : les inscriptions sont déjà ouvertes."),
    (32.47, 35.79, "Pour participer, tu dois t'inscrire sur FoundClub et rejoindre une équipe."),
    (36.34, 39.30, "Ton coach peut directement inscrire ton équipe et inviter tous ses joueurs."),
    (39.30, 42.60, "Et si tu préfères jouer avec tes potes, tu peux aussi créer ta propre équipe."),
    (42.94, 48.75, "Alors dès maintenant, inscris-toi, fais inscrire ton équipe, et partage cette vidéo à tous ceux avec qui tu veux participer."),
    (49.14, 50.28, "Mais pourquoi on fait ça ?"),
    (50.62, 53.40, "Parce qu'avec FoundClub, on veut rendre le sport plus accessible."),
    (53.40, 57.20, "Et on a décidé d'organiser cet événement pour mettre en lumière l'accessibilité dans le sport."),
    (57.20, 60.56, "Évidemment, pour réussir ça en 365 jours, on va avoir besoin de vous :"),
    (61.24, 66.44, "des équipes, des terrains, des arbitres, des partenaires, et surtout une communauté prête à faire connaître ce projet dans le monde entier."),
    (67.06, 71.02, "Et justement, dans la prochaine vidéo, on vous expliquera comment on compte organiser tout ça, étape par étape."),
    (71.67, 76.97, "Mais en attendant, si ce projet te chauffe, envoie cette vidéo à ton coach, tes coéquipiers, tes potes, et faites-la tourner au maximum."),
    (77.98, 81.43, "Un an pour créer un Mondial de football amateur : c'est maintenant, et c'est à vous de jouer."),
]

# Foyers qui s'allument sur la carte (coordonnées de la carte 1000 x 520), dans l'ordre d'allumage — aucun pays nommé
HUBS = [(520, 150), (470, 250), (230, 200), (330, 330), (560, 300), (610, 210), (690, 240), (800, 190), (870, 370), (180, 160), (540, 135), (720, 170)]
RAYON_HUB = 26

carte = json.load(open("medias/carte-points.json", encoding="utf-8"))
def points():
    lignes = []
    for x, y, fr in carte["points"]:
        hub = next((i for i, (hx, hy) in enumerate(HUBS) if math.hypot(x - hx, y - hy) < RAYON_HUB), None)
        classe = f' class="h{hub}"' if hub is not None else ""
        lignes.append(f'            <circle cx="{x}" cy="{y}" r="3.2"{classe}/>')
    return "\n".join(lignes)
def france():
    return "\n".join(f'            <circle cx="{x}" cy="{y}" r="0.62"/>' for x, y in carte["franceFine"])

def tableau():  # 8 équipes -> 4 -> 2 -> 1 vainqueur ; chaque trait a une longueur de pointillé de 300 pour se « dessiner »
    s, ys = [], [12 + i * 46 + 15 for i in range(8)]
    def slot(x, y): s.append(f'          <rect class="equipe" x="{x}" y="{y - 15}" width="90" height="30" rx="8"/>')
    def trait(classe, x0, ya, yb, x1, x2):
        yc = (ya + yb) / 2
        for y in (ya, yb):
            s.append(f'          <path class="{classe}" stroke-dasharray="300" d="M{x0} {y} H{x1} V{yc} H{x2}"/>')
        return yc
    for y in ys: slot(20, y)
    y2 = [trait("tour1", 110, ys[i], ys[i + 1], 220, 330) for i in range(0, 8, 2)]
    for y in y2: slot(330, y)
    y3 = [trait("tour2", 420, y2[i], y2[i + 1], 500, 580) for i in range(0, 4, 2)]
    for y in y3: slot(580, y)
    yv = trait("tour3", 670, y3[0], y3[1], 730, 786)
    s.append(f'          <circle class="vainqueur" cx="820" cy="{yv}" r="34"/>')
    s.append(f'          <path class="vainqueur coupe" d="M806 {yv - 12}h28v8a14 14 0 0 1-28 0z"/>')
    return "\n".join(s)

ICONES = {
    "equipes": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.6"/><path d="M16 14.2c3.1.2 5.5 2.4 5.5 5.8"/>',
    "terrains": '<rect x="2.5" y="5" width="19" height="14" rx="1.5"/><path d="M12 5v14"/><circle cx="12" cy="12" r="3"/>',
    "arbitres": '<circle cx="9" cy="14" r="5"/><path d="M12.5 10.5L20 6M14 9h7"/>',
    "partenaires": '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z"/>',
    "communaute": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
}
NOMS = {"equipes": "Des équipes", "terrains": "Des terrains", "arbitres": "Des arbitres", "partenaires": "Des partenaires", "communaute": "Une communauté"}
def besoins():
    out = []
    for i, cle in enumerate(NOMS):
        large = ' large' if cle == "communaute" else ""
        sous = '<span class="sous">Dans le monde entier</span>' if cle == "communaute" else ""
        couleur = "#27d6a3" if cle == "communaute" else "#01b3f4"
        out.append(f'          <div id="besoin-{i}" class="besoin{large}"><svg width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="{couleur}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONES[cle]}</svg>{NOMS[cle]}{sous}</div>')
    return "\n".join(out)

ICONES_ETAT = ('<svg width="74" height="14" viewBox="0 0 74 14"><rect x="0" y="9" width="3" height="5" rx="1" fill="#fff"/><rect x="5" y="6" width="3" height="8" rx="1" fill="#fff"/>'
               '<rect x="10" y="3" width="3" height="11" rx="1" fill="#fff"/><rect x="15" y="0" width="3" height="14" rx="1" fill="#fff"/>'
               '<path d="M30 5a10 10 0 0 1 14 0M32.5 8a6 6 0 0 1 9 0M35 11a2.5 2.5 0 0 1 4 0" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>'
               '<rect x="50" y="1" width="21" height="12" rx="3.5" stroke="#fff" stroke-opacity=".5" fill="none"/><rect x="52" y="3" width="7" height="8" rx="2" fill="#fff"/><rect x="72" y="5" width="2" height="4" rx="1" fill="#fff" fill-opacity=".5"/></svg>')
TROPHEE = ('<svg width="96" height="96" viewBox="0 0 64 64"><path d="M18 8h28v12a14 14 0 0 1-28 0z" fill="#01b3f4"/>'
           '<path d="M18 12H9v4a9 9 0 0 0 9 9M46 12h9v4a9 9 0 0 1-9 9" fill="none" stroke="#01b3f4" stroke-width="4"/>'
           '<rect x="28" y="33" width="8" height="10" fill="#99e1fb"/><rect x="20" y="43" width="24" height="6" rx="2" fill="#fff"/><rect x="16" y="50" width="32" height="7" rx="2" fill="#99e1fb"/></svg>')

lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
src = lire("index.gabarit.html")
src = src.replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--MAQUETTES-->", lire("maquettes.html").replace("<!--ICONES-ETAT-->", ICONES_ETAT).replace("<!--TROPHEE-->", TROPHEE))
src = src.replace("<!--POINTS-->", points()).replace("<!--FRANCE-->", france()).replace("<!--TABLEAU-->", tableau()).replace("<!--BESOINS-->", besoins())
src = src.replace("<!--SOUSTITRES-->", "\n".join(f'        <p id="st-{i}" class="st">{html.escape(t)}</p>' for i, (_, _, t) in enumerate(SOUS_TITRES)))
src = src.replace("/*T*/", json.dumps(T)).replace("/*ST*/", json.dumps([[d, f] for d, f, _ in SOUS_TITRES])).replace("/*HUBS*/", json.dumps(HUBS))
src = (src.replace("__DUREE_VIDEO__", f"{DUREE_VIDEO:.2f}").replace("__DEBUT_CARTON__", f"{DEBUT_CARTON:.2f}")
          .replace("__DUREE_CARTON__", f"{DUREE - DEBUT_CARTON:.2f}").replace("__DUREE__", f"{DUREE:.2f}"))
open("index.html", "w", encoding="utf-8").write(src)
print("index.html :", len(src), "caractères,", len(SOUS_TITRES), "sous-titres, durée", DUREE, "s")
