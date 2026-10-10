"""Pour chaque bruitage pris seul : son niveau le plus fort (100 ms) face au niveau de la voix autour (400 ms).
Usage : python3 -I outils/mesurer-sons.py [sons.json] [voix.wav ou vidéo]"""
import sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, "outils"); import sons as B
voix = sys.argv[2] if len(sys.argv) > 2 else "medias/video/ach10-voix.wav"
sr = 48000
vm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", voix, "-map", "0:a:0", "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                   capture_output=True, check=True).stdout, dtype="<f4").astype(np.float64).reshape(-1, 2).mean(1)   # comme la mesure des bruitages
L = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "sons.json"))
def court(x, n):  # niveau RMS glissant
    e = np.convolve(x ** 2, np.ones(n) / n, mode="valid"); return 10 * np.log10(e + 1e-12)
par = {}
for r in L:
    f = B.SONS[r["son"]]; x = (f(r.get("note", 0)) if r["son"] in B.AVEC_NOTE else f()).mean(1)
    x *= 10 ** ((B.NIVEAU[r["son"]] + r.get("db", 0)) / 20)
    e = court(x, int(0.1 * sr)); k = int(np.argmax(e)); pic = e[k]
    t_pic = r["t"] + (k - (len(x) if r["son"] in B.FINIT_A_T else 0)) / sr
    a = int((t_pic - 0.2) * sr); seg = vm[max(0, a):a + int(0.4 * sr)]
    voix = 10 * np.log10((seg ** 2).mean() + 1e-12) if len(seg) > sr * 0.1 else float("nan")
    par.setdefault(r["son"], []).append(pic - voix)
for k, x in sorted(par.items(), key=lambda kv: -np.nanmedian(kv[1])):
    x = np.array(x); x = x[~np.isnan(x)]
    if len(x): print(f"{k:9} {np.median(x):+6.1f} dB sous/sur la voix (de {x.min():+.1f} à {x.max():+.1f}, n={len(x)})")
