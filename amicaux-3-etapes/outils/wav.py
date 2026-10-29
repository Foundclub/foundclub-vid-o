"""Écrit un WAV stéréo 24 bits avec la bibliothèque standard (soundfile n'est pas installé sur le PC d'Adel)."""
import wave, numpy as np

def ecrire(chemin, x, sr=48000):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    assert np.abs(x).max() < 1.0, "le WAV saturerait"
    e = np.round(x * (2 ** 23 - 1)).astype("<i4").reshape(-1)
    octets = e.view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
    with wave.open(chemin, "wb") as w:
        w.setnchannels(2); w.setsampwidth(3); w.setframerate(sr); w.writeframes(octets)
