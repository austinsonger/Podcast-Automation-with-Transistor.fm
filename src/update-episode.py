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

def update_episode(episode_id, case_id, data):
    """
    Updates an episode in Transistor.fm with the given data, audio, and image.
    """
    url = f"{TRANSISTOR_API_URL}/{episode_id}"

    # Find the audio and image files
    audio_file = find_first_file_in_directory(os.path.join(CASE_BASE_PATH, case_id, 'audio'), ['mp3', 'wav'])
    image_file = find_first_file_in_directory(os.path.join(CASE_BASE_PATH, case_id, 'images'), ['jpg', 'jpeg', 'png'])

    files = {}
    if audio_file:
        files['audio'] = (os.path.basename(audio_file), open(audio_file, 'rb'), mimetypes.guess_type(audio_file)[0])
    if image_file:
        files['image'] = (os.path.basename(image_file), open(image_file, 'rb'), mimetypes.guess_type(image_file)[0])

    payload = {
        "episode": {
            "show_id": TRANSISTOR_SHOW_ID,
            "title": data['title'],
            "description": data['summary']
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
