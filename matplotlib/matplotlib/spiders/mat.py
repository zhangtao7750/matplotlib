# -*- coding: utf-8 -*-
import scrapy
from matplotlib.items import MatplotlibItem
from scrapy.linkextractors import LinkExtractor


class MatSpider(scrapy.Spider):
    name = 'mat'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        le = LinkExtractor(restrict_css="div.toctree-wrapper.compound", deny='/index.html$')
        # print(len(le.extract_links(response)))
        for link in le.extract_links(response):
            yield scrapy.Request(
                link.url,
                callback=self.parse_detail,
            )

    def parse_detail(self, response):
        href = response.css("a.reference.external::attr(href)").extract_first()
        url = response.urljoin(href)
        item = MatplotlibItem()
        item['file_urls'] = [url]
        yield item
