# -*- coding: utf-8 -*-
import scrapy


class FindtrapsSpider(scrapy.Spider):
    name = 'findtraps'
    allowed_domains = ['utexas.edu']
    start_urls = ['http://utexas.edu']

    handle_httpstatus_list = [404]

    def parse(self, response):
        url = response.url
        if response.status == 404:
            req = response.request
            yield {
                # headers in scrapy are bytes, need decoding to be str
                'source': req.headers.get('referer', None).decode(),

                # [url] as fallback when no redirect_urls
                # need to be list so type matches
                'dead_link': req.meta.get('redirect_urls', [url])[0]
            }
        else:
            for link in response.css('a::attr(href)'):
                yield response.follow(link, headers={'referer': url},
                                      callback=self.parse)
