import pandas as pd
import os
import subprocess
from datetime import datetime

def download_scotus_case_audio():
    """
    Downloads audio files for Supreme Court cases from the given CSV file.
    
    The function reads a CSV file containing case details and iterates over each row.
    For each case, it parses the argument date to create a directory by year and month,
    then downloads the corresponding audio file into this directory using curl command.
    If the file already exists, it skips downloading.
    
    Args:
        None
        
    Returns:
        None
    """
    # Load the CSV file
    file_path = './config/scotus.csv' # Adjust path as needed
    scotus_df = pd.read_csv(file_path)

    # Iterate over each row to process the case
    for index, row in scotus_df.iterrows():
        # Extract case ID and argument date
        case_id = row['Case ID'].strip()
        argument_date = row['Argument Date']

        # Parse the argument date and format it for directory naming
        parsed_date = datetime.strptime(argument_date, "%m-%d-%Y")
        year = parsed_date.strftime("%Y")
        month = parsed_date.strftime("%B").upper()

        # Base directory for the case
        base_dir = os.path.join(f'./{year}/{month}/audio/')

        # Ensure the directory exists
        os.makedirs(base_dir, exist_ok=True)

        # Full path for the audio file
        audio_file_path = os.path.join(base_dir, f"{case_id}.mp3")

        # Generate the curl command
        curl_command = f"curl https://www.supremecourt.gov/media/audio/mp3files/{case_id}.mp3 --output {audio_file_path}"

        # Check if the file already exists
        if not os.path.exists(audio_file_path):
            # File doesn't exist, execute the curl command
            subprocess.run(curl_command, shell=True, check=True)
        else:
            # File already exists, skip downloading
            print(f'Skipping download, file already exists: {audio_file_path}')

# Call the function to start the download process
download_scotus_case_audio()
