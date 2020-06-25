import requests
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from ast import literal_eval


app = Flask(__name__)

# Main 화면 route
@app.route('/')
def home():

    
    return render_template("Main.html")



# OP.GG를 통해서 Summoner 존재 여부 
@app.route('/Search', methods=['GET'])
def Search():
   # url: "/test?ID_Search=" + search를 보낸다.   
   ID_Search = request.args.get('ID_Search')
   headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#  OP.GG에서 아이디를 받아 오기!
   data = requests.get('https://www.op.gg/summoner/userName='+ID_Search,headers=headers)   
#  BS4를 사용해서 가공시키기
   soup = BeautifulSoup(data.text,'html.parser')
   mydivs = soup.findAll("div", {"class": "SummonerNotFoundLayout"})
   print(mydivs)
#  summonernotfound를 통해서 닉네임 존재 여부 확인하기
   if(len(mydivs)==0): 
        result=True
   else:
        result=False
   # return print(result)
   print("-------------------------------------------")
   print(jsonify({'result':result,'summoner':ID_Search}))
   print("-------------------------------------------") 
   return jsonify({'result':result,'summoner':ID_Search}) 


# sumonner에 따른 route 동적 할당 만들기 
@app.route('/User/<summoner>')
def User(summoner):
    return render_template("User.html")


@app.route('/data_inquery', methods=['GET'])
def Data_Inquery():
    
    User = request.args.get('User')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    client = MongoClient('localhost', 27017)
    db = client.LOL_hunters
    # db.users.find_one({'user_id': User})
    print(db.users.find_one({'user_id': User}))
    if((db.users.find_one({'user_id': User})) == None): 
        user_data = {
            'user_id': User,
            'receive_report':0,
            '타 포지션 요구': 0,
            '라인 방해': 0,
            '비정상 플레이': 0,
            '버프 스틸':0,
            '탈주':0,
            '던짐':0,
            '킬 스틸':0,
            'CS 스틸:':0,
            '티어에 맞지않음':0,
            '솔킬 자주 따임':0,
            '단독 플레이':0,
            'RPG 유저':0,
            '카정후 킬따임':0,
            '맵리를 안함':0,
            '비합리적 오더':0,
            '욕설러':0,
            '정치질':0,
            '불평 자주함':0,
            '무리한 핑':0,
            '거짓말':0,
            '합리화 자주함':0,
            '대리게임의혹':0,
            '충챔픽커':0,
            '즐겜러':0,
            'oneline':[]
        }
        db.users.insert(user_data)
        state='new'
    else:
        state='old'

    print(state)
    return jsonify({'result': 'success','state':state})




@app.route('/OP.GG_Crawling', methods=['GET'])
def User_data():
    User = request.args.get('User')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#  OP.GG에서 아이디를 받아 오기!
    data = requests.get('https://www.op.gg/summoner/userName='+User,headers=headers)   
#  BS4를 사용해서 가공시키기
    soup = BeautifulSoup(data.text,'html.parser')
    image = soup.select('.ProfileImage')    
    print(image[0]['src'])
    return jsonify({'User_Icon': image[0]['src']}) 

@app.route('/Report_database',methods=['POST'])
def Report():
   
    client = MongoClient('localhost', 27017)
    db = client.LOL_hunters
    id = request.form['id']
    check = request.form.getlist('check[]')
    oneline = request.form['oneline_send']

# 
    troll_list = ['타 포지션 요구',
            '라인 방해',
            '비정상 플레이',
            '버프 스틸',
            '탈주',
            '던짐',
            '킬 스틸',
            'CS 스틸:',
            '티어에 맞지않음',
            '솔킬 자주 따임',
            '단독 플레이',
            'RPG 유저',
            '카정후 킬따임',
            '맵리를 안함',
            '비합리적 오더',
            '욕설러',
            '정치질',
            '불평 자주함',
            '무리한 핑',
            '거짓말',
            '합리화 자주함',
            '대리게임의혹',
            '충챔픽커',
            '즐겜러']

    user=db.users.find_one({'user_id': id})


    for i in range(0,len(check)):
        num=int(check[i])
        new=user[troll_list[num]]+1
        db.users.update_one({'user_id': id},{'$set':{troll_list[num]:new}}) 

    num_report=user['receive_report']+1
    db.users.update_one({'user_id': id},{'$set':{'receive_report':num_report}})
    if not oneline:
        print("데이터없음")
    else:
        db.users.update_one({'user_id': id},{'$push':{'oneline':oneline}})
   
    return jsonify({'result': 'success'})


@app.route('/Doughnut_data',methods=['GET'])
def Doughnut_data():
    client = MongoClient('localhost', 27017)
    db = client.LOL_hunters
    User = request.args.get('User')


    data=list(db.users.find({'user_id':User}))
    all_troll=data[0]

    a=0
    attempt=0
    unreason=0
    ohter=0
    report=0

    for value in all_troll.values():
        if(a==2):
            report= value
        if(a>=3 and a<=10):
            attempt += value
        elif(a>=11 and a<=17):
            unreason += value
        elif(a>=18 and a<=26):
            ohter += value
        a+=1

    a=0
    troll_list=list()
    oneline_list=list()

    for value in all_troll.values():
        if(3<=a and a<=26):
            troll_list.append(value)
        if(a==27):
            oneline_list=value
        a+=1

    troll_list=list(set(troll_list))
    troll_list.sort(reverse=True)
    
    final_list=list()
    number_list=list()
    data_list=list()

    a=0

    for value in troll_list:
        if(a==7):
            break
        for key in all_troll.keys():
            if(all_troll[key]==value):
                final_list.append(key)
                number_list.append(value)
                a+=1

    real_list=list()

    for i in range(7):
        real_list.append(final_list[i])
        data_list.append(number_list[i])

    result={'result': 'success', 'report':report,'atmp':attempt,'unre':unreason,'oth':ohter,'bar_list':real_list,'bar_list_data':data_list,'oneline_list':oneline_list}
    return jsonify(result)

if __name__ == '__main__':  
   app.run('localhost',port=5000,debug=True)