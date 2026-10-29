"""Fabrique la piste son : la musique (medias/musique/fond.wav) et, par-dessus, les bruitages de sons.json
(fichiers .mp3 de medias/sfx/, ou sons synthétisés par outils/sons.py). Usage : python outils/mixer.py <durée> <sortie.wav>"""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sons as B
from wav import ecrire
SR = 48000
lire = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                               capture_output=True, check=True).stdout, dtype="<f4").astype(np.float64).reshape(-1, 2)
duree, sortie = float(sys.argv[1]), sys.argv[2]
n = int(duree * SR)
m = lire("medias/musique/fond.wav")[:n]
m = np.r_[m, np.zeros((n - len(m), 2))]
m *= 10 ** (-6 / 20)                                   # la musique reste un fond : les bruitages passent devant
f = int(1.6 * SR); m[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5       # elle s'éteint sur le carton
m[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
piste = m.copy()
for r in json.load(open("sons.json", encoding="utf-8")):
    if r["son"].endswith(".mp3"):
        x = lire("medias/sfx/" + r["son"]); x = x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20)
    else:
        x = B.SONS[r["son"]](); x = x * 10 ** ((B.NIVEAU[r["son"]] + 9) / 20)
    x = x * 10 ** (r["db"] / 20); i = int(r["t"] * SR); j = min(n, i + len(x))
    piste[i:j] += x[:j - i]
piste /= max(1.0, np.abs(piste).max() / 0.9)
ecrire(sortie, piste, SR)
print(f"piste : {duree:.2f} s, musique + {len(json.load(open('sons.json')))} bruitages -> {sortie}")
