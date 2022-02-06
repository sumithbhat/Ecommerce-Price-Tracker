import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = "https://www.flipkart.com/apple-iphone-13-pink-128-gb/p/itm6e30c6ee045d2?pid=MOBG6VF5GXVFTQ5Y&lid=LSTMOBG6VF5GXVFTQ5YSGQY4O&marketplace=FLIPKART&sattr[]=color&sattr[]=storage&st=storage&otracker=search"
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.101 Safari/537.36'}

def check_price():
    page = requests.get(URL,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')

    div_title = soup.find('span',{"class":'B_NuCI'})
    title = str(div_title.text)

    div_price = soup.find('div',{"class":"_30jeq3 _16Jk6d"})
    price = div_price.text
    converted_price = float(price[1:3]+price[4:])

    if(converted_price<=18000):
        send_mail(title,converted_price)
        pass

    print(title)
    print(converted_price)

def send_mail(title,converted_price):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('sumith.is18@bmsce.ac.in','omekddnufusdtbuj')

    subject = 'Price Alert!!!'
    #body = 'Product Name: '+title+'\nPrice: '+str(converted_price)+'\nCheck the Link: '+ URL
    body = 'Product: '+'\nCheck the link: '+URL
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

check_price()