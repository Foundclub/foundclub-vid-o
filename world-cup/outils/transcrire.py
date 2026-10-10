"""Transcrit un fichier audio 16 kHz mono (wav) : decoupe par detection de voix, puis Whisper (sherpa-onnx).
Usage : python -I transcrire.py <dossier_modele> <silero_vad.onnx> <audio.wav> <sortie.srt>"""
import sys, time
import numpy as np, soundfile as sf, sherpa_onnx

dossier, vad_path, wav, srt = sys.argv[1:5]
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{dossier}/turbo-encoder.int8.onnx", decoder=f"{dossier}/turbo-decoder.int8.onnx",
    tokens=f"{dossier}/turbo-tokens.txt", language="fr", task="transcribe", num_threads=4)
cfg = sherpa_onnx.VadModelConfig()
cfg.silero_vad.model = vad_path
cfg.silero_vad.min_silence_duration = 0.2
cfg.silero_vad.max_speech_duration = 8
cfg.sample_rate = 16000
vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=600)
audio, sr = sf.read(wav, dtype="float32")
assert sr == 16000 and audio.ndim == 1, (sr, audio.shape)
segments, w = [], cfg.silero_vad.window_size
def vider():
    while not vad.empty():
        segments.append((vad.front.start / sr, np.array(vad.front.samples, dtype=np.float32))); vad.pop()
for i in range(0, len(audio), w):
    vad.accept_waveform(audio[i:i + w]); vider()
vad.flush(); vider()
def hms(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
t0 = time.time()
with open(srt, "w", encoding="utf-8") as out:
    for n, (debut, ech) in enumerate(segments, 1):
        pad = np.zeros(int(0.5 * sr), dtype=np.float32)  # evite que Whisper coupe le dernier mot
        s = rec.create_stream(); s.accept_waveform(sr, np.concatenate([pad, ech, pad])); rec.decode_stream(s)
        texte = s.result.text.strip()
        out.write(f"{n}\n{hms(debut)} --> {hms(debut + len(ech) / sr)}\n{texte}\n\n")
print(f"{len(segments)} segments, {len(audio)/sr:.1f} s d'audio, decodage {time.time()-t0:.1f} s")
