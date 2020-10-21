
import requests
def get_quote():
    url = "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
    r = requests.get(url)
    quote = r.json()
    quote_string = '"' + quote['quoteText'] +'"\n- ' + quote['quoteAuthor']
    return quote_string
