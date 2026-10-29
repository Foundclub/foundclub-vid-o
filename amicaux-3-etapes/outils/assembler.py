"""Assemble index.html (« Trouver un match amical en 3 étapes », vendredi 30/10) à partir de gabarit.html et de outils/scenes.js,
écrit sons.json (bruitages) et rendus/texte-a-l-ecran.txt.
Usage : python outils/assembler.py   (depuis le dossier du projet, après outils/preparer.sh)"""
import json, html

# Les instants (s). La musique (120 temps/min) bat la mesure toutes les 2 s : les étapes changent sur une mesure.
# Allongée le 29/10 (« ça va trop vite ») : 25 -> 29,8 s, chaque étape reste plus longtemps
# 29/10 (Adel) : l'étape 2 montre l'autre équipe qui cherche et filtre ; la notification passe dans l'étape 3
T = {"tel": 2.45, "e1": 2.7, "e2": 11.5, "filtres": 12.4, "retour": 16.4, "e3": 18.0, "notif": 18.3, "ouvre": 19.55,
     "acc": 21.3, "plan": 22.7, "celeb": 24.8, "fin": 26.8}
T["sous1"] = [2.7, 4.9, 7.5, 9.5]          # les 5 passages de medias/ecran/etape1.mp4 (outils/preparer.sh)
DUREE_CARTON = 3.0
DUREE = T["fin"] + DUREE_CARTON
K = 560 / 1080                                    # pixels de la capture -> pixels de l'écran du téléphone
# Appuis : (instant, x, y) en pixels de la capture d'origine (1080 × 2424), lus sur les images
APPUIS = [(2.95, 540, 1228),     # « + Créer un match amical »
          (11.15, 540, 2264),    # « Publier l'annonce »
          (12.2, 918, 1343),     # l'autre équipe ouvre les filtres (liste de recette)
          (17.35, 425, 2075),    # « Proposer un match » sur la carte d'une annonce
          (20.9, 541, 1960),     # « Accepter » dans la discussion
          (22.3, 538, 1403)]     # « Accepter » de « Accepter cette proposition ? »
APPUI_NOTIF = 19.3               # le doigt touche la notification (posée hors du téléphone)
STICKERS = [(0.2, 2.45, 300, -3, "Pas de match ce week-end ?"),
            (1.0, 2.45, 420, 2, "Trouve un match amical\nen 3 étapes"),
            (25.05, 26.75, 820, -2, "Il ne reste qu'à jouer.")]

insecable = lambda t: t.replace(" !", " !").replace(" ?", " ?").replace(" :", " :").replace("« ", "« ").replace(" »", " »")
appuis_html = [f'        <div id="appui-{i}" class="appui" style="left: {x * K:.0f}px; top: {y * K:.0f}px;"></div>' for i, (_, x, y) in enumerate(APPUIS)]
appuis_js = [{"t": t} for t, _, _ in APPUIS]
stickers_html = [f'      <div id="sticker-{i}" class="sticker" style="top: {h}px;"><span>{html.escape(insecable(txt)).replace(chr(10), "<br>")}</span></div>'
                 for i, (_, _, h, _, txt) in enumerate(STICKERS)]
stickers_js = [{"debut": d, "fin": f, "penche": p} for d, f, _, p, _ in STICKERS]

src = open("gabarits/gabarit.html", encoding="utf-8").read()
src = src.replace("/*POLICES*/", open("outils/polices.css", encoding="utf-8").read()).replace("/*JS*/", open("outils/scenes.js", encoding="utf-8").read())
src = src.replace("<!--APPUIS-->", "\n".join(appuis_html)).replace("<!--STICKERS-->", "\n".join(stickers_html))
# l'appui sur la notification est posé dans la notification elle-même
src = src.replace('<div id="notif"><img', f'<div id="notif"><div id="appui-{len(APPUIS)}" class="appui" style="left: 390px; top: 190px;"></div><img')
appuis_js.append({"t": APPUI_NOTIF})
src = src.replace("/*T*/", json.dumps(T)).replace("/*APPUISJS*/", json.dumps(appuis_js)).replace("/*STICKERSJS*/", json.dumps(stickers_js))
for k, v in {"__E1__": f'{T["e1"]:.3f}', "__DUREE_E1__": "8.8", "__FILTRES__": f'{T["filtres"]:.3f}', "__DUREE_FILTRES__": f'{T["retour"] - T["filtres"]:.3f}', "__CELEB__": f'{T["celeb"]:.3f}', "__FIN__": f'{T["fin"]:.3f}',
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
S += [(t, "key-press.mp3", -14, {}) for t in (T["filtres"], T["retour"], T["ouvre"], T["plan"])]
for e in ("e2", "e3"):
    S += [(T[e] - 0.08, "whoosh.mp3", -6, {}), (T[e] + 0.12, "impact-bass-1.mp3", -10, {})]
S += [(t, "key-press.mp3", -14, {}) for t in T["sous1"][1:]]               # les sous-étapes qui s'allument
S += [(t + 0.05, "click.mp3", -6, {}) for t, _, _ in APPUIS] + [(APPUI_NOTIF + 0.05, "click.mp3", -6, {})]
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
lignes += [f'{T["tel"]:5.2f} s  1 — Publie ton annonce (Ton équipe · Tes dates · L\'adversaire · Publier)',
           f'{T["e2"]:5.2f} s  2 — Une équipe cherche un match (Les annonces · Les filtres · Proposer un match)',
           f'{T["e3"]:5.2f} s  3 — Tu acceptes, c\'est dans le planning (Tu es prévenu · Accepter · Le planning)']
lignes.append(f"{STICKERS[2][0]:5.2f} s  sticker : {STICKERS[2][4]}")
lignes.append(f'{T["fin"]:5.2f} s  carton : FoundClub — Trouve ton prochain match amical — Accueil → Matchs amicaux — App Store, Google Play — foundclub.app')
lignes += ["", "Images : écrans de l'app de recette (données fictives : Montrivage Olympique, Valbrune U13), plans tournés par FoundClub.",
           "Musique : « Groovy Upbeat Drums and Percussions », SOFRA via Pixabay (Pixabay Content License : usage commercial, crédit facultatif ;",
           "  pas inscrite à Content ID le 30/09 — à revérifier sur sa fiche le jour de la publication). Crédit possible : « Musique : SOFRA via Pixabay ».",
           "Bruitages : bibliothèque HyperFrames, sons Pixabay (Pixabay Content License), et deux sons synthétisés (sticker, vibration)."]
open("rendus/texte-a-l-ecran.txt", "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print(f"index.html : durée {DUREE} s, {len(appuis_js)} appuis, {len(STICKERS)} stickers, {len(sons)} bruitages")
