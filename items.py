# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdBBSResponseItem(scrapy.Item):
	detail = scrapy.Field()
	update_time = scrapy.Field()
	author_name = scrapy.Field()

class JdBBSItem(scrapy.Item):
	topic = scrapy.Field()
	author_name = scrapy.Field()
	update_time = scrapy.Field()
	tweet_count = scrapy.Field()
	detail_url = scrapy.Field()
	response_items = scrapy.Field()


class JdItem(scrapy.Item):
	author_name = scrapy.Field()
	content = scrapy.Field()
	update_time = scrapy.Field()

class AmazonItem(scrapy.Item):
	title = scrapy.Field()
	author_name = scrapy.Field()
	content = scrapy.Field()
	update_time = scrapy.Field()

class UrlItem(scrapy.Item):
	url = scrapy.Field()