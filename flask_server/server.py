import httplib2
import os
import json
import random
import time
import sys
import lxml
import requests
import urllib
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Manager, Value
from flask import Flask, render_template, url_for, session
from pprint import pprint
from operator import itemgetter

profile_list = ['levelFrame', 'playtime_quick', 'playtime_competitive', 'avatar', 'username', 'star', 'level', 'games_quick_wins', 'games_competitive_played', 'games_competitive_lost', 'games_competitive_wins', 'competitive_rank_img', 'competitive_rank']
quick_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadsDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'ReconAssists']
competitive_allheros_list = ['MeleeFinalBlows', 'SoloKills', 'ObjectiveKills', 'FinalBlows', 'DamageDone', 'Eliminations', 'EnvironmentalKills', 'Multikills', 'HealingDone', 'TeleporterPadDestroyed', 'Eliminations-MostinGame', 'FinalBlows-MostinGame', 'DamageDone-MostinGame', 'HealingDone-MostinGame', 'DefensiveAssists-MostinGame', 'OffensiveAssists-MostinGame', 'ObjectiveKills-MostinGame', 'ObjectiveTime-MostinGame', 'Multikill-Best', 'SoloKills-MostinGame', 'TimeSpentonFire-MostinGame', 'MeleeFinalBlows-Average', 'TimeSpentonFire-Average', 'SoloKills-Average', 'ObjectiveTime-Average', 'ObjectiveKills-Average', 'HealingDone-Average', 'FinalBlows-Average', 'Deaths-Average', 'DamageDone-Average', 'Eliminations-Average', 'Deaths', 'EnvironmentalDeaths', 'Cards', 'Medals', 'Medals-Gold', 'Medals-Silver', 'Medals-Bronze', 'GamesWon', 'TimeSpentonFire', 'ObjectiveTime', 'TimePlayed', 'MeleeFinalBlows-MostinGame', 'DefensiveAssists', 'DefensiveAssists-Average', 'OffensiveAssists', 'OffensiveAssists-Average', 'GamesPlayed', 'GamesTied', 'GamesLost']
achievements_list = ['name', 'finished', 'image', 'description', 'category']
hero_list = ['Ana', 'Bastion', 'DVa', 'Genji', 'Hanzo', 'Junkrat', 'Lucio', 'Mccree', 'Mei', 'Mercy', 'Pharah', 'Reaper', 'Reinhardt', 'Roadhog', 'Soldier76', 'Symmetra', 'Torbjoern', 'Tracer', 'Widowmaker', 'Winston', 'Zarya', 'Zenyatta']
profiles = {}
quick_heroses = {}
cookies = {}
hero_datas = {}
scores = {}
achievs = {}
user_no = 1
background_count = 7
request_count = 0

images = [{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000029.png','name':'Genji'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000042.png','name':'McCree'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000002.png','name':'Reaper'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E000000000006E.png','name':'Soldier:76'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000007.png','name':'Reinhardt',},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000005.png','name':'Hanzo',},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000003.png','name':'Tracer'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000079.png','name':'L&#xFA;cio'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000040.png','name':'Roadhog'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000009.png','name':'Winston'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000065.png','name':'Junkrat'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E000000000013B.png','name':'Ana'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000004.png','name':'Mercy'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000008.png','name':'Pharah'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E00000000000DD.png','name':'Mei'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000068.png','name':'Zarya'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000006.png','name':'Torbj&#xF6;rn'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E000000000000A.png','name':'Widowmaker'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E000000000007A.png','name':'D.Va'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000020.png','name':'Zenyatta'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000015.png','name':'Bastion'},{'image':'https://blzgdapipro-a.akamaihd.net/game/heroes/small/0x02E0000000000016.png','name':'Symmetra'}]
server_domain = '0.0.0.0'
server_port = 5000

app = Flask(__name__)
app.secret_key = 'this isssssssssssss secret!'



def get_youtube_content():
	html = requests.get('https://www.youtube.com/results?search_query=LW+nanohana+%EB%A7%A4%EB%93%9C%EB%AC%B4%EB%B9%84')
	soup = BeautifulSoup(html.text, 'lxml')
	results = soup.find_all('a', {'class':'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 spf-link '}, href=True)
	lists = ''
	data = ''
	youtube_list = str('')
	for link in results:
		lists += (link['href'])
		results_list = lists.split('/watch?v=')

	a = results_list[1:]

	for i in range(0,3):
		youtube_list += ("<iframe width='260' height='260' src='https://www.youtube.com/embed/%s' frameborder='0' allowfullscreen></iframe>" % a[random.randrange(0,19)])
		youtube_list += ','
	final_results = youtube_list.split(',')
	return final_results[:3]


def api_origin_profile(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/profile'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        dic = {}
        dic['levelFrame'] = j['data']['levelFrame']
        dic['playtime_quick'] = j['data']['playtime']['quick']
        dic['playtime_competitive'] = j['data']['playtime']['competitive']
        dic['avatar'] = j['data']['avatar']
        dic['username'] = j['data']['username']
        dic['star'] = j['data']['star']
        dic['level'] = str(j['data']['level'])
        dic['games_quick_wins'] = j['data']['games']['quick']['wins']
        dic['games_competitive_played'] = j['data']['games']['competitive']['played']
        dic['games_competitive_lost'] = j['data']['games']['competitive']['lost']
        dic['games_competitive_wins'] = j['data']['games']['competitive']['wins']
        dic['competitive_rank_img'] = j['data']['competitive']['rank_img']
        dic['competitive_rank'] = j['data']['competitive']['rank']
        return j
    except:
        return False

def api_profile(name,d,count,ident):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/profile'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        dic = {}
        dic['levelFrame'] = j['data']['levelFrame']
        dic['playtime_quick'] = j['data']['playtime']['quick']
        dic['playtime_competitive'] = j['data']['playtime']['competitive']
        dic['avatar'] = j['data']['avatar']
        dic['username'] = j['data']['username']
        dic['star'] = j['data']['star']
        dic['level'] = str(j['data']['level'])
        dic['games_quick_wins'] = j['data']['games']['quick']['wins']
        dic['games_competitive_played'] = j['data']['games']['competitive']['played']
        dic['games_competitive_lost'] = j['data']['games']['competitive']['lost']
        dic['games_competitive_wins'] = j['data']['games']['competitive']['wins']
        dic['competitive_rank_img'] = j['data']['competitive']['rank_img']
        dic['competitive_rank'] = j['data']['competitive']['rank']
        d[ident] = j
        count.value += 1
        return True
    except:
        return False

def api_achievements(name):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/achievements'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j['achievements']
    except:
        pass

def api_quick_heros(name,d,count,ident):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/quickplay/heroes'%(name), 'GET')
        j = json.loads(content.decode('utf-8'))
        d[ident] = j
        count.value += 1
        return True
    except:
        return False

def api_quick_hero(name, hero, d,count):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive/hero/%s/'%(name,hero), 'GET')
        j = json.loads(content.decode('utf-8'))
        d[hero] = j
        count.value += 1
        return True
    except:
        return False

def api_competitive_hero(name, hero):
    try:
        h = httplib2.Http('.cache', disable_ssl_certificate_validation=True)
        resp, content = h.request('https://api.lootbox.eu/pc/kr/%s/competitive/hero/%s/'%(name,hero), 'GET')
        j = json.loads(content.decode('utf-8'))
        return j
    except:
        pass

@app.before_request
def before_request():
    try:
        global user_no
        if 'session' in session and 'user-id' in session:
            pass
        else:
            session['session'] = os.urandom(32)
            session['username'] = 'user' + str(user_no)
            user_no += 1
    except:
        pass

@app.route('/')
def chatting():
#    try:
        return render_template('index.html',random=random.randint(1,background_count),video_list=get_youtube_content())
#    except:
#        pass

@app.route('/info/<name>/')
def info(name):
    global request_count
    request_count += 1
    print(request_count)
    #try:
    if True:
        name = name.replace('#','-')
        if cookies.get(name) != None and (time.time() - cookies.get(name)) < 3600:
            profile = profiles[name]
            quick_heros = quick_heroses[name]
            d = hero_datas[name]
            top_hero = scores[name]
            achiev = achievs[name]
        else:
            # Multi Processing...
            manager = Manager()
            d = manager.dict()
            count = Value('i',0)
            p = {}
            p[1] = Process(target=api_profile,args=(name,d,count,'1'))
            p[2] = Process(target=api_quick_heros,args=(name,d,count,'2'))
            p[1].start()
            p[2].start()
            p[1].join()
            p[2].join()
            profiles[name] = d['1']
            quick_heroses[name] = d['2']
            d.pop('1')
            d.pop('2')
            for h in hero_list:
                p[h] = Process(target=api_quick_hero,args=(name,h,d,count))
                p[h].start()
            for h in hero_list:
                p[h].join()
            # Multi Processing End...

            profile = profiles[name]
            quick_heros = quick_heroses[name]
            if profile == False:
                return "<html><head><script>alert('no username');document.location='/'</script></head><body></body></html>"
            cookies[name] = time.time()
            hero_datas[name] = d
            scores[name] = {}
            achiev = api_achievements(name)
            achievs[name] = achiev
            for h in hero_list:
                score = 0
                try:
                    score += float(d[h][h]['DamageDone-Average'].replace(',',''))
                except:
                    pass
                try:
                    score += float(d[h][h]['Eliminations-Average'].replace(',',''))
                except:
                    pass
                try:
                    score -= float(d[h][h]['Deaths-Average'].replace(',',''))
                except:
                    pass
                try:
                    score += float(d[h][h]['SoloKills-Average'].replace(',',''))*3
                except:
                    pass
                try:
                    if h == 'Ana':
                        score += float(d[h][h]['HealingDone-Average'].replace(',',''))
                    elif h == 'DVa':
                        score += float(d[h][h]['DamageBlocked-Average'].replace(',',''))*0.5
                    elif h == 'Genji':
                        score += float(d[h][h]['ObjectiveKills-Average'].replace(',',''))*2000
                    elif h == 'Hanzo':
                        score += float(d[h][h]['FinalBlows-Average'].replace(',',''))*1000
                    elif h == 'Lucio':
                        score += float(d[h][h]['HealingDone-Average'].replace(',',''))
                    elif h == 'Mccree':
                        score += float(d[h][h]['FantheHammerKills-Average'].replace(',',''))*1000
                    elif h == 'Mei':
                        score += float(d[h][h]['BlizzardKills-Average'].replace(',',''))*1000
                    elif h == 'Mercy':
                        score += float(d[h][h]['HealingDone-Average'].replace(',',''))
                    elif h == 'Pharah':
                        score += float(d[h][h]['ObjectiveKills-Average'].replace(',',''))*2000
                    elif h == 'Reaper':
                        score += float(d[h][h]['ObjectiveKills-Average'].replace(',',''))*2000
                    elif h == 'Reinhardt':
                        score += float(d[h][h]['DeathBlossomKills-Average'].replace(',',''))*2000
                    elif h == 'Roadhog':
                        score += float(d[h][h]['HookAccuracy'].replace('%',''))*100
                    elif h == 'Soldier76':
                        score += float(d[h][h]['TacticalVisorKills-Average'].replace(',',''))*2000
                    elif h == 'Symmetra':
                        score += float(d[h][h]['ShieldsProvided-Average'].replace(',',''))*3000
                    elif h == 'Torbjoern':
                        score += float(d[h][h]['MoltenCoreKills-Average'].replace(',',''))*2000
                    elif h == 'Tracer':
                        score += float(d[h][h]['PulseBombsAttached-Average'].replace(',',''))*5000
                    elif h == 'Widowmaker':
                        score += float(d[h][h]['PulseBombsAttached-Average'].replace('%',''))*100
                    elif h == 'Winston':
                        score += float(d[h][h]['DamageBlocked-Average'].replace(',',''))
                    elif h == 'Zarya':
                        score += float(d[h][h]['DamageBlocked-Average'].replace(',',''))
                    elif h == 'Zenyatta':
                        score += float(d[h][h]['HealingDone-Average'].replace(',',''))
                except:
                    pass
                scores[name][h] = score
            top_hero = sorted(scores[name].items(),key=itemgetter(1),reverse=True)[0:5]
            scores[name] = top_hero
        return render_template('info.html',random=random.randint(1,background_count),pro=profile['data'],qui=quick_heros,infos=[profile['data']['competitive']['rank_img'],profile['data']['level'],profile['data']['competitive']['rank'],profile['data']['username'],profile['data']['avatar']],hero_data=d,top=top_hero,image=images,ach=achiev)
    #except:
    #    return "<html><head><script>alert('no username');document.location='/'</script></head><body></body></html>"

@app.route('/achievements/<name>/')
def achievements(name):
    try:
        name = name.replace('#','-')
        profile = api_origin_profile(name)
        if profile == False:
            return 'no username'
        achievements = api_achievements(name)
        return render_template('achievements.html',ach=achievements)
    except:
        pass

@app.route('/hero/<name>/<hero>/')
def hero(name,hero):
    try:
        name = name.replace('#','-')
        profile = api_profile(name)
        if profile == False:
            return 'no username'
        hero_data = api_competitive_hero(name,hero)
        return render_template('hero.html',her=list(hero_data.items())[0][1])
    except:
        pass

@app.route('/chart/')
def chart():
    try:
        return render_template('chart.html')
    except:
        pass

if __name__ == '__main__':
    app.run(host=server_domain, port=server_port, debug=True)
