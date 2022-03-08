from attr import field
import scrapy
import re

from ZeekKnowledge.items import LogItem


class ZeekknowledgeSpider(scrapy.Spider):
    name = 'zeekknowledge'
    allowed_domains = ['docs.zeek.org']
    start_urls = ['https://docs.zeek.org/en/lts/script-reference/log-files.html']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.url_regex = re.compile(r'^https://docs.zeek.org/en/lts/scripts/.*::.*Info$')
        self.info_regex = re.compile(r'.*::.*Info')
        self.log_list = []

    def parse(self, response):
        log_urls = response.xpath('//tbody//a/@href').extract()
        for url in log_urls:
            url = response.urljoin(url)
            if self.url_regex.findall(url):
                self.log_list.append(url.split('#')[-1])
                yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response, **kwargs):
        entries = response.xpath("//dl[@class='zeek type']")
        log, fields, descs = '', [], []
        for entry in entries:
            id = entry.xpath('./dt/@id').extract_first()
            if id in self.log_list:
                log = id.replace('type-', '')
                fields = entry.xpath("./dd//dd[@class='field-odd']//dl//dt")
                descs = entry.xpath("./dd//dd[@class='field-odd']//dl//dd")
                break
        if log == '':
            raise Exception('No Log is Found')
        for i in range(len(fields)):
            item = LogItem()
            field, desc = fields[i], descs[i]
            item['log'] = log
            item['field'] = field.xpath(".//text()").extract()[0].replace(': ', '')
            item['types'] = ''.join(field.xpath(".//text()").extract()[1:])
            # item['desc'] = ''.join(desc.xpath('string(.)').extract()).replace('\n', ' ').replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
            item['desc'] = ''.join(desc.xpath(".//text()").extract()).replace('\n', ' ').replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
            yield item
