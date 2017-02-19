#!/usr/bin/env python


import sys
import argparse
import pandas as pd
import pandas_datareader.data as web
import datetime
import requests
import bs4
import pprint


def init_argparse():
    parser = argparse.ArgumentParser(description="olhc - open, high, low, close analyzer")
    parser.add_argument("--symbol", dest="symbol",
                        help="Stock symbol")
    parser.add_argument("--start-date", dest="startDate",
                        help="Start date for analysis (MM/DD/YYYY format)")
    parser.add_argument("--end-date", dest="endDate",
                        help="End date for analysis (MM/DD/YYYY format)")
    return parser.parse_args()


def get_earnings_data(date, symbol="QQQ"):
    html = requests.get("https://biz.yahoo.com/research/earncal/{}.html".format(date), headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"}).text
    soup = bs4.BeautifulSoup(html)
    quotes = []
    for tr in soup.find_all("tr"):
        if len(tr.contents) > 3:
            if len(tr.contents[1].contents) > 0:
                if tr.contents[1].contents[0].name == "a":
                    if tr.contents[1].contents[0]["href"].startswith("http://finance.yahoo.com/q?s="):
                        if  tr.contents[1].contents[0].text == symbol:
                            quotes.append({     "name"  : tr.contents[0].text
                                               ,"symbol": tr.contents[1].contents[0].text
                                               ,"url"   : tr.contents[1].contents[0]["href"]
                                               ,"eps"   : tr.contents[2].text if len(tr.contents) == 6 else u'N/A'
                                               ,"time"  : tr.contents[3].text if len(tr.contents) == 6 else tr.contents[2].text
                                           })
    return quotes


def main(argv):
    print('Begin run...')
    args = init_argparse()

    ed = get_earnings_data("20170221", "WMT")
    print(ed)

    print()

    pprint.pprint(ed[0])

    print('End run.')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
