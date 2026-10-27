"""Transcrit tous les rushs qui parlent, sur la carte graphique (faster-whisper large-v3-turbo, float16).

Reprend `youtube-clips/outils/transcrire.py` (mots horodatés, .srt, .txt) avec les noms propres de l'épisode.
Lit TRAVAIL/son16/*.wav (fabriqués par preparer_rushs.py), écrit TRAVAIL/transcriptions/. Un rush déjà fait
n'est pas refait.

python outils/transcrire_rushs.py [dossier_travail] [nom_du_rush …]
(sans -I : faster-whisper est installé dans le dossier Python de l'utilisateur)
"""
import os
import site
import sys
from pathlib import Path

# cuBLAS et cuDNN viennent des paquets pip nvidia-* (installés en --user le 27/10/2026)
for base in (site.getusersitepackages(), *site.getsitepackages()):
    for sous in ("cublas", "cudnn", "cuda_nvrtc"):
        dll = Path(base) / "nvidia" / sous / "bin"
        if dll.is_dir():
            os.add_dll_directory(str(dll))
            os.environ["PATH"] = f"{dll};{os.environ['PATH']}"

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "youtube-clips" / "outils"))
from transcrire import WhisperModel, transcribe  # noqa: E402

TRAVAIL = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\App\video\rushs\interview\travail")
PROMPT = ("Interview pour AchhLife, la série YouTube d'Achraf sur la chaîne Achh10. Football, National 2, "
          "Montpellier Atlas Paillade, la Mosson, la Paillade, Montpellier, FoundClub.")

if __name__ == "__main__":
    # ponytail: modèle téléchargé à la main (Invoke-WebRequest) dans modeles/large-v3-turbo, car le téléchargement
    # par huggingface_hub est coupé sur ce PC ; sans ce dossier, faster-whisper le télécharge lui-même.
    local = TRAVAIL.parent / "modeles" / "large-v3-turbo"
    modele = str(local) if (local / "model.bin").exists() else "large-v3-turbo"
    print(f"Chargement {modele}, CUDA float16", flush=True)
    model = WhisperModel(modele, device="cuda", compute_type="float16",
                         download_root=str(TRAVAIL.parent / "modeles"))
    sortie = TRAVAIL / "transcriptions"
    choisis = set(sys.argv[2:])
    for wav in sorted((TRAVAIL / "son16").glob("*.wav")):
        if (choisis and wav.stem not in choisis) or (sortie / f"{wav.stem}-mesures.json").exists():
            continue
        transcribe(model, wav, sortie, wav.stem, prompt=PROMPT)
        print("OK", wav.stem, flush=True)
    print("FINI", flush=True)
