# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZeekknowledgeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LogItem(scrapy.Item):
    log = scrapy.Field()
    field = scrapy.Field()
    types = scrapy.Field()
    attr = scrapy.Field()
    desc = scrapy.Field()
