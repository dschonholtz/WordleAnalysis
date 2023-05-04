import requests
from bs4 import BeautifulSoup


def extract_used_words(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <p> elements
    p_elements = soup.find_all('p')

    # Extract the words from the <p> elements
    used_words = []
    for p in p_elements:
        content = p.get_text()
        parts = content.split('. ')
        if len(parts) > 1 and parts[0].isdigit():
            word = parts[1].split(' ')[0]
            used_words.append(word)

    return used_words

# Example usage
url = 'https://www.stadafa.com/2021/09/every-worlde-word-so-far-updated-daily.html'
used_words = extract_used_words(url)
print(used_words)
