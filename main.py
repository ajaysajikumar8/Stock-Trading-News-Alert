import requests
import os
from twilio.rest import Client

ACCOUNT_SID = ""
AUTH_TOKEN = ""
twilio_num = None
my_num = None

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY_STOCK = ""
API_KEY_NEWS = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "outputsize" : "compact",
    "apikey" : API_KEY_STOCK
}
response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
Y_closing_price = data_list[0]["4. close"]
DBY_closing_price = data_list[1]["4. close"]

difference = (float(Y_closing_price) - float(DBY_closing_price))
up_down = None
if difference > 5:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percent = round((difference/float(Y_closing_price)) * 100)

if abs(diff_percent) > 0:
    news_parameters = {
        "q" : COMPANY_NAME,
        "apikey" : API_KEY_NEWS
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params= news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    news_list = [f"{STOCK_NAME} {up_down}{diff_percent}%\nHeadline: {article['title']}\n\nBrief: {article['description']}" for article in news_data ]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in news_list:
        message = client.messages \
                    .create(
                        body=article,
                        from_=twilio_num,
                        to= my_num
                    )
        print(message.status)
