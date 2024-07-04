# searches google for a random image of the given beach

### IMPORTS
from bs4 import BeautifulSoup
import requests
import random
from duckduckgo_search import DDGS

# Get the thumbnail URL via google search
def get_thumb(search: str) -> str:
    '''
    Searches Google Images for pictures of a given beach and returns one of them.

    Returns:
        - URL of the image
    '''

    url = f'https://www.google.com/search?q={search}+beach&tbm=isch'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    results = soup.findAll('img')

    try:
        i = random.randrange(0, 10)
        image_url = results[i].get('src')
    except:
        image_url = 'https://i.imgur.com/fCyBeda.jpg'

    return image_url

def get_img(search: str) -> str:
    '''
    Searches DuckDuckGo for pictures of a given beach and returns one of them.

    Returns:
        - URL of the image
    '''

    results = DDGS().images(keywords=search, max_results=10, safesearch="off")

    try:
        i = random.randrange(0, 10)
        image_url = results[i]['image']
    except:
        image_url = 'https://i.imgur.com/fCyBeda.jpg'

    return image_url

if __name__ == '__main__':
    print(get_thumb('sao pedro de moel'))
    print(get_img('sao pedro de moel'))