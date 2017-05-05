# -*- coding: utf-8 -*-
import scrapy

from web_comments_crawler.items import *

max_count = 2000
max_detail_count = 500

class amazonSpider(scrapy.Spider):
    count = 0
    name = "amazon"
    allowed_domains = ["amazon.cn"]
    start_urls = [
        # "http://www.jd-bbs.com/forum-25-1.html"
    ]

    def __init__(self):
        with open("amazon.urls") as f:
            for line in f:
                self.start_urls.append(line.strip())
        print(self.start_urls)

    def parse(self, response):
        self.logger.debug('start to parse method')
        base_url = response.xpath('//base/@href')
        next_page = response.xpath('//li[@class="a-last"]/a/@href')
        title = response.xpath('//title/text()')

        threads = response.xpath('//div[@class="a-section review"]')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        max_thread = 2
        processed_thread = 0
        for thread in threads:
            item = AmazonItem()
            if title:
                item['title'] = title[0].extract()
            content = thread.xpath('div[@class="a-row review-data"]/descendant::span/text()')
            c = ""
            if content:
                for s in content.extract():
                    c += s
            if c:
                item['content'] = c

            # authors = thread.xpath('tr/td[@class="by"]/descendant::a/text()')
            # if authors:
            #     item['author_name'] = authors[0].extract()
            #
            # update_times = thread.xpath('tr/td[@class="by"]/descendant::em/span/text()')
            # if update_times:
            #     item['update_time'] = update_times[0].extract()

            yield item

        if next_page:
            url = response.urljoin(next_page[0].extract())
            self.count += 1
            self.logger.warning('No item received for %s', url)
            if (self.count < max_count):
                self.logger.info('start to crawl %s.',url)
                yield scrapy.Request(url, callback=self.parse)
        else:
            self.logger.warning('No next page')

    def parse_detail(self, response):
        # item = response.meta['item']
        # post_messages = response.xpath('//td[contains(@id, "postmessage")]/text()')
        #
        # if post_messages:
        #     for post_message in post_messages:
        #         response_item = JdBBSResponseItem()
        #         if post_message:
        #             message =  post_message.extract()
        #             if message.strip():
        #                 response_item['detail'] = message.strip()
        #                 self.append_item(item, response_item)
        #
        # next_page = response.xpath('//a[@class="nxt"]/@href')
        # post_message_count = 0
        # if 'response_items' in item:
        #     post_message_count = len(item['response_items'])
        #
        # if next_page and post_message_count < max_detail_count:
        #     url = response.urljoin(next_page[0].extract())
        #     yield scrapy.Request(url, callback=self.parse_detail, meta={'item':item})
        # else:
        #     yield item
        pass

    def append_item(self, item, response_item):
        # if 'response_items' not in item:
        #     item['response_items'] = list()
        #
        # item['response_items'].append(response_item)
        pass





