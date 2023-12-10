import csv
import os
import requests
import json
import mimetypes
import glob

# Constants
csv_file_path = './config/scotus.csv'
TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
TRANSISTOR_SHOW_ID = os.getenv('TRANSISTOR_SHOW_ID')
headers = {"x-api-key": TRANSISTOR_API_KEY, "Content-Type": "application/json"}
CASE_BASE_PATH = '../2023/'
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

# Dry run flag
DRY_RUN = True


def find_first_file_in_directory(directory_path, file_types):
    """
    Finds the first file in the given directory that matches the file types.
    """
    for file_type in file_types:
        files = glob.glob(os.path.join(directory_path, f'*.{file_type}'))
        if files:
            return files[0]  # Return the first file found
    return None

def authorize_and_upload_audio(episode_id, audio_file_path):
    # Step 1: Authorize Audio Upload
    auth_url = f"{TRANSISTOR_API_URL}/{episode_id}/audio_upload"
    auth_response = requests.post(auth_url, headers=headers)
    upload_url = auth_response.json().get('data', {}).get('url')

    # Step 2: Upload Audio File
    with open(audio_file_path, 'rb') as audio_file:
        upload_response = requests.put(upload_url, data=audio_file)

    if upload_response.status_code != 200:
        print(f"Error uploading audio file: {upload_response.status_code}")
        return None

    return upload_url


def authorize_and_upload_image(episode_id, image_file_path):
    """
    Uploads an image to Imgur and returns the image URL.
    """
    headers = {
        'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'
    }

    with open(image_file_path, 'rb') as image:
        data = {
            'image': image.read(),
            'type': 'file'
        }

        response = requests.post('https://api.imgur.com/3/upload', headers=headers, files=data)
        if response.status_code == 200:
            return response.json()['data']['link']
        else:
            print(f"Error uploading image: {response.status_code}")
            return None




def update_episode(episode_id, case_id, data):
    """
    Updates an episode in Transistor.fm with the given data, audio, and image.
    """
    audio_file = find_first_file_in_directory(os.path.join(CASE_BASE_PATH, case_id, 'audio'), ['mp3', 'wav'])
    image_file = find_first_file_in_directory(os.path.join(CASE_BASE_PATH, case_id, 'images'), ['jpg', 'jpeg', 'png'])

    audio_url = authorize_and_upload_audio(episode_id, audio_file) if audio_file else None
    image_url = authorize_and_upload_image(episode_id, image_file) if image_file else None  

    payload = {
        "episode": {
            "show_id": TRANSISTOR_SHOW_ID,
            "title": data['title'],
            "description": data['summary'],
            "audio_url": audio_url,  # Update the audio URL
            "image_url": image_url   # Update the image URL
        }
    }

    # If DRY_RUN is True, print the information instead of making an actual request
    if DRY_RUN:
        print(f"Dry run: Would update episode {episode_id} with data: {data}")
        print(f"Audio file to upload: {audio_file}")
        print(f"Image file to upload: {image_file}")
        # Close file handles if opened
        for file in files.values():
            file[1].close()
        return {"message": "Dry run, no update made"}

    # Make the actual request if not in dry run mode
    response = requests.put(url, headers=headers, data=payload, files=files)
    for file in files.values():
        file[1].close()

    if response.status_code != 200:
    print(f"Error updating episode: {response.status_code}")
    print(f"Response: {response.text}")  # More detailed logging

    return response.json()    



def process_csv(csv_path):
    """
    Processes each row in the CSV file and updates the corresponding episode.
    """
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if 'Episode ID' in row and row['Episode ID'] and 'Case ID' in row:
                episode_data = {
                    "title": row["Title"],
                    "summary": row["Summary"]
                }

                response = update_episode(row['Episode ID'], row['Case ID'], episode_data)
                print(f"Episode updated: {response}")

# Main execution
process_csv(csv_file_path)
