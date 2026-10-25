"""Assemble index.html pour un clip à partir de gabarits/ et de clips/NN.json.
Usage : python3 -I outils/assembler.py clips/NN.json"""
import sys, json, html, subprocess
c = json.load(open(sys.argv[1], encoding="utf-8")); NN = f"{c['numero']:02d}"
DUREE_VIDEO = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          f"medias/video/clip-{NN}-carre.mp4"], capture_output=True, text=True).stdout) - 0.02, 2)
DEBUT_FIN = DUREE_VIDEO; DUREE = round(DUREE_VIDEO + 3.4, 2)
FOLLOW = c.get("follow", 3.0)   # la bulle « suivre » (≈ 2 s) ; -1 pour ne pas la mettre
lire = lambda f: open("gabarits/" + f, encoding="utf-8").read()
st = "\n".join(f'        <p id="st-{i}" class="st">' + " ".join(f'<span id="st-{i}-{k}" class="m">{html.escape(m)}</span>' for k, m in enumerate(texte.split())) + "</p>"
               for i, (_, _, texte) in enumerate(c["phrases"]))
partie = f'<span class="etiq partie">{html.escape(c["partie"])}</span>' if c.get("partie") else ""
src = lire("index.gabarit.html").replace("/*POLICES*/", lire("polices.css")).replace("/*STYLES*/", lire("styles.css")).replace("/*JS*/", lire("scenes.js"))
src = src.replace("<!--SOUSTITRES-->", st).replace("/*PHRASES*/", json.dumps([[d, f, [len(m) + 2 for m in t.split()]] for d, f, t in c["phrases"]]))
for k, v in {"__NN__": NN, "__EMISSION__": html.escape(c["emission"]), "__PARTIE__": partie, "__TITRE1__": html.escape(c["titre"][0]),
             "__TITRE2__": html.escape(c["titre"][1]), "__TAILLE1__": f'{min(84, int(1000 / (0.47 * len(c["titre"][0]))))}px',
             "__TAILLE2__": f'{min(78, int(980 / (0.47 * len(c["titre"][1]))))}px',  # Anton, tailles : une seule ligne chacun
             "__TITRE_EPISODE__": html.escape(c["titre_episode"]), "__DUREE_EPISODE__": c["duree_episode"], "__EMISSION_LONGUE__": html.escape(c["emission_longue"]),
             "__CHAINE__": html.escape(c["chaine"]), "__DUREE_VIDEO__": f"{DUREE_VIDEO:.2f}", "__DEBUT_FIN__": f"{DEBUT_FIN:.2f}",
             "__DUREE_FIN__": f"{DUREE - DEBUT_FIN:.2f}", "__DUREE__": f"{DUREE:.2f}", "__FOLLOW__": f"{FOLLOW:.2f}"}.items():
    src = src.replace(k, v)
open("index.html", "w", encoding="utf-8").write(src)
# Bruitages du clip : l'accroche, les coupes de plan, le carton final (bibliothèque outils/sons.py)
sons = [dict(t=0.1, son="swish"), dict(t=0.35, son="pop", note=7), dict(t=1.0, son="tap", db=-4)]
sons += [dict(t=t, son="coupe", db=-6) for t in c.get("coupes", []) if 0.8 < t < DUREE_VIDEO - 0.3]
if FOLLOW >= 0:   # bulle « suivre » : la photo, le bouton, l'appui, la coche
    sons += [dict(t=FOLLOW, son="pop", note=4, db=-3), dict(t=FOLLOW + 0.18, son="pop", note=9, db=-6), dict(t=FOLLOW + 0.62, son="tap", db=-2), dict(t=FOLLOW + 0.8, son="choix", note=7, db=-6)]
F = DEBUT_FIN
sons += [dict(t=F, son="whoosh", db=-2), dict(t=F + 0.1, son="swish", db=-3), dict(t=F + 0.3, son="pop", note=7, db=-2),
         dict(t=F + 0.6, son="whoosh", db=-6), dict(t=F + 0.95, son="impact", db=-8), dict(t=F + 1.45, son="tick", db=-2)]
json.dump(sons, open("sons.json", "w", encoding="utf-8"), indent=0)
print(f"index.html : clip {NN}, {len(c['phrases'])} phrases, vidéo {DUREE_VIDEO} s + carton 3,4 s")
