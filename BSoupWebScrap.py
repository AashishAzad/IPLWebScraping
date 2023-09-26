import requests
import pandas as pd
from bs4 import BeautifulSoup


def getDataFrame(tableTag):
    title = tableTag.find_all("th")
    headers = []
    for i in title:
        headers.append(i.text)

    df = pd.DataFrame(columns=headers)
    rows = tableTag.find_all("tr")
    for i in rows[1:]:
        first_td = i.find_all("td")[0].find("div", class_="ih-pt-ic").text.strip()
        data = i.find_all("td")[1:]
        row = [tr.text for tr in data]
        row.insert(0, first_td)
        df.loc[len(df)] = row

    return df


url = "https://www.iplt20.com/auction/2022#:~:text=TATA%20IPL%20Auction%20%2D%202022,IPL)%202022%20Auction%20in%20Bengaluru."
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

table = soup.find_all("table", class_="ih-td-tab auction-tbl")
auctionDetailTable = getDataFrame(table[0])
buyTable = getDataFrame(table[1])
completeTable = pd.merge(auctionDetailTable, buyTable, on='TEAM', how='inner')
completeTable.to_csv("Complete Auction Table 2022.csv", index=False)
