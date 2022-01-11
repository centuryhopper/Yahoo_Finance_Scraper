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
# '\n(function (root) {\n/* -- Data -- */\nroot.App || (root.App = {});\nroot.App.now = 1600309174461;\nroot.App.main = {"context":{"dispatcher":{"stores":{"PageStore":{"currentPageName":"quote","currentRenderTargetId":"default","pagesConfigRaw":{"base":{"quote":{"layout":{"bundleName":"yahoodotcom-layout.TwoColumnLayout","name":"TwoColumnLayout","config":{"enableHeaderCollapse":true,"additionalBodyWrapperClasses":"Bgc($layoutBgColor)!","contentWrapperClasses":"Bgc($lv2BgColor)!","Header":{"isFixed":tru'

# print()

# the end
# print(script_data[-500:])
# 'how":{"strings":1},"tdv2-applet-sponsored-moments":{"strings":1},"tdv2-applet-stream":{"strings":1},"tdv2-applet-stream-hero":{"strings":1},"tdv2-applet-swisschamp":{"strings":1},"tdv2-applet-uh":{"strings":1},"tdv2-applet-userintent":{"strings":1},"tdv2-applet-video-lightbox":{"strings":1},"tdv2-applet-video-modal":{"strings":1},"tdv2-wafer-adfeedback":{"strings":1},"tdv2-wafer-header":{"strings":1},"yahoodotcom-layout":{"strings":1}}},"options":{"defaultBundle":"td-app-finance"}}}};\n}(this));\n'
# find the starting position of the json string
start = script_data.find("context")-2

# slice the json string
json_data = json.loads(script_data[start:-12])
# print(json.dumps(json_data, indent=4, sort_keys=True))
# Financial statements
# Now that you have the data, you can explore the dictionary to discover what's inside. This dataset contains both Annual and Quarterly financial statements, as you can see from the dictionary paths listed below.

# json_data['context'].keys()
# dict_keys(['dispatcher', 'options', 'plugins'])
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()


# dict_keys(['financialsTemplate', 'cashflowStatementHistory', 'balanceSheetHistoryQuarterly', 'earnings', 'price', 'incomeStatementHistoryQuarterly', 'incomeStatementHistory', 'balanceSheetHistory', 'cashflowStatementHistoryQuarterly', 'quoteType', 'summaryDetail', 'symbol', 'pageViews'])

# income statement
annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

# cash flow statement
annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

# balance sheet
annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
quarterly_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']
# example of income statmement accounts
print(annual_is[0])

# {'researchDevelopment': {}, 'effectOfAccountingCharges': {}, 'incomeBeforeTax': {'raw': -640000000, 'fmt': '-640M', 'longFmt': '-640,000,000'}, 'minorityInterest': {'raw': 45000000, 'fmt': '45M', 'longFmt': '45,000,000'}, 'netIncome': {'raw': 47000000, 'fmt': '47M', 'longFmt': '47,000,000'}, 'sellingGeneralAdministrative': {'raw': 10218000000, 'fmt': '10.22B', 'longFmt': '10,218,000,000'}, 'grossProfit': {'raw': 12876000000, 'fmt': '12.88B', 'longFmt': '12,876,000,000'}, 'ebit': {'raw': 2658000000, 'fmt': '2.66B', 'longFmt': '2,658,000,000'}, 'endDate': {'raw': 1577750400, 'fmt': '2019-12-31'}, 'operatingIncome': {'raw': 2658000000, 'fmt': '2.66B', 'longFmt': '2,658,000,000'}, 'otherOperatingExpenses': {}, 'interestExpense': {'raw': -1049000000, 'fmt': '-1.05B', 'longFmt': '-1,049,000,000'}, 'extraordinaryItems': {}, 'nonRecurring': {}, 'otherItems': {}, 'incomeTaxExpense': {'raw': -724000000, 'fmt': '-724M', 'longFmt': '-724,000,000'}, 'totalRevenue': {'raw': 155900000000, 'fmt': '155.9B', 'longFmt': '155,900,000,000'}, 'totalOperatingExpenses': {'raw': 153242000000, 'fmt': '153.24B', 'longFmt': '153,242,000,000'}, 'costOfRevenue': {'raw': 143024000000, 'fmt': '143.02B', 'longFmt': '143,024,000,000'}, 'totalOtherIncomeExpenseNet': {'raw': -3298000000, 'fmt': '-3.3B', 'longFmt': '-3,298,000,000'}, 'maxAge': 1, 'discontinuedOperations': {}, 'netIncomeFromContinuingOps': {'raw': 84000000, 'fmt': '84M', 'longFmt': '84,000,000'}, 'netIncomeApplicableToCommonShares': {'raw': 47000000, 'fmt': '47M', 'longFmt': '47,000,000'}}
# # there's a variety of  number formats provided
# annual_is[0]['operatingIncome']
# {'raw': 2658000000, 'fmt': '2.66B', 'longFmt': '2,658,000,000'}
# # The data can be consoldated into an easy to read, or export, data set with a loop

# annual_is_stmts = []

# # consolidate annual
# for s in annual_is:
#     statement = {}
#     for key, val in s.items():
#         try:
#             statement[key] = val['raw']
#         except TypeError:
#             continue
#         except KeyError:
#             continue
#     annual_is_stmts.append(statement)
# annual_is_stmts[0]
# {'incomeBeforeTax': -640000000,
#  'minorityInterest': 45000000,
#  'netIncome': 47000000,
#  'sellingGeneralAdministrative': 10218000000,
#  'grossProfit': 12876000000,
#  'ebit': 2658000000,
#  'endDate': 1577750400,
#  'operatingIncome': 2658000000,
#  'interestExpense': -1049000000,
#  'incomeTaxExpense': -724000000,
#  'totalRevenue': 155900000000,
#  'totalOperatingExpenses': 153242000000,
#  'costOfRevenue': 143024000000,
#  'totalOtherIncomeExpenseNet': -3298000000,
#  'netIncomeFromContinuingOps': 84000000,
#  'netIncomeApplicableToCommonShares': 47000000}
# # This model can be applied to all other financial statements, as you can see from the examples below.

# annual_cf_stmts = []
# quarterly_cf_stmts = []

# # annual
# for s in annual_cf:
#     statement = {}
#     for key, val in s.items():
#         try:
#             statement[key] = val['raw']
#         except TypeError:
#             continue
#         except KeyError:
#             continue
#     annual_cf_stmts.append(statement)

# # quarterly
# for s in quarterly_cf:
#     statement = {}
#     for key, val in s.items():
#         try:
#             statement[key] = val['raw']
#         except TypeError:
#             continue
#         except KeyError:
#             continue
#     quarterly_cf_stmts.append(statement)
# annual_cf_stmts[0]
# {'investments': -543000000,
#  'changeToLiabilities': 5260000000,
#  'totalCashflowsFromInvestingActivities': -13721000000,
#  'netBorrowings': -277000000,
#  'totalCashFromFinancingActivities': -3129000000,
#  'changeToOperatingActivities': 1554000000,
#  'netIncome': 47000000,
#  'changeInCash': 834000000,
#  'endDate': 1577750400,
#  'repurchaseOfStock': -237000000,
#  'effectOfExchangeRate': 45000000,
#  'totalCashFromOperatingActivities': 17639000000,
#  'depreciation': 8490000000,
#  'otherCashflowsFromInvestingActivities': -152000000,
#  'dividendsPaid': -2389000000,
#  'changeToInventory': 206000000,
#  'changeToAccountReceivables': -816000000,
#  'otherCashflowsFromFinancingActivities': -226000000,
#  'changeToNetincome': 2898000000,
#  'capitalExpenditures': -7632000000}
# # Profile Data
# # We can copy the same steps from the Financial statements on the Profile data

# response = requests.get(url_profile.format(stock, stock))
# soup = BeautifulSoup(response.text, 'html.parser')
# pattern = re.compile(r'\s--\sData\s--\s')
# script_data = soup.find('script', text=pattern).contents[0]
# start = script_data.find("context")-2
# json_data = json.loads(script_data[start:-12])
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()
# dict_keys(['financialsTemplate', 'price', 'secFilings', 'quoteType', 'calendarEvents', 'summaryDetail', 'symbol', 'assetProfile', 'pageViews'])
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile'].keys()
# dict_keys(['zip', 'sector', 'fullTimeEmployees', 'compensationRisk', 'auditRisk', 'longBusinessSummary', 'city', 'phone', 'state', 'shareHolderRightsRisk', 'compensationAsOfEpochDate', 'governanceEpochDate', 'boardRisk', 'country', 'companyOfficers', 'website', 'maxAge', 'overallRisk', 'address1', 'industry'])
# # data for company officers (just the first 3 are listed for brevity )
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['companyOfficers'][:3]
# [{'totalPay': {'raw': 3661316, 'fmt': '3.66M', 'longFmt': '3,661,316'},
#   'exercisedValue': {'raw': 0, 'fmt': None, 'longFmt': '0'},
#   'yearBorn': 1957,
#   'name': 'Mr. William Clay Ford Jr.',
#   'title': 'Exec. Chairman',
#   'maxAge': 1,
#   'fiscalYear': 2019,
#   'unexercisedValue': {'raw': 0, 'fmt': None, 'longFmt': '0'},
#   'age': 62},
#  {'totalPay': {'raw': 4167237, 'fmt': '4.17M', 'longFmt': '4,167,237'},
#   'exercisedValue': {'raw': 0, 'fmt': None, 'longFmt': '0'},
#   'yearBorn': 1955,
#   'name': 'Mr. James Patrick Hackett',
#   'title': 'Pres, CEO & Director',
#   'maxAge': 1,
#   'fiscalYear': 2019,
#   'unexercisedValue': {'raw': 0, 'fmt': None, 'longFmt': '0'},
#   'age': 64},
#  {'totalPay': {'raw': 4018261, 'fmt': '4.02M', 'longFmt': '4,018,261'},
#   'exercisedValue': {'raw': 0, 'fmt': None, 'longFmt': '0'},
#   'yearBorn': 1967,
#   'name': 'Mr. Timothy R. Stone',
#   'title': 'Chief Financial Officer',
#   'maxAge': 1,
#   'fiscalYear': 2019,
#   'unexercisedValue': {'raw': 0, 'fmt': None, 'longFmt': '0'},
#   'age': 52}]
# # business description
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['longBusinessSummary']
# 'Ford Motor Company designs, manufactures, markets, and services a range of Ford cars, trucks, sport utility vehicles, electrified vehicles, and Lincoln luxury vehicles worldwide. It operates through three segments: Automotive, Mobility, and Ford Credit. The Automotive segment sells Ford and Lincoln vehicles, service parts, and accessories through distributors and dealers, as well as through dealerships to commercial fleet customers, daily rental car companies, and governments. The Mobility segment designs and builds mobility services; and provides self-driving systems development and vehicle integration, autonomous vehicle research and engineering, and autonomous vehicle transportation-as-a-service network development services. The Ford Credit segment primarily engages in vehicle-related financing and leasing activities to and through automotive dealers. It provides retail installment sale contracts for new and used vehicles; and direct financing leases for new vehicles to retail and commercial customers, such as leasing companies, government entities, daily rental companies, and fleet customers. This segment also offers wholesale loans to dealers to finance the purchase of vehicle inventory; and loans to dealers to finance working capital and enhance dealership facilities, purchase dealership real estate, and other dealer vehicle programs. The company was founded in 1903 and is based in Dearborn, Michigan.'
# # sec filings from Edgars ( just the first 3 are listed for brevity )
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['secFilings']['filings'][:3]
# [{'date': '2020-08-04',
#   'epochDate': 1596549938,
#   'type': '8-K',
#   'title': 'Change in Directors or Principal Officers, Financial Statements and Exhibits',
#   'edgarUrl': 'https://yahoo.brand.edgar-online.com/DisplayFiling.aspx?TabIndex=2&dcn=0000037996-20-000059&nav=1&src=Yahoo',
#   'maxAge': 1},
#  {'date': '2020-07-31',
#   'epochDate': 1596194245,
#   'type': '10-Q',
#   'title': 'Quarterly Report',
#   'edgarUrl': 'https://yahoo.brand.edgar-online.com/DisplayFiling.aspx?TabIndex=2&dcn=0000037996-20-000057&nav=1&src=Yahoo',
#   'maxAge': 1},
#  {'date': '2020-07-31',
#   'epochDate': 1596193825,
#   'type': '8-K',
#   'title': 'Results of Operations and Financial Condition, Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant, Financial Statements and Exhibits',
#   'edgarUrl': 'https://yahoo.brand.edgar-online.com/DisplayFiling.aspx?TabIndex=2&dcn=0000037996-20-000056&nav=1&src=Yahoo',
#   'maxAge': 1}]
# # lot of other data is available
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']
# {'previousClose': {'raw': 7.04, 'fmt': '7.04'},
#  'regularMarketOpen': {'raw': 7.05, 'fmt': '7.05'},
#  'twoHundredDayAverage': {'raw': 6.0061593, 'fmt': '6.01'},
#  'trailingAnnualDividendYield': {'raw': 0.06392045, 'fmt': '6.39%'},
#  'payoutRatio': {},
#  'volume24Hr': {},
#  'regularMarketDayHigh': {'raw': 7.12, 'fmt': '7.12'},
#  'navPrice': {},
#  'averageDailyVolume10Day': {'raw': 64910450,
#   'fmt': '64.91M',
#   'longFmt': '64,910,450'},
#  'totalAssets': {},
#  'regularMarketPreviousClose': {'raw': 7.04, 'fmt': '7.04'},
#  'fiftyDayAverage': {'raw': 6.9228573, 'fmt': '6.92'},
#  'trailingAnnualDividendRate': {'raw': 0.45, 'fmt': '0.45'},
#  'open': {'raw': 7.05, 'fmt': '7.05'},
#  'toCurrency': None,
#  'averageVolume10days': {'raw': 64910450,
#   'fmt': '64.91M',
#   'longFmt': '64,910,450'},
#  'expireDate': {},
#  'yield': {},
#  'algorithm': None,
#  'dividendRate': {},
#  'exDividendDate': {'raw': 1580256000, 'fmt': '2020-01-29'},
#  'beta': {'raw': 1.323299, 'fmt': '1.32'},
#  'circulatingSupply': {},
#  'startDate': {},
#  'regularMarketDayLow': {'raw': 6.99, 'fmt': '6.99'},
#  'priceHint': {'raw': 2, 'fmt': '2', 'longFmt': '2'},
#  'currency': 'USD',
#  'regularMarketVolume': {'raw': 45529000,
#   'fmt': '45.53M',
#   'longFmt': '45,529,000'},
#  'lastMarket': None,
#  'maxSupply': {},
#  'openInterest': {},
#  'marketCap': {'raw': 27928297472,
#   'fmt': '27.93B',
#   'longFmt': '27,928,297,472'},
#  'volumeAllCurrencies': {},
#  'strikePrice': {},
#  'averageVolume': {'raw': 67381340, 'fmt': '67.38M', 'longFmt': '67,381,340'},
#  'priceToSalesTrailing12Months': {'raw': 0.21418063, 'fmt': '0.21'},
#  'dayLow': {'raw': 6.99, 'fmt': '6.99'},
#  'ask': {'raw': 7.07, 'fmt': '7.07'},
#  'ytdReturn': {},
#  'askSize': {'raw': 45900, 'fmt': '45.9k', 'longFmt': '45,900'},
#  'volume': {'raw': 45529000, 'fmt': '45.53M', 'longFmt': '45,529,000'},
#  'fiftyTwoWeekHigh': {'raw': 9.6, 'fmt': '9.60'},
#  'forwardPE': {'raw': 9.887324, 'fmt': '9.89'},
#  'maxAge': 1,
#  'fromCurrency': None,
#  'fiveYearAvgDividendYield': {'raw': 5.93, 'fmt': '5.93'},
#  'fiftyTwoWeekLow': {'raw': 3.96, 'fmt': '3.96'},
#  'bid': {'raw': 7.05, 'fmt': '7.05'},
#  'tradeable': False,
#  'dividendYield': {},
#  'bidSize': {'raw': 47300, 'fmt': '47.3k', 'longFmt': '47,300'},
#  'dayHigh': {'raw': 7.12, 'fmt': '7.12'}}
# # Statistics
# response = requests.get(url_stats.format(stock, stock))
# soup = BeautifulSoup(response.text, 'html.parser')
# pattern = re.compile(r'\s--\sData\s--\s')
# script_data = soup.find('script', text=pattern).contents[0]
# start = script_data.find("context")-2
# json_data = json.loads(script_data[start:-12])
# json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']
# {'annualHoldingsTurnover': {},
#  'enterpriseToRevenue': {'raw': 1.266, 'fmt': '1.27'},
#  'beta3Year': {},
#  'profitMargins': {'raw': -0.016280001, 'fmt': '-1.63%'},
#  'enterpriseToEbitda': {'raw': 26.996, 'fmt': '27.00'},
#  '52WeekChange': {'raw': -0.2389189, 'fmt': '-23.89%'},
#  'morningStarRiskRating': {},
#  'forwardEps': {'raw': 0.71, 'fmt': '0.71'},
#  'revenueQuarterlyGrowth': {},
#  'sharesOutstanding': {'raw': 3907539968,
#   'fmt': '3.91B',
#   'longFmt': '3,907,539,968'},
#  'fundInceptionDate': {},
#  'annualReportExpenseRatio': {},
#  'totalAssets': {},
#  'bookValue': {'raw': 7.748, 'fmt': '7.75'},
#  'sharesShort': {'raw': 98362703, 'fmt': '98.36M', 'longFmt': '98,362,703'},
#  'sharesPercentSharesOut': {'raw': 0.0247, 'fmt': '2.47%'},
#  'fundFamily': None,
#  'lastFiscalYearEnd': {'raw': 1577750400, 'fmt': '2019-12-31'},
#  'heldPercentInstitutions': {'raw': 0.55063, 'fmt': '55.06%'},
#  'netIncomeToCommon': {'raw': -2123000064,
#   'fmt': '-2.12B',
#   'longFmt': '-2,123,000,064'},
#  'trailingEps': {'raw': -0.535, 'fmt': '-0.54'},
#  'lastDividendValue': {},
#  'SandP52WeekChange': {'raw': 0.13119566, 'fmt': '13.12%'},
#  'priceToBook': {'raw': 0.90604025, 'fmt': '0.91'},
#  'heldPercentInsiders': {'raw': 0.00176, 'fmt': '0.18%'},
#  'nextFiscalYearEnd': {'raw': 1640908800, 'fmt': '2021-12-31'},
#  'yield': {},
#  'mostRecentQuarter': {'raw': 1593475200, 'fmt': '2020-06-30'},
#  'shortRatio': {'raw': 1.76, 'fmt': '1.76'},
#  'sharesShortPreviousMonthDate': {'raw': 1596153600, 'fmt': '2020-07-31'},
#  'floatShares': {'raw': 3898144890, 'fmt': '3.9B', 'longFmt': '3,898,144,890'},
#  'beta': {'raw': 1.323299, 'fmt': '1.32'},
#  'enterpriseValue': {'raw': 165106728960,
#   'fmt': '165.11B',
#   'longFmt': '165,106,728,960'},
#  'priceHint': {'raw': 2, 'fmt': '2', 'longFmt': '2'},
#  'threeYearAverageReturn': {},
#  'lastSplitDate': {'raw': 965260800, 'fmt': '2000-08-03'},
#  'lastSplitFactor': '1748175:1000000',
#  'legalType': None,
#  'morningStarOverallRating': {},
#  'earningsQuarterlyGrowth': {'raw': 6.547, 'fmt': '654.70%'},
#  'priceToSalesTrailing12Months': {},
#  'dateShortInterest': {'raw': 1598832000, 'fmt': '2020-08-31'},
#  'pegRatio': {'raw': 1.28, 'fmt': '1.28'},
#  'ytdReturn': {},
#  'forwardPE': {'raw': 9.887324, 'fmt': '9.89'},
#  'maxAge': 1,
#  'lastCapGain': {},
#  'shortPercentOfFloat': {'raw': 0.0278, 'fmt': '2.78%'},
#  'sharesShortPriorMonth': {'raw': 115899333,
#   'fmt': '115.9M',
#   'longFmt': '115,899,333'},
#  'category': None,
#  'fiveYearAverageReturn': {}}
# # Historical Stock Data
# # This data uses a hidden api, as you can see from the "query" prefix, the version number (V7), and the variety of parameters.

# stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/F?period1=1568483641&period2=1600106041&interval=1d&events=history'
# response = requests.get(stock_url)
# # extract the csv data
# file = StringIO(response.text)
# reader = csv.reader(file)
# data = list(reader)

# # show the first 5 records
# for row in data[:5]:
#     print(row)
# ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
# ['2019-09-16', '9.360000', '9.450000', '9.240000', '9.300000', '8.996831', '50052600']
# ['2019-09-17', '9.270000', '9.310000', '9.180000', '9.280000', '8.977483', '27391200']
# ['2019-09-18', '9.260000', '9.360000', '9.220000', '9.250000', '8.948462', '24309400']
# ['2019-09-19', '9.310000', '9.330000', '9.100000', '9.100000', '8.803351', '28780700']
# # You can start to customize this by pulling out the parameters from the URL and putting them into a dictionary.

# stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?'

# params = {
#     'period1':'1568483641',
#     'period2':'1600106041',
#     'interval':'1d',
#     'events':'history'
# }
# # By inspecting the request headers and parameters online, it's possible to see how this can be simplified further... by using the range parameter instead of the periods.

# params = {
#     'range': '5y',
#     'interval':'1d',
#     'events':'history'
# }
# response = requests.get(stock_url.format(stock), params=params)
# # extract the csv data
# file = StringIO(response.text)
# reader = csv.reader(file)
# data = list(reader)

# # show the first 5 records
# for row in data[:5]:
#     print(row)