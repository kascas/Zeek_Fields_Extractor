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
        self.log_dict = {}

    def parse(self, response):
        entries = response.xpath("//code[@class='file docutils literal notranslate']")
        for entry in entries:
            log_name = entry.xpath(".//text()").extract_first()
            log_desc = self.text_clean(entry.xpath("../../../td[2]/p/text()").extract_first())
            log_url = response.urljoin(entry.xpath("../../../td[3]//a/@href").extract_first())
            self.log_dict[log_url.split('#')[-1].replace('type-', '')] = (log_name, log_desc)
            yield scrapy.Request(log_url.split('#')[0], callback=self.parse_item)

    def parse_item(self, response, **kwargs):
        entries = response.xpath("//dl[@class='zeek type']")
        for entry in entries:
            id = entry.xpath('./dt/@id').extract_first().replace('type-', '')
            if id in self.log_dict:
                (log_name, log_desc) = self.log_dict[id]
                field_names = entry.xpath("./dd//dd[@class='field-odd']//dl//dt")
                field_descs = entry.xpath("./dd//dd[@class='field-odd']//dl//dd")
                for i in range(len(field_names)):
                    item = LogItem()
                    field, desc = field_names[i], field_descs[i]
                    item['log_name'] = log_name
                    item['log_desc'] = log_desc
                    item['field_name'] = field.xpath(".//text()").extract()[0].replace(': ', '')
                    item['field_type'] = ''.join(field.xpath(".//text()").extract()[1:])
                    item['field_desc'] = self.text_clean(''.join(desc.xpath(".//text()").extract()))
                    yield item

    def text_clean(self, s):
        return s.replace('\n', ' ').replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
