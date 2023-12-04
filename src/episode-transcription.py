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
    csv_file = './config/scotus.csv'  
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        audio_file_path = row['AudioFilePath']  
        transcription = transcribe_audio(audio_file_path)
        print(f"Transcription for {audio_file_path}:")
        print(transcription)

if __name__ == "__main__":
    main()
