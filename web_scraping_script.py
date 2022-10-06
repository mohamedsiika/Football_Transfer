from turtle import position
import pandas as pd
import requests
import html5lib
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as dt
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
#url='https://www.transfermarkt.com/transfers/transfertagedetail/statistik/top/land_id_ab//land_id_zu//leihe//datum/2022-09-12/plus/1/galerie/0/page/1'

def get_market_days():
    market_start=datetime(2022,7,1).date()
    today=datetime.now().date()
    dif=(today-market_start).days
    print(dif)
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
    for i in range(0,len(ages),2):
        age.append(str(ages[i]).split('>',1)[1].split('<',1)[0])
        nat=ages[i+1].find_all('img',attrs={'class':'flaggenrahmen'})
        temp=[]
        for j in nat:
                temp.append(str(j).split('alt="',1)[1].split('" class',1)[0])
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
    for i in range(len(days)):
        url='https://www.transfermarkt.com/transfers/transfertagedetail/statistik/top/land_id_ab//land_id_zu//leihe//datum/'+days[i]+'/plus/1/galerie/0/page/1'
        r=requests.get(url,headers=headers)
        soup=BeautifulSoup(r.content,'html5lib')
        table=soup.find('table',attrs={'class':'items'})
        names=get_players_names(table)
        nationalities,ages,positions=get_players_details(table)
        from_club,from_league,from_country,to_club,to_league,to_country=get_clubs_information(table)
        market_values,fees=get_money_information(table)
        print(names)





