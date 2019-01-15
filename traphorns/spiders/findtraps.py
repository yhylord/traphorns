# -*- coding: utf-8 -*-
import scrapy


class FindtrapsSpider(scrapy.Spider):
    name = 'findtraps'
    allowed_domains = ['utexas.edu']
    start_urls = ['http://utexas.edu']

    handle_httpstatus_list = [404]

    def parse(self, response):
        url = response.url
        req = response.request
        dead = response.status == 404

        yield {
            # headers in scrapy are bytes, need decoding to be str
            'source': req.headers.get('referer', bytes()).decode(),

            # Two ways to hit 404:
            # 1. Being redirected to a 404 page from the real dead link,
            #    which is redirect_urls[0]
            # 2. redirect_urls are not present,
            #    means the dead link itself returns 404
            # wrap url into list so type matches
            'link': req.meta.get('redirect_urls', [url])[0],
            'dead': dead
        }

        for link in response.css('a::attr(href)'):
            yield response.follow(link, headers={'referer': url},
                                  callback=self.parse)
