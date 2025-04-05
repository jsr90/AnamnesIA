import os

def load_file(filename):
    """
    Charge le contenu d'un fichier texte.

    Args:
        filename (str): Nom du fichier à charger.

    Returns:
        str: Contenu du fichier.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    full_path = os.path.join(base_path, filename)
    with open(full_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def format_transcription(data):
    """
    Formate les données de transcription en un dialogue structuré.

    Args:
        data (dict): Données de transcription JSON.

    Returns:
        str: Dialogue formaté.
    """
    speaker_mapping = {
        "spk_0": "Kiné",
        "spk_1": "Patient"
    }

    segments = data["results"]["speaker_labels"]["segments"]
    items = data["results"]["items"]

    def get_text_for_segment(segment):
        text = []
        for item in segment["items"]:
            for word in items:
                if word.get("start_time") == item["start_time"]:
                    text.append(word["alternatives"][0]["content"])
        return " ".join(text)

    dialogue = ["[Début de la transcription]"]
    for segment in segments:
        speaker = speaker_mapping.get(segment["speaker_label"], "Inconnu")
        text = get_text_for_segment(segment)
        if text.strip():  # Vérifie que le texte n'est pas vide
            dialogue.append(f"{speaker} : {text}")

    dialogue.append("[Fin de la transcription]")

    formatted_dialogue = "\n".join(dialogue)
    return formatted_dialogue
