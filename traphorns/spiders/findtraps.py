# -*- coding: utf-8 -*-
import scrapy


class FindtrapsSpider(scrapy.Spider):
    name = 'findtraps'
    allowed_domains = ['utexas.edu']
    start_urls = ['http://utexas.edu/']

    def parse(self, response):
