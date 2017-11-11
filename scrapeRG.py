import os
import urllib
from bs4 import BeautifulSoup
import requests

url_base = 'http://www.justjared.com'
urls = ['http://www.justjared.com/photos/ryan-gosling/']
for x in range(1,20):
    link = urls[0] + str(x) + '/'
    urls.append(link)

count = 0
for idx, url in enumerate(urls[1:]):
    print('Saving images from page {}'.format(idx+1))
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    imgs = soup.findAll("div", {"class":"tn"})
    for img in imgs:
        imgUrl = url_base + img.a['href']
        req_img = requests.get(imgUrl)
        soup_img = BeautifulSoup(req_img.text, 'html.parser')

        pic = soup_img.find('div', {'class':'mainphoto'})
        picUrl = pic.img['src']

        urllib.request.urlretrieve(picUrl, 'data/raw_images/{}.jpg'.format(count))
        count += 1

print('All done!')
print('A total of {} images were saved.'.format(count))
