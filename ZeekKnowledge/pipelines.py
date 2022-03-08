# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from ZeekKnowledge.items import LogItem


class ZeekknowledgePipeline:
    def __init__(self) -> None:
        self.fp = open('./Zeek Fields.csv', 'w')

    def process_item(self, item: LogItem, spider):
        self.fp.write(item['log'] + '\t' + item['field'] + '\t' + item['types'] + '\t' + item['desc'] + '\n')
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.fp.close()
