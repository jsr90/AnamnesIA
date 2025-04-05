import sounddevice as sd
import wave
from datetime import datetime

try:
    import keyboard  # Nécessaire pour détecter les touches du clavier
except ImportError:
    print("Le module 'keyboard' n'est pas installé. Veuillez l'installer avec 'pip install keyboard'.")
    raise

def record_audio(samplerate=44100):
    """
    Enregistre de l'audio et sauvegarde dans un fichier WAV.

    Args:
        samplerate (int): Taux d'échantillonnage de l'enregistrement (par défaut 44100).

    Returns:
        str: Chemin du fichier audio enregistré.
    """
    audio_path = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

    print("Recording... Press 'q' to stop.")
    frames = []

    try:
        # Vérifiez le périphérique audio par défaut
        device_info = sd.query_devices(sd.default.device[0], 'input')
        max_channels = device_info['max_input_channels']
        channels = min(2, max_channels)  # Utilisez au maximum 2 canaux ou moins si non supporté
    except Exception as e:
        print(f"Erreur lors de la vérification du périphérique audio : {e}")
        return None

    try:
        while not keyboard.is_pressed('q'):  # Interrompt l'enregistrement si 'q' est pressé
            try:
                recording = sd.rec(int(1 * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
                sd.wait()
                frames.append(recording)
            except Exception as e:
                print(f"Erreur lors de l'enregistrement d'une trame audio : {e}")
                break
    except KeyboardInterrupt:
        print("Recording interrupted manually.")
    except Exception as e:
        print(f"Erreur inattendue lors de l'enregistrement audio : {e}")

    try:
        with wave.open(audio_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(b''.join(frame.tobytes() for frame in frames))
        print("Recording saved as", audio_path)
        return audio_path
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier audio : {e}")
        return None