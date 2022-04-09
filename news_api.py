import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('api_key')


response = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={}".format(api_key))

#print(response.title)

json_object = json.loads(response.content)

# json_data = response.json()
articles = json_object["articles"]

articles_dict = []

for element in articles:
    title = str(element.get('title'))
    published = str(element.get('publishedAt'))
    author = str(element.get('author'))
    description = str(element.get('description'))
    url_for_article = str(element.get('url'))
    content = str(element.get('content'))

    element = '''**Title:** {}\n**Date Published:** {}\n**Author:** {}\n**Description**: {}\n\n{}\n\n{}\n
    '''.format(title, published, author, description, content, url_for_article)

    articles_dict.append(element)

articles = articles_dict[6]

# print(articles)
