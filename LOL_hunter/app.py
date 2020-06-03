import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request,jsonify


app = Flask(__name__)

# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://www.op.gg/summoner/userName=%ED%95%AB%20%EB%B6%80',headers=headers)


# data를 text형태로 바꿔야 한다.

# print(data) -> 200 ok 반응이 나온다
# print(data.text) -> 크롤링 해온다

# # request에 대한 기본 이해도
# naver = 'https://www.naver.com/'
# response = requests.get(url=naver)
# print(response.text)



# soup = BeautifulSoup(data.text,'html.parser')
# print(soup)

@app.route('/')
def home():
    return render_template("Main.html")

@app.route('/test', methods=['GET'])
def test_get():
   ID_Search = request.args.get('ID_Search')
   headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get('https://www.op.gg/summoner/userName='+ID_Search,headers=headers)   
   soup = BeautifulSoup(data.text,'html.parser')


   mydivs = soup.findAll("div", {"class": "SummonerNotFoundLayout"})
   if(len(mydivs)==0): 
        result=True
   else:
        result=False

   # return print(result) 
   return jsonify({'result':result}) 


if __name__ == '__main__':  
   app.run('localhost',port=5000,debug=True)