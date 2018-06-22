from urllib import request
from bs4 import BeautifulSoup
from urllib import error

url="https://www.chunyuyisheng.com/pc/disease/273362/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url, headers=headers)
try:
    page_info = request.urlopen(page).read().decode('utf-8')
except error.URLError as e:
    print("404")
else:
    list = []
    soup = BeautifulSoup(page_info, 'lxml')  # html.parser
    path_judge = "body > div.ui-grid.ui-main.clearfix > div.left-container > ul.tab-type-two > li"
    all = soup.select(path_judge)
    print(all[0])



