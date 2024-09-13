import random
from ConnectDB import Connect
import requests
from bs4 import BeautifulSoup

def InsertPlayers():
    
    url = "https://liquipedia.net/dota2/api.php?action=parse&page=Players_(all)&format=json"
    headers = {
        "USER_AGENT": "TourneyHub/1.0 (sasha.chernukha20021901@mail.ru)",
        "Accept-Encoding": "gzip"
    }
    response = requests.get(url, headers=headers)
    tolkoText = response.json()
    soup = BeautifulSoup(tolkoText['parse']['text']['*'], 'lxml')
    All_Players = {}
    countries = []
    i = 0
    for h3 in soup.find_all('h3'):
        countries.append(h3.a['title'])
        i+=1
    i = 0
    for cels in soup.find_all('table'):
        players_list = []
        for rows in cels.find_all('tr')[2:]:
            b = rows.find('td')
            t = b.a.get('title')                                         
            players_list.append(t)
        All_Players[i] = {"Country": countries[i], "Players": players_list}
        i+=1  
    
    conn = Connect()
    if (conn):
        for key in All_Players:
            Country = All_Players[key]['Country']
            for nickname in All_Players[key]['Players']:
                nick = nickname
                with conn.cursor() as cursor:
                    curr_query = "INSERT INTO `tourneyhub_db`.`players` " \
                        "(`Nickname`, `Game`,`Country`) VALUES " \
                        f'("{nick}", "Dota 2", "{Country}");'
                    cursor.execute(curr_query)
                    conn.commit()
        return "Работает!!!"
    else:
        return "Ошибка!"
    
def InsertTeams():

    url = "https://liquipedia.net/dota2/api.php?action=parse&page=Portal:Teams&format=json"
    headers = {
        "USER_AGENT": "TourneyHub/1.0 (sasha.chernukha20021901@mail.ru)",
        "Accept-Encoding": "gzip"
    }
    response = requests.get(url, headers=headers)
    tolkoText = response.json()
    soup = BeautifulSoup(tolkoText['parse']['text']['*'], 'lxml')
    All_Teams = {}
    countries = []
    i = 0
    for h3 in soup.find_all('h3')[:7]:
        countries.append(h3.span['id'])
        i+=1
    
    i = 0
    for cels in soup.find_all('div',attrs={"class":"panel-box-body"})[:7]:
        teams_list = []
        for rows in cels.find_all('span',attrs={"class":"team-template-text"}):
            t = rows.a.get('title')                                       
            teams_list.append(t)
        All_Teams[i] = {"Region": countries[i], "Teams": teams_list}
        i+=1
    conn = Connect()
    if (conn):
        for key in All_Teams:
            reg = All_Teams[key]['Region']
            for names in All_Teams[key]['Teams']:
                Tn = names
                with conn.cursor() as cursor:
                    curr_query = "INSERT INTO `tourneyhub_db`.`teams` " \
                        "(`TeamName`, `Region`, `Game`) VALUES " \
                        f'("{Tn}", "{reg}", "Dota 2");'
                    cursor.execute(curr_query)
                    conn.commit()
        return "Работает!!!"
    else:
        return "Ошибка!"

def InsertTournaments():
        
    url = "https://liquipedia.net/dota2/api.php?action=parse&page=Portal:Tournaments&format=json"
    headers = {
        "USER_AGENT": "TourneyHub/1.0 (sasha.chernukha20021901@mail.ru)",
        "Accept-Encoding": "gzip"
    }
    response = requests.get(url, headers=headers)
    tolkoText = response.json()
    soup = BeautifulSoup(tolkoText['parse']['text']['*'], 'lxml')
    All_Tournaments = {}
    status = []
    i = 0
    for h3 in soup.find_all('h3'):
        m = h3.find('span')
        status.append(m.text)
        i+=1
    i = 0
    for cels in soup.find_all('div',attrs={"class": "gridTable"}):
        tournaments_list = {}
        j = 0
        for rows in cels.find_all('div', attrs={"class":"gridRow"}):

            Tn = rows.find('div', attrs={"class":"gridCell Tournament Header"}) # Title
            Tour = Tn.find_all('a')
            if len(Tour) > 1:
                for ash in Tour:
                    Tour_Title = ash.text
            else:
                Tour = Tn.find('a')
                Tour_Title = Tour.text
            
            Tn = rows.find('div', attrs={"class":"gridCell EventDetails Date Header"}) # Date
            Tour_Date = Tn.text

            Tn = rows.find('div', attrs={"class":"gridCell EventDetails Location Header"}) # Location
            TL = Tn.text
            Tl1 = TL.split()
            Tour_Loc = Tl1[0]

            tournaments_list[j] = {'Title': Tour_Title, 'date': Tour_Date, 'location': Tour_Loc}
            j += 1
        All_Tournaments[i] = {"Status": status[i], "Tournaments": tournaments_list}
        i+=1
        
    conn = Connect()
    if (conn):
        for key in All_Tournaments:
            Stat = All_Tournaments[key]['Status']
            for i in All_Tournaments[key]['Tournaments']:
                titles = All_Tournaments[key]['Tournaments'][i]['Title']
                dates = All_Tournaments[key]['Tournaments'][i]['date']
                loc = All_Tournaments[key]['Tournaments'][i]['location']   
                with conn.cursor() as cursor:
                    curr_query = "INSERT INTO `tourneyhub_db`.`tournaments` " \
                        "(`Name`, `Game`, `Location`, `Date`, `Status`) VALUES " \
                        f'("{titles}", "Dota 2", "{loc}", "{dates}", "{Stat}");'
                    cursor.execute(curr_query)
                    conn.commit()
        return "Работает!!!"
    else:
        return "Ошибка!"




    
