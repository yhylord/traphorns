# -*- coding: utf-8 -*-
import scrapy


class FindtrapsSpider(scrapy.Spider):
    name = 'findtraps'
    allowed_domains = ['utexas.edu']
    start_urls = ['http://utexas.edu']

    handle_httpstatus_list = [404]

    def parse(self, response):
        if response.status == 404:
            yield {
                'dead_link': response.request.meta.get('redirect_urls',
                                                       [response.url])[0]
            }
        else:
            for link in response.css('a::attr(href)'):
                yield response.follow(link, callback=self.parse)
