import json
import http.client
from datetime import datetime

totalShares = 0
monthlyAdd = 0
principal = 10000
startDate = str(int(datetime(2004, 5, 6).timestamp()))
endDate = str(int(datetime(2024, 5, 5).timestamp()))
ticker = 'SPY'

conn = http.client.HTTPSConnection("query1.finance.yahoo.com")
payload = ''
headers = {}

# Weekly request
request_url = "/v8/finance/chart/"+ticker+"?events=capitalGain%257Cdiv%257Csplit&formatted=true&includeAdjustedClose=true&interval=1wk&period1="+startDate+"&period2="+endDate+"&symbol=VOO&userYfid=true&lang=en-US&region=US"

conn.request("GET", request_url, payload, headers)

res = conn.getresponse()
data = res.read()
response = json.loads(data.decode("utf-8"))
prices = response['chart']['result'][0]['indicators']['quote'][0]['close']

prices = list(map(lambda x: round(x, 2) if x else None, prices))

# Params
month_window = 3
threshold = 20

for month_window in range(1, 13):
    for threshold in range(1, 20):

        # List of prices that fit threshold criteria
        dip_weeks = []

        # Number used to quickly calc moving average
        running_window = 0

        for i in range(len(prices)):

            # Current price
            price = prices[i]

            # Do not do window math for first weeks if within first month window
            if i < month_window*4:
                running_window += price
                continue

            # Calculate rolling average stock price
            window_avg = running_window / (month_window*4)

            # If match threshold criteria, add price to dip_weeks
            if price < (1 - threshold/100.0) * window_avg:
                dip_weeks.append(price)

            # Adds current price to window and removes oldest price from window
            running_window -= prices[i-month_window*4]
            running_window += price

        # Don't print anything if nothing fit criteria
        if len(dip_weeks) == 0:
            continue

        # This will work with any number since we're calculating return at the end anyways
        total_principal = 100000

        # Amount of money to put in at one time when invest criteria is met
        week_add = round(total_principal / len(dip_weeks), 2)

        # Calculate total amount of shares you would have presently
        total_shares = 0
        for price in dip_weeks:
            shares = week_add/price
            totalShares += shares

        # Total result amount is amount of shares you have multiplied by current stock price
        endAmt = round(totalShares * prices[len(prices)-1], 2)

        # Calculate annualized return
        annual_return = (endAmt/total_principal) ** (1/20)

        print("Month Window: ", month_window, " | Threshold: ", threshold, "% | Return: ", round((annual_return-1) * 100, 2), "% | Occurences: ", len(dip_weeks), "% | Total: ", endAmt, "% | WeekAdd: ", week_add, "% | ShouldBeP: ", week_add*len(dip_weeks))

#print(len(dip_weeks))

'''
totalShares += principal/prices[0]

for price in prices:
    
    #Rate is being subbed for current price
    shares = monthlyAdd/price

    totalShares += shares

endAmt = totalShares * prices[len(prices)-1]
totalContrib = principal + monthlyAdd*len(prices)
print(ticker + " from " + str(datetime(2020, 4, 26)) + " to " + str(datetime(2024, 4, 26)))
print("Principal: $" + str(principal))
print("Monthly addition: $" + str(monthlyAdd))
print()
print("End amount: $" + str(round(endAmt, 2)))
print("Total contributions: $" + str(totalContrib))
print()
print("Adjusted Total Return: " + str(    round(((endAmt/totalContrib)-1)*100, 2)     ) + "%")
print("Adjusted Annualized Return: " + str(    round(100*((endAmt/totalContrib)**(12/len(prices)) - 1), 2)     ) + "%")
'''
'''
for i in range(timeLength):
    
    #Rate is being subbed for current price
    price = (1 + rate/100) ** i
    shares = monthlyAdd/price

    totalShares += shares

print(totalShares * (1+rate/100)**(timeLength-1))
'''
'''
conn = http.client.HTTPSConnection("query1.finance.yahoo.com")
payload = ''
headers = {}
conn.request("GET", "/v8/finance/chart/VOO?events=capitalGain%257Cdiv%257Csplit&formatted=true&includeAdjustedClose=true&interval=1mo&period1=767332800&period2=1714104000&symbol=VOO&userYfid=true&lang=en-US&region=US", payload, headers)
res = conn.getresponse()
data = res.read()
#response = json.loads(data.decode("utf-8"))
#print(response['chart']['result'][0]['indicators']['quote'][0]['close'])
'''

