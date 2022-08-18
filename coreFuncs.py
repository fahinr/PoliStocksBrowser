import os
import numpy as np

from pathlib import Path

from mechanize import Browser
from bs4 import BeautifulSoup
import requests

from tqdm import tqdm
from time import sleep
from selenium import webdriver

import pandas as pd
import lxml.html as lh

from sqlalchemy import create_engine
import pymysql



def pageScraping():
    
    ## MOST ACCURATE ONE SINCE I CAN EXTRAPOLATE THE EXACT DATA I NEED (H3S, ETC)
    currp = 1
    maxp = 1
    # ^ For page numbers of same link (not working no idea why) Doesn't grab the second page, defaults to the first even when link is valid
    chartarr = []
    df = pd.DataFrame(columns = ['Politician', 'Issuer', 'Ticker', 'Trade_Date', 'Type', 'Size', 'Price', 'Analyst_Rating'])
    #print(df)


    while currp <= maxp:
        page =  f'https://www.capitoltrades.com/trades?page={currp}'
        print(page)
        r = requests.get(page)
        soup = BeautifulSoup(r.text, 'html.parser') 
        poltable = soup.find('table')

        for team in poltable.find_all('tbody'):
            rows = team.find_all('tr', class_ = 'q-tr')
            for row in rows:
                ### NAME ###
                poli = row.find('td', class_ = 'q-td q-column--politician')
                for po in poli:
                    name = po.find('h3', class_ = 'q-fieldset politician-name').text
                    #print(name)

                ### ISSUER AND TICKER ###
                issuer = row.find('td', class_ = 'q-td q-column--issuer')
                for iss in issuer:
                    issuerTitle = iss.find('h3', class_ = 'q-fieldset issuer-name').text
                    ticker = iss.find('span', class_ = 'q-field issuer-ticker').text
                    #print(ticker)
                    #print(issuerTitle)

                ### DATE TRADED ###
                date = row.find('td', class_ = 'q-td q-column--txDate')
                for dates in date:
                    year = dates.find('div', class_ = 'q-label').text
                    day = dates.find('div', class_ = 'q-value').text
                    tradeDate = year + day
                    #print(day,year)

                ### TRADE TYPE (BUY/SELL) ###
                tradeTy = row.find('td', class_ = 'q-td q-column--txType').text
                #print(tradeTy)

                ### TRADED RANGE AMOUNT ###       
                result_prices_pc = row.find("span", attrs={"class": "text hoverable text--size-s text--color-light"})
                size = result_prices_pc.text
                #print(result_prices_pc.text)

                ### PRICE TRADED AT ###
                price = row.find('td', class_ = 'q-td q-column--price').text
                #price = float(price)
                try:
                    price = float(price)

                except:
                    price = 'N/A'
                    pass

                #print(price)

                ### APPENDING ###
                df = df.append({'Politician' : name, 'Issuer' : issuerTitle, 'Ticker' : ticker, 'Trade_Date' : tradeDate, 
                    'Type' : tradeTy, 'Size' : size, 'Price' : price}, ignore_index = True)

            ### MARKETWATCH PHASE FOR ANALYTICS ###    
            for tix, price in zip(df['Ticker'], df['Price']):
                sleep(10)

                tickerPart = tix.partition(':')
                tickerSymb = tickerPart[0]
                tickerCountry = tickerPart[2]                

                if tickerCountry == 'US':
                    mpage = f'http://www.marketwatch.com/investing/stock/{tickerSymb}?mod=search_symbol'
                    mwr = requests.get(mpage)
                    msoup = BeautifulSoup(mwr.text, 'html.parser')

                    if(price == 'N/A'):
                        #Make a function to grab price on whenever the trade day was. Make sure Ticker is valid
                        pass
                    #print(tickerPart)
                    try:
                        chart = msoup.find('li', class_ = 'analyst__option active').text
                        chartarr.append(chart)
                    except AttributeError:
                        try:

                            mpage = f'https://www.marketwatch.com/investing/fund/{tickerSymb}'
                            mwr = requests.get(mpage)
                            msoup = BeautifulSoup(mwr.text, 'html.parser')

                            lipper = str(msoup.find('div', class_ = 'element__details').text)
                            chartarr.append(lipper)
                            continue
                            ### !!!! PARSE AND FIND LIPPER LEADER OF FUND, EXCEPTION MEANS NONE FOUND
                        except AttributeError:
                            print(tickerSymb," Ticker/Issuer not found. Likely a local investment.")
                            unk = 'N/A'
                            chartarr.append(unk)
                            continue
                else:
                    notus = 'NOT US'
                    chartarr.append(notus)                

        ### APPEND ANALYTIC RATINGS ARRAY ###
        df['Analyst_Rating'] = chartarr
        currp += 1
        #sleep(10)



    print(df)
    return df



def dataInsertion(tablename, data):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='database')
    cursor = connection.cursor()
    
    cols = "`,`".join([str(i) for i in data.columns.tolist()])
    for i,row in data.iterrows():
        sql = f"INSERT INTO `{tablename}` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        try:
            run = cursor.execute(sql, tuple(row))
        except:
            print("Entry was not inserted correctly.")
            

    connection.commit()
    

def removeDuplicates(tablename):
    ### !! If this doesn't work, kill the sql transactional process (show processlist;, kill {id} (sleep ones),
    ###   mysql> SET transaction_isolation = 'READ-COMMITTED';, SET GLOBAL transaction_isolation = 'READ-COMMITTED';
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='database')
    cursor = connection.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM {tablename}')
    total = cursor.fetchall()
    
    ### This is the command to remove duplicates and keep the one with the lesser primary key. 
    # gotta figure out how to rehash the primary key and update it
    deletion = f"""
    DELETE t1 FROM {tablename} t1
    INNER JOIN {tablename} t2
    WHERE
        t1.id > t2.id AND
        t1.politician = t2.politician AND
        t1.issuer = t2.issuer AND
        t1.type = t2.type AND
        t1.size = t2.size AND
        t1.trade_date = t2.trade_date; """
    #print(deletion)
    cursor.execute(deletion)
    connection.commit()
    
    cursor.execute(f'SELECT COUNT(*) FROM {tablename}')
    count = cursor.fetchall()
    count = total[0][0] - count[0][0]
    print('Removed', count, 'duplicate entries.')

    
def printTable(tablename):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='database')
    cursor = connection.cursor()
    #[index], [politician], [issuer], [ticker], [trade date], [type], [size], [price], [analyst rsting]
    # Execute Query
    cursor.execute(f'SELECT * FROM {tablename}')

    # Fetch the records
    result = cursor.fetchall()

    for i in result:
        print(i)
