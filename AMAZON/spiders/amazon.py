# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from Amazon.items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['http://www.amazon.cn/']
    custom_settings = {
        'REQUEST_HEADERS':{
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        }
    }

    def __init__(self,keyword,*args,**kwargs):
        super(AmazonSpider,self).__init__(*args,**kwargs)
        self.keyword=keyword

    def start_requests(self):
        url='https://www.amazon.cn/s/ref=nb_sb_noss_1?'+urlencode({"field-keywords":self.keyword})
        yield scrapy.Request(url=url,
                             headers=self.settings.get('REQUEST_HEADERS'),
                             callback=self.parse,
                             dont_filter=True
                             )

    def parse(self, response):
        if response.status == 200:
            detail_urls=response.xpath('//*[contains(@id,"result_")]/div/div[3]/div[1]/a/@href').extract()
            for detail_url in detail_urls:
                yield scrapy.Request(url=detail_url,
                                     headers=self.settings.get('REQUEST_HEADERS'),
                                     callback=self.parse_detail,
                                     dont_filter=True
                                     )
            next_url=response.urljoin(response.xpath('//*[@id="pagnNextLink"]/@href').extract_first())
            yield scrapy.Request(url=next_url,
                                 headers=self.settings.get('REQUEST_HEADERS'),
                                 callback=self.parse,
                                 dont_filter=True,
                                 )


    def parse_detail(self,response):
        if response.status == 200:
            name=response.xpath('//*[@id="productTitle"]/text()').extract_first()
            if name:
                name=name.strip()
            # price=response.xpath('//*[@id="price"]//*[@class="a-size-medium a-color-price"]/text()').extract_first()
            price=response.xpath('//*[@id="price"]//*[contains(@class,"a-color-price")]/text()').extract_first()
            delivery_method=''.join(response.xpath('//*[@id="ddmMerchantMessage"]//text()').extract())
            print(response.url)
            print(name)
            print(price)
            print(delivery_method)

            item=AmazonItem()
            item['name']=name
            item['price']=price
            item['delivery_method']=delivery_method
            return item








