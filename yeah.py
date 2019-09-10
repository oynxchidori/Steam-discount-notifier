# An application notifying you the price of a game you desire with an email when an discount happens.
import requests
from bs4 import BeautifulSoup
import smtplib
import time


def notifier():
    Url = input('Input the URL of the store page of the game you want on Steam :\n')
    agent_info = input('Input the user agent of your browser: (You can find this by searching for "my user agent" on Google) \n')
    agent = {'User-Agent': agent_info}
    gmail = input("Your gmail address (Notification will be sent from this address): \n")
    app_pass = input("Your app password for Gmail (not your Gmail password): \n")
    receive = input("The email address that you want to use to receive the notification: \n")

    page_info=requests.get(Url, headers=agent)
    refined = BeautifulSoup(page_info.content, 'html.parser')
    if 'discount_final_price' in refined.prettify():
        name = refined.find(attrs={"class": "apphub_AppName"}).get_text().strip()
        discount = refined.find(attrs={"class": "discount_pct"}).get_text().strip()
        countdown = refined.find(attrs={"class": "game_purchase_discount_countdown"}).get_text().strip()
        price = refined.find(attrs={"class": "discount_final_price"}).get_text().strip()
        price_msg = f" The current price is {price} and on a discount of {discount}. Check out at {Url}!"
        subject = name + ' '+'is on discount!'
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail, app_pass)
        body = countdown+price_msg
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(gmail, receive, message)
        server.quit()
        print("Email has been sent!\n")


while(1):
    notifier()
    time.sleep(3600)
