import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from twilio.rest import Client

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
PAGE_URL = "https://www.costco.com/xbox-series-x-1tb-console-with-additional-controller.product.100691493.html"


def get_twilio_client():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    return Client(account_sid, auth_token)


def send_notification():
    twilio_client = get_twilio_client()
    twilio_client.messages.create(
        body="Costco item is available for purchase!",
        from_=os.getenv("SEND_PHONE_NUMBER"),
        to=os.getenv("RECEIVE_PHONE_NUMBER")
    )


def get_page_html(url):
    headers = {
        "User-Agent": USER_AGENT,
    }
    page = requests.get(url, headers=headers)
    return page.content


def check_item_in_stock(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    out_of_stock_divs = soup.findAll("img", {"class": "oos-overlay hide"})
    return len(out_of_stock_divs) != 0


def check_inventory(url):
    page_html = get_page_html(url)
    if check_item_in_stock(page_html):
        print("Item is in stock!")
        send_notification()
        return True
    else:
        print(f"{datetime.now()} - Item is out of stock... :(")
        return False


def main():
    load_dotenv(os.path.join(os.path.expanduser(os.getcwd()), '.env'))
    while True:
        if check_inventory(PAGE_URL):
            break
        else:
            time.sleep(60)


if __name__ == "__main__":
    main()
