import time
import requests
import re
import json
#获得一页内容
def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    response = requests.get(url= url,headers = headers)
    if response.status_code == 200 :
        return response.text
    else:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*? data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    print(items)
    for item in items:
         yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip(),
            'time': item[4].strip(),
            'srore': item[5].strip()+item[6].strip()
        }


def write_to_file(item):
    with open('一百部最受欢迎电影.text', 'a',encoding='utf-8')as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')



#当做主函数，进行网址的构造和解析
def main(i):
    url = 'http://maoyan.com/board/4?offset={}'.format(i)#构造网址，翻页
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ =='__main__':
    for i in range(0,100,10):
        main(i)
        time.sleep(4)
