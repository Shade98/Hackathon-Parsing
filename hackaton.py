import requests as rq
from bs4 import BeautifulSoup as bs
import csv

def main():
    url = 'https://www.cars.com/shopping/results/?page=1&stock_type=all&zip=60606'
    html = get_html(url)
    get_data(html)
    while True:
        try:
            url = get_page(html)
            html = get_html(url)
            get_data(html)
        except Exception as e:
            print(e)
            print('Parsing is complete')
            break

def get_html(url):
    html = rq.get(url)
    return html.text

def get_data(html):
    soup = bs(html,'lxml')
    cars = soup.find('div',class_='vehicle-cards').find_all('div',class_='vehicle-card-main')
    for car in cars:
        url = car.find('a').get('href')
        url = 'https://www.cars.com' + url

        title = car.find('h2',class_='title').text
        price = car.find('span',class_='primary-price').text
        description = get_description(url)        
        milage = car.find('div',class_='mileage')
        if milage == None:
            milage = "Milage not defined"
        else:
            milage = milage.text
        img = car.find('div',class_= 'image-wrap').find('img').get('src')
        if img == '/images/placeholder_10x10.png':
            img = car.find('div',class_= 'image-wrap').find('img').get('data-src')

        data = {
            'title':title,
            'price':price,
            'milage':milage,
            'img':img,
            'description':description
            }
        
        to_file(data)



def get_description(url):
    html = rq.get(url)
    soup = bs(html.text,'lxml')
    description = soup.find('section',class_='sds-page-section seller-notes scrubbed-html')
    h2 = description.find('h2')
    if h2:
        h2 = h2.text
    else:
        h2 = ''
    seller_notes = description.find('div',class_='sellers-notes').text
    batch_tagline = description.find('div',class_='batch-tagline sellers-notes scrubbed-html').text
    description = h2+'\n'+seller_notes+batch_tagline
    return description

def get_page(html):
    soup = bs(html,'lxml')
    page = soup.find('div',class_='sds-pagination__controls').find_all('a')[-1].get('href')
    url = 'https://www.cars.com'+page
    print(url)
    return url

def to_file(data):
    with open('file.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'],data['price'],data['milage'],data['img'],data['description']])

with open('file.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(['title','price','milage','img','description'])

main()