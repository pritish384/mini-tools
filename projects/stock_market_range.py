import requests
from bs4 import BeautifulSoup
from math import sqrt

def get_index_price(symbol):
    url = f'https://www.google.com/finance/quote/{symbol}:INDEXNSE'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    index_price_element = soup.find('div', {'class': 'YMlKec fxKbKc'}).text
    index_price = float(index_price_element.replace(',', ''))    
   

    return index_price

def calculate_range(symbol , time):
    index_price = get_index_price(symbol)
    vix = get_index_price('INDIA_VIX')
    percentage = (vix/sqrt(time))
    uncertinity = 0.09/100
    # add percentage and uncertainity
    max = index_price * (1 + (percentage/100 + uncertinity))
    min = index_price * (1 - (percentage/100 + uncertinity))
    return round(max) , round(min)
