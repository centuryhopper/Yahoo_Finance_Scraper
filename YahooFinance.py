# Yahoo! Finance Scraper
# Extract financial data and historical stock prices from Yahoo! Finance using background java strings and a hidden api.

import re
import json
import csv
from io import StringIO
from bs4 import BeautifulSoup
import requests

# First, navigate to https://finance.yahoo.com/ and enter the stock you want to look up.
# You'll noticed several tabs along the page such as "Stats", "Chart", "Financials", "Analysis", etc...
# Navigate to the "Financials" tab. Notice that the Income Statement and the Balance Sheet are available as well as Annual and Quarterly options.
# Copy the url for this tab, and for "Profile" and "Financials". We are going to scrape the data from these 3 tabs first.
# Replace the stock symbol in the url with a curly brace to turn it into a template.



# url templates
# These are just three of the many tabs you can choose from
url_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# the stock I want to scrape
stock = 'F'

# Extracting and parsing the html & json data
# Now, use the "Financials" template to request the webpage, passing in the stock variable to fill in the url template.

response = requests.get(url_financials.format(stock, stock), headers=HEADERS)
# print(response.status_code)


# Next, parse the html using BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')
# If you were to look at the raw html, you would notice that there is a lot of javascript code and not a lot of html to work with. You may also notice that embedded in the code there are json formatted text strings. Fortunately for us, there is a javascript function, appropriately commented with "--Data--". This function is located inside of a generic "script" tag. However, we can use regular expressions with BeautifulSoup in order to identify the script tag with the function we're looking for.

pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]
# print(script_data)
# There's a lot of good json data here, but it's wrapped in a javascript function, as you can clearly see. However, if we can identify the starting and ending position of this json data, we can slice it and then parse it with the json.loads function.

# beginning
# print(script_data[:500])


# print()

# the end
# print(script_data[-500:])

# find the starting position of the json string
start = script_data.find("context")-2

# slice the json string
json_data = json.loads(script_data[start:-12])
# print(json.dumps(json_data, indent=4, sort_keys=True))

# Financial statements
# Now that you have the data, you can explore the dictionary to discover what's inside. This dataset contains both Annual and Quarterly financial statements, as you can see from the dictionary paths listed below.

# json_data['context'].keys() => dict_keys(['dispatcher', 'options', 'plugins'])
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys() => dict_keys(['financialsTemplate', 'cashflowStatementHistory', 'balanceSheetHistoryQuarterly', 'earnings', 'price', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory', 'balanceSheetHistory', 'cashflowStatementHistoryQuarterly', 'quoteType', 'summaryDetail', 'symbol', 'pageViews'])


# income statement
annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

# cash flow statement
annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

# balance sheet
annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
quarterly_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']


# there's a variety of  number formats provided
# annual_is[0]['operatingIncome']


# The data can be consoldated into an easy to read, or export, data set with a loop
annual_is_stmts = []


# consolidate annual
for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_is_stmts.append(statement)

# This model can be applied to all other financial statements, as you can see from the examples below.
annual_cf_stmts = []
quarterly_cf_stmts = []

# annual
for s in annual_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_cf_stmts.append(statement)

# quarterly
for s in quarterly_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    quarterly_cf_stmts.append(statement)


# Profile Data
# We can copy the same steps from the Financial statements on the Profile data
response = requests.get(url_profile.format(stock, stock), headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]
start = script_data.find("context")-2
json_data = json.loads(script_data[start:-12])

# json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile'].keys()
# # data for company officers (just the first 3 are listed for brevity )
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['companyOfficers'][:3]

# business description
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['longBusinessSummary']

# sec filings from Edgars ( just the first 3 are listed for brevity )
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['secFilings']['filings'][:3]

# # lot of other data is available
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']





# Statistics
# response = requests.get(url_stats.format(stock, stock), headers=HEADERS)
# soup = BeautifulSoup(response.text, 'html.parser')
# pattern = re.compile(r'\s--\sData\s--\s')
# script_data = soup.find('script', text=pattern).contents[0]
# start = script_data.find("context")-2
# json_data = json.loads(script_data[start:-12])
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']



# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1610415491&period2=1641951491&interval=1d&events=history&includeAdjustedClose=true

# Historical Stock Data
# This data uses a hidden api, as you can see from the "query" prefix, the version number (V7), and the variety of parameters.

stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/F?period1=1568483641&period2=1600106041&interval=1d&events=history'
response = requests.get(stock_url, headers=HEADERS)
# extract the csv data
# convert strings to files
file = StringIO(response.text)
reader = csv.reader(file)
data = list(reader)

# show the first 5 records
for row in data[:5]:
    print(row)
# ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
# ['2019-09-16', '9.360000', '9.450000', '9.240000', '9.300000', '8.996831', '50052600']
# ['2019-09-17', '9.270000', '9.310000', '9.180000', '9.280000', '8.977483', '27391200']
# ['2019-09-18', '9.260000', '9.360000', '9.220000', '9.250000', '8.948462', '24309400']
# ['2019-09-19', '9.310000', '9.330000', '9.100000', '9.100000', '8.803351', '28780700']
# You can start to customize this by pulling out the parameters from the URL and putting them into a dictionary.

# stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?'

# params = {
#     'period1':'1568483641',
#     'period2':'1600106041',
#     'interval':'1d',
#     'events':'history'
# }

# By inspecting the request headers and parameters online, it's possible to see how this can be simplified further... by using the range parameter instead of the periods.

params = {
    'range': '5y',
    'interval':'1d',
    'events':'history'
}
response = requests.get(stock_url.format(stock), headers=HEADERS, params=params)
# extract the csv data
file = StringIO(response.text)
reader = csv.reader(file)
data = list(reader)

# show the first 5 records
for row in data[:5]:
    print(row)