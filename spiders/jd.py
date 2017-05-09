# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from web_comments_crawler.items import *
from selenium.common.exceptions import TimeoutException

max_count = 10
max_detail_count = 20
max_pages = 3

class JdSpider(scrapy.Spider):
    count = 0
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = [
        # "http://www.jd-bbs.com/forum-25-1.html"
    ]

    def __init__(self):
        with open("urls/jd.urls") as f:
            for line in f:
                self.start_urls.append(line.strip())
        # self._driver = webdriver.Firefox(firefox_binary="/home/roger/aa/firefox/firefox")
        self._driver = webdriver.Chrome()

    def parse(self, response):
        self._driver.get(response.url)
        # self._driver.set_page_load_timeout(50)
        # self._driver.implicitly_wait(50)
        # try:
        #     wait = WebDriverWait(self._driver, 20)
        #     element = wait.until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@id='plist']"))
        #     )
        #     # self._driver.implicitly_wait(7.)
        # except:
        #     pass
        # finally:
        #     pass

        # extract detail url for product
        items = self._driver.find_elements_by_xpath("//a[@class='comment']")
        detail_urls = []
        for link in items:
            detail_url = link.get_attribute("href")
            # link.click()
            # comments = self._driver.find_elements_by_class_name("comment-con")
            # for comment in comments:
            #     item = dict()
            #     item["content"] = comment.text
            #     yield item
            detail_urls.append(detail_url)
            # for test
            break
            # end test
        # self._driver.close()

        count = 0
        items = []
        for url in detail_urls:
            # self.parse_detail(url)
            # self._driver.get(url)
            # self._driver.set_page_load_timeout(20)
            # self._driver.implicitly_wait(20)
            # self.hello(url)
            try:
                print("crawl detail url: ", url)
                self._driver.maximize_window()
                self._driver.get(url)
                comments = self._driver.find_elements_by_class_name("comment-con")
                for comment in comments:
                    item = dict()
                    item["content"] = comment.text
                    items.append(item)

                pages = 0
                next_button = True
                print("for loop")
                while next_button is not None and pages < max_pages:


                    # comments = self._driver.find_elements_by_class_name("comment-con")
                    print("get item")
                    comment_items = self._driver.find_elements_by_class_name("comment-item")
                    for comment in comment_items:
                        item = dict()
                        content = comment.find_element_by_class_name("comment-con")
                        if content:
                            item["content"] = content.text

                        user = comment.find_element_by_class_name("user-info")
                        if user:
                            item["user_info"] = user.text

                        sprite_praise = comment.find_element_by_class_name("sprite-praise")
                        sprite_comment = comment.find_element_by_class_name("sprite-comment")

                        if sprite_praise:
                            item["sprite_praise"] = sprite_praise.text

                        if sprite_comment:
                            item["sprite_comment"] = sprite_comment.text

                        order_info = comment.find_element_by_class_name("order-info")
                        if order_info:
                            date_elements = order_info.find_elements_by_tag_name("span")
                            if len(date_elements) > 2:
                                item["date_info"] = date_elements[2].text

                        items.append(item)

                    for it in items:
                        yield it

                    next_button = self._driver.find_element_by_class_name("ui-pager-next")
                    print("click next button")
                    print(next_button)
                    next_button.click()
                    time.sleep(5)

                    count += 1
                    if count >= max_count:
                         break

                    # if next_button.is_enabled():
                    pages += 1
                    # break
            except TimeoutException as ex:
                print(ex.message)
            except Exception as ex:
                print("other error occur.")
                print(ex.message)


        # self._driver.close()
        # self._driver.quit()

    # def hello(self, detail_url):
        # self._driver = webdriver.Chrome()
        # self._driver.set_page_load_timeout(20)
        # self._driver.implicitly_wait(20)


        # self._driver.close()

    def __del__(self):
        self._driver.quit()