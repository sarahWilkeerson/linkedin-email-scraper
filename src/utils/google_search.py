thonimport requests
from bs4 import BeautifulSoup

def search_google(query):
    """
    Perform a Google search and return LinkedIn profiles.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    profiles = [a['href'] for a in soup.find_all('a', href=True) if "linkedin.com/in" in a['href']]
    return profiles