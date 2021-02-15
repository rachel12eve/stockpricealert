import requests
from twilio.rest import Client
#====Twilio=========
account_sid = 'AC531c3284a319ffdd974c94965b423070'
auth_token = '6420397483d2ad61085e8c2583f2dcc1'
API_KEY = "ebe9e119df4cd1b1ec52c4864d2ae8f4"

#====STOCK INFO=========
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
Q = "tesla"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_VANTAGE_API="9R3YTAQ7AOYHWK5N"
STOCK_PARAMS={"function":"TIME_SERIES_DAILY","symbol":STOCK_NAME, "apikey":STOCK_VANTAGE_API}
NEWS_API="d79c4239da67496a91a1b7f0f0d6df4c"
NEWS_PARAMS={"q":Q,"sortBy":"publishedAt","language":'en',"apiKey":NEWS_API}

response=requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
print(response)
stock_database=response.json()
print(stock_database)
extract_price=stock_database["Time Series (Daily)"]

date_set=[]#create a list to store date
closing_price_set=[]#create a list to store closing price

for date, y in extract_price.items():
  closing_price=y['4. close']
  date_set.append(date)
  closing_price_set.append(closing_price)

print(date_set[0],closing_price_set[0])
print(date_set[1],closing_price_set[1])

#get the stock price in the last 2 days
yesterday_price=float(closing_price_set[0])
daybefore_price=float(closing_price_set[1])

#calculate the change %
difference=round((yesterday_price-daybefore_price)/daybefore_price*100,2)
print(difference)



#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(difference)>=5:
    #print("Get news")
    news=requests.get(NEWS_ENDPOINT,params=NEWS_PARAMS).json()
    #print(news)
    content=[]
    all_news=news["articles"][0:3]

    for i in range(0,3):
        headline=all_news[i]["title"]
        brief=all_news[i]["description"]
        client = Client(account_sid, auth_token)
        if difference>0:
            change="⇧"
        else:
            change="⇩"

        message = client.messages \
            .create(
            body=f"{STOCK_NAME}:{change}{abs(difference)}%\n Headline:{headline}\n Brief:{brief}",
            from_='+12017718092',
            to='+85295894580'
        )

        print(message.sid)

