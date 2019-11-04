# 爬取豆瓣T250
python爬虫 豆瓣电影T250 不断改进的过程~
相比其它很多经典的爬虫，还提取了影片、导演和演员的英文名称
----------------------------------------------------------------------------------------------------------------------------------------
#crawldouban.py
import requests
import xlwt
from bs4 import BeautifulSoup
import re
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36','Host':'movie.douban.com'}
movie_ch_list=[]
movie_en_list=[]
director_ch_list=[]
director_en_list=[]
actor_ch_list=[]
actor_en_list=[]
time_list=[]

for i in range(0,10):
    try:
        url='https://movie.douban.com/top250?start='+str(i*25) #每页有24个电影的信息
        res=requests.get(url,headers=headers,timeout=10)
        res.raise_for_status()
    except:
        continue
        print('第'+str(i+1)+'页读取失效')
    soup=BeautifulSoup(res.text,'lxml')
    div_list=soup.find_all('div',class_='hd')
    div1_list=soup.find_all('div',class_='bd')
    div2_list=soup.find_all('div',class_='star')
    
    for each in div_list:
        mo=[]
        for  child in each.a.children:
            if child.string=='\n':
                continue
            mo.append(child.string)
        movie_ch_list.append(mo[0])
        movie_en_list.append(mo[1])

    for each in div1_list[1:]:
        a=each.p.text.split("导演:")[1].split("主演:")
        try:
            a1=re.findall(r'[\u4e00-\u9fa5]+·*[\u4e00-\u9fa5]*',a[0])[0]#中文导演名
            a2=a[0].replace(a1,"").split('\xa0')[0].strip(" ")#英文导演名
        except:
            a1=" "
            a2=" "
        director_ch_list.append(a1)
        director_en_list.append(a2)

        try:
            b1=re.findall(r'[\u4e00-\u9fa5]+·*[\u4e00-\u9fa5]*',a[1])[0]#中文演员名
            b2=a[1].replace(b1,"").split('\xa0')[0].strip(" ")#包含演员英文名和时间
            a3=re.findall(r'[A-Za-z]+\s*[A-Za-z]*',b2)[0]#演员英文名
        except:
            b1=" "
            a3=" "
        a4=b2[-4:]
        actor_ch_list.append(b1)
        actor_en_list.append(a3)
        time_list.append(a4)
#写入csv文件
fp="D:\\python学习\\douban250中文.csv"
fp1="D:\\python学习\\douban250英文.csv"
f=open(fp,"w+")
f1=open(fp1,"w+")
f.write("排名,中文电影名,中文导演名,中文演员名,时间\n")
f1.write("排名,英文电影名,英文导演名,英文演员名,时间\n")
for i in range(0,250):
    f.write(str(i+1)+','+movie_ch_list[i]+','+director_ch_list[i]+','+actor_ch_list[i]+','+time_list[i]+','+'\n')
for i in range(0,250):
    f1.write(str(i+1)+','+movie_en_list[i]+','+director_en_list[i]+','+actor_en_list[i]+','+time_list[i]+','+'\n')
f.close()
----------------------------------------------------------------------------------------------------------------------------------------
Debug总结：
1、因为是在介绍页进行提取，因此会发生导演名称缺省的问题，还有一些法文或者印度语之类的情况，不能被正则表达式匹配到...
2、中文导演名的正则表达式r'[\u4e00-\u9fa5]+·*[\u4e00-\u9fa5]*'
3、英文会出现/xa00这种情况，不能被写入文件


接下来会进行改进
2019.114中文部分的修改：
进入介绍页的具体电影链接href，爬取导演名或者演员名
代码文件为crawdouban_ch.py
