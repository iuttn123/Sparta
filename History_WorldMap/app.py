import requests
import os
import sys
import urllib.request
import json
import pycountry
from flask import Flask, render_template, request, jsonify

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from geopy.geocoders import Nominatim


app = Flask(__name__)



@app.route('/')
def home():
   return render_template("Main.html")


# def wikipedia():
    # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get('https://en.wikipedia.org/wiki/1999',headers=headers)
    # client = MongoClient('localhost', 27017)
    # db = client.History_Map
    # all_data={}


    # # #  BS4를 사용해서 가공시키기
    # soup = BeautifulSoup(data.text,'html.parser')

    # all_data['Year']=1999
    # all_data['January'] = wiki_data('January')
    # all_data['February'] = wiki_data('February')
    # all_data['March'] = wiki_data('March')
    # all_data['April'] = wiki_data('April')
    # all_data['May'] = wiki_data('May')
    # all_data['June'] = wiki_data('June')
    # all_data['July'] = wiki_data('July')
    # all_data['August'] = wiki_data('August')
    # all_data['September'] = wiki_data('September')
    # all_data['October'] = wiki_data('October')
    # all_data['November'] = wiki_data('November')
    # all_data['December'] = wiki_data('December')

    # wiki_data('January')
    # wiki_data('February')
    # wiki_data('March')
    # wiki_data('April')
    # wiki_data('May')
    # wiki_data('June')
    # wiki_data('July')
    # wiki_data('August')
    # wiki_data('September')
    # wiki_data('October')
    # wiki_data('November')
    # wiki_data('December')

    # db.years.insert(all_data)

    # db.users.find_one({'user_id': User})


    # client_id = "4qO7rR7DaF9PEf6RiE34"
    # client_secret = "72jWYtaGM9"
    # encText = urllib.parse.quote("반갑습니다")
    # data = "source=ko&target=en&text=" + encText
    # url = "https://openapi.naver.com/v1/papago/n2mt"
    # request = urllib.request.Request(url)
    # request.add_header("X-Naver-Client-Id",client_id)
    # request.add_header("X-Naver-Client-Secret",client_secret)
    # response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    # rescode = response.getcode()
    # if(rescode==200):
    #     response_body = response.read()
    #     data=response_body.decode('utf-8')
    #     data=json.loads(data)
    #     print(data['message']['result']['translatedText'])
    # else:
    #     print("Error Code:" + rescode)
    
    # contury_list = []
    # num =0
    # for con in pycountry.countries:
    #     contury_list.append(con.name)

    # print(contury_list)


@app.route('/Search', methods=['GET'])
def Search():

   client = MongoClient('localhost', 27017)
   db = client.History_Map
   all = db.wiki_history.find({'Month': 'April'})
   all = list(all)
   jsonStr = json.dumps(all)
   print(jsonStr)

   return jsonify({'result': 'success', 'data': jsonStr})


def wiki_data(month):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://en.wikipedia.org/wiki/1999',headers=headers)
    client = MongoClient('localhost', 27017)
    db = client.History_Map
    
    soup = BeautifulSoup(data.text,'html.parser')

    # 모든 나라 list 
    contury_list = []
    for con in pycountry.countries:
        contury_list.append(con.name)
    
    
    wiki=soup.find('span', id=month)
    wiki=wiki.find_parent()
    monthly_data=wiki.find_next('ul').text
    sentence=monthly_data.split(".")
    

    geolocator = Nominatim(user_agent="History_Map")
   
    for con in contury_list:
        for sen in sentence:
            all_data={}
            if(sen.find(con) != -1):
                
                location = geolocator.geocode(con)
                all_data['Year']=1999
                all_data['Month']=month
                all_data['Event']=sen
                all_data['Contury']=con
                all_data['Latitude']=location.latitude
                all_data['Longitude']=location.longitude
                db.wiki_history.insert(all_data)
                

    return 0



# Search()

if __name__ == '__main__':  
   app.run('localhost',port=5000,debug=True)

   
