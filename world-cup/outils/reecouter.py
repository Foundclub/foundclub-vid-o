"""Re-decode un passage precis (debut fin en secondes) avec Whisper, avec 1 s de silence autour.
Usage : python -I reecouter.py <dossier_modele> <audio.wav> <debut> <fin> [<debut> <fin> ...]"""
import sys
import numpy as np, soundfile as sf, sherpa_onnx
d, wav, *bornes = sys.argv[1:]
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/turbo-encoder.int8.onnx", decoder=f"{d}/turbo-decoder.int8.onnx",
    tokens=f"{d}/turbo-tokens.txt", language="fr", task="transcribe", num_threads=4)
a, sr = sf.read(wav, dtype="float32")
pad = np.zeros(sr, dtype=np.float32)
for i in range(0, len(bornes), 2):
    deb, fin = float(bornes[i]), float(bornes[i + 1])
    s = rec.create_stream(); s.accept_waveform(sr, np.concatenate([pad, a[int(deb * sr):int(fin * sr)], pad])); rec.decode_stream(s)
    print(f"{deb:5.1f}-{fin:5.1f} : {s.result.text.strip()}")
