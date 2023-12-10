import pandas as pd
import requests
from datetime import datetime
import pytz
import os

# Constants
CSV_FILE_PATH = './config/scotus.csv'
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
TRANSISTOR_SHOW_ID = '12890'
TRANSISTOR_API_URL = 'https://api.transistor.fm/v1/episodes'

# Paths for audio and images
AUDIO_PATH = '../2023/audio/'
IMAGES_PATH = '../2023/images/'

# Headers for API requests
headers = {"x-api-key": TRANSISTOR_API_KEY}

def create_and_schedule_episode(title, description, audio_filename, cover_image_filename, argument_date):
    cst_timezone = pytz.timezone('America/Chicago')
    scheduled_time = datetime.strptime(argument_date, '%Y-%m-%d').replace(tzinfo=pytz.utc).astimezone(cst_timezone)
    scheduled_time = scheduled_time.replace(hour=20, minute=0, second=0)  # 8 PM CST

    data = {
        'show_id': TRANSISTOR_SHOW_ID,
        'title': title,
        'description': description,
        'status': 'draft',
        'publish_at': scheduled_time.isoformat()
    }

    # Create the episode
    episode_response = requests.post(TRANSISTOR_API_URL, headers=headers, json=data)
    if episode_response.status_code == 201:
        episode_data = episode_response.json()
        episode_id = episode_data['data']['id']

        # Upload audio file
        audio_file_path = os.path.join(AUDIO_PATH, audio_filename)
        with open(audio_file_path, 'rb') as audio_file:
            requests.post(f'{TRANSISTOR_API_URL}/{episode_id}/audio', headers=headers, files={'audio': audio_file})

        # Upload cover image
        cover_image_path = os.path.join(IMAGES_PATH, cover_image_filename)
        with open(cover_image_path, 'rb') as image_file:
            requests.post(f'{TRANSISTOR_API_URL}/{episode_id}/images', headers=headers, files={'image': image_file})
    else:
        print(f'Error creating episode: {episode_response.status_code}')

def main():
    df = pd.read_csv(CSV_FILE_PATH)

    for index, row in df.iterrows():
        title = row['title']
        description = row['description']
        audio_filename = row['audio_file_path']
        cover_image_filename = row['cover_image_path']
        argument_date = row['argument_date']

        create_and_schedule_episode(title, description, audio_filename, cover_image_filename, argument_date)

if __name__ == "__main__":
    main()
