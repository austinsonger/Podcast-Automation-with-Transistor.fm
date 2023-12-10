"""
# Podcast Episode Draft Creator Script

## Overview
This script automates the creation of podcast episode drafts by reading episode details from a CSV file and uploading them to the Transistor.fm platform using its API. It is ideal for podcasters who manage episode details in a spreadsheet and wish to streamline the process of creating drafts in their Transistor.fm account.

## Functionality
- **CSV Parsing**: Reads titles and summaries of podcast episodes from a CSV file.
- **Draft Episode Creation**: Creates draft episodes on Transistor.fm for each entry in the CSV file.
- **API Integration**: Utilizes Transistor.fm's API to automate the creation of podcast episodes.

## Requirements
- Python 3
- `requests` library for Python
- Access to Transistor.fm API and an API key

## Setup and Usage
1. **Install Required Libraries**: Ensure the `requests` library is installed in your Python environment.
2. **CSV File Preparation**: Prepare your CSV file with at least two columns: title and summary for each episode.
3. **API Key and Show ID**: Obtain your API key from Transistor.fm and know your Show ID.
4. **Script Configuration**: Replace the placeholder API key and Show ID in the script with your actual values.
5. **Execution**: Run the script with the path to your CSV file. The script will create draft episodes on Transistor.fm for each row in the CSV file.

## Script Components
- **Function `create_draft_episodes_from_csv`**: Parses the CSV file and prepares episode data.
- **Transistor.fm API Integration**: The script interacts with the Transistor.fm API to create episodes.
- **Function `create_draft_episode_in_transistor`**: Handles the API request to create a single draft episode.
- **Main Process Function `process_episodes`**: Orchestrates the overall process of reading the CSV and creating drafts on Transistor.fm.
- **Error Handling**: The script provides feedback on the success or failure of each episode creation attempt.

## Notes
- The script assumes the CSV file has a header row and at least two columns (title and summary).
- API rate limits and errors from Transistor.fm are not extensively handled in this script. It's advisable to monitor for any API-related errors during execution.

"""

import csv
import requests


# Constants
csv_file_path = './config/scotus.csv'
api_url = "https://api.transistor.fm/v1/episodes" # Transistor.fm API endpoint and authorization
transistor_api_key = os.getenv('TRANSISTOR_API_KEY')  # Transistor.fm API endpoint and authorization
show_id = "12890"  # Transistor.fm API endpoint and authorization



# Function to parse the CSV file and create draft episodes
def create_draft_episodes_from_csv(csv_file_path, show_id):
    episodes = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if len(row) < 2:  # Ensure the row has at least title and summary
                continue
            title, summary = row[0], row[1]
            episode = {
                "episode[show_id]": show_id,
                "episode[title]": title.strip(),
                "episode[summary]": summary.strip()
            }
            episodes.append(episode)
    return episodes


# Headers for the API request
headers = {
    "x-api-key": transistor_api_key
}

# Function to create a draft episode in Transistor
def create_draft_episode_in_transistor(episode):
    response = requests.post(api_url, data=episode, headers=headers)
    return response

# Main function to process the CSV and create episodes in Transistor
def process_episodes(csv_file_path):
    episodes = create_draft_episodes_from_csv(csv_file_path, show_id)
    for episode in episodes:
        response = create_draft_episode_in_transistor(episode)
        if response.status_code == 201:
            print(f"Draft episode '{episode['episode[title]']}' created successfully.")
        else:
            print(f"Failed to create episode '{episode['episode[title]']}'. Status Code: {response.status_code}, Response: {response.json()}")


process_episodes(csv_file_path)
