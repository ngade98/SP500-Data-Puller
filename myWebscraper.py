# Scrapes Wikipedia page for list of SP 500 companies
# and queries Yahoo finance to save the historical data for tickers.
# Author: Kiran Bhattacharyya
# License: MIT License

import urllib2
import pytz
import pandas_datareader.data as web
import datetime
from bs4 import BeautifulSoup
import csv

thisurl = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

myPage = urllib2.urlopen(thisurl)

mySoup = BeautifulSoup(myPage, "html.parser")

table = mySoup.find('table', {'class': 'wikitable sortable'})

sector_tickers = dict()
for row in table.findAll('tr'):
    col = row.findAll('td')
    if len(col) > 0:
        sector = str(col[3].string.strip()).lower().replace(' ', '_')
        ticker = str(col[0].string.strip())
        if sector not in sector_tickers:
            sector_tickers[sector] = list()
        sector_tickers[sector].append(ticker)

sector_tickers[sector].append('SPY')

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 12, 27)

myKeys = sector_tickers.keys()

for i in xrange(1,len(myKeys)):
    myTickers = sector_tickers[myKeys[i]]
    for j in xrange(1,len(myTickers)):
        myData = web.DataReader(myTickers[j], 'yahoo', start, end)
        fileName = myTickers[j] + '.csv'
        myData.to_csv(fileName)
