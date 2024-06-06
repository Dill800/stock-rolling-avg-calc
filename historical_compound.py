import json
import http.client
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

totalShares = 0
monthlyAdd = 0
principal = 10000
year_range = 12
startDate = str(int((datetime(2009, 6, 1) - relativedelta(years=year_range)).timestamp()))
endDate = str(int(datetime(2009, 6, 1).timestamp()))
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

matrix = []

for month_window in range(1, 100):

    matrix.append([])

    for threshold in range(1, 100):

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
            total_shares += shares

        # Total result amount is amount of shares you have multiplied by current stock price
        endAmt = round(total_shares * prices[len(prices)-1], 2)

        # Calculate annualized return
        annual_return = (endAmt/total_principal) ** (1/year_range)

        matrix[month_window-1].append(round((annual_return-1) * 100, 2))

        # Occurences
        #matrix[month_window-1].append(len(dip_weeks))

        #print("Month Window: ", month_window, " | Threshold: ", threshold, "% | Return: ", round((annual_return-1) * 100, 2), "% | Occurences: ", len(dip_weeks))

#print(len(dip_weeks))
        
df = pd.DataFrame(matrix)
print(df)
df.to_csv(str(ticker) + '_' + str(year_range) + 'yr' + '_flatmarket.csv')

