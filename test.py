import requests

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
from datetime import datetime

domain = "https://www.sceea.cn"
env = Environment(loader=FileSystemLoader("templates/"))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}


response = requests.get("https://www.ahzsks.cn/gdjyzxks/search2.jsp?c=77",headers=headers)
print(response.encoding)

print(response.text)

soup = BeautifulSoup(response.text, "html.parser")
list = soup.select(".classnews-list li")

print(list)