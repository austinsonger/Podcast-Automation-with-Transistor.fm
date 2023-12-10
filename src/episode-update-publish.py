import csv
import os
import requests
from datetime import datetime

# Constants
csv_file_path = './config/scotus.csv'
TRANSISTOR_API_URL = "https://api.transistor.fm/v1/episodes"
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
headers = {"x-api-key": TRANSISTOR_API_KEY, "Content-Type": "application/json"}

def publish_episode(episode_id):
    """
    Publish an episode on Transistor.fm
    """
    url = f"{TRANSISTOR_API_URL}/{episode_id}/publish"

    response = requests.post(url, headers=headers)
    return response.json()

def process_csv(csv_path):
    """
    Process the CSV file and publish episodes if the argument date has passed and they are not published.
    """
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            argument_date = datetime.strptime(row["Argument Date"], "%Y-%m-%d").date()
            current_date = datetime.now().date()

            if 'Episode ID' in row and row['Episode ID'] and argument_date < current_date:
                # Assuming there's a column 'Published' to check if the episode is already published
                if row.get('Published', 'no').lower() != 'yes':
                    response = publish_episode(row['Episode ID'])
                    print(f"Episode {row['Episode ID']} published: {response}")

# Main execution
process_csv(csv_file_path)
