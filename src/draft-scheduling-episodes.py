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

def extract_argument_date_from_title(title):
    # Extract the argument date from the title, assuming it's in the format "[Arg: date]"
    date_start = title.find("[Arg: ")
    date_end = title.find("]", date_start)
    if date_start != -1 and date_end != -1:
        date_str = title[date_start + 6 : date_end].strip()
        try:
            argument_date = datetime.strptime(date_str, '%m.%d.%Y').strftime('%Y-%m-%d')
            return argument_date
        except ValueError:
            pass
    return None

def create_and_schedule_episode(title, summary):
    argument_date = extract_argument_date_from_title(title)

    if argument_date is not None:
        cst_timezone = pytz.timezone('America/Chicago')
        scheduled_time = datetime.strptime(argument_date, '%Y-%m-%d').replace(tzinfo=pytz.utc).astimezone(cst_timezone)
        scheduled_time = scheduled_time.replace(hour=20, minute=0, second=0)  # 8 PM CST

        data = {
            'show_id': TRANSISTOR_SHOW_ID,
            'title': title,
            'description': summary,  # Use the 'Summary' column as the description
            'status': 'draft',
            'publish_at': scheduled_time.isoformat()
        }

        # Create the episode
        episode_response = requests.post(TRANSISTOR_API_URL, headers=headers, json=data)
        if episode_response.status_code == 201:
            episode_data = episode_response.json()
            episode_id = episode_data['data']['id']

            # Upload audio file (assuming it's located at the same path for all episodes)
            audio_file_path = os.path.join(AUDIO_PATH, f'{episode_id}.mp3')
            with open(audio_file_path, 'rb') as audio_file:
                requests.post(f'{TRANSISTOR_API_URL}/{episode_id}/audio', headers=headers, files={'audio': audio_file})

            # Upload cover image (assuming it's located at the same path for all episodes)
            cover_image_path = os.path.join(IMAGES_PATH, f'{episode_id}.jpg')
            with open(cover_image_path, 'rb') as image_file:
                requests.post(f'{TRANSISTOR_API_URL}/{episode_id}/images', headers=headers, files={'image': image_file})
        else:
            print(f'Error creating episode: {episode_response.status_code}')

def main():
    df = pd.read_csv(CSV_FILE_PATH)

    for index, row in df.iterrows():
        title = row['Title']
        summary = row['Summary']

        create_and_schedule_episode(title, summary)

if __name__ == "__main__":
    main()
