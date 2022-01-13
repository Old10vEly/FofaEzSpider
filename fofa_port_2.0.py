import requests
from urllib.parse import quote
import threading   
import base64
import time
import os
import re
from lxml import etree



cookies =""
http = "http"

#多线程
def Th(search,filename,pageend): 
    with open('{}.txt'.format(filename), 'a') as f:
        l = list(range(1, pageend+1))
        thread_list =[]
        for i in l:
            t =threading.Thread(target=getData,args=(i,search,f,))
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:                                                                                           
            t.join() 
        f.close()
def pageend(search):
    url = 'https://fofa.so/result?page=1&q={}&qbase64={}&full=true'.format(quote(search), quote(base64.b64encode(search.encode('utf-8'))))
    data = requests.get(url, headers = {"Cookie": cookies}).text
    if 'Retry later' in data:
        print('Get the page_end again')
        time.sleep(2)
        return pageend()
    r = etree.HTML(data)
    c_list = r.xpath('//span[@class="el-pagination__total"]/text()')
    total = re.sub('\D','',str([x.strip() for x in c_list if x.strip() != ''])) 
    if total == "":
        page_end=1
        print('共有数据小于10条,爬取'+str(page_end)+'页')
    else:
        total=int(total)
        if total >10 and total <= 100:
            page = page_end = int(total/10)+1
        elif total >100 and total <= 1000:
            page = page_end = int(total/10)+1
        elif total >1000 and total <= 10000:
            page = page_end = int(total/10)+1
        elif total >10000 :
            page_end = 1000
            page = int(total/10)+1          
        else:
            page_end = 1
        print('共有数据' + str(total) + '条,共能爬取' + str(page_end) + '页,爬取'+str(page_end)+'页')
    return page_end  

def getData(page,search,f):
    if pageend >= 5:
        pool_sema.acquire()
    print('[START] Page '+str(page))
    url = 'https://fofa.so/result?page={}&q={}&qbase64={}'.format(str(page), quote(search), quote(base64.b64encode(search.encode('utf-8'))))
    data = requests.get(url, headers = {"Cookie": cookies}).text
    if 'Retry later' in data:
        print('[!!!!!!]'+str(page)+'[!!!!!]')
        time.sleep(2.5)
        return getData(page, search)
    r = etree.HTML(data)
    i_list = r.xpath('//span[@class="aSpan"]/text()')
    p_list = r.xpath('//a[@class="portHover"]/text()' )
    c_list = ["{0}:{1}".format(str(i_list[i]),str(p_list[i])) for i in range(0,len(i_list))]
    ret = [x.strip() for x in c_list if x.strip() != '']
    if (ret and page ==2) or (page ==1) or (page >=3):

        for j in range(0,len(ret)):
            retu = ret[j]
            if int(retu.find(http)) == -1:
                ret[j] = retu
        print(ret)
        print('[END] Page ' + str(page))
    else:
        print("请检查cookies是否设置正确")
        f.close()
        os._exit(1) 
    for x in ret:
        f.write(x+'\n')
        f.flush()
    time.sleep(1)
    if pageend >= 100: 
    	time.sleep(5)
    if pageend >= 5:  
        pool_sema.release()
if __name__ == '__main__':
    print('''
         _______     ___          _______          _          _     _             
        (_______)   / __)        (_______)        | |        (_)   | |            
         _____ ___ | |__ ____ ___ _____   _____    \ \  ____  _  _ | | ____  ____ 
        |  ___) _ \|  __) _  (___)  ___) (___  )    \ \|  _ \| |/ || |/ _  )/ ___)
        | |  | |_| | | ( ( | |   | |_____ / __/ _____) ) | | | ( (_| ( (/ /| |    
        |_|   \___/|_|  \_||_|   |_______|_____|______/| ||_/|_|\____|\____)_|    
                                                       |_|                      
                                                     by Old10vEly   version:2.0    
        ''')
    search = input('Search command: (ex:app="Weblogic")'+"\n")
    filename = input("filename:(default=localtime.txt)")
    if filename == '':
        filename=time.strftime('%Y-%m-%d %H_%M_%S', time.localtime())
    pageend=pageend(search)

    max_connections = 5  #线程数
    pool_sema = threading.BoundedSemaphore(max_connections)
    lock = threading.Lock()
    Th(search,filename,pageend)
