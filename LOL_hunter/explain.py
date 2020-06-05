
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


# >>> from bs4 import BeautifulSoup
# >>> soup = BeautifulSoup('<META NAME="City" content="Austin">')
# >>> soup.find("meta", {"name":"City"})
# <meta name="City" content="Austin" />
# >>> soup.find("meta", {"name":"City"})['content']
# u'Austin'