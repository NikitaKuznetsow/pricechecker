import time
import re
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import traceback
import urllib.parse
import os
import pickle
import random

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from time import sleep
from .item import Item

users = [{'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
          'http_proxy': 'http://gXzytP:qHpNAy@91.188.242.153:9083'}]


def create_driver(proxy, headless=True):
    print('create_driver()')

    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--proxy-server=http://XzytP:qHpNAy@91.188.242.153:9083')
    # chrome_options.add_argument('--proxy-server='+proxy)
    chrome_options.add_argument("disable-blink-features=AutomationControlled")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_settings.geolocation": 1,
        "profile.default_content_settings.popups": 0
    })

    caps = DesiredCapabilities().CHROME

    caps["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps, chrome_options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
	  const newProto = navigator.__proto__
	  delete newProto.webdriver
	  navigator.__proto__ = newProto		
	  """
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    caps["pageLoadStrategy"] = "none"
    driver.implicitly_wait(30)

    return driver


def get_ozon_soup(search_url):
    driver = create_driver(proxy=users[0]['http_proxy'])
    driver.get(search_url)
    driver.execute_script(f"window.scrollTo(5, {random.randint(3950, 4050)})")
    driver.find_element(By.CLASS_NAME, "e4")
    soup = bs(driver.page_source, 'html.parser')
    time.sleep(random.randint(5, 10))
    return soup


def get_item_ozon(url):
    soup = get_ozon_soup(url)
    item_json = json.loads(soup.find("script", type="application/ld+json").text)
    item_ = Item(link=item_json['offers']['url'], title=item_json['name'], desc=item_json['description'],
                 brand=item_json['brand'], price=item_json['offers']['price'], links_image=[item_json['image']],
                 rating=item_json['aggregateRating']['ratingValue'], review_count=item_json['aggregateRating']['reviewCount'])
    return item_