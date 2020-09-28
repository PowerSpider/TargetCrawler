# -*- coding: utf-8 -*-
# @Time     :   2020/3/30 20:00
# @Author   :   Payne
# @File     :   3-30-selenium.py
# @Software :   PyCharm

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
TIME_OUT = 10
TOTAL_PAGE = 10
browser = webdriver.Chrome()
wait = WebDriverWait(browser, TIME_OUT)


def scrape_page(url, condition, locator):
    logging.info('scraping %s', url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('Error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    url = INDEX_URL.format(page=page)
    scrape_page(url, condition=EC.visibility_of_all_elements_located,
                locator=(By.CSS_SELECTOR, '#index.item'))


def parse_index():
    elements = browser.find_elements_by_css_selector('#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(INDEX_URL, href)


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            logging.info('details urls %s', list(detail_urls))
    finally:
        browser.close()


if __name__ == '__main__':
    main()
