# -*- coding: utf-8 -*-
import scrapy

from web_comments_crawler.items import *

max_count = 2000
max_detail_count = 500

class amazonSpider(scrapy.Spider):
    count = 0
    name = "amazon_review_home"
    allowed_domains = ["amazon.cn"]
    start_urls = [
        "https://www.amazon.cn/s?ie=UTF8&page=1&rh=n%3A874269051%2Cp_89%3ASony%20%E7%B4%A2%E5%B0%BC",
        "https://www.amazon.cn/gp/search/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A2016116051%2Cn%3A%212016117051%2Cn%3A874259051%2Cn%3A874269051%2Cp_89%3ASharp+%E5%A4%8F%E6%99%AE&bbn=874269051&sort=review-rank&ie=UTF8&qid=1471943631",
        "https://www.amazon.cn/s/ref=sr_nr_p_89_6?fst=as%3Aoff&rh=n%3A2016116051%2Cn%3A%212016117051%2Cn%3A874259051%2Cn%3A874269051%2Cp_89%3ALG&bbn=874269051&sort=review-rank&ie=UTF8&qid=1471943200",
        "https://www.amazon.cn/s/ref=sr_in_-2_p_89_9?fst=as%3Aoff&rh=n%3A2016116051%2Cn%3A%212016117051%2Cn%3A874259051%2Cn%3A874269051%2Cp_89%3ALG%7CSamsung+%E4%B8%89%E6%98%9F&bbn=874269051&sort=review-rank&ie=UTF8&qid=1471943245&rnid=125596071"
    ]


    def parse(self, response):
        self.logger.debug('start to parse method')
        achors = response.xpath('//a[@class="a-size-small a-link-normal a-text-normal"]/@href')

        if achors:
            for achor in achors:

                url = achor.extract()
                print(type(url))
                if url.find('Reviews') >=0:
                    if (self.count < max_count):
                        self.logger.info('start to crawl %s.', url)
                        yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        achors = response.xpath('//a[@class="a-link-emphasis a-text-bold"]/@href')
        if achors:
            for achor in achors:
                url = achor.extract()
                print(url)
                item = UrlItem()
                item["url"] = url
                yield item







