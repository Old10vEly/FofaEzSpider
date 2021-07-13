import requests
from urllib.parse import quote
import base64
import re
import time
from lxml import etree


cookies="Hm_lvt_b5514a35664fd4ac6a893a1e56956c97=1626080214,1626080224; Hm_lpvt_b5514a35664fd4ac6a893a1e56956c97=1626154416; Hm_lvt_9490413c5eebdadf757c2be2c816aedf=1626082809; Hm_lpvt_9490413c5eebdadf757c2be2c816aedf=1626155755; _fofapro_ars_session=0dfa7847792cc12ceae450592017642c; referer_url=%2F"
http = "http"
def main(search,filename):
    with open('{}.txt'.format(filename), 'a') as f:
        for i in range(1, pageend+1):
            for x in getData(i, search):
                f.write(x+'\n')
                f.flush()
    f.close()
def pageend(search):
    url = 'https://classic.fofa.so/result?page=1&q={}&qbase64={}'.format(quote(search), quote(base64.b64encode(search.encode('utf-8'))))
    data = requests.get(url, headers = {"Cookie": cookies}).text
    if 'Retry later' in data:
        print('Get the page_end again')
        time.sleep(2)
        return pageend()
    r = etree.HTML(data)
    c_list = r.xpath('//div[@class="list_jg"]/text()')
    total = re.sub('\D','',str(re.findall(re.compile(r"(.*?)\(", re.S), str(c_list)))) 
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
        print('共有数据' + str(total) + '条,共有' + str(page_end) + '页,爬取'+str(page_end)+'页')
    return page_end 

def getData(page, search):
    print('[START] Page '+str(page))
    time.sleep(1)
    url = 'https://classic.fofa.so/result?page={}&q={}&qbase64={}'.format(str(page), quote(search), quote(base64.b64encode(search.encode('utf-8'))))
    data = requests.get(url, headers = {"Cookie": cookies}).text
    if 'Retry later' in data:
        print('[!!！!!!]'+str(page)+'[!!!!!]')
        time.sleep(20)
        return getData(page, search)
    r = etree.HTML(data)
    c_list = r.xpath('//div[@class="ip-no-url"]/text()')
    ret = [x.strip() for x in c_list if x.strip() != ''] 
    print(ret)
    print('[END] Page ' + str(page))
    return ret

if __name__ == '__main__':
    search = input('Search command: (protocol="rdp")'+"\n")
    filename = input("filename:(default=localtime.txt)")
    pageend=pageend(search)
    if filename == '':
        filename=time.strftime('%Y-%m-%d %H_%M_%S', time.localtime())
    main(search,filename)