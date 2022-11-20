from bs4 import BeautifulSoup
import requests
import pandas as pd



url = "https://www.coinbase.com/es/price?resolution=hour"
r=requests.get(url)
url=r.content
soup = BeautifulSoup(url,'html.parser')


""" txtfile = open("text.txt", "w")
txtfile.write(data)
txtfile.close() """

tables = soup.find_all('table', class_ = 'AssetTable__Table-sc-1hzgxt1-1 kWFqyT')

""" tab = soup.find("table",{"class":"AssetTable__Table-sc-1hzgxt1-1 kWFqyT jquery-tablesorter"}) """

print(tables)




