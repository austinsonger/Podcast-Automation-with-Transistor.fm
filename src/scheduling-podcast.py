import pandas as pd
import requests
from datetime import datetime
import pytz

# Constants
CSV_FILE_PATH = '/config/scotus.csv'
TRANSISTOR_API_KEY = os.getenv('TRANSISTOR_API_KEY')
TRANSISTOR_SHOW_ID = '12890'
TRANSISTOR_API_URL = 'https://api.transistor.fm/v1/episodes'

def schedule_episode(episode_id, date_str):
    cst_timezone = pytz.timezone('America/Chicago')
    argument_date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=pytz.utc).astimezone(cst_timezone)
    release_time = argument_date.replace(hour=20, minute=0, second=0)  # 8 PM CST
    
    headers = {'Authorization': f'Bearer {TRANSISTOR_API_KEY}'}
    data = {'publish_at': release_time.isoformat()}
    
    response = requests.patch(f'{TRANSISTOR_API_URL}/{episode_id}', headers=headers, json=data)
    print(f'Scheduling response: {response.status_code}')

def main():
    df = pd.read_csv(CSV_FILE_PATH)

    for index, row in df.iterrows():
        episode_id = row['episode_id']
        argument_date = row['argument_date']
        schedule_episode(episode_id, argument_date)

if __name__ == "__main__":
    main()
