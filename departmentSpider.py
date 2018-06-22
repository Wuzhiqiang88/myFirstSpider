from urllib import request
from bs4 import BeautifulSoup
import pymysql
import time
from urllib import error
import socket
socket.setdefaulttimeout(30)
def department_intoDB(department_1_name,get_department_2_names):
    db = pymysql.connect("localhost", "root", "123456", "spider",charset='utf8')
    cursor = db.cursor()
    sql = 'INSERT INTO t_departments(department_1_name,department_2_name) VALUES (%s,%s)'
    for department_2_names in get_department_2_names:
        department_2_name = department_2_names.find('a').get_text()
        try:
            # 执行sql语句
            cursor.execute(sql, (department_1_name, department_2_name))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            db.close()
        # 关闭数据库连接
    db.close()

def symptoms_intoDB(department_2_name,get_symptoms_names):
    db = pymysql.connect("localhost", "root", "123456", "spider",charset='utf8')
    cursor = db.cursor()
    sql = 'INSERT INTO t_symptoms(department_2_name,symptoms_name) VALUES (%s,%s)'
    for symptoms_names in get_symptoms_names:
        symptoms_name = symptoms_names.find('a').get_text()
        try:
            # 执行sql语句
            cursor.execute(sql, (department_2_name, symptoms_name))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            db.close()
        # 关闭数据库连接
    db.close()

def disease_intoDB(list):
    db = pymysql.connect("localhost", "root", "123456", "spider",charset='utf8')
    cursor = db.cursor()
    print(list[0])
    sql = 'INSERT INTO t_disease(symptom,introduction_of_disease,high_incidence_group,contagion,state,inspect,diagnosis,cure,nursing) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        # 执行sql语句
        cursor.execute(sql, (list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8]))
        # 提交到数据库执行
        db.commit()
        db.close()
    except:
        # 如果发生错误则回滚
        print("sql出错啦！")
        db.rollback()
        db.close()
    # 关闭数据库连接

def spider(url,path):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    try:
        page_info = request.urlopen(page).read().decode('utf-8')
    except error.URLError as e:
        all_spider = ""
        return all_spider
    else:
        soup = BeautifulSoup(page_info, 'lxml')  # html.parser
        all_spider = soup.select(path)
        return all_spider

def get_disease(symptoms_name,url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    list = []
    try:
        page_info = request.urlopen(page).read().decode('utf-8')
    except error.URLError as e:
        list.append(symptoms_name)
        list.append("")
        list.append("")
        list.append("")
        list.append("")
        list.append("")
        list.append("")
        list.append("")
        list.append("")
        disease_intoDB(list)
    else:
        introduction_of_disease=""
        high_incidence_group=""
        contagion=""
        state=""
        inspect=""
        diagnosis=""
        cure=""
        nursing=""
        disease_list = []
        soup = BeautifulSoup(page_info, 'lxml')  # html.parser
        path_judge ="body > div.ui-grid.ui-main.clearfix > div.left-container > ul.tab-type-two > li"
        num = len(soup.select(path_judge))
        for i in range(1,num+1):
            path = "body > div.ui-grid.ui-main.clearfix > div.left-container > div.slider-wrap > div:nth-of-type(%d) > div > p" % i
            all_spider = soup.select(path)
            disease_list.append(all_spider[0].get_text())
        for a in range(0,num):
            if soup.select(path_judge)[a].get_text() == "疾病介绍":
                introduction_of_disease = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "高发群体":
                high_incidence_group = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "传染":
                contagion = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "症状":
                state = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "检查":
                inspect = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "诊断和鉴别":
                diagnosis = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "治疗":
                cure = disease_list[a]
            if soup.select(path_judge)[a].get_text() == "护理":
                nursing = disease_list[a]
        list.append(symptoms_name)
        list.append(introduction_of_disease)
        list.append(high_incidence_group)
        list.append(contagion)
        list.append(state)
        list.append(inspect)
        list.append(diagnosis)
        list.append(cure)
        list.append(nursing)
        disease_intoDB(list)
global i
i=0
def get_symptoms(department_2_name,url):
    symptoms_path = 'div.ui-grid.ui-main.clearfix > ul.tab-type-one.disease-list.tab-type-free > li.tab-item'
    get_symptoms_names = spider(url,symptoms_path)
 #   symptoms_intoDB(department_2_name,get_symptoms_names)
    for symptoms_names in get_symptoms_names:
        symptoms_name = symptoms_names.find('a').get_text()
        url_3 = 'https://www.chunyuyisheng.com' + symptoms_names.find('a')['href']
        time.sleep(0.5)
        get_disease(symptoms_name,url_3)

def get_department_2(department_1_name,url):
    global i
    department_2_path = 'div.slider-wrap.dropdown-wrap > ul.tab-type-one.tab-type-free.border-dashed.slider-item.cur > li.tab-item'
    get_department_2_names = spider(url,department_2_path)
 #   department_intoDB(department_1_name,get_department_2_names)
    for department_2_names in get_department_2_names:
        department_2_name = department_2_names.find('a').get_text()
        url_2 = 'https://www.chunyuyisheng.com/pc/disease/hot/' + department_2_names.find('a')['href']
        if 28 < i:
            get_symptoms(department_2_name,url_2)
        i +=1


def get_department_1(url):
    department_1_path = 'div.ui-grid.ui-main.clearfix > ul.tab-type-one.border-dashed.j-tab-wrap > li.tab-item'
    get_department_1_names = spider(url,department_1_path)
    for department_1_names in get_department_1_names:
        department_1_name = department_1_names.find('a').get_text()
        url_1 = url + department_1_names.find('a')['href']
        get_department_2(department_1_name,url_1)

def main():
    start_url = 'https://www.chunyuyisheng.com/pc/disease/hot/'
    get_department_1(start_url)

if __name__=='__main__':
    start = time.clock()
    main()
    end = time.clock()
    print("time: %f s" % (end - start))



