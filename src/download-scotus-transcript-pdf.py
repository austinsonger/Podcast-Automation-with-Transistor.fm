import pandas as pd
import os
import requests
import random
import string

# Load the CSV file
file_path = './config/scotus.csv'  # Replace with your actual file path
scotus_df = pd.read_csv(file_path)

# Base URL for the Supreme Court webpage
base_url = 'https://www.supremecourt.gov/oral_arguments/audio/2023/'

# Iterate over each row to generate and execute the PDF download commands
for index, row in scotus_df.iterrows():
    case_id = row['Case ID'].strip()

    # Full path for the case directory
    case_dir = os.path.join(base_dir, case_id)

    # Create directory for the case if it doesn't exist
    pdf_dir = os.path.join(case_dir, 'pdf')
    os.makedirs(pdf_dir, exist_ok=True)

    # Construct the PDF URL based on the case_id
    pdf_url = f'{base_url}{case_id}'

    # Send an HTTP GET request to the PDF URL
    response = requests.get(pdf_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Generate a random filename for the PDF to avoid naming conflicts
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.pdf'
        
        # Save the PDF file with the random filename
        pdf_path = os.path.join(pdf_dir, random_filename)
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        
        print(f'Downloaded PDF for Case ID {case_id} to {pdf_path}')
    else:
        print(f'Failed to download PDF for Case ID {case_id}. Status code: {response.status_code}')
