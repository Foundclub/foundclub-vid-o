"""Assemble index.html (« Trouver un match amical en 3 étapes », vendredi 30/10) à partir de gabarit.html et de outils/scenes.js,
écrit sons.json (bruitages) et rendus/texte-a-l-ecran.txt.
Usage : python outils/assembler.py   (depuis le dossier du projet, après outils/preparer.sh)"""
import json, html

# Les instants (s). La musique (120 temps/min) bat la mesure toutes les 2 s : les étapes changent sur une mesure.
# Allongée le 29/10 (« ça va trop vite ») : 25 -> 29,8 s, chaque étape reste plus longtemps
T = {"tel": 2.45, "e1": 2.7, "e2": 13.5, "notif": 13.85, "ouvre": 15.4, "e3": 19.0, "plan": 21.0, "celeb": 24.8, "fin": 26.8}
T["sous1"] = [2.7, 4.9, 7.9, 9.9, 11.5]          # les 5 passages de medias/ecran/etape1.mp4 (outils/preparer.sh)
DUREE_CARTON = 3.0
DUREE = T["fin"] + DUREE_CARTON
K = 560 / 1080                                    # pixels de la capture -> pixels de l'écran du téléphone
# Appuis : (instant, x, y) en pixels de la capture d'origine (1080 × 2424), lus sur les images
APPUIS = [(2.95, 540, 1228),     # « + Créer un match amical »
          (13.15, 540, 2264),     # « Publier l'annonce »
          (18.4, 541, 1960),    # « Accepter » dans la discussion
          (20.55, 538, 1403)]     # « Accepter » de « Accepter cette proposition ? »
APPUI_NOTIF = 15.15               # le doigt touche la notification (posée hors du téléphone)
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
for k, v in {"__E1__": f'{T["e1"]:.3f}', "__DUREE_E1__": "10.8", "__CELEB__": f'{T["celeb"]:.3f}', "__FIN__": f'{T["fin"]:.3f}',
             "__DUREE_CARTON__": f"{DUREE_CARTON:.3f}", "__DUREE__": f"{DUREE:.3f}"}.items():
    src = src.replace(k, v)
assert "__" not in src.replace("__timelines", ""), "repère non remplacé"
open("index.html", "w", encoding="utf-8").write(src)

# Bruitages : peu, et réels (Adel, 28/10) — clics de l'écran, la notification qui arrive et le téléphone qui vibre,
# les stickers qui se plaquent. Les fichiers .mp3 viennent de la bibliothèque Pixabay (medias/sfx/CREDITS.md) ; « sticker »,
# « vibre » et « tampon » sont synthétisés (outils/sons.py du « week-end gâché »). db : réglage par rapport à la musique.
S = [(d + 0.14, "sticker", -2) for d, _, _, _, _ in STICKERS]
S += [(t + 0.05, "click-soft.mp3", -4) for t, _, _ in APPUIS] + [(APPUI_NOTIF + 0.05, "click-soft.mp3", -4)]
S += [(T["notif"], "notification.mp3", -11), (T["notif"], "vibre", -9), (T["fin"] + 0.15, "tampon", -6)]
json.dump([{"t": round(t, 3), "son": s, "db": d} for t, s, d in sorted(S)], open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

lignes = ["Trouver un match amical en 3 étapes — vidéo verticale 1080 × 1920, %.1f s (vendredi 30/10)" % DUREE, "",
          "Texte visible à l'écran, dans l'ordre :", ""]
for d, _, _, _, txt in STICKERS[:2]:
    lignes.append(f"{d:5.2f} s  sticker : {txt.replace(chr(10), ' ')}")
lignes += [f'{T["tel"]:5.2f} s  1 — Publie ton annonce (Ton équipe · Tes dates · L\'adversaire · Un mot · Publier)',
           f'{T["e2"]:5.2f} s  2 — Une équipe te propose un match (Tu es prévenu · Vous en parlez)',
           f'{T["e3"]:5.2f} s  3 — Tu acceptes, c\'est dans le planning (Accepter · Le planning des deux équipes)']
lignes.append(f"{STICKERS[2][0]:5.2f} s  sticker : {STICKERS[2][4]}")
lignes.append(f'{T["fin"]:5.2f} s  carton : FoundClub — Trouve ton prochain match amical — Accueil → Matchs amicaux — App Store, Google Play — foundclub.app')
lignes += ["", "Images : écrans de l'app de recette (données fictives : Montrivage Olympique, Valbrune U13), plans tournés par FoundClub.",
           "Musique : « Race The Sun », Scott Buckley — licence CC BY 4.0 : le crédit est OBLIGATOIRE dans la description de chaque post :",
           "  Race The Sun by Scott Buckley – released under CC-BY 4.0. www.scottbuckley.com.au",
           "Bruitages : bibliothèque Pixabay (clic, notification), et sons synthétisés (sticker, vibration, tampon)."]
open("rendus/texte-a-l-ecran.txt", "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print(f"index.html : durée {DUREE} s, {len(appuis_js)} appuis, {len(STICKERS)} stickers, {len(S)} bruitages")
