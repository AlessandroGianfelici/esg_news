# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
from datetime import datetime

class MySpider(CrawlSpider):
    name = 'gspider'
    allowed_domains = ['esgnews.it']
    start_urls = [r'https://esgnews.it']
    rules = (# Extract and follow all links!
        Rule(LinkExtractor(), callback='parse_item', follow=True), )
    def parse_item(self, response):
        if "esgnews.it" in response.url:
            filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}.html'
            with open(os.path.join("data", filename), 'wb') as f:
                f.write(response.body)
        self.log('crawling'.format(response.url))
