"""Assemble index.html à partir d'un carrousel décrit dans carrousels/<nom>.json : les pages défilent une par mesure de
musique, les appuis tombent sur les boutons, les stickers se plaquent au-dessus de la page, puis le carton final.
Écrit aussi sons.json (bruitages) et texte-a-l-ecran.txt.
Usage : python outils/assembler.py car-b   (depuis le dossier carrousels-video)"""
import json, html, sys

NOM = sys.argv[1] if len(sys.argv) > 1 else "car-b"
C = json.load(open(f"carrousels/{NOM}.json", encoding="utf-8"))
M = C["mesure"]                       # une page par mesure (4 temps) : la musique change d'accord au moment où la page glisse
ECHELLE, GAUCHE, HAUT = 0.88, 32, 360  # la page de 1080 × 1350 dans le cadre 1080 × 1920 (voir styles.css)
DUREE_CARTON = M
FIN = round(len(C["pages"]) * M, 3)
DUREE = round(FIN + DUREE_CARTON, 3)

insecable = lambda t: t.replace(" !", " !").replace(" ?", " ?").replace(" :", " :").replace("« ", "« ").replace(" »", " »")

pages_js, pages_html, stickers_js, stickers_html, S = [], [], [], [], []
for i, p in enumerate(C["pages"]):
    debut, fin = round(i * M, 3), round((i + 1) * M, 3)
    appuis = p.get("appuis", [])
    pages_js.append({"debut": debut, "fin": fin, "appuis": [{"a": a["a"]} for a in appuis], **({"vibre": p["vibre"]} if "vibre" in p else {})})
    ronds = "".join(f'<div id="appui-{i}-{k}" class="appui" style="left: {a["x"] * ECHELLE:.0f}px; top: {a["y"] * ECHELLE:.0f}px;"></div>'
                    for k, a in enumerate(appuis))
    pages_html.append(f'        <div id="page-{i}" class="page"><div class="appuyer"><div class="zoom">'
                      f'<img src="medias/pages/{NOM}/{p["image"]}" alt="" />{ronds}</div></div></div>')
    for a in appuis:
        S.append((debut + a["a"] + 0.05, "clic", 0))
    if "vibre" in p:
        S.append((debut + p["vibre"], "vibre", 0))
    for j, s in enumerate(p.get("stickers", [])):
        k = len(stickers_js)
        stickers_js.append({"debut": round(debut + s["a"], 3), "fin": fin, "penche": s["penche"]})
        # deux stickers au plus par page, l'un sous l'autre, entre y = 150 et y = 340 (au-dessus de la page)
        stickers_html.append(f'        <div id="sticker-{k}" class="sticker" style="top: {150 + 100 * j}px;"><span>{html.escape(insecable(s["texte"]))}</span></div>')
        S.append((debut + s["a"] + 0.14, "sticker", -j))
S.append((FIN + 0.2, "tampon", -6))     # le logo se pose

lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
src = lire("index.gabarit.html")
src = src.replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--PAGES-->", "\n".join(pages_html)).replace("<!--STICKERS-->", "\n".join(stickers_html))
src = src.replace("/*PAGESJS*/", json.dumps(pages_js)).replace("/*STICKERSJS*/", json.dumps(stickers_js))
for k, v in {"__FIN__": f"{FIN:.3f}", "__DUREE_CARTON__": f"{DUREE_CARTON:.3f}", "__DUREE__": f"{DUREE:.3f}"}.items():
    src = src.replace(k, v)
assert "__" not in src.replace("__timelines", ""), "repère non remplacé"
open("index.html", "w", encoding="utf-8").write(src)

# Peu de sons, et des bruits réels (Adel, 28/10) : le clic du doigt, la vibration de la notification, le sticker qui se
# plaque. Pas de son sur les glissements de page : c'est la musique qui change d'accord.
# Réglés à la mesure contre la musique (fenêtre de 100 ms) : clic ≈ -10 dB, sticker ≈ -6 dB (-12 sur la musique pleine), vibration ≈ -4 dB
GAIN_SONS = -6.0
PAR_SON = {"clic": 10, "sticker": 6, "vibre": 4, "tampon": 0}
sons = [{"t": round(t, 3), "son": s, "db": d + GAIN_SONS + PAR_SON[s]} for t, s, d in sorted(S)]
json.dump(sons, open("sons.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump({"duree": DUREE, "mesure": M, "pages": len(C["pages"])}, open("musique.json", "w", encoding="utf-8"))

# Le texte visible à l'écran, page par page, pour la session réseaux
lignes = [f"{C['titre']} — vidéo verticale 1080 × 1920, {DUREE:.1f} s", ""]
for i, p in enumerate(C["pages"]):
    lignes.append(f"{i * M:5.1f} s  page {i + 1} : {p['texte']}")
    for s in p.get("stickers", []):
        lignes.append(f"{i * M + s['a']:5.1f} s  sticker : {s['texte']}")
lignes.append(f"{FIN:5.1f} s  carton final : {C['carton']}")
open(f"rendus/{NOM}-texte-a-l-ecran.txt", "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print(f"index.html : {len(C['pages'])} pages de {M} s, {len(stickers_js)} stickers, {len(sons)} bruitages, carton à {FIN} s, durée {DUREE} s")
