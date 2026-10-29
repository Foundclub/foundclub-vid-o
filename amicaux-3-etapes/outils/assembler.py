"""Assemble index.html (« Trouver un match amical en 3 étapes », vendredi 30/10) à partir de gabarit.html et de outils/scenes.js,
écrit sons.json (bruitages) et rendus/texte-a-l-ecran.txt.
Usage : python outils/assembler.py   (depuis le dossier du projet, après outils/preparer.sh)"""
import json, html

# Les instants (s). Plan d'Adel (29/10, « 1- A ») : on va dans Matchs amicaux, puis deux solutions — créer son match, ou
# chercher (filtres, annonces) et proposer —, puis l'autre accepte et le match est dans le planning.
T = {"tel": 2.45, "e1": 2.6, "e2": 4.7, "creer": 6.7, "chercher": 14.3, "filtres": 14.9, "retour": 18.1,
     "e3": 19.5, "notif": 19.75, "ouvre": 20.6, "plan": 22.1, "celeb": 24.8, "fin": 26.8}
DUREE_CARTON = 3.0
DUREE = T["fin"] + DUREE_CARTON
K = 560 / 1080                                    # pixels de la capture -> pixels de l'écran du téléphone
# Passages de medias/ecran/etape1.mp4 (outils/preparer.sh) : ton équipe 1,6 s · tes dates 2,4 · l'adversaire 1,8 · publier 1,8
SOUS_A = [T["creer"], T["creer"] + 1.6, T["creer"] + 4.0, T["creer"] + 5.8]
VUES = [("vue-accueil", T["e1"]), ("vue-liste", T["e2"]), ("vue-e1", T["creer"]), ("vue-liste", T["chercher"]),
        ("vue-filtres", T["filtres"]), ("vue-liste", T["retour"]), ("vue-disc", T["e3"]), ("vue-plan", T["plan"])]
ZOOMS = [(SOUS_A[3] + 0.6, T["chercher"] - 0.05, 1.2, 280, 1174),    # « Publier l'annonce »
         (T["retour"] + 0.1, T["e3"] - 0.15, 1.3, 280, 1000),         # la carte de l'annonce, « Proposer un match »
         (T["ouvre"] + 0.2, T["plan"] - 0.25, 1.3, 280, 820),         # la proposition, « Accepter »
         (T["plan"] + 0.35, T["celeb"] + 0.5, 1.22, 280, 600)]        # la carte du match dans le planning
ACTIFS = [("#et-1 .sous", 1, T["e1"]), ("#et-1 .sous", 2, T["e1"] + 1.55)]
ACTIFS += [("#sous-2a", k + 1, t) for k, t in enumerate(SOUS_A)]
ACTIFS += [("#sous-2b", 1, T["filtres"]), ("#sous-2b", 2, T["retour"]), ("#sous-2b", 3, T["retour"] + 0.85)]
ACTIFS += [("#et-3 .sous", 1, T["notif"]), ("#et-3 .sous", 2, T["ouvre"]), ("#et-3 .sous", 3, T["plan"])]
# Appuis : (instant, x, y, largeur, hauteur du bouton) en pixels de la capture (1080 × 2424), lus sur les images.
# Le bouton réagit à l'appui (il s'enfonce, une onde part du doigt), comme dans l'app (Adel, 29/10 : « y'a pas l'animation
# du bouton cliqué »). Un seul appui par geste : plus d'appuis pour montrer les « deux solutions » (« beaucoup trop de clics »).
APPUIS = [(T["e1"] + 1.5, 291, 1531, 470, 300),     # la case « Matchs amicaux » de l'accueil (enregistrement d'Adel)
          (T["creer"] + 0.1, 540, 1228, 976, 150),  # « + Créer un match amical »
          (SOUS_A[3] + 1.45, 540, 2264, 1000, 110), # « Publier l'annonce »
          (T["filtres"] - 0.3, 975, 1448, 110, 110),  # les filtres
          (T["retour"] + 0.95, 445, 2118, 694, 100),  # « Proposer un match » sur la carte d'une annonce
          (T["plan"] - 0.4, 541, 1960, 760, 100)]   # « Accepter » dans la discussion
# « Deux solutions » : un halo sur chaque bouton, l'un après l'autre, sans appui ni son
HALOS = [(T["e2"] + 0.55, 540, 1261, 1000, 150), (T["e2"] + 1.25, 975, 1448, 110, 110)]
APPUI_NOTIF = T["ouvre"] - 0.25           # le doigt touche la notification (posée hors du téléphone)
STICKERS = [(0.2, 2.45, 300, -3, "Pas de match ce week-end ?"),
            (1.0, 2.45, 420, 2, "Trouve un match amical\nen 3 étapes"),
            (25.05, 26.75, 820, -2, "Il ne reste qu'à jouer.")]

insecable = lambda t: t.replace(" !", " !").replace(" ?", " ?").replace(" :", " :").replace("« ", "« ").replace(" »", " »")
boite = lambda x, y, w, h: f"left: {(x - w / 2) * K:.0f}px; top: {(y - h / 2) * K:.0f}px; width: {w * K:.0f}px; height: {h * K:.0f}px;"
appuis_html = [f'        <div id="bouton-{i}" class="bouton" style="{boite(x, y, w, h)}"><div class="onde" style="left: {w * K / 2:.0f}px; top: {h * K / 2:.0f}px;"></div></div>\n'
               f'        <div id="appui-{i}" class="appui" style="left: {x * K:.0f}px; top: {y * K:.0f}px;"></div>' for i, (_, x, y, w, h) in enumerate(APPUIS)]
appuis_html += [f'        <div id="halo-{i}" class="halo" style="{boite(x, y, w, h)}"></div>' for i, (_, x, y, w, h) in enumerate(HALOS)]
appuis_js = [{"t": a[0], "bouton": True} for a in APPUIS]
stickers_html = [f'      <div id="sticker-{i}" class="sticker" style="top: {h}px;"><span>{html.escape(insecable(txt)).replace(chr(10), "<br>")}</span></div>'
                 for i, (_, _, h, _, txt) in enumerate(STICKERS)]
stickers_js = [{"debut": d, "fin": f, "penche": p} for d, f, _, p, _ in STICKERS]

src = open("gabarits/gabarit.html", encoding="utf-8").read()
src = src.replace("/*POLICES*/", open("outils/polices.css", encoding="utf-8").read()).replace("/*JS*/", open("outils/scenes.js", encoding="utf-8").read())
src = src.replace("<!--APPUIS-->", "\n".join(appuis_html)).replace("<!--STICKERS-->", "\n".join(stickers_html))
# l'appui sur la notification est posé dans la notification elle-même
src = src.replace('<div id="notif"><img', f'<div id="notif"><div id="appui-{len(APPUIS)}" class="appui" style="left: 390px; top: 190px;"></div><img')
appuis_js.append({"t": APPUI_NOTIF})
src = src.replace("/*HALOSJS*/", json.dumps([{"t": h[0]} for h in HALOS]))
src = src.replace("/*VUESJS*/", json.dumps([{"id": i, "debut": d} for i, d in VUES]))
src = src.replace("/*ZOOMSJS*/", json.dumps([{"debut": d, "fin": f, "s": z, "ox": x, "oy": y} for d, f, z, x, y in ZOOMS]))
src = src.replace("/*ACTIFSJS*/", json.dumps([{"sel": s, "k": k, "t": t} for s, k, t in ACTIFS]))
src = src.replace("/*T*/", json.dumps(T)).replace("/*APPUISJS*/", json.dumps(appuis_js)).replace("/*STICKERSJS*/", json.dumps(stickers_js))
for k, v in {"__ACCUEIL__": f'{T["e1"]:.3f}', "__DUREE_ACCUEIL__": f'{T["e2"] - T["e1"]:.3f}',
             "__E1__": f'{T["creer"]:.3f}', "__DUREE_E1__": f'{T["chercher"] - T["creer"]:.3f}',
             "__FILTRES__": f'{T["filtres"]:.3f}', "__DUREE_FILTRES__": f'{T["retour"] - T["filtres"]:.3f}',
             "__CELEB__": f'{T["celeb"]:.3f}', "__FIN__": f'{T["fin"]:.3f}',
             "__DUREE_CARTON__": f"{DUREE_CARTON:.3f}", "__DUREE__": f"{DUREE:.3f}"}.items():
    src = src.replace(k, v)
assert "__" not in src.replace("__timelines", ""), "repère non remplacé"
open("index.html", "w", encoding="utf-8").write(src)

# Sound design (Adel, 29/10 : « trouve de meilleurs sons ») : la bibliothèque HyperFrames (sons Pixabay, medias/sfx/CREDITS.md),
# autre série que la vidéo compo (qui a click-soft, notification, whoosh-short). Le « sticker » et la vibration restent
# synthétisés (outils/sons.py). (instant, son, db, réglages) — l'instant est celui où le son doit « tomber » (son pic).
PIC = {"riser.mp3": 3.02, "whoosh-cinematic.mp3": 2.91, "impact-bass-2.mp3": 1.83}
S = [(0.0, "impact-bass-1.mp3", -5, {}),                                   # l'ouverture frappe
     (STICKERS[0][0] + 0.12, "sticker", 0, {}), (STICKERS[1][0] + 0.12, "sticker", -2, {}),
     (T["tel"] + 0.05, "riser.mp3", -7, {"saute": 3.02 - 1.35, "duree": 1.45}),        # la montée vers le téléphone
     (T["tel"] + 0.1, "whoosh-cinematic.mp3", -4, {"saute": 2.0, "duree": 1.8}),
     (T["tel"] + 0.3, "impact-bass-1.mp3", -6, {})]                         # le « 1 » se pose
S += [(T["chercher"] - 0.08, "whoosh.mp3", -9, {})]                          # on passe à « ou cherche-en un »
for e in ("e2", "e3"):
    S += [(T[e] - 0.08, "whoosh.mp3", -6, {}), (T[e] + 0.12, "impact-bass-1.mp3", -10, {})]
S += [(a[0] + 0.05, "click.mp3", -6, {}) for a in APPUIS] + [(APPUI_NOTIF + 0.05, "click.mp3", -6, {})]
S += [(T["notif"] + 0.1, "ping.mp3", -6, {}), (T["notif"], "vibre", -8, {}),
      (T["plan"] + 0.05, "chime.mp3", -8, {}),                                # le match est dans le planning
      (T["celeb"] - 0.05, "whoosh.mp3", -8, {}), (T["celeb"] + 0.05, "impact-bass-1.mp3", -8, {}),
      (STICKERS[2][0] + 0.12, "sticker", 0, {}),
      (T["fin"] + 0.45, "impact-bass-2.mp3", -9, {}), (T["fin"] + 0.85, "sparkle.mp3", -10, {})]
sons = []
for t, son, db, opt in sorted(S, key=lambda s: s[0]):
    debut = t - (PIC.get(son, 0) - opt.get("saute", 0) if son in PIC else 0)
    sons.append({"t": round(max(0, debut), 3), "son": son, "db": db, **opt})
json.dump(sons, open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

lignes = ["Trouver un match amical en 3 étapes — vidéo verticale 1080 × 1920, %.1f s (vendredi 30/10)" % DUREE, "",
          "Texte visible à l'écran, dans l'ordre :", ""]
for d, _, _, _, txt in STICKERS[:2]:
    lignes.append(f"{d:5.2f} s  sticker : {txt.replace(chr(10), ' ')}")
lignes += [f'{T["tel"]:5.2f} s  1 — Va dans Matchs amicaux (Accueil · Matchs amicaux)',
           f'{T["e2"]:5.2f} s  2 — Crée ton match, ou cherche-en un',
           f'{T["creer"]:5.2f} s      (Ton équipe · Tes dates · L\'adversaire · Publier)',
           f'{T["chercher"]:5.2f} s      (Les filtres · Les annonces · Proposer un match)',
           f'{T["e3"]:5.2f} s  3 — L\'autre accepte : c\'est dans le planning (Prévenu · Accepter · Le planning)']
lignes.append(f"{STICKERS[2][0]:5.2f} s  sticker : {STICKERS[2][4]}")
lignes.append(f'{T["fin"]:5.2f} s  carton : FoundClub — Trouve ton prochain match amical — Accueil → Matchs amicaux — App Store, Google Play — foundclub.app')
lignes += ["", "Images : écrans de l'app de recette (données fictives : Montrivage Olympique, Valbrune U13), accueil et filtres de l'enregistrement",
           "  d'Adel (29/10 ; ni cotisations ni clubs à l'écran), plans tournés par FoundClub.",
           "Musique : « Groovy Upbeat Drums and Percussions », SOFRA via Pixabay (Pixabay Content License : usage commercial, crédit facultatif ;",
           "  pas inscrite à Content ID le 30/09 — à revérifier sur sa fiche le jour de la publication). Crédit possible : « Musique : SOFRA via Pixabay ».",
           "Bruitages : bibliothèque HyperFrames, sons Pixabay (Pixabay Content License), et deux sons synthétisés (sticker, vibration)."]
open("rendus/texte-a-l-ecran.txt", "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print(f"index.html : durée {DUREE} s, {len(appuis_js)} appuis, {len(STICKERS)} stickers, {len(sons)} bruitages")
