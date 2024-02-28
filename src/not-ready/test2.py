import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_and_parse_html(url):
    """
    Fetches HTML content from the given URL and parses it to extract case details.

    Parameters:
    url (str): URL to fetch the HTML content from.

    Returns:
    DataFrame: A DataFrame containing the parsed case details.
    """
    # Fetch the HTML content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    case_details = []
    for case in soup.find_all('div', class_='case_issue_holding'):
        title = case.find_previous('a', class_='case-title').text.strip()
        case_no_element = case.find_previous('span', class_='case-info-item').find('a')
        case_no = case_no_element.text.strip() if case_no_element else "N/A"
        arg_date = case.find_previous('span', class_='case-info-item').text.strip().split('[')[-1].replace('Arg: ', '').replace(']', '').strip()
        summary = case.text.strip().replace('Issue(s): ', '').replace('Holding: ', '')
        
        case_details.append({
            'Title': title,
            'Case No': case_no,
            'Argument Date': arg_date,
            'Summary': summary
        })

    return pd.DataFrame(case_details)

def save_cases_to_csv(df, file_path):
    """
    Saves the DataFrame of case details to a CSV file.

    Parameters:
    df (DataFrame): DataFrame containing case details.
    file_path (str): Path to save the CSV file.
    """
    df.to_csv(file_path, index=False)
    print(f"Saved case details to {file_path}")

# URL to the SCOTUS term page for October Term 2023
term_url = 'https://www.scotusblog.com/case-files/terms/ot2023/'

# Fetch and parse the HTML content from the URL
df_cases = fetch_and_parse_html(term_url)

# Specify the path where the CSV will be saved
csv_file_path = 'scotus_cases_ot2023_from_url.csv'

# Save the extracted case details to a CSV file
save_cases_to_csv(df_cases, csv_file_path)
