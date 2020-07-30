from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

import pandas as pd
import numpy as np

#function started
def scarp_site():
	#created dataframe to store columns and rows
	df = pd.DataFrame(columns=['Stocks', 'Ticker Symbol', 'Company Name'])

	#url from where I have fetch the most active,gainer and losers data
	my_url='https://money.cnn.com/data/hotstocks/ '

	#opening up connection and grabbing the page
	uClient=uReq(my_url)

	#upload the content into variable
	page_html=uClient.read()

	#connection close
	uClient.close()

	#html parse
	page_soup=soup(page_html,"html.parser")

    #this id will fetch the html content for most active,gainer and loosers
	first=page_soup.findAll("div",{"id":"wsod_hotStocks"})

    #this is category list that holds the most active,gainer etc
	category = ['Most Active', 'Gainers', 'Losers']

	#this for loop will run from 0-2 that is from most active till losers
	for j in range (0, len(first)):

		#storing the first index in variable
		fst=first[j]


		for fst in first:

			#from this it will grab the company from most active category
			second=page_soup.findAll("table",{"class":"wsod_dataTable wsod_dataTableBigAlt"})

			for i in range(len(second)):
				# print(cat[i])

				#creating the list for ticker,company and stock
				ticker = []
				company = []
				stock = []

                #this loop will give us the company name and ticker symbol for that company
				for row in second[i].findAll("td"):
					
                    #use try catch to continue searching
					try:
						# print(row)
						linkName=row.find("a").text
						text=row.find("span").text
						# print(linkName," ",text)
						ticker.append(linkName)
						company.append(text)
						stock.append(category[i])
					except:
						print(end="")

				# print(ticker, company, stock)

				#created dataframe and passed data to column in dataframe
				temp = pd.DataFrame({'Stocks': stock, 'Ticker Symbol': ticker, 'Company Name':company})
			
				df = df.append(temp, ignore_index=True)
	
	
	for name, data in df.groupby('Stocks', sort=False):
        
		print(name)
		print(data[['Ticker Symbol', 'Company Name']])

	
	#asking user to input the name of the stock
	stockName = (input("Enter stock name :- "))

    #checking if the user is entering the correct stock name from the given category
	if not stockName in category:
		print('This stock name is not in the category')
		print(category)
		stockName = (input("Enter stock name :- "))
		if not stockName in category:
			print('Again you have entered the wrong stock name....')
			exit(0)

    #asking the user to enter the ticker symbol for the company
	tickerSymbol = (input("Enter company ticker symbol :- "))

	#FILTER THE DATA BY STOCK NAME AND CREATE THE LIST OF ALL TICKER SYMBOL  THEN
  	#CHECK WHETHER THE PROVIDED TICKER SYMBOL IS PRESENT IN  THAT LIST OR NOT
	if not tickerSymbol in df['Ticker Symbol'][df['Stocks']==stockName].values:

		print('The company you enter do not belong to entered category')
		print(df['Ticker Symbol'][df['Stocks']==stockName].values)
		tickerSymbol = (input("Enter company ticker symbol :- "))
		if not tickerSymbol in df['Ticker Symbol'][df['Stocks']==stockName].values:
			print('Again you have enterd wrong ticker symbol....')
			exit(0)
     
    #this will return the index where stockname and ticker symbol will match 
	index = np.where((df['Stocks']==stockName) & (df['Ticker Symbol']==tickerSymbol))[0][0]
	print('The data for {} {} is the following:'.format(tickerSymbol, df['Company Name'].iloc[index]))
	print('{} {}'.format(tickerSymbol, df['Company Name'].iloc[index]))
	
	
	#CREATED DF WITH PROVIDED STOCK NAME,TICKER NAME AND THEIR RESP COMPANY NAME
 
	data = pd.DataFrame({'Stock': stockName, 'Ticker Name': tickerSymbol, \
			'Company Name': df['Company Name'].iloc[index]}, index=[0]) 
    
    #url that will return the open price etc
	my_url1="https://money.cnn.com/quote/quote.html?symb="+tickerSymbol+""
	# print(my_url1)

	uClient1=uReq(my_url1)

	page_html1=uClient1.read()

	uClient1.close()

	page_soup1=soup(page_html1,"html.parser")

	#first1=page_soup1.findAll("div",{"id":"wsod_newsAndPressReleaseContainer"})

	second1=page_soup1.find("table",{"class":"wsod_dataTable wsod_dataTableBig"})

	info = ["Today’s open", "Previous close", "Volume", "Market cap"]

	for row in second1.findAll("tr"):
        #this will store the label like previous close
		label=row.find("td").text

		#this will give the price for each label
		value=row.find("td",{"class":"wsod_quoteDataPoint"}).text

		if label in info:
			# data.insert(len(data.columns.tolist()), label, value, True)
			# data.insert(len(data.columns.values), label, value, True)
			data.insert(data.columns.shape[0], label, value, True)

	print(data)
	data.to_csv('Stock.csv', index=False)

def main():
	scarp_site()

if __name__ == '__main__':
	main()





