import pymongo
from requests_html import HTMLSession
import json
from pymongo import InsertOne
from settings import DATABASE_URL


client = pymongo\
    .MongoClient(DATABASE_URL)

db = client.mexdata_sandbox
collection = db.political_news_headers_complete

x = collection.delete_many({})

print(x.deleted_count, " documents deleted.")

session = HTMLSession()
# convert tag into tags multiple tags into dict
# sort by date
# add tweets about every topic

political_news_urls = [
    {
        'link':'https://news.google.com/search?q=morena&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'MORENA'
    },
    {
        'link':'https://news.google.com/search?q=PAN&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'PAN'
    },
    {
        'link':'https://news.google.com/search?q=PRI&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'PRI'
    },
    {
        'link':'https://news.google.com/search?q=PRD&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'PRD'
    },
    {
        'link':'https://news.google.com/search?q=movimiento%20ciudadano&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'MOVIMIENTO CIUDADANO'
    }
]

news_list = []

json_file = {
    "data": []
}

for url in political_news_urls:
    response = session.get(url['link'])
    response.html.render(sleep=1, scrolldown=1)
    articles = response.html.find('article')

    for article in articles:
        try:
            news_row = article.find('h3', first=True)
            news_item = {
                'title': news_row.text,
                'link': list(news_row.absolute_links)[0],
                'tag': url['tag']
            }
            news_list.append(news_item)
        except:
            pass

json_file['data'] = news_list

with open('politicalnewstoday.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(json_file, ensure_ascii=False))

bulk_write_list = []

for json_obj in json_file['data']:
    bulk_write_list.append(InsertOne(json_obj))

result = collection.bulk_write(bulk_write_list)
client.close()


#with open('newstoday.json') as f:
    #data = json.load(f)