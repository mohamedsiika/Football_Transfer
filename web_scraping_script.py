
import pandas as pd
import requests
import numpy as np
import html5lib
import random
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
#url='https://www.transfermarkt.com/transfers/transfertagedetail/statistik/top/land_id_ab//land_id_zu//leihe//datum/2022-09-12/plus/1/galerie/0/page/1'

def page_num(soup):
    pages_num = soup.find_all('a', attrs={'class': 'tm-pagination__link'})
    if pages_num != []:
        x = str(pages_num[-1]).split(')">', 1)[0]
        num = int(x.split()[-1])
        return num
    else:
        return 1

def get_market_days():
    market_start=datetime(2022,6,30).date()
    today=datetime(2022,9,30).date()
    dif=(today-market_start).days
    days=[]
    for i in range(1,dif):
        days.append(str(today-dt.timedelta(i)))
    return(days)

def get_players_names(table):
    names=[]
    players=table.find_all('img',attrs={'class':"bilderrahmen-fixed lazy lazy"})
    for row in players:
        names.append(str(str(row).split('" class',1)[0].split('<img alt="',1)[1]))
    return names

def get_players_details(table):
    nationality=[]
    age=[]
    position=[]

    ages=table.find_all('td',attrs={'class':'zentriert'})
    for i in range(0, len(ages), 2):
        age.append(str(ages[i]).split('>', 1)[1].split('<', 1)[0])
        nat = ages[i + 1].find_all('img', attrs={'class': 'flaggenrahmen'})

        temp = (str(nat[0]).split('alt="', 1)[1].split('" class', 1)[0])
        nationality.append(temp)

    pos=[i.find_all('td')[-1] for i in table.find_all('table',attrs={'class':'inline-table'})]
    for i in range(0,len(pos),3):
        position.append(str(pos[i]).split('>',1)[1].split('<',1)[0])

    return nationality,age,position

def get_clubs_information(table):


    from_club=[]
    from_league=[]
    from_country=[]

    to_club=[]
    to_league=[]
    to_country=[]
    #the inline table contains the data of the clubs 
    info=table.find_all('table',attrs={'class':'inline-table'})

    from_info=[]
    to_info=[]
    # the info is divided into 3 inline tables the first for the players and we will ignore it the second is the from_info and the third is the to_info
    for i in range(1,len(info),3):
            #the from Data is divided into 2 tr one for the club and the other for the league and the country 
            for j in info[i].find_all('tr'):
                    z=j.find_all('td')[0]
                    if z.find_all('a')==[]  :
                            from_info.append('unknown_league')
                            continue
                    from_info.append(str(z).split('href="/',1)[1].split('/',1)[0])
            if z.find_all('img')==[] :
                    from_country.append("unknown_country")
            else:
                    from_country.append(str(z.find_all('img',attrs={'class':'flaggenrahmen'})[0]).split('alt="',1)[1].split('"',1)[0])

            #the to Data is divided into 2 tr one for the club and the other for the league and the country 

            for j in info[i+1].find_all('tr'):
                    z=j.find_all('td')[0]
                    if z.find_all('a')==[] :
                            to_info.append('unknown_league')
                            continue
                    to_info.append(str(z).split('href="/',1)[1].split('/',1)[0])
            if z.find_all('img')==[] :
                    to_country.append("unknown_country")
            else:
                    to_country.append(str(z.find('img',attrs={'class':'flaggenrahmen'})).split('alt="',1)[1].split('"',1)[0])

    #arrange everything 

    for i in range(0,len(from_info),2):
            from_club.append(from_info[i])
            from_league.append(from_info[i+1])
    for i in range(0,len(to_info),2):
            to_club.append(to_info[i])
            to_league.append(to_info[i+1])

    return from_club,from_league,from_country,to_club,to_league,to_country

def get_money_information(table):
    market_value=[]
    fee=[]

    money=table.find_all('td',attrs={'class':["rechts"]})
    for i in range(0,len(money),2):
        market_value.append(str(money[i]).split('>',1)[1].split('<',1)[0])
        fee.append(str(money[i+1]).split('>',2)[2].split('<',1)[0])
    return market_value,fee

if __name__=='__main__':
    days=get_market_days()
    names,nationalities,ages,positions,from_club,from_league,from_country,to_club,to_league,to_country,market_values,fees=np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object'),np.array([],dtype='object')

    for i in range(len(days)):


        url='https://www.transfermarkt.com/transfers/transfertagedetail/statistik/top/land_id_ab//land_id_zu//leihe//datum/'+days[i]+'/plus/1/galerie/0/page/1'
        r=requests.get(url,headers=headers)
        soup=BeautifulSoup(r.content,'html5lib')

        pages=page_num(soup)
        for j in range(pages):

            url = 'https://www.transfermarkt.com/transfers/transfertagedetail/statistik/top/land_id_ab//land_id_zu//leihe//datum/' + days[i] + '/plus/1/galerie/0/page/'+str(j+1)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html5lib')

            table=soup.find('table',attrs={'class':'items'})
            names=np.append(names,get_players_names(table))

            details=get_players_details(table)
            nationalities,ages,positions=np.append(nationalities,details[0]),np.append(ages,details[1]),np.append(positions,details[2])

            clubs=get_clubs_information(table)
            from_club,from_league,from_country,to_club,to_league,to_country=np.append(from_club,clubs[0]),np.append(from_league,clubs[1]),np.append(from_country,clubs[2]),np.append(to_club,clubs[3]),np.append(to_league,clubs[4]),np.append(to_country,clubs[5])

            money=get_money_information(table)
            market_values,fees=np.append(market_values,money[0]),np.append(fees,money[1])
            print('day',days[i],"page",j+1,'Done')
        print(names.shape,ages.shape,positions.shape,nationalities.shape,from_club.shape,from_league.shape,from_country.shape,to_club.shape,to_league.shape,to_country.shape,market_values.shape,fees.shape)

        print(days[i], "table Extracted successfully")

    data={'name':names,'age':ages,'positions':positions,'nationality':nationalities,'from_club':from_club,'from_league':from_league,'from_country':from_country,'to_club':to_club,'to_league':to_league,'to_country':to_country,'market_value':market_values,'transfer_value':fees}
    df=pd.DataFrame(data)
    print(df)
    df.to_excel("summer_transfer_window_2022.xlsx")





