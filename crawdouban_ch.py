import requests
import xlwt
from bs4 import BeautifulSoup
import re
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36','Host':'movie.douban.com'}
movie_ch_list=[]
#movie_en_list=[]
director_ch_list=[]
#director_en_list=[]
actor_ch_list=[]
#actor_en_list=[]
time_list=[]

for i in range(0,10):
    try:
        url='https://movie.douban.com/top250?start='+str(i*25)
        res=requests.get(url,headers=headers,timeout=10)
        res.raise_for_status()
    except:
        print('第'+str(i+1)+'页读取失效')
        continue
    soup=BeautifulSoup(res.text,'lxml')
    div_list=soup.find_all('div',class_='hd')
    div1_list=soup.find_all('div',class_='bd')
    #div2_list=soup.find_all('div',class_='star')
    
    for each in div_list:
        mo=[]
        for  child in each.a.children:
            if child.string=='\n':
                continue
            mo.append(child.string)
        movie_ch_list.append(mo[0])
        #movie_en_list.append(mo[1])

    k=0#记录进行到第几个电影
    for each in div1_list[1:]:
        a=each.p.text.split("导演:")[1].split("主演:")
        k=k+1
        try:
            a1=re.findall(r'[\u4e00-\u9fa5]+·*[\u4e00-\u9fa5]*',a[0])[0]#中文导演名
            #a2=a[0].replace(a1,"").split('\xa0')[0].strip(" ")#英文导演名
            b1=re.findall(r'[\u4e00-\u9fa5]+·*[\u4e00-\u9fa5]*',a[1])[0]#中文演员名
            #b2=a[1].replace(b1,"").split('\xa0')[0].strip(" ")#包含演员英文名和时间
            #a3=re.findall(r'[A-Za-z]+\s*[A-Za-z]*',b2)[0]#演员英文名     
            a4=re.findall(r'[0-9]{4}',a[1])[0]         
        except:
            url1=div_list[k-1].a.attrs['href']
            res1=requests.get(url1,headers=headers,timeout=10)
            soup1=BeautifulSoup(res1.text,'lxml')
            a1=soup1.find_all('a',attrs={"rel":"v:directedBy"})[0].string
            b1=soup1.find_all('a',attrs={'rel':"v:starring"})[0].string
            a4=soup1.find_all('span',attrs={'property':"v:initialReleaseDate"})[0].string[0:4]
        director_ch_list.append(a1)
        #director_en_list.append(a2)
        actor_ch_list.append(b1)
        #actor_en_list.append(a3)
        time_list.append(a4)

fp="D:\\python学习\\douban250中文.csv"
#fp1="D:\\python学习\\douban250英文.csv"
f=open(fp,"w+")
#f1=open(fp1,"w+")
f.write("排名,中文电影名,中文导演名,中文演员名,时间\n")
#f1.write("排名,英文电影名,英文导演名,英文演员名,时间\n")
for i in range(0,250):
    f.write(str(i+1)+','+movie_ch_list[i]+','+director_ch_list[i]+','+actor_ch_list[i]+','+time_list[i]+','+'\n')
f.close()









            


     