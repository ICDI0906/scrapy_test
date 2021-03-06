# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SohutestItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    history = scrapy.Field()
    comments = scrapy.Field()
    # read_nums = scrapy.Field()
    url = scrapy.Field()
