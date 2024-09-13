import random
from rss_parser import RSSParser
from requests import get  
from ConnectDB import Connect,ConnectSocial
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def GivePostText(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    s = soup.find("div", {"class": "content_5HuK5"})
    texts = s.find_all("p",{"class": "paragraph_+1D2F"})
    f = []
    f.insert(0,texts[0].text)
    final_text = ''
    for p in texts:
        final_text += p.text + "\n\n"

    f.insert(1,final_text)    
    return f
    
def Parser():
    
    # Получение и форматирование rss данных в rss_data
    rss_url = "https://www.cybersport.ru/rss/materials"
    response = get(rss_url)
    rss = RSSParser.parse(response.text)
    last_topic = ''
    rss_data = []
    for item in rss.channel.items:
        rssT = item.title[:200]
        rssDescr = item.description[:200]
        rssImg = item.enclosure.attributes['url']
        rssPubDate = item.pub_date.content
        link = item.link.content
        linkSource = item.link.content[12:25]
        rss_data.append({"Title": rssT, "Description": rssDescr, "ImgSrc": rssImg , "PubDate": rssPubDate, "LinkOrig": link, "Source": linkSource})
    # Получение и форматирование rss данных в rss_data
    
    # Обновление постов в бд
    rss_last = rss_data[0]["Title"]     
    conn = ConnectSocial()
    with conn.cursor() as cursor: 
        curr_query = "SELECT * FROM posts ORDER BY idPost DESC LIMIT 1"  
        cursor.execute(curr_query)
        posts = cursor.fetchall()
        post_last = posts[0]["Title"]
        if (post_last != rss_last):       
            post_text = GivePostText(rss_data[0]['LinkOrig'])
            curr_query = f"INSERT INTO posts (`Title`, `Description`, `Text`, `ImgSrc`,`PubDate`) VALUES ('{rss_data[0]['Title']}', '{post_text[0][:144]}...' ,'{post_text[1]}', '{rss_data[0]['ImgSrc']}','{rss_data[0]['PubDate']}');"
            cursor.execute(curr_query)
            conn.commit()
            print ("Появились новости! Записываю...")
        else:
            print ("Новые новости не появились")        
    # Обновление постов в бд
   
def LiveMatches():

    url = "https://www.cybersport.ru/matches"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pr = soup.find('div',{'class': 'root_Ts3Rx'})
    f = pr.find_all('div',{'class': 'item_uto6z'})
    h = []
    for items in f:
        m = items.find('div',{'class': 'date_Qyw+T'})
        stat = len(m.text)
        if (stat == 7):
            gm = 'Dota 2'
        elif (stat == 4):
            gm = 'Cs 2'
        else:
            gm = 'Unknown'
        m = items.find('div',{'class': 'participant1_xWFn2'})
        team1 = m.text
        m = items.find('div',{'class': 'participant2_P9p5D'})
        team2 = m.text
        m = items.find('div',{'class': 'score_+pSbU'})
        score1 = m.text[0:1]
        score2 = m.text[2:3]
        secret = f'{team1}vs{team2}'
        h.append({'Status': 'Live', 'Team1': team1, 'Score1': score1, 'Score2': score2, 'Team2': team2, 'Game': gm , 'Secret': secret})
    
    conn = Connect()   # Добавление в бд с проверкой если уже добавили
    with conn.cursor() as cursor:
        for matches in h:
            m = matches['Secret']
            curr_query = f"SELECT * FROM matches WHERE MatchCode = '{m}' AND Status = 'Live'"
            cursor.execute(curr_query)
            pr = cursor.rowcount
            if (pr >= 1):
                pass
            else:
                curr_query = f"INSERT INTO matches (`Status`, `FirstTeam`, `FirstTeamScore`, `SecondTeamScore`, `SecondTeam`, `Game`, `MatchCode`) VALUES ('{matches['Status']}', '{matches['Team1']}', '{matches['Score1']}', '{matches['Score2']}', '{matches['Team2']}', '{matches['Game']}', '{matches['Secret']}');"
                cursor.execute(curr_query)
                conn.commit()

    conn = Connect() # Обновление данных в бд
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM matches WHERE Status = 'Live'"
        cursor.execute(curr_query) 
        pr = cursor.fetchall()
        for bdmatches in pr:
            
            i = 0
            for matches in h: 
                if (bdmatches['MatchCode'] == matches['Secret']):
                    if (bdmatches['FirstTeamScore'] != matches['Score1'] or  bdmatches['SecondTeamScore'] != matches['Score2']):
                        m1 = matches['Score1']
                        m2 = matches['Score2']
                        curr_query = f"UPDATE matches SET FirstTeamScore = '{m1}', SecondTeamScore = '{m2}' WHERE idMatch = '{bdmatches['idMatch']}';"
                        cursor.execute(curr_query)
                        conn.commit()
                    i += 1
                    
            if ( i >= 1 ):
                print(f"Матч {bdmatches['FirstTeam']} vs {bdmatches['SecondTeam']} еще идет!")
            else:
                curr_query = f"UPDATE matches SET Status = 'Ended', `MatchCode` = '-' WHERE idMatch = '{bdmatches['idMatch']}';"
                cursor.execute(curr_query)
                conn.commit()

