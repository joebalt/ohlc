#!/usr/bin/env python


import sys
import argparse
import pandas as pd
import pandas_datareader.data as web
import datetime
import requests
import bs4
import pprint
import time


def init_argparse():
    parser = argparse.ArgumentParser(description="olhc - open, high, low, close analyzer")
    parser.add_argument("--symbol", dest="symbol",
                        help="Stock symbol")
    parser.add_argument("--start-date", dest="startDate",
                        help="Start date for analysis (YYYYMMDD format)")
    parser.add_argument("--end-date", dest="endDate",
                        help="End date for analysis (YYYYMMDD format)")
    parser.add_argument("--outfile", dest="outfile",
                        help="output file", default="/var/tmp/outfile")
    return parser.parse_args()


def get_earnings_data(date, symbol="QQQ"):
    uri = "https://biz.yahoo.com/research/earncal/{}.html".format(date)
    html = requests.get(uri, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"}).text
    soup = bs4.BeautifulSoup(html)
    quotes = []
    for tr in soup.find_all("tr"):
        if len(tr.contents) > 3:
            if len(tr.contents[1].contents) > 0:
                if tr.contents[1].contents[0].name == "a":
                    if tr.contents[1].contents[0]["href"].startswith("http://finance.yahoo.com/q?s="):
                        if  tr.contents[1].contents[0].text == symbol:
                            quotes.append({     "date"  : date
                                               ,"name"  : tr.contents[0].text
                                               ,"symbol": tr.contents[1].contents[0].text
                                               ,"url"   : tr.contents[1].contents[0]["href"]
                                               ,"eps"   : tr.contents[2].text if len(tr.contents) == 6 else u'N/A'
                                               ,"time"  : tr.contents[3].text if len(tr.contents) == 6 else tr.contents[2].text
                                           })
                            break
    return quotes


def main(argv):
    print('Begin run...')
    args = init_argparse()

    el = []
    bdatelist = pd.bdate_range(args.startDate, args.endDate).tolist()
    # bdatelist = pd.bdate_range("20070201", pd.datetime.today() ).tolist()
    f = open(args.outfile, 'wb')
    for bd in bdatelist:
        sdate = str(bd.year) + "{:02}".format(bd.month) + "{:02}".format(bd.day)
        print("checking: " + sdate)
        ed = get_earnings_data(sdate, args.symbol)
        if len(ed) > 0:
            el.append(ed)
            f.write(sdate + '\n')
        time.sleep(0.25)
    f.close()
    print(el)

    print('End run.')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
