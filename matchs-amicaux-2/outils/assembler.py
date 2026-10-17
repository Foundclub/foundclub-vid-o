"""Assemble index.html (vidéo « matchs amicaux 2 ») à partir de gabarits/ et de calage.json, découpe les extraits de
l'enregistrement d'écran à la bonne vitesse pour tomber sur la voix, et écrit sons.json (bruitages).
La vidéo d'ach10 est coupée juste après « la vie de ma mère, je vais jouer ! » pour y glisser l'extrait de la vidéo
de référence : medias/reference/extrait.mp4 s'il existe, sinon un emplacement réservé de 2,5 s.
calage.json est dans le temps de la vidéo d'origine ; tout ce qui vient après la coupe est décalé ici.
Usage : python3 -I outils/assembler.py   (depuis le dossier du projet)"""
import json, html, subprocess, os

IPS = 30
DUREE_SOURCE = 55.2667
COUPE = 578 / IPS                 # 19,267 s : fin de « jouer ! » (creux de la voix, mesuré au 1/100 s)
REPRISE = 582 / IPS               # 19,400 s : début de « Mais c'est quoi la raison » ; les 4 images entre les deux sautent
EXTRAIT = "medias/reference/extrait.mp4"
if os.path.exists(EXTRAIT):
    INSERT = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", EXTRAIT],
                                  capture_output=True, text=True, check=True).stdout)
    INSERT = round(INSERT * IPS) / IPS
else:
    INSERT = 2.5
REPRISE_T = COUPE + INSERT
DECALAGE = REPRISE_T - REPRISE
dec = lambda t: round(t + DECALAGE, 3) if t >= REPRISE - 0.001 else round(t, 3)
DUREE_VIDEO = dec(DUREE_SOURCE)
FIN = dec(55.15)                  # le carton final arrive sur le dernier souffle de « jouer ! »
DUREE_CARTON = 3.2
DUREE = round(FIN + DUREE_CARTON, 2)

T0 = json.load(open("calage.json", encoding="utf-8"))
T = {k: dec(v) for k, v in T0.items()}

SOUS_TITRES = [  # (début, fin, texte), dans le temps de la vidéo d'origine
    (0.13, 3.30, "Les footballeurs professionnels se plaignent parce qu'ils jouent tous les 3 jours."),
    (3.65, 6.80, "Dites-vous : nous, en amateur, des fois, pendant un mois, on joue pas."),
    (6.80, 11.10, "Entre les week-ends de coupe, les matchs reportés ou les trêves…"),
    (11.27, 12.95, "Des fois, pendant un mois, on joue pas."),
    (12.95, 16.65, "Dites-vous, il y en a, ils payent leur licence jusqu'à 550 € !"),
    (17.16, COUPE, "À 550 €… la vie de ma mère, je vais jouer !"),
    (REPRISE, T0["raison"] + 0.35, "Mais c'est quoi la raison, en fait ?"),
    (T0["raison"] + 0.35, 22.58, "Pourquoi on joue pas pendant autant de temps, des fois ?"),
    (22.76, 24.60, "Les coachs, ils ont toujours la même excuse."),
    (24.81, 29.43, "« On sait pas contre qui jouer, faut s'organiser, est-ce qu'on joue à domicile ou à l'extérieur ? »"),
    (29.67, 32.80, "Mais maintenant, plus d'excuses. J'ai un outil pour vous, les gars :"),
    (32.80, 33.75, "FoundClub."),
    (33.89, T0["application"] + 0.2, "Ton coach, il a juste à aller sur l'application,"),
    (T0["application"] + 0.2, 39.38, "il cherche un club qui est disponible le week-end où il a envie de faire ce match."),
    (39.59, 41.91, "Et il choisit : à domicile ou à l'extérieur."),
    (42.18, 44.86, "Que ce soit pendant un match reporté, un week-end de coupe,"),
    (45.09, T0["semaine"] + 0.25, "pendant la trêve ou même en semaine,"),
    (T0["semaine"] + 0.25, 49.40, "vous pouvez continuer à jouer et garder le rythme."),
    (49.67, T0["coach"] + 0.3, "Maintenant, t'as plus qu'à envoyer la vidéo à ton coach."),
    (T0["coach"] + 0.3, 55.15, "Et à 550 € la licence… la tête de ma mère, je vais jouer !"),
]

# Coupures de presse : titres recopiés mot pour mot (recherches web du 16/10/2026), média en texte, aucun logo.
# Les mots entre [crochets] reçoivent le surligneur.
ARTICLES_PROS = [
    ("art-1", "left: 70px; top: 370px;", "Soccerway", "fr.soccerway.com",
     "“On est proche” [d'une grève], dit Rodri à propos des [calendriers surchargés]", 2),
    ("art-2", "left: 70px; top: 930px;", "La DH", "dhnet.be · éditorial du 19/09/2024",
     "Grève des joueurs : quand [les footballeurs pros] crachent dans la soupe", 1),
]
ARTICLES_AMATEURS = [
    ("art-3", "left: 70px; top: 540px;", "ICI Limousin", "ici.fr · Les échos du Limousin",
     "En Corrèze, [le casse-tête des matchs de foot à reprogrammer] en raison des intempéries de ces dernières semaines", 1),
]

def article(id_, style, media, source, titre, lignes):
    t = html.escape(titre).replace("[", '<span class="mq">').replace("]", "</span>")
    taille = ' style="font-size: 60px;"' if len(titre) > 90 else ""
    traits = "".join(f'<span style="width: {w}%;"></span>' for w in (100, 92, 64)[:lignes + 1])
    return (f'        <div id="{id_}" class="article" style="{style}">\n'
            f'          <div class="a-tete"><span class="a-media">{html.escape(media)}</span></div>\n'
            f'          <div class="a-titre"{taille}>{t}</div>\n'
            f'          <div class="a-lignes">{traits}</div>\n'
            f'          <div class="a-source">{html.escape(source)}</div>\n'
            f'        </div>')

# Octobre 2026 : le 1er est un jeudi. Les tampons se posent sur les week-ends des 3 premières lignes.
TAMPONS = [("t-coupe", "Coupe", 0), ("t-reporte", "Reporté", 1), ("t-treve", "Trêve", 2)]

# Extraits de l'enregistrement d'écran (secondes de l'enregistrement) et fenêtre visée dans la vidéo d'origine.
# Le téléphone arrive pendant « ton coach » : le logo FoundClub reste à l'écran 1,2 s.
X0 = T0["application"] - 0.6
EXTRAITS = [
    ("x-0", 0.0, 3.0, X0, T0["application"] + 0.75),                        # l'accueil, puis « Rechercher »
    ("x-1", 3.0, 5.4, T0["application"] + 0.75, T0["week"] - 0.5),          # « Trouver un adversaire », la liste des clubs
    ("x-2", 13.0, 15.0, T0["week"] - 0.5, T0["choisit"] - 0.35),           # la fiche du club : la date proposée, un dimanche
    ("x-3", 16.0, 21.25, T0["choisit"] - 0.35, T0["exterieur2"] + 0.25),   # « Proposer un match » : Senior 1, « Je reçois »
    ("x-4", 21.25, 23.4, T0["exterieur2"] + 0.25, T0["reporte2"] - 0.2),   # « Félicitations, proposition envoyée ! »
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
for nom, deb, fin, debut0, fin0 in EXTRAITS:
    debut, duree = dec(debut0), round(fin0 - debut0, 3)
    v = couper(nom, deb, fin, duree)
    extraits_js.append({"debut": debut, "duree": duree})
    extraits_html.append(f'            <div id="{nom}" class="extrait"><video id="v-{nom}" src="medias/enregistrement/{nom}.mp4" muted playsinline '
                         f'data-start="{debut:.3f}" data-duration="{duree:.3f}" data-track-index="3"></video></div>')
    print(f"{nom} : {deb}-{fin} s de l'enregistrement -> {debut:.2f}-{debut + duree:.2f} s (vitesse x{v:.2f})")

def cases():
    sortie = ['            <div class="case vide"></div>'] * 3  # lundi 28, mardi 29, mercredi 30 sept.
    for jour in range(1, 32):
        col = (jour + 2) % 7          # 0 = lundi
        sortie.append(f'            <div class="{"case we" if col >= 5 else "case"}"><span class="num">{jour}</span></div>')
    return "\n".join(sortie)

def tampons():  # centrés sur les colonnes samedi-dimanche des 3 premières semaines
    cx = 34 + 5 * 126 + 121
    y0 = 34 + 49 + 22 + 29 + 12
    return "\n".join(f'          <div id="{i}" class="tampon" style="left:{cx}px;top:{y0 + r * 138 + 64}px;">{html.escape(t)}</div>'
                     for i, t, r in TAMPONS)

if os.path.exists(EXTRAIT):
    insert_html = (f'          <video id="v-reference" src="{EXTRAIT}" playsinline data-has-audio="true" '
                   f'data-start="{COUPE:.4f}" data-duration="{INSERT:.4f}" data-track-index="12"></video>')
else:  # emplacement réservé, tant que l'extrait n'est pas fourni
    insert_html = ('          <div class="k">Emplacement réservé</div>\n'
                   '          <div class="t">L\'extrait de la vidéo<br />de référence</div>\n'
                   '          <div class="s">à partir de 0:30 — « la tête de ma mère, je vais jouer »</div>')

# Scènes à durée fixe (débuts et fins dans le temps final)
S4_DEBUT = round(T0["mois2"] + 0.3, 3)
S5_DEBUT, S5_FIN = REPRISE_T, dec(22.7)
S6_DEBUT, S6_FIN = dec(T0["coachs"] - 0.5), dec(X0) - 0.4   # le logo s'efface quand le téléphone arrive
S11_DEBUT = dec(T0["rythme"] + 0.6)

remplacements = {
    "__DUREE_VIDEO__": f"{DUREE_VIDEO:.4f}", "__DUREE_CARTON__": f"{DUREE_CARTON:.2f}",
    "__COUPE__": f"{COUPE:.4f}", "__REPRISE_T__": f"{REPRISE_T:.4f}", "__REPRISE__": f"{REPRISE:.4f}",
    "__DUREE_B__": f"{DUREE_SOURCE - REPRISE:.4f}", "__INSERT__": f"{INSERT:.4f}", "__FIN__": f"{FIN:.3f}",
    "__S4_DEBUT__": f"{S4_DEBUT:.3f}", "__S4_DUREE__": f"{COUPE - S4_DEBUT:.3f}",
    "__S5_DEBUT__": f"{S5_DEBUT:.4f}", "__S5_DUREE__": f"{S5_FIN - S5_DEBUT:.3f}",
    "__S6_DEBUT__": f"{S6_DEBUT:.3f}", "__S6_DUREE__": f"{S6_FIN - S6_DEBUT:.3f}",
    "__S11_DEBUT__": f"{S11_DEBUT:.3f}", "__S11_DUREE__": f"{FIN + 0.4 - S11_DEBUT:.3f}",
    "__DUREE__": f"{DUREE:.2f}",
}
lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
src = lire("index.gabarit.html")
src = src.replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--CASES-->", cases()).replace("<!--TAMPONS-->", tampons()).replace("<!--EXTRAITS-->", "\n".join(extraits_html))
src = src.replace("<!--ARTICLES_PROS-->", "\n".join(article(*a) for a in ARTICLES_PROS))
src = src.replace("<!--ARTICLES_AMATEURS-->", "\n".join(article(*a) for a in ARTICLES_AMATEURS))
src = src.replace("<!--INSERT-->", insert_html)
st = [(dec(d) if d >= REPRISE - 0.001 else d, dec(f) if f > REPRISE else f, t) for d, f, t in SOUS_TITRES]
src = src.replace("<!--SOUSTITRES-->", "\n".join(f'        <p id="st-{i}" class="st">{html.escape(t)}</p>' for i, (_, _, t) in enumerate(st)))
src = src.replace("/*T*/", json.dumps(T)).replace("/*ST*/", json.dumps([[round(d, 3), round(f, 3)] for d, f, _ in st]))
src = src.replace("/*EXTRAITS*/", json.dumps(extraits_js))
for k, v in remplacements.items():
    src = src.replace(k, v)
assert "__" not in src.replace("__timelines", ""), "repère non remplacé"
open("index.html", "w", encoding="utf-8").write(src)

# ── Bruitages (outils/sons.py) : chaque animation a son son, aux mêmes instants que scenes.js ──
P0, CAL, S4 = 0.15, T["jours"] + 0.55, T["mois2"] + 0.4
TEL = extraits_js[0]["debut"] - 0.75
APRES = extraits_js[-1]["debut"] + extraits_js[-1]["duree"]
SORTIE = T["rythme"] + 0.5
S = [
    (P0, "whoosh", -3), (P0 + 0.35, "montee", -6), (P0 + 0.63, "impact", -4), (P0 + 0.8, "zip", -2),
    (T["plaignent"] - 0.5, "swish", 0), (T["plaignent"] - 0.05, "zip", -2), (T["jours"] - 0.85, "pop", -2, 0), (T["jours"] - 0.5, "pop", -2, 4),
    (CAL - 0.15, "souffle", 2), (CAL + 0.1, "whoosh", -4), (T["amateur"] - 0.75, "swish", -2), (T["mois"] - 0.55, "swish", 0),
    (T["mois"] - 0.1, "secousse", 0),
    (T["coupe"] - 0.13, "impact", -6), (T["reportes"] - 0.13, "impact", -6), (T["treve"] - 0.13, "impact", -4), (T["treve"] - 0.13, "secousse", 2),
    (T["mois2"] - 1.25, "montee", -6), (T["mois2"] - 0.97, "impact", -5), (T["mois2"] - 0.85, "zip", -2), (T["mois2"] - 0.4, "zip", 0),
    (S4 - 0.1, "whoosh", -3), (S4 + 0.3, "swish", 0), (T["550"] - 1.1, "montee", -4), (T["550"], "impact", -4),
    (T["mere"] - 0.8, "pop", 0, 0), (T["jouer"] - 0.3, "secousse", 2),
    (COUPE, "coupe", 4),
    (REPRISE_T, "coupe", 2), (REPRISE_T + 0.05, "swish", 0), (T["raison"] - 0.5, "zip", 0),
    (T["coachs"] - 0.35, "pop", 0, -2), (T["contre"] - 0.6, "swish", 0), (T["organiser"] - 0.6, "swish", 0), (T["exterieur"] - 1.2, "swish", 0),
    (T["exterieur"], "tap", -2),
    (T["excuses"] - 0.8, "zip", 0), (T["excuses"] - 0.45 - 0.0, "montee", -8), (T["excuses"] - 0.23, "impact", -2), (T["excuses"] - 0.23, "secousse", 0),
    (T["outil"] + 0.3, "souffle", 2),
    (T["found"] - 0.6, "pop", 0, 0), (T["found"] - 0.3, "impact", -3), (T["found"] + 0.15, "scintille", 0),
    (TEL, "whoosh", -3), (TEL + 0.45, "swish", 0), (TEL + 0.8, "swish", -2), (T["disponible"] - 0.45, "swish", -2),
    (T["week"] - 0.35, "pop", 0, 0), (T["domicile2"] - 0.4, "pop", 0, 2), (T["exterieur2"] - 0.4, "pop", 0, 4),
] + [(x["debut"], "tick", 0) for x in extraits_js[1:]] + [
    (extraits_js[-1]["debut"] + 0.1, "bulle", 0, 0),
    (APRES - 0.6, "souffle", 0), (APRES, "swish", -2), (APRES + 0.1, "swish", -4),
    (T["reporte2"] - 0.4, "pop", 0, 0), (T["coupe2"] - 0.4, "pop", 0, 2), (T["coupe2"] - 0.1, "tap", 0), (T["coupe2"] + 0.35, "tick", 0),
    (T["treve2"] - 0.4, "pop", 0, 4), (T["treve2"] - 0.2, "tap", 0), (T["treve2"] + 0.2, "tick", 0), (T["semaine"] - 0.4, "pop", 0, 7),
    (T["continuer"] - 0.6, "souffle", 0), (T["continuer"] - 0.5, "swish", 0), (T["rythme"] - 0.5, "choix", 0),
    (SORTIE, "whoosh", -3),
    (T["coach"] - 0.9, "pop", 0, 0), (T["licence2"] - 0.8, "pop", 0, 3), (T["jouer2"] - 0.3, "secousse", 2),
    (FIN, "whoosh", -2), (FIN + 0.25, "impact", -3), (FIN + 0.9, "scintille", 0), (FIN + 1.05, "pop", -2, 4),
]
# La voix de cette vidéo est enregistrée 7 dB plus bas que celle d'ach10 (-18,8 contre -11,7 LUFS, mesuré sur les rendus bruts) :
# les bruitages descendent d'autant pour garder l'écart à la voix validé sur ach10.
GAIN_SONS = -7.0
sons = [{"t": round(s[0], 3), "son": s[1], "db": s[2] + GAIN_SONS, **({"note": s[3]} if len(s) > 3 else {})} for s in sorted(S, key=lambda s: s[0])]
json.dump(sons, open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"index.html : {len(src)} caractères, {len(st)} sous-titres, {len(EXTRAITS)} extraits, {len(sons)} bruitages ; "
      f"coupe {COUPE:.3f} s, extrait {INSERT:.2f} s ({'fourni' if os.path.exists(EXTRAIT) else 'emplacement réservé'}), durée {DUREE:.2f} s")
