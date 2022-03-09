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
    log_name = scrapy.Field()
    log_desc=scrapy.Field()
    field_name = scrapy.Field()
    field_type = scrapy.Field()
    field_desc = scrapy.Field()
