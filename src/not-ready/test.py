import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_and_parse_html(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    case_details = []
    for case in soup.find_all('tr'):
        title_element = case.find('a', class_='case-title')
        if title_element:
            title = title_element.text.strip()
            case_no_element = case.find('span', class_='case-info-item').find('a')
            case_no = case_no_element.text.strip() if case_no_element else ""
            arg_date_element = case.find('span', class_='arg-date')
            if arg_date_element:
                arg_date = arg_date_element.text.strip()
            else:
                arg_date = ""

            summary = ' '.join(case.find('div', class_='case_issue_holding').text.split()).replace('Issue(s): ', '').replace('Holding: ', '')
            
            case_details.append({
                'Title': f"{title}, No. {case_no} [Arg: {arg_date}]",
                'Summary': summary,
                'Case ID': case_no,
                'Episode ID': '',
                'Argument Date': arg_date if arg_date else "N/A"
            })

    return pd.DataFrame(case_details)



def save_cases_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Saved case details to {file_path}")

# URL to the SCOTUS term page for October Term 2023
term_url = 'https://www.scotusblog.com/case-files/terms/ot2023/'

df_cases = fetch_and_parse_html(term_url)
csv_file_path = 'scotus_cases_ot2023_from_url.csv'
save_cases_to_csv(df_cases, csv_file_path)
