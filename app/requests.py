from urllib import response
import requests
from .models import Quote

url = "http://quotes.stormconsultancy.co.uk/random.json"

def get_quote():
    '''
    Function to return random quotes from API
    '''
    random_quote = Quote(response.get('quote'), response.get('author'), response.get('permalink'))
    response = requests.get(url).json()