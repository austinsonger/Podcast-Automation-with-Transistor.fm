import pandas as pd
import os
import subprocess

# Load the CSV file
file_path = './config/scotus.csv'  # Replace with your actual file path
scotus_df = pd.read_csv(file_path)

# Base directory for the year
base_dir = '../2023/'

# Iterate over each row to generate and execute the curl commands
for index, row in scotus_df.iterrows():
    case_id = row['Case ID'].strip()

    # Full path for the case directory
    case_dir = os.path.join(base_dir, case_id)

    # Create directory for the case if it doesn't exist
    audio_dir = os.path.join(case_dir, 'audio')
    os.makedirs(audio_dir, exist_ok=True)

    # Generate the curl command
    curl_command = f"curl https://www.supremecourt.gov/media/audio/mp3files/{case_id}.mp3 --output {case_dir}/audio/{case_id}.mp3"

    # Check if the file already exists
    file_path = os.path.join(audio_dir, f'{case_id}.mp3')
    if not os.path.exists(file_path):
        # File doesn't exist, execute the curl command
        subprocess.run(curl_command, shell=True, check=True)
    else:
        # File already exists, skip downloading
        print(f'Skipping download, file already exists: {file_path}')
        
