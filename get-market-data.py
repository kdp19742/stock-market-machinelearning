import requests                 # handles http interactions
from bs4 import BeautifulSoup   # beautiful soup handles the html to text conversion and more
import re                       # regex needed to find the crumb
from datetime import datetime   # string to datetime object conversion
from time import mktime         # mktime transforms datetime to unix timestamps
from datetime import date       
from datetime import timedelta
import html5lib

def get_cookie(ticker):
  url = "https://finance.yahoo.com/quote/{ticker}/history?p={ticker}".format(ticker=ticker)
  with requests.session():
    header = {
      'Connection': 'keep-alive',
      'Expires': '-1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
      AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    website = requests.get(url, headers=header)
    soup = BeautifulSoup(website.text, 'html5lib')
    crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))

    return(header, crumb[0], website.cookies)

def convert_to_unix(date):
  datum = datetime.strptime(date, '%Y-%m-%d')
  
  return int(mktime(datum.timetuple()))

def load_csv_data(ticker):
  now_time = str(date.today())
  start_time = str(date.today() - timedelta(days=3650))
  interval = '1d'
  
  print(now_time)
  print(start_time)

  day_begin_unix = convert_to_unix(start_time)
  day_end_unix = convert_to_unix(now_time)

  header, crumb, cookies = get_cookie(ticker)

  with requests.session():
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' \
          '{ticker}?period1={day_begin}&period2={day_end}&interval={interval}&events=history&crumb={crumb}' \
          .format(ticker=ticker, day_begin=day_begin_unix, day_end=day_end_unix, interval=interval, crumb=crumb)
    
    website = requests.get(url, headers=header, cookies=cookies)
    print(url)
    #return website.text.split('\n')[:-1]
    
  with open("market-data.csv", 'wb') as f:
    f.write(website.content)

get_cookie('SPY')
load_csv_data('SPY')