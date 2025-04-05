import boto3
import os

def upload_to_s3(filename, bucket):
    """
    Télécharge un fichier dans un bucket S3.

    :param filename: Nom du fichier local à télécharger.
    :param bucket: Nom du bucket S3.
    """
    s3 = boto3.client('s3')
    
    # Vérifier si le bucket existe
    try:
        s3.head_bucket(Bucket=bucket)
    except s3.exceptions.ClientError:
        # Créer le bucket s'il n'existe pas
        s3.create_bucket(Bucket=bucket)
        print(f"Bucket {bucket} créé.")

    # Obtenir le nom du fichier sans le chemin complet
    filename_only = os.path.basename(filename)
    
    # Ajouter le préfixe "audio/"
    s3_key = f"audio/{filename_only}"

    # Télécharger le fichier avec le chemin modifié
    s3.upload_file(filename, bucket, s3_key)
    print(f"Fichier {filename} téléchargé dans le bucket S3 {bucket} sous {s3_key}")
    return s3_key