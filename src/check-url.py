import requests
from bs4 import BeautifulSoup

def extract_text(element):
    """Helper function to safely extract text from a BeautifulSoup element or return an empty string if the element is None."""
    return element.get_text(strip=True) if element else ''

def preview_data(url):
    """
    Attempts to access a URL, checks if the page is readable and contains HTML content,
    and prints a preview of the data if possible.
    
    Args:
        url (str): The URL to access and preview.
        
    Returns:
        None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        if 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.title or soup.body:
                print(f"Page at {url} can be read and contains scrape-able data. Here's a preview:")
                
                # Print the page title
                title = extract_text(soup.title)
                print(f"Title: {title}")
                
                # Print the first few sentences from the body, if available
                body_text = ' '.join(soup.body.stripped_strings)
                preview_length = 250  # Adjust based on how much text you want to preview
                print(f"Body preview: {body_text[:preview_length]}...")
                
                # Print headings found on the page (h1 to h3)
                headings = [extract_text(tag) for tag in soup.find_all(['h1', 'h2', 'h3'])]
                if headings:
                    print("Headings found on the page:")
                    for heading in headings:
                        print(f" - {heading}")
                else:
                    print("No headings found on the page.")
            else:
                print(f"Page at {url} does not contain recognizable HTML content for scraping.")
        else:
            print(f"Page at {url} does not contain HTML content.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {url}: {e}")

# Example usage
if __name__ == "__main__":
    url = "https://www.scotusblog.com/case-files/terms/ot2023/"  # Replace with the URL you want to check
    preview_data(url)
