import requests
from lxml import html
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_web_driver = ChromeDriverManager().install()


def get_tree(url: str, filename=None):
    headers = {'Content-Type': 'text/html', }
    response = requests.get(url, headers=headers)
    html_raw = response.text

    tree = html.fromstring(html_raw)

    return tree


def get_tree_by_driver(url: str, filename=None):
    driver = webdriver.Chrome(chrome_web_driver)
    driver.get(url)
    time.sleep(1)

    html_element = driver.find_element_by_css_selector("html")
    tree = html.fromstring(html_element.get_attribute('innerHTML'))
    # driver.close()
    return tree


