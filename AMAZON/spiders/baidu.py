# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            errback=self.parse_err,
            dont_filter=True,
        )

    def parse(self, response):
        pass

    def parse_err(self,err):
        print('----->',err)