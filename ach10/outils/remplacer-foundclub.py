"""Remplace, dans la voix d'ach10, la phrase « Cette application, c'est FoundClub » (16,7–18,9 s)
par une prise refaite où « FoundClub » est prononcé à l'anglaise (a-monter/ach10-foundclub.mov).
L'image ne change pas : la prise est posée sur les lèvres de l'ancienne, en deux morceaux
(« Cette application » / « c'est FoundClub ») recalés chacun sur la base, puis égalisée et mise au
même niveau que le reste de la voix. Fondus de 80 ms dans les silences,
crêtes limitées à -1 dBFS.
Usage : python3 -I outils/remplacer-foundclub.py <video-base> <prise.mov> <sortie.wav> [prise 1|2|3]"""
import sys, subprocess
import numpy as np, soundfile as sf

base_f, prise_f, sortie = sys.argv[1:4]
NUM = sys.argv[4] if len(sys.argv) > 4 else "1"
SR = 48000
# Décalages mesurés (alignement DTW sur le spectre, 10/10/2026) : temps base = temps prise + décalage.
# Morceau 1 = « Cette application », morceau 2 = « c'est FoundClub ». Écart résiduel aux repères :
# prise 1 ±20 ms, prise 2 ±40 ms, prise 3 ±50 ms (seuil de perception : 45 ms en avance, 125 ms en retard).
PRISES = {"1": (9.59, 9.63), "2": (4.22, 4.20), "3": (-2.81, -2.86)}
COUPE = 17.85                     # milieu de la pause après « application », silencieux dans les 4 enregistrements
DEBUT, FIN, FONDU = 16.70, 18.90, 0.08

def lire(f):
    brut = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-ac", "2", "-ar", str(SR),
                           "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(brut, dtype="<f4").reshape(-1, 2).astype(np.float64)

base, prise = lire(base_f), lire(prise_f)
d1, d2 = PRISES[NUM]
t = np.arange(int(DEBUT * SR) - int(FONDU * SR), int(FIN * SR) + int(FONDU * SR)) / SR
def pris(d):  # la prise lue sur l'axe de temps de la base
    i = np.round((t - d) * SR).astype(int)
    return prise[i]
w = np.clip((t - COUPE) / 0.04 + 0.5, 0, 1)[:, None]          # bascule morceau 1 -> 2 en 40 ms
neuf = pris(d1) * (1 - w) + pris(d2) * w

# Timbre : rapport des spectres moyens des deux enregistrements (base 0–16,6 s, prise 7,2–21,7 s),
# lissé au tiers d'octave, borné à ±6 dB, appliqué par un filtre à phase linéaire
def spectre(x):
    n = 2048; m = x.mean(1); trames = [m[i:i + n] * np.hanning(n) for i in range(0, len(m) - n, n // 2)]
    return np.mean([np.abs(np.fft.rfft(f)) ** 2 for f in trames], axis=0)
gb, gn = spectre(base[:int(16.6 * SR)]), spectre(prise[int(7.2 * SR):int(21.7 * SR)])
fq = np.fft.rfftfreq(2048, 1 / SR)
oct_ = np.log2(np.maximum(fq, 20) / 1000)
lisse = lambda s: np.array([s[np.abs(oct_ - o) < 1 / 6].mean() for o in oct_])
corr_db = 10 * np.log10(lisse(gb) / lisse(gn))
corr_db -= np.median(corr_db[(fq > 200) & (fq < 4000)])        # le niveau global se règle à part
corr_db = np.clip(corr_db, -6, 6); corr_db[fq < 60] = 0
h = np.fft.fftshift(np.fft.irfft(10 ** (corr_db / 20)))[1024 - 512:1024 + 513] * np.hanning(1025)
neuf = np.stack([np.convolve(neuf[:, c], h, mode="same") for c in range(2)], 1)

# Niveau. ach10 appuie « FoundClub » plus fort que « Cette application » ; la prise, elle, retombe.
# 1) Chaque morceau reçoit la même énergie que le morceau d'origine qu'il remplace.
# 2) Limiteur à -1 dBFS (anticipation 3 ms, relâchement 20 ms) : la base est écrêtée vers 0 dBFS.
#    Il fait baisser l'énergie : on règle le gain de nouveau jusqu'à ce qu'il tienne.
# 3) Dans les silences de la prise, le souffle est ramené au niveau de celui de la base.
# Les fondus se font dans les silences ; hors de 16,62–18,98 s, la voix d'origine est intacte, échantillon pour échantillon.
rms = lambda x: np.sqrt((x ** 2).mean())
def lisser(cible, att, rel):
    a, r = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR)); out, v = np.empty_like(cible), cible[0]
    for k, c in enumerate(cible):
        v = c + (v - c) * (a if c < v else r)
        out[k] = v
    return out
def niveau_db(x, fen):  # niveau RMS glissant (dB)
    m = (x ** 2).mean(1); n = int(fen * SR)
    return 10 * np.log10(np.convolve(m, np.ones(n) / n, mode="same") + 1e-12)
parole = niveau_db(neuf, 0.010) > -40      # avant gain : souffle de la prise vers -48 dB
PLAFOND = 10 ** (-1 / 20); n3 = int(0.003 * SR)
def limiter(x):
    cible = np.minimum(1, PLAFOND / np.maximum(np.abs(x).max(1), 1e-9))
    cible = np.array([cible[max(0, k - n3):k + n3 + 1].min() for k in range(len(cible))])
    g = lisser(cible, 1e-6, 0.020)
    return x * g[:, None], g
MORCEAUX = [(16.84, 17.76), (17.96, 18.80)]
gains, brut = [1.0, 1.0], neuf
for _ in range(5):
    neuf, g = limiter(brut * (gains[0] * (1 - w) + gains[1] * w))
    for m, (a0, a1) in enumerate(MORCEAUX):
        gains[m] *= rms(base[int(a0 * SR):int(a1 * SR)]) / rms(neuf[(t >= a0) & (t <= a1)])
g1, g2 = gains
neuf, g = limiter(brut * (g1 * (1 - w) + g2 * w))
tenue = int(0.020 * SR)                                        # la voix « tient » 20 ms avant et après
parole = np.convolve(parole.astype(float), np.ones(2 * tenue + 1), mode="same") > 0
fond_cible = rms(base[int(18.84 * SR):int(18.96 * SR)])
fond_actuel = rms(neuf[~parole & (t > DEBUT) & (t < FIN)])
m = lisser(parole.astype(float), 0.010, 0.030)
neuf *= (m + (1 - m) * min(1, fond_cible / fond_actuel))[:, None]
# La pause après « application » (souffle, respiration) : pas plus forte que celle de la base
P0, P1 = 17.76, 17.95
gp = min(1, rms(base[int(P0 * SR):int(P1 * SR)]) / rms(neuf[(t >= P0) & (t <= P1)]))
fen = np.clip(np.minimum(t - P0, P1 - t) / 0.015, 0, 1)
neuf *= (1 - fen * (1 - gp))[:, None]

# Collage : fondu de 80 ms à l'entrée et à la sortie, dans les silences
a = np.clip((t - (DEBUT - FONDU / 2)) / FONDU, 0, 1) * np.clip(((FIN + FONDU / 2) - t) / FONDU, 0, 1)
j = np.round(t * SR).astype(int)
sortie_audio = base.copy()
sortie_audio[j] = base[j] * (1 - a[:, None]) + neuf * a[:, None]
sf.write(sortie, sortie_audio.astype(np.float32), SR, subtype="FLOAT")
fond_base = 20 * np.log10(rms(base[int(18.84 * SR):int(18.96 * SR)]))
fond_neuf = 20 * np.log10(rms(neuf[(t >= 18.84) & (t <= 18.88)]))
print(f"prise {NUM} : gain {20 * np.log10(g1):+.1f} / {20 * np.log10(g2):+.1f} dB, égalisation {corr_db[(fq>100)&(fq<8000)].min():+.1f}/{corr_db[(fq>100)&(fq<8000)].max():+.1f} dB, "
      f"limiteur {20 * np.log10(g.min()):.1f} dB au plus fort, pause {20 * np.log10(gp):+.1f} dB, bruit de fond base {fond_base:.1f} dB / prise {fond_neuf:.1f} dB -> {sortie}")
