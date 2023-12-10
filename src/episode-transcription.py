import pandas as pd
import os
import re
from pydub import AudioSegment
import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        # Convert MP3 to WAV
        temp_path = file_path.replace('.mp3', '.wav')
        if not os.path.exists(temp_path):  # Convert only if .wav file doesn't exist
            audio = AudioSegment.from_mp3(file_path)
            audio.export(temp_path, format="wav")

        # Now use the converted WAV file for transcription
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"Error transcribing file {file_path}: {e}"

def main():
    csv_file = './config/scotus.csv'  # Replace with your CSV file path
    base_dir = '../2023/'  # Adjust based on the download-scotus.py script

    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        title = row['Title']  # Assuming the column name is 'Title'
        # Extract case ID using regular expression
        match = re.search(r'No\. (\d{2}-\d{4})', title)
        if match:
            case_id = match.group(1).strip()
            audio_file_path = os.path.join(base_dir, case_id, 'audio', f'{case_id}.mp3')
            transcription = transcribe_audio(audio_file_path)
            print(f"Transcription for {audio_file_path}:")
            print(transcription)
        else:
            print(f"No case ID found in title: {title}")

if __name__ == "__main__":
    main()
