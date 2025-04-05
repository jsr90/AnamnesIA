import boto3
import time
import json

AWS_REGION = "us-east-1"

def start_transcription(job_name, bucket, filename):
    """
    Démarre un travail de transcription sur AWS Transcribe.

    Args:
        job_name (str): Nom du travail de transcription.
        bucket (str): Nom du bucket S3 contenant le fichier.
        filename (str): Nom du fichier à transcrire.

    Returns:
        None
    """
    transcribe = boto3.client('transcribe', region_name=AWS_REGION)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='fr-FR',
        Media={'MediaFileUri': f"s3://{bucket}/{filename}"},
        OutputBucketName=bucket,
        Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 2}
    )
    print("Transcription démarrée.")

def get_transcription_uri(job_name):
    """
    Attend la fin de la transcription et récupère l'URL du fichier transcrit.

    Args:
        job_name (str): Nom du travail de transcription.

    Returns:
        str: URI du fichier transcrit ou None si échoué.
    """
    transcribe = boto3.client('transcribe', region_name=AWS_REGION)
    try:
        while True:
            response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]
            if status in ["COMPLETED", "FAILED"]:
                break
            print("En attente de la transcription...")
            time.sleep(10)

        if status == "COMPLETED":
            print("Transcription terminée.")
            return response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        elif status == "FAILED":
            print("La transcription a échoué.")
    except Exception as e:
        print(f"Erreur lors de la récupération de l'URI de transcription : {e}")
    return None

def get_transcription(transcription_uri):
    """
    Récupère le contenu de la transcription à partir de l'URI.

    Args:
        transcription_uri (str): URI du fichier transcrit.

    Returns:
        dict: Contenu de la transcription ou None si échoué.
    """
    s3 = boto3.client('s3', region_name=AWS_REGION)
    bucket, key = transcription_uri.replace("https://", "").split("/", 2)[1:3]
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        return json.loads(data)
    except Exception as e:
        print(f"Erreur lors de la récupération de la transcription : {e}")
        return None