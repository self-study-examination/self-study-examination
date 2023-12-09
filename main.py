import requests
import json
import logging
import re
import os

from urllib.parse import urljoin
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
env = Environment(loader=FileSystemLoader("templates/"))

class AbstractTown(object):
    
    """省份"""
    def __init__(self,conf:dict):
        self.conf = conf
        self.env = env
    
    
    def clean(self):
        
        logging.info("clean old file. %s",self.conf['output'])
        
        if os.path.exists(self.conf['output']):
            os.remove(self.conf['output'])
            
        
    
    def run(self):
        logging.info("==============================")
        
        logging.info("start. self object is %s",self)
        list = self.__request()
        
        if list is None:
            logging.warning("request error.")
            return []
        
        data = []
        
        for item in list:
            result = self.__handler(item)
            if result is None:
                continue
            data.append(result)
        
        self.__write(data)
        
        return data
    
    def __write(self,data):
        # wtire to template 
        template = self.env.get_template(self.conf['template'])
        content = template.render(conf=self.conf,data=data)
        
        logging.info("write file to %s",self.conf['output'])
        
        with open(self.conf['output'], "w", encoding="utf-8") as f:
                f.write(content)


    # 获得标题对象
    def get_title(self,index):
        return index.a
    def get_url(self,index):
        return index.a
    def get_time(self,index):
        return index.p
    
    def handler_title(self,title):
        return title.text
    def handler_time(self,time):
        return time.text
    def handler_url(self,url):
        return url['href']
    
    def __handler(self,index):
        
        title = self.get_title(index)
        time = self.get_time(index)
        url = self.get_url(index)
        
        if title is None or time is None or url is None:
            logging.warning("we have found a None. %s",index.text)
            return None
        
        u = self.handler_url(title)
        t = self.handler_time(time)
        
        return {
            'title': self.handler_title(title),
            'url': self.__cover_url(u),
            'date': self.__cover_date(t)
        }
    
    ## 解析url，
    def __cover_url(self,url):
        
        if url.startswith('http'):
            return url
        return urljoin(self.conf['request'],url)
    
    
    def __cover_date(self,str):
        
        m = re.search('\d{4}.\d{1,2}.\d{1,2}',str)
        
        if m:
            return datetime.strptime(m.group(),self.conf['dateformater']).strftime('%Y-%m-%d')
        else:
            return str
    
    
    def __request_to_file(self,content):
        
        if not os.path.exists('output'):
            os.mkdir('output')
        
        with open(f"output/{self.conf['city']}.request",'w') as f:
            f.write(content)
        
    def __request(self):
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        
        logging.info("request to url=%s",self.conf['request'])
        
        try:
            response = requests.get(self.conf['request'],headers=headers)
            logging.info("response status_code=%s encoding=%s",response.status_code,response.encoding)
        except Exception as e:
            logging.error('request error.',e)
            return None
        
        if 200 != response.status_code:
            return None
        
        # handle encoding.
        if (response.encoding == 'ISO-8859-1'):
            response.encoding = 'utf-8'
        
        self.__request_to_file(response.text)
        
        soup = BeautifulSoup(response.text, "html.parser")
        list = soup.select(self.conf['select'])
        
        logging.info("BeautifulSoup select number is %d", len(list))
        
        return list

# 甘肃省
class Gs(AbstractTown):
    def get_time(self,index):
        return index.span
    
# 陕西省    
class Sx(AbstractTown):
    
    def get_time(self,index):
        return index.time

# 甘肃省
class Bj(AbstractTown):
    def get_time(self,index):
        return index.span
    
# 安徽
class Ah(AbstractTown):
    def get_time(self,index):
        return index.a.font

# 浙江    
class Zj(AbstractTown):
    def get_time(self,index):
        return index
    
    def handler_time(self,time):
        m = re.search(r'\(.+\)',time.text)
        if m:
            return m.group(0)
        
# 江苏
class Js(AbstractTown):
    def get_time(self,index):
        return index.a.span
    
    def handler_title(self,title):
        return title.next

def switch(conf):
    match conf['city']:
        case "北京":
            return Bj(conf)
        case "甘肃":
            return Gs(conf)
        case "陕西":
            return Sx(conf)
        case "安徽":
            return Ah(conf)
        case "浙江":
            return Zj(conf)
        case "江苏":
            return Js(conf)        
        case _:
            return AbstractTown(conf)

def write_readme(list):
    
    # wtire to readme
    template = env.get_template('readme.md')
    content = template.render(list=list)
    
    with open('docs/README.md', "w", encoding="utf-8") as f:
            f.write(content)
    

def main():
    
    with open('config.json') as file:
        json_data = json.load(file)
    
    data = []
    time = datetime.now().strftime('%Y-%m-%d')
    
    for j in json_data:
        d = switch(j).run()
        data.append({
            'conf': j,
            'data': d,
            'time': time
        })
    write_readme(data)    

    
    
if __name__ == "__main__":
    main()