# -*- coding: utf-8 -*-
import scrapy

from web_comments_crawler.items import *

max_count = 2000
max_detail_count = 500

class JdbbsSpider(scrapy.Spider):
    count = 0
    name = "jd-bbs"
    allowed_domains = ["jd-bbs.com"]
    start_urls = [
        "http://www.jd-bbs.com/forum-25-1.html"
    ]

    # def parse(self, response):
    #     self.parse_articles_follow_next_page(response)

    def parse(self, response):
        self.logger.debug('start to parse method')
        base_url = response.xpath('//base/@href')
        next_page = response.xpath('//a[@class="nxt"]/@href')

        threads = response.xpath('//*[contains(@id, "normalthread")]')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        max_thread = 2
        processed_thread = 0
        for thread in threads:
            item = JdBBSItem()
            content = thread.xpath('tr/descendant::a[contains(@class,"xst")]')
            if content:
                item['topic'] = content.xpath('text()')[0].extract()
                item['detail_url'] = content.xpath('@href')[0].extract()

            authors = thread.xpath('tr/td[@class="by"]/descendant::a/text()')
            if authors:
                item['author_name'] = authors[0].extract()

            update_times = thread.xpath('tr/td[@class="by"]/descendant::em/span/text()')
            if update_times:
                item['update_time'] = update_times[0].extract()

            tweet_count = thread.xpath('tr/td[@class="num"]/descendant::em/text()')
            if tweet_count:
                item['tweet_count'] = tweet_count[0].extract()

            detail_url = thread.xpath('tr/th[@class="new"]/descendant::a[@class="xst"]/@href')
            if detail_url:
                item['detail_url'] = detail_url[0].extract()

            if item['detail_url']:
                # crawle detail page
                detail_page_url = response.urljoin(item['detail_url'])
                # print detail_page_url
                yield scrapy.Request(detail_page_url, callback=self.parse_detail, meta={'item': item})
            else:
                yield item

        if next_page:
            url = response.urljoin(next_page[0].extract())
            self.count += 1
            if (self.count < max_count):
                yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        # from scrapy.shell import  inspect_response
        # inspect_response(response, self)
        item = response.meta['item']
        post_messages = response.xpath('//td[contains(@id, "postmessage")]/text()')
        #
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        if post_messages:
            for post_message in post_messages:
                response_item = JdBBSResponseItem()
                if post_message:
                    message =  post_message.extract()
                    if message.strip():
                        response_item['detail'] = message.strip()
                        self.append_item(item, response_item)

        next_page = response.xpath('//a[@class="nxt"]/@href')
        post_message_count = 0
        if 'response_items' in item:
            post_message_count = len(item['response_items'])

        if next_page and post_message_count < max_detail_count:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, callback=self.parse_detail, meta={'item':item})
        else:
            yield item


    def append_item(self, item, response_item):
        if 'response_items' not in item:
            item['response_items'] = list()

        item['response_items'].append(response_item)





