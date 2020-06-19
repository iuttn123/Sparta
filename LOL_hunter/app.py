import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request,jsonify


app = Flask(__name__)


# Main 화면 route
@app.route('/')
def home():
    return render_template("Main.html")


# sumonner에 따른 route 동적 할당 만들기 
@app.route('/User/<summoner>')
def User(summoner):
    return render_template("User.html")


# OP.GG를 통해서 Summoner 존재 여부 
@app.route('/Search', methods=['GET'])
def Search():
   # url: "/test?ID_Search=" + search를 보낸다.
   ID_Search = request.args.get('ID_Search')
   print(ID_Search)
   headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#  OP.GG에서 아이디를 받아 오기!
   data = requests.get('https://www.op.gg/summoner/userName='+ID_Search,headers=headers)   
#  BS4를 사용해서 가공시키기
   soup = BeautifulSoup(data.text,'html.parser')
   mydivs = soup.findAll("div", {"class": "SummonerNotFoundLayout"})
#  summonernotfound를 통해서 닉네임 존재 여부 확인하기
   if(len(mydivs)==0): 
        result=True
   else:
        result=False
   # return print(result) 
   return jsonify({'result':result,'summoner':ID_Search}) 


#
@app.route('/OP.GG_Crawling', methods=['GET'])
def User_data():
    User = request.args.get('User')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    print("===============================================================")
    print(User)
    print("===============================================================")
#  OP.GG에서 아이디를 받아 오기!
    data = requests.get('https://www.op.gg/summoner/userName='+User,headers=headers)   
#  BS4를 사용해서 가공시키기
    soup = BeautifulSoup(data.text,'html.parser')
    image = soup.select('.ProfileImage')
    print(image[0]['src'])
    return jsonify({'User_Icon': image[0]['src']}) 


if __name__ == '__main__':  
   app.run('localhost',port=5000,debug=True)