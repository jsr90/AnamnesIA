import os
import json
from openai import OpenAI, OpenAIError
from langchain import PromptTemplate
from .utils import load_file

# Charger la clé API depuis la variable d'environnement
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_anamnesis_data(template_path="data/template.txt", transcription=None, transcription_path=None):
    """
    Génère les données d'anamnèse en utilisant l'API OpenAI.

    Args:
        template_path (str): Chemin vers le fichier template.
        transcription (str, optional): Texte de la transcription.
        transcription_path (str, optional): Chemin vers le fichier de transcription.

    Returns:
        dict: Données d'anamnèse générées ou None en cas d'erreur.
    """
    try:
        # Charger les fichiers
        template = load_file(template_path)
        print(f"Template chargé depuis {template_path}")
        if transcription is None:
            transcription = load_file(transcription_path)
    except FileNotFoundError as e:
        print(f"Erreur: {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue lors du chargement des fichiers: {e}")
        return None

    try:
        # Remplacer le placeholder dans le template par la transcription
        prompt_template = PromptTemplate(
            input_variables=["transcription"], template=template)
        prompt = prompt_template.template.format(transcription=transcription)

        # Appeler l'API OpenAI avec le modèle choisi
        response = client.responses.create(
            model="gpt-3.5-turbo",
            instructions="Vous êtes un assistant médical spécialisé en kinésithérapie.",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt}
                    ]
                }
            ]
        )

        # Traiter la réponse de l'API
        res = response.output[0].content[0].text.replace(
            "\n", "").replace("  ", "")
        data = json.loads(res)
        return data
    except OpenAIError as e:
        print(f"Erreur lors de l'appel à l'API OpenAI: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Erreur lors du décodage de la réponse JSON: {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return None
