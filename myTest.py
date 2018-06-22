import requests
import threading
from lxml import etree
from bs4 import BeautifulSoup
from queue import Queue
out_queue=Queue()

def get_html(url1):
    header={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.516.400 QQBrowser/9.4.8186.400'}
    request=requests.get(url=url1,headers=header)
    response=request.content
    return response
class threadDownload(threading.Thread):
    def __init__(self,que,no):
        threading.Thread.__init__(self)
        self.que = que
        self.no = no
    def run(self):
        while True:
            if not self.que.empty():
                   save_img(self.que.get()[0])
            else:
                break
def get_img_html(html1):
    y=[]
    soup=BeautifulSoup(html1,'lxml')
    for hrefs in soup.find_all('a',class_='list-group-item random_list'):
        y.append(hrefs.get('href'))
    return y

def get_img(html2):
    html=get_html(html2)
    soup=etree.HTML(html)
    items=soup.xpath('//div[@class="artile_des"]')
    for item in items:
        imgurl_list=item.xpath('table/tbody/tr/td/a/img/@onerror')
        out_queue.put(item.xpath('table/tbody/tr/td/a/img/@onerror'))
    for a in range(0,imgurl_list.__len__()):
        print(imgurl_list.__len__())
        threadD = threadDownload(out_queue,a)
        threadD.start()
x=1
def save_img(img_url):
    global x
    x+=1
    img_url1 =img_url.split('=')[-1][1:-2].replace('jp','jpg').replace('pn','png').replace('gi','gif')
    print(u'正在下载'+'http:'+img_url1)
 #   img_content=requests.get('http:'+img_url1).content
 #   with open('doutu/%s.jpg'% x,'wb') as f:
 #       f.write(img_content)



def main():
    start_url='https://www.doutula.com/article/list/?page='
    for j in range(1,5):
        start_html=get_html(start_url+str(j))
        b=get_img_html(start_html)
        for i in b:
            get_img(i)
if __name__=='__main__':
    main()