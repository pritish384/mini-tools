# import requests
# from bs4 import BeautifulSoup

# def get_exchange_rate(from_currency, to_currency):
#     url = f'https://www.x-rates.com/calculator/?from={from_currency}&to={to_currency}&amount=1'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     exchange_rate_element = soup.find('span', {'class': 'ccOutputTrail'}).previous_sibling
#     exchange_rate = float(exchange_rate_element.strip())

#     return exchange_rate

# def convert_currency(amount, exchange_rate):
#     return round(amount * exchange_rate, 2)

# if __name__ == '__main__':
#     from_currency = input("Enter the source currency code (e.g., USD): ").upper()
#     to_currency = input("Enter the target currency code (e.g., EUR): ").upper()
#     amount = float(input("Enter amount: "))
    
#     exchange_rate = get_exchange_rate(from_currency, to_currency)

#     if exchange_rate is not None:
#         converted_amount = convert_currency(amount, exchange_rate)
#         print(f"Conversion rate: 1 {from_currency} = {exchange_rate} {to_currency}")
#         print(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")
#     else:
#         print("Unable to fetch exchange rate.")
