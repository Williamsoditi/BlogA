import requests
from .models import Quote

url = "http://quotes.stormconsultancy.co.uk/random.json"

def get_quote():
    '''
    Function to return random quotes from API
    '''
    response = requests.get(url).json()
    random_quote = Quote(response.get('quote'), response.get('author'))

    return random_quote
