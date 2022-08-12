import requests
import value as value
import os
from twilio.rest import Client

# You can change the comapny name and stock name to which you want info about
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# ADD YOUR API KEYS BELOW

Stock_api_key = ""
News_api_key = ""
Twilio_sid = ""
Twilio_auth_token = ""

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": Stock_api_key
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
print(yesterday_closing)

day_before_yester_data = data_list[1]
day_before_yester_closing = day_before_yester_data["4. close"]
print(day_before_yester_closing)

change_in_price = float(yesterday_closing) - float(day_before_yester_closing)
up_down = None
if change_in_price > 0:
    up_down = "📈"
else:
    up_down = "📉"

change_percentage = round((change_in_price / float(yesterday_closing)) * 100)
print(change_percentage)

if abs(change_percentage) > 1:
    news_params = {
        "apiKey": News_api_key,
        "qInTitle": COMPANY_NAME
    }
    newsrespone = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = newsrespone.json()["articles"]

first_three_articles = articles[:3]
print(first_three_articles)

formatted_articles = [
    f"{STOCK_NAME}:{up_down}{change_percentage}%.\nHeadline: {article['title']}. \nBrief: {article['description']}" for
    article in first_three_articles]

client = Client(Twilio_sid, Twilio_auth_token)
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        # add the twilio phone number i from
        from_="",
        # add the number to which we want to send the messages
        to=""
    )
