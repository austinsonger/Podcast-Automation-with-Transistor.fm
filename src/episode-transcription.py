import pandas as pd
import os
import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"Error transcribing file {file_path}: {e}"

def main():
    csv_file = './config/scotus.csv'  # Replace with your CSV file path
    base_dir = '../2023/'  # Adjust based on the download-scotus.py script

    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        case_id = row['Case ID'].strip()  # Replace 'Case ID' with the actual column name
        audio_file_path = os.path.join(base_dir, case_id, 'audio', f'{case_id}.mp3')
        transcription = transcribe_audio(audio_file_path)
        print(f"Transcription for {audio_file_path}:")
        print(transcription)

if __name__ == "__main__":
    main()
