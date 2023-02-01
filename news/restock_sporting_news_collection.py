import pymongo
from requests_html import HTMLSession
import json
from pymongo import InsertOne
from settings import DATABASE_URL


client = pymongo\
    .MongoClient(DATABASE_URL)

db = client.mexdata_sandbox
collection = db.sporting_news_headers_complete

x = collection.delete_many({})

print(x.deleted_count, " documents deleted.")

session = HTMLSession()
# convert tag into tags multiple tags into dict
# sort by date
# add tweets about every topic
sporting_news_urls = [
    {
        'link':'https://news.google.com/search?q=capitanes%20cdmx&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'CAPITANES NBA G LEAGUE'
    },
    {
        'link':'https://news.google.com/search?q=lfa&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'LFA'
    },
    {
        'link':'https://news.google.com/search?q=lmb&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'LMB'
    },
    {
        'link':'https://news.google.com/search?q=lnbp&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'LNBP'
    },
    {
        'link':'https://news.google.com/search?q=lmp&hl=es-419&gl=MX&ceid=MX%3Aes-419',
        'tag':'LAMP'
    }
]

news_list = []

json_file = {
    "data": []
}

for url in sporting_news_urls:
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

#random.shuffle(news_list)
json_file['data'] = news_list

with open('sportingnewstoday.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(json_file, ensure_ascii=False))

bulk_write_list = []

#with open('newstoday.json') as f:
    #data = json.load(f)
for json_obj in json_file['data']:
    bulk_write_list.append(InsertOne(json_obj))

result = collection.bulk_write(bulk_write_list)
client.close()