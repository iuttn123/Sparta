import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request,jsonify



headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.op.gg/summoner/userName=%ED%95%AB%20%EB%B6%80',headers=headers)


# data를 text형태로 바꿔야 한다.

# print(data) 
# print(data.text) 

# soup = BeautifulSoup(data.text,'html.parser')
# print(soup)
# # request에 대한 기본 이해도
# naver = 'https://www.naver.com/'
# response = requests.get(url=naver)
# print(response.text)