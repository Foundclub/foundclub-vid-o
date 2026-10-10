"""Trouve l'instant ou chaque mot-cle vient d'etre prononce : on decode [debut, t] et on cherche
le plus petit t dont la transcription contient le mot (recherche par dichotomie, precision 50 ms).
Usage : python -I caler_mots.py <dossier_modele> <audio.wav> <debut> <fin> <mot1> [<mot2> ...]"""
import sys, unicodedata
import numpy as np, soundfile as sf, sherpa_onnx
d, wav, deb, fin, *mots = sys.argv[1:]
deb, fin = float(deb), float(fin)
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/turbo-encoder.int8.onnx", decoder=f"{d}/turbo-decoder.int8.onnx",
    tokens=f"{d}/turbo-tokens.txt", language="fr", task="transcribe", num_threads=4)
a, sr = sf.read(wav, dtype="float32")
pad = np.zeros(int(0.6 * sr), dtype=np.float32)
norm = lambda s: unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()
cache = {}
def texte(t):
    t = round(t, 2)
    if t not in cache:
        s = rec.create_stream(); s.accept_waveform(sr, np.concatenate([pad, a[int(deb * sr):int(t * sr)], pad])); rec.decode_stream(s)
        cache[t] = norm(s.result.text)
    return cache[t]
bas = deb + 0.2
for mot in mots:
    m, lo, hi = norm(mot), bas, fin
    if m not in texte(hi):
        print(f"{mot:>16} : introuvable dans [{deb}, {fin}] -> {texte(hi)}"); continue
    while hi - lo > 0.05:
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if m in texte(mid) else (mid, hi)
    print(f"{mot:>16} : fini a {hi:6.2f} s"); bas = max(bas, hi - 0.6)
