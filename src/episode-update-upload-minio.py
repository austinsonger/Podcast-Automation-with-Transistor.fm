import csv
import os
import requests
from minio import Minio
from minio.error import S3Error
import mimetypes
import glob


# Constants from previous script
csv_file_path = './config/scotus.csv'
TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
TRANSISTOR_SHOW_ID = os.getenv('TRANSISTOR_SHOW_ID')
headers = {"x-api-key": TRANSISTOR_API_KEY, "Content-Type": "application/json"}
CASE_BASE_PATH = '../2023/'

# MinIO Configuration
minio_client = Minio(
    'YOUR_MINIO_ENDPOINT',
    access_key='YOUR_ACCESS_KEY',
    secret_key='YOUR_SECRET_KEY',
    secure=True
)

bucket_name = '<BUCKET-NAME>'

def upload_file_to_minio(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        return minio_client.presigned_get_object(bucket_name, object_name)
    except S3Error as e:
        print(f"MinIO Error: {e}")
        return None

def update_transistor_episode(episode_id, audio_url=None, image_url=None):
    url = f"https://api.transistor.fm/v1/episodes/{episode_id}"
    headers = {"x-api-key": "YOUR_TRANSISTOR_API_KEY", "Content-Type": "application/json"}

    payload = {
        "episode": {
            "audio_url": audio_url,
            "image_url": image_url
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

# Example usage
audio_url = upload_file_to_minio('/path/to/audio.mp3', bucket_name)
image_url = upload_file_to_minio('/path/to/image.jpg', bucket_name)

response = update_transistor_episode('episode_id_here', audio_url, image_url)
print(response)
