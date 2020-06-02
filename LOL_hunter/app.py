import requests
from bs4 import BeautifulSoup


# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

# soup = BeautifulSoup(data,'html.parser')
# print(soup)



# request에 대한 기본 이해도
naver = 'https://www.naver.com/'
response = requests.get(url=naver)
print(response.text)