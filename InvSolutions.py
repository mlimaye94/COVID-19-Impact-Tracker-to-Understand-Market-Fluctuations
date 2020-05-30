# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 00:20:11 2020

File Name: InvSolutions.py 

Mandar Limaye
Steffie Rego
Shubham Lalwani
"""

#importing libraries
import pandas as pd
import numpy as np
import time
import datetime
import urllib.request as rq
import bs4 as bs
import requests
from dateutil import parser
from functools import reduce
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings("ignore")


pd.plotting.register_matplotlib_converters()


#this function scrapes the web to get bitcoin data uptil current date (web-scarping - tabular format data)
def getBitcoinData():
    #setting current date
    date=str(pd.datetime.now().date())
    date = date.replace("-", "")
    
    #url to scrape the data
    url='https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20200228&end='+date
    sauce = rq.urlopen(url).read()
    #using beautifulsoup read the html
    soup = bs.BeautifulSoup(sauce , "lxml")

    #extarct the heading from the 'thead' tag and insert into the headings list
    headings=[]
    table_head=soup.find('thead')
    table_head_row=table_head.find('tr')
    table_head_data=table_head_row.find_all('th')
    for th in table_head_data:
        headings.append(th.text)

    #extarct rows of data from all the 'tr' tags inside 'tbody' tag and append to the rows list
    rows=[]
    table=soup.find('tbody')
    table_rows=table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        rows.append(row)
        
    #create a dataframe using the rows as data and headings as column names
    bitcoin_df=pd.DataFrame(rows,columns=headings)
    
    #changing the date into a consistent format 
    bitcoin_dates=[]
    for i in bitcoin_df['Date']:
        now=parser.parse(str(i))
        bitcoin_dates.append(now.date())
    bitcoin_df['Date']=bitcoin_dates
    
    #replacing commas and making it float format
    bitcoin_df["bitcoin_Open"] = bitcoin_df["Open*"].str.replace(",","").astype(float)
    bitcoin_df["bitcoin_Close"] = bitcoin_df["Close**"].str.replace(",","").astype(float)
    bitcoin_df["bitcoin_MarketCap"] = bitcoin_df["Market Cap"].str.replace(",","").astype(float)
    
    #extracting and returning only useful columns
    bitcoin_df=bitcoin_df.loc[:,['Date','bitcoin_Open','bitcoin_Close','bitcoin_MarketCap']]
    
    return bitcoin_df

#this function scrapes the web to get covid-19 data uptil current date (API extarction - json data format)
def getCovidData():
    
    #setting current date
    date=str(pd.datetime.now().date())
    date = date.replace("-", "")
    
    #url to scrape the data
    covid_data = requests.get("https://covidtracking.com/api/v1/us/daily.json")
    #filling null values with 0 and storing the json data into a dataframe
    covid_df = pd.DataFrame(covid_data.json()).fillna(0)
    #selecting only relevant data according to dates
    covid_df=covid_df[(covid_df['date']>20200227) & (covid_df['date']<=int(date))]
    
    #changing the date into a consistent format 
    covid_dates=[]
    for i in covid_df['date']:
        now=parser.parse(str(i))
        covid_dates.append(now.date())
    covid_df['date']=covid_dates
    
    #extracting and returning only useful columns
    covid_df=covid_df.loc[:,['date','positive','hospitalizedCurrently','hospitalizedCumulative','recovered','death','totalTestResults']]
    covid_df.rename(columns = {'date':'Date'}, inplace = True)
    return covid_df

#this function scrapes the web to get annual mortagage data uptil current date (web scraping - tabular format)
def getAPRData():
    
    #url to scrape the data
    url='https://www.nerdwallet.com/blog/mortgages/current-interest-rates/'
    sauce = rq.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce , "lxml")

    #extarct the heading from the 'thead' tag and insert into the headings list
    headings=[]
    table_head=soup.find('thead')
    table_head_row=table_head.find('tr')
    table_head_data=table_head_row.find_all('th')
    for th in table_head_data:
        headings.append(th.text)

    #extarct rows of data from all the 'tr' tags inside 'tbody' tag and append to the rows list
    rows=[]
    table=soup.find('tbody')
    table_rows=table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        rows.append(row)

    #creating a dataframe out of rows data 
    apr_df=pd.DataFrame(rows,columns=headings)
    
    #changing the date into a consistent format and only selecting dates that are in 2020
    dates=[]
    for date in apr_df['Date']:
        if '2020' in date:
            dates.append(date)
    apr_df=apr_df[apr_df['Date'].isin(dates)]
    apr_df=apr_df[:-39]
    
    apr_dates=[]
    for i in apr_df['Date']:
        now=parser.parse(str(i))
        apr_dates.append(now.date())
    apr_df['Date']=apr_dates
    
    #replacing commas and making it float format
    apr_df["Avg Mortgage APR"] = apr_df["Average 5/1 ARM APR"].str.replace("%","").astype(float)
    
    #extarcting only useful columns and returning
    apr_df=apr_df.loc[:,['Date','Avg Mortgage APR']]
    return apr_df


#this function scrapes the web to get stock market (NASDAQ) data uptil current date (web-scarping - tabular format data)
def getNasdaqData():
    
    #fetching current date
    today_Date = str(pd.datetime.now().date())
    #computing the Unixtimestamp of current date
    UnixFormat = int(time.mktime(datetime.datetime.strptime(today_Date, "%Y-%m-%d").timetuple()))

    
    #url of web page to be scraped with Unixtimestamp of current date appended
    url = 'https://finance.yahoo.com/quote/%5EIXIC/history?period1=1582848000&period2='+str(UnixFormat)+'&interval=1d&filter=history&frequency=1d'
    html = rq.urlopen(url)
    bsyc = bs.BeautifulSoup(html.read(), "lxml")
    
    
    #find all table tags in the html
    tc_table_list = bsyc.findAll('table')
    tc_table = tc_table_list[0]
    
    
    #capture the table headers and table data and adding it to a list
    list_data = []
    for c in tc_table.children:
        for r in c.children:
            for p in r.children:
                list_data.append(p.text)


    #dropping the last element of the list           
    list_data = list_data[:-1]
    #converting list to numpy array
    arr = np.array(list_data)
    #creating a 2d numpy array using reshape
    arr = arr.reshape(len(arr)//7 , 7)


    
    df = pd.DataFrame(arr)
    #grab the first row for the header
    new_header = df.iloc[0] 
    df = df[1:] 
    #set the header row as the df header
    df.columns = new_header
    df.reset_index()
    
    df = df.rename(columns = {"Close*" : "Close"})
    
    
    #removing hyphen , commas in columns and making it float format
    df["Open"] = df["Open"].str.replace("-" , "0")
    df["nasdaq_Open"] = df["Open"].str.replace(",","").astype(float)
    
    df["Close"] = df["Close"].str.replace("-" , "0")
    df["nasdaq_Close"] = df["Close"].str.replace(",","").astype(float)
    
    df["Volume"] = df["Volume"].str.replace("-" , "0")
    df["nasdaq_Volume"] = df["Volume"].str.replace(",","").astype(float)

    
    #changing the dates into consistent format
    nasdaq_dates=[]
    for i in df['Date']:
        now=parser.parse(str(i))
        nasdaq_dates.append(now.date())
    df['Date']=nasdaq_dates
    
     #extarcting only useful columns and returning
    df = df.loc[: , ["Date" , "nasdaq_Open" , "nasdaq_Close" , "nasdaq_Volume"]]
    df.drop(df[df.nasdaq_Open ==0].index,inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

#this function scrapes the web to get gold market data uptil current date (web-scarping - tabular format data)
def getGoldData():

     #fetching current date
    today_Date = str(pd.datetime.now().date())
    #computing the Unixtimestamp of current date
    UnixFormat = int(time.mktime(datetime.datetime.strptime(today_Date, "%Y-%m-%d").timetuple()))

    
    #url of web page to be scraped with Unixtimestamp of current date appended
    url = 'https://finance.yahoo.com/quote/GC%3DF/history?period1=1582848000&period2='+str(UnixFormat)+'&interval=1d&filter=history&frequency=1d'
    html = rq.urlopen(url)
    bsyc = bs.BeautifulSoup(html.read(), "lxml")
    
    
    #find all table tags in the html
    tc_table_list = bsyc.findAll('table')
    tc_table = tc_table_list[0]
    
    
     #capture the table headers and table data and adding it to a list
    list_data = []
    for c in tc_table.children:
        for r in c.children:
            for p in r.children:
                list_data.append(p.text)


    #dropping the last element of the list 
    list_data = list_data[:-1]
    #converting list to numpy array
    arr = np.array(list_data)
    #creating a 2d numpy array using reshape
    arr = arr.reshape(len(arr)//7 , 7)


    
    df = pd.DataFrame(arr)
     #grab the first row for the header
    new_header = df.iloc[0]
    df = df[1:] 
    #set the header row as the df header
    df.columns = new_header 
    df.reset_index()
    
    
    df = df.rename(columns = {"Close*" : "Close"})
    
    
    #removing hyphen , commas in columns and making it float format
    df["Open"] = df["Open"].str.replace("-" , "0")
    df["gold_Open"] = df["Open"].str.replace(",","").astype(float)
    
    df["Close"] = df["Close"].str.replace("-" , "0")
    df["gold_Close"] = df["Close"].str.replace(",","").astype(float)
    
    df["Volume"] = df["Volume"].str.replace("-" , "0")
    df["gold_Volume"] = df["Volume"].str.replace(",","").astype(float)

    
    #changing the dates into consistent format
    gold_dates=[]
    for i in df['Date']:
        now=parser.parse(str(i))
        gold_dates.append(now.date())
    df['Date']=gold_dates
    
    #extarcting only useful columns and returning
    df = df.loc[: , ["Date" , "gold_Open" , "gold_Close" , "gold_Volume"]]
    df.drop(df[df.gold_Open ==0].index,inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

#this function gets the latest data and aggregates it to a final merged dataframe
def getNewData():    
    gold_df = getGoldData()
    bitcoin_df=getBitcoinData()
    covid_df=getCovidData()
    apr_df=getAPRData()
    nasdaq_df=getNasdaqData()

    dataframes =[covid_df,apr_df,nasdaq_df,gold_df,bitcoin_df]
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],how='outer'), dataframes)
    final_df=df_merged.dropna(axis=0,how='any')
    final_df.reset_index(drop=True,inplace=True)
    return final_df

#--------------------------------------------------------------------------------

'''
Note - the dates may vary according to data since some prices may not be vailable for all days 
Ex. Saturday prices not available for nasdaq but avilable for covid data
options -
 1 - latest available price
 2 - last 15 available days price
 3 - last 30 month(latest 30 available) days price
df_name is market name
 'stock' - Stock Market(Nasdaq)
 'gold' - Gold Market
 'bitcoin' - Bitcoin Market
 'apr' - US Mortgage Rates
'''

#this function calls the specific dataframe depending on the market name and days of data required
def reviewTable(df_name,option):
    if(df_name == 'stock'):
        df=getNasdaqData()
        if(option == 1):
            return df.iloc[0,:].to_frame().transpose()
        if(option == 2):
            return df.iloc[0:15,:]
        if(option == 3):
            return df.iloc[0:30,:]
    if(df_name == 'gold'):
        df=getGoldData()
        if(option == 1):
            return df.iloc[0,:].to_frame().transpose()
        if(option == 2):
            return df.iloc[0:15,:]
        if(option == 3):
            return df.iloc[0:30,:]
    if(df_name == 'bitcoin'):
        df=getBitcoinData()
        if(option == 1):
            return df.iloc[0,:].to_frame().transpose()
        if(option == 2):
            return df.iloc[0:15,:]
        if(option == 3):
            return df.iloc[0:30,:]
    if(df_name == 'apr'):
        df=getAPRData()
        if(option == 1):
            return df.iloc[0,:].to_frame().transpose()
        if(option == 2):
            return df.iloc[0:15,:]
        if(option == 3):
            return df.iloc[0:30,:]


#-----------------------------------------------------------------------------------------------------

'''
Note - the dates may vary according to data since some prices may not be vailable for all days 
Ex. Saturday prices not available for nasdaq but avilable for covid data
options -
 1 - last 15 days visualization
 2 - last 30 days visualization
df_name is market name
 'stock' - Stock Market(Nasdaq)
 'gold' - Gold Market
 'bitcoin' - Bitcoin Market
 'apr' - US Mortgage Rates

'''

#this function calls the specific dataframe depending on the market name and days of data required
def visualization(df_merged , name , option):
    no_of_days = ""
    if(name == 'stock'):
        if(option == 1):
             df_nasdaq = df_merged.loc[0:14, ['Date' , 'positive' , 'recovered' , 'nasdaq_Close']]
             no_of_days = 15 
        if(option == 2):
             df_nasdaq = df_merged.loc[0:29, ['Date' , 'positive' , 'recovered' , 'nasdaq_Close']]
             no_of_days = 30
         
        # create figure and axis objects with subplots()
        fig,ax = plt.subplots(figsize=(20,10))
       
        # make a plot
        l1 = ax.plot(df_nasdaq["Date"], df_nasdaq["positive"], color="red", marker="o" , label = "Covid-19 Positive Cases")
        # set x-axis label
        ax.set_xlabel("Date",fontsize=14)
        # set y-axis label
        ax.set_ylabel("Positive Cases",color="red",fontsize=14)
        

        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        l2 = ax2.plot(df_nasdaq["Date"], df_nasdaq["nasdaq_Close"],color="blue",marker="o" , label = " NASDAQ Closing prices")
        ax2.set_ylabel("Nasdaq Close Price",color="blue",fontsize=14)
        
        leg = l1 + l2
        labs = [l.get_label() for l in leg]
        ax.legend(leg, labs, loc=0)
        
        plt.title("Impact of Covid-19 Positive Cases on NASDAQ Closing Prices ( " + str(no_of_days) + " days )")
        plt.show()

        
    if(name == 'gold'):
        if(option == 1):
             df_gold = df_merged.loc[0:14, ['Date' , 'positive' , 'recovered' , 'gold_Close']]
             no_of_days = 15 
        if(option == 2):
             df_gold = df_merged.loc[0:29, ['Date' , 'positive' , 'recovered' , 'gold_Close']]
             no_of_days = 30
        
        # create figure and axis objects with subplots()
        fig,ax = plt.subplots(figsize=(20,10))
       
        # make a plot
        l1 = ax.plot(df_gold["Date"], df_gold["positive"], color="red", marker="o" , label= "Covid-19 Positive Cases")
        # set x-axis label
        ax.set_xlabel("Date",fontsize=14)
        # set y-axis label
        ax.set_ylabel("Positive Cases",color="red",fontsize=14)
        

        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        l2 = ax2.plot(df_gold["Date"], df_gold["gold_Close"],color="blue",marker="o" , label = "Gold Closing Prices")
        ax2.set_ylabel("Gold Close Price",color="blue",fontsize=14)
        
        leg = l1 + l2
        labs = [l.get_label() for l in leg]
        ax.legend(leg, labs, loc=0)
        
        plt.title("Impact of Covid-19 Positive Cases on Gold Closing Prices ( " + str(no_of_days) + " days )")
        plt.show()

        
    if(name == 'bitcoin'):
        if(option == 1):
             df_bitcoin = df_merged.loc[0:14, ['Date' , 'positive' , 'recovered' , 'bitcoin_Close']]
             no_of_days = 15 
        if(option == 2):
             df_bitcoin = df_merged.loc[0:29, ['Date' , 'positive' , 'recovered' , 'bitcoin_Close']]
             no_of_days = 30


        # create figure and axis objects with subplots()
        fig,ax = plt.subplots(figsize=(20,10))

        # make a plot
        l1 = ax.plot(df_bitcoin["Date"], df_bitcoin["positive"], color="red", marker="o" , label = "Covid-19 Positive Cases")
        # set x-axis label
        ax.set_xlabel("Date",fontsize=14)
        # set y-axis label
        ax.set_ylabel("Positive Cases",color="red",fontsize=14)


        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        l2 = ax2.plot(df_bitcoin["Date"], df_bitcoin["bitcoin_Close"],color="blue",marker="o" , label = "Bitcoin Closing Prices")
        ax2.set_ylabel("Bitcoin Close Price",color="blue",fontsize=14)
        
        leg = l1 + l2
        labs = [l.get_label() for l in leg]
        ax.legend(leg, labs, loc=0)
        
        plt.title("Impact of Covid-19 Positive Cases on Bitcoin Closing Prices ( " + str(no_of_days) + " days )")
        plt.show()
        

    if(name == 'apr'):
        if(option == 1):
             df_apr = df_merged.loc[0:14, ['Date' , 'positive' , 'recovered' , 'Avg Mortgage APR']]
             no_of_days = 15   
        if(option == 2):
             df_apr = df_merged.loc[0:29, ['Date' , 'positive' , 'recovered' , 'Avg Mortgage APR']]
             no_of_days = 30 
 

        # create figure and axis objects with subplots()
        fig,ax = plt.subplots(figsize=(20,10))

        # make a plot
        l1 = ax.plot(df_apr["Date"], df_apr["positive"], color="red", marker="o" , label = "Covid-19 Positive Cases")
        # set x-axis label
        ax.set_xlabel("Date",fontsize=14)
        # set y-axis label
        ax.set_ylabel("Positive Cases",color="red",fontsize=14)


        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        l2 = ax2.plot(df_apr["Date"], df_apr["Avg Mortgage APR"],color="blue",marker="o" , label = "Average Mortage Rate")
        ax2.set_ylabel("Avg Mortgage APR",color="blue",fontsize=14)
        
        leg = l1 + l2
        labs = [l.get_label() for l in leg]
        ax.legend(leg, labs, loc=0)
        
        plt.title("Impact of Covid-19 Positive Cases on Avg Mortgage APR ( " + str(no_of_days) + " days )" )
        plt.show()

#-------------------------------------------------------------------------------

# function for trend analysis

def marketTrends(df_merged):
    
#     fig,ax = plt.subplots(figsize=(20,10))
    fig, (ax1, ax2 , ax3 , ax4) = plt.subplots(4 , figsize=(20,10))
    fig.suptitle("Comparative Study of trends of all Markets")

    
    # make a plot
    ax1.plot(df_merged["Date"], df_merged["nasdaq_Close"], color="red", marker="o")
    # set x-axis label
    ax1.set_xlabel("Date",fontsize=14)
    # set y-axis label
    ax1.set_ylabel("NASDAQ Closing Price",color="red",fontsize=10)
    
    
    # make a plot
    ax2.plot(df_merged["Date"], -(df_merged["gold_Close"]), color="blue", marker="o")
    # set x-axis label
    ax2.set_xlabel("Date",fontsize=14)
    # set y-axis label
    ax2.set_ylabel("Gold Closing Price",color="blue",fontsize=10)
    
    
    # make a plot
    ax3.plot(df_merged["Date"], -(df_merged["bitcoin_Close"]), color="green", marker="o")
    # set x-axis label
    ax3.set_xlabel("Date",fontsize=14)
    # set y-axis label
    ax3.set_ylabel("Bitcoin Closing Price",color="green",fontsize=10)
    
    
    # make a plot
    ax4.plot(df_merged["Date"], -(df_merged["Avg Mortgage APR"]), color="orange", marker="o")
    # set x-axis label
    ax4.set_xlabel("Date",fontsize=14)
    # set y-axis label
    ax4.set_ylabel("Average Mortage Rate",color="orange",fontsize=10)
    plt.show()
    

#this function generates predicted values for various markets based on covid numbers
def getPredictedValue(df,p_cases,mkt_name):
#     calculating hospitalised ratio,recovered ratio and death ratio 
    curr_pos_ratio=df.hospitalizedCurrently.sum()/df.positive.sum()
    rec_pos_ratio=df.recovered.sum()/df.positive.sum()
    death_pos_ratio=df.death.sum()/df.positive.sum()
    #input vector for the model
    input=[p_cases,p_cases*curr_pos_ratio,p_cases*rec_pos_ratio,p_cases*death_pos_ratio]
    df_input=pd.DataFrame(input)
    #covid dataframe extracted from the merged dataframe
    df_covid=df.iloc[:,[1,2,4,5]]
    #generating model
    model=RandomForestRegressor(random_state=0)
    #based on market, the model is trained and value is predicted
    if(mkt_name=='stock'):
        df_stock=df.nasdaq_Close.to_frame()
        model.fit(df_covid,df_stock)
        prediction=model.predict([input])
        return np.round(prediction,1)[0]
    if(mkt_name=='gold'):
        df_gold=df.gold_Close.to_frame()
        model.fit(df_covid,df_gold)
        prediction=model.predict([input])
        return np.round(prediction,1)[0]
    if(mkt_name=='bitcoin'):
        df_bitcoin=df.bitcoin_Close.to_frame()
        model.fit(df_covid,df_bitcoin)
        prediction=model.predict([input])
        return np.round(prediction,1)[0]
    if(mkt_name=='apr'):
        df_apr=df.iloc[:,7].to_frame()
        model.fit(df_covid,df_apr)
        prediction=model.predict([input])
        return prediction[0]