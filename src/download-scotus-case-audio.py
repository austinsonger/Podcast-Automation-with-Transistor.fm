import pandas as pd
import os
import subprocess

# Configuration for debugging and error handling
DEBUG = True
ERROR_HANDLING = True

def log_debug(message):
    """Prints debug messages if debugging is enabled."""
    if DEBUG:
        print(f"DEBUG: {message}")

def download_scotus_case_audio():
    """
    Downloads audio files for Supreme Court cases from the given CSV file.
    """
    try:
        # Load the CSV file
        file_path = './config/scotus.csv'  # Replace with your actual file path
        scotus_df = pd.read_csv(file_path)
    except Exception as e:
        if ERROR_HANDLING:
            print(f"Error loading CSV file: {e}")
        return

    # Base directory for the year
    base_dir = './2024/'

    for index, row in scotus_df.iterrows():
        try:
            case_id = row['Case ID'].strip()
            case_dir = os.path.join(base_dir, case_id)
            audio_dir = os.path.join(case_dir, 'audio')
            os.makedirs(audio_dir, exist_ok=True)

            file_path = os.path.join(audio_dir, f'{case_id}.mp3')
            if not os.path.exists(file_path):
                curl_command = f"curl https://www.supremecourt.gov/media/audio/mp3files/{case_id}.mp3 --output {file_path}"
                log_debug(f"Executing: {curl_command}")
                subprocess.run(curl_command, shell=True, check=True)
            else:
                log_debug(f"Skipping download, file already exists: {file_path}")
        except subprocess.CalledProcessError as e:
            if ERROR_HANDLING:
                print(f"Error downloading file for case {case_id}: {e}")
        except Exception as e:
            if ERROR_HANDLING:
                print(f"Unexpected error for case {case_id}: {e}")

if __name__ == "__main__":
    download_scotus_case_audio()
