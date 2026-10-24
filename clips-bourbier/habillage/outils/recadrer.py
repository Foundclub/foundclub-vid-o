"""Prépare la vidéo carrée 1080×1080 d'un clip, à partir de l'extrait horizontal (1920×1080).
Deux formats, choisis dans clips/NN.json ("format") :
- "carre" : un carré qui suit la personne qui parle, pleine hauteur ou de côté "cote" pris en haut de l'image
  (pour laisser dehors un bandeau incrusté en bas, comme le nom du président dans le clip 10). Le centre horizontal suit des repères posés à la main
  ("cadrage" : [[t, centre_x], ...]), lissés dans chaque plan et coupés net aux changements de plan ("coupes").
- "large" : l'image entière en 16:9 au milieu, sur la même image floutée (match, drone, montages : rien n'est coupé).
Usage : python3 -I outils/recadrer.py clips/NN.json"""
import sys, json, subprocess
import numpy as np

cfg = json.load(open(sys.argv[1], encoding="utf-8"))
src = cfg["source"]; sortie = f"medias/video/clip-{cfg['numero']:02d}-carre.mp4"
# "garder" : [début, fin] en secondes de l'extrait (fin None = jusqu'au bout), pour raccourcir un clip
debut, fin = (cfg.get("garder") or [0, None])
PLAGE = ["-ss", str(debut)] + (["-t", str(round(fin - debut, 3))] if fin else [])
SORTIE = ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
          "-movflags", "+faststart", sortie]
if cfg.get("format", "large") == "large":
    subprocess.run(["ffmpeg", "-v", "error", "-y", *PLAGE, "-i", src, "-filter_complex",
                    "[0:v]split=2[bg][fg];[bg]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,gblur=sigma=30,"
                    "eq=brightness=-0.12[fond];[fg]scale=1080:608:flags=lanczos[img];[fond][img]overlay=0:236,setsar=1[v]",
                    "-map", "[v]", "-map", "0:a", *SORTIE], check=True)
    print(f"{sortie} : image entière sur fond flou"); sys.exit()
W, H, FPS = 1920, 1080, 30
C = cfg.get("cote", 1080)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
dur = (fin or dur) - debut
n = int(round(dur * FPS))
t = np.arange(n) / FPS
coupes = [0.0] + cfg.get("coupes", []) + [dur + 1]
reperes = sorted(cfg["cadrage"])                       # [[t, centre_x], ...]
cx = np.zeros(n)
for a, b in zip(coupes[:-1], coupes[1:]):              # chaque plan à part
    m = (t >= a) & (t < b)
    if not m.any(): continue
    r = [(rt, rc) for rt, rc in reperes if a <= rt < b] or [min(reperes, key=lambda p: abs(p[0] - (a + b) / 2))]
    rt, rc = np.array([p[0] for p in r]), np.array([p[1] for p in r], float)
    cx[m] = np.interp(t[m], rt, rc)
    # lissage dans le plan (gaussienne de 0,45 s), sans déborder sur le plan voisin
    k = np.exp(-0.5 * (np.arange(-40, 41) / (0.45 * FPS)) ** 2); k /= k.sum()
    seg = cx[m]; pad = np.pad(seg, 40, mode="edge"); cx[m] = np.convolve(pad, k, mode="same")[40:-40]
x0 = np.clip(np.round(cx - C / 2), 0, W - C).astype(int)
dec = subprocess.Popen(["ffmpeg", "-v", "error", *PLAGE, "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{C}x{C}", "-r", str(FPS), "-i", "-",
                        *PLAGE, "-i", src, "-map", "0:v", "-map", "1:a", "-shortest",
                        *([] if C == 1080 else ["-vf", "scale=1080:1080:flags=lanczos"]), *SORTIE], stdin=subprocess.PIPE)
taille = W * H * 3
for i in range(n + 5):
    buf = dec.stdout.read(taille)
    if len(buf) < taille: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    j = min(i, n - 1)
    enc.stdin.write(np.ascontiguousarray(img[:C, x0[j]:x0[j] + C]).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print(f"{sortie} : {n} images, cadre de {x0.min()} à {x0.max()} px")
