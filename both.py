import requests
from bs4 import BeautifulSoup
import smtplib
import time

#Amazon Link
URL1 = "https://www.amazon.in/Apple-iPhone-13-256GB-Pink/dp/B09G9HRYFZ/ref=sr_1_3?crid=1N43WR13W7XK6&keywords=iphone+13&qid=1644155984&sprefix=iphone+13%2Caps%2C218&sr=8-3"

#Flipkart Link
URL2 = "https://www.flipkart.com/apple-iphone-13-pink-128-gb/p/itm6e30c6ee045d2?pid=MOBG6VF5GXVFTQ5Y&lid=LSTMOBG6VF5GXVFTQ5YSGQY4O&marketplace=FLIPKART&sattr[]=color&sattr[]=storage&st=storage&otracker=search"
#Set your target price here
budget = 80000  #optional

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.101 Safari/537.36'}

def check_price_amazon():
    page = requests.get(URL1,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    title = soup.find(id='productTitle').get_text()

    price = soup.find(id="priceblock_ourprice").get_text()
    value = price[2:]
    converted_price = float(value.replace(",",""))

    #print('Amazon Title:'+title.strip())
    #print('Amazon Price:'+str(converted_price))

    return converted_price


def check_price_flipkart():
    page = requests.get(URL2,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')

    div_title = soup.find('span',{"class":'B_NuCI'})
    title = str(div_title.text)

    div_price = soup.find('div',{"class":"_30jeq3 _16Jk6d"})
    price = div_price.text
    value = price[1:]
    converted_price = float(value.replace(",",""))

    #print('Flipkart Title:'+title)
    #print('Flipkart Price:'+str(converted_price))

    return converted_price
    

def send_mail(URL,website,price):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('sumith.is18@bmsce.ac.in','omekddnufusdtbuj')

    print('Amazon Price:'+str(price))
    print('Flipkart Price:'+str(price))

    subject = 'Price Alert on '+website+"!!!"
    body = 'Price: '+str(price)+'\nCheck the link: '+URL
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        #from mail address
        'sumith.is18@bmsce.ac.in',
        #to mail address
        'sumithbhat123@gmail.com',
        msg
    )
    print('EMAIL HAS BEEN SENT!')

    server.quit()

while(True):

    if check_price_amazon()<check_price_flipkart():
        if check_price_amazon()<=budget: send_mail(URL1,'Amazon',check_price_amazon())
    elif check_price_amazon()>check_price_flipkart():
        if check_price_flipkart()<=budget: send_mail(URL2,'Flipkart',check_price_flipkart())
    else:
        if (check_price_amazon() or check_price_flipkart())<=budget:
            send_mail(URL1,'Amazon',check_price_amazon())
            send_mail(URL2,'Flipkart',check_price_flipkart())

    time.sleep(60*5)
