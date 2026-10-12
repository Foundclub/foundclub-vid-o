"""Recadre une coupe 16:9 (1920x1080) en carré 1080x1080 qui suit la personne qui parle.
Le carré source fait 800x800 et s'arrête à y=800 : les sous-titres incrustés de la vidéo YouTube (y >= 838)
restent dehors. Le centre horizontal suit des repères posés à la main (clips/NN.json, "cadrage"),
lissés dans chaque plan et coupés net aux changements de plan.
Usage : python3 -I outils/recadrer.py clips/NN.json"""
import sys, json, subprocess
import numpy as np

cfg = json.load(open(sys.argv[1], encoding="utf-8"))
src = cfg["source"]; sortie = f"medias/video/clip-{cfg['numero']:02d}-carre.mp4"
W, H, C, FPS = 1920, 1080, 800, 30
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
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
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{C}x{C}", "-r", str(FPS), "-i", "-",
                        "-i", src, "-map", "0:v", "-map", "1:a", "-vf", "scale=1080:1080:flags=lanczos,unsharp=5:5:0.6",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", sortie], stdin=subprocess.PIPE)
taille = W * H * 3
for i in range(n + 5):
    buf = dec.stdout.read(taille)
    if len(buf) < taille: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    j = min(i, n - 1)
    enc.stdin.write(np.ascontiguousarray(img[0:C, x0[j]:x0[j] + C]).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print(f"{sortie} : {n} images, cadre de {x0.min()} à {x0.max()} px")
