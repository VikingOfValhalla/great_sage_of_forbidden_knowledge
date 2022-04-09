import requests
from bs4 import BeautifulSoup
import random


# print(random_int)

url = "http://rosettacode.org/wiki/Category:Programming_Tasks"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

programming_task = []

def compile_list(programming_task):

    random_int = random.randint(0,1147)

    for title in soup.find_all('a'):
        # programming_task.append(title.get_text())
        link = str(title.get('href'))
        task = str(title.get('title'))
        title = (task + "\n" + "http://rosettacode.org" + link)
        title_element = programming_task.append(title)
        programming_task.append(title)

    programming_list = programming_task[31:1178]

    return programming_list[random_int]

