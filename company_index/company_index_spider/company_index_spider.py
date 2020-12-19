import scrapy
from scrapy_splash import SplashRequest
from w3lib.url import urljoin
from datetime import datetime
from ..items import IdxcrawlingItem


class IdxCrawlingSpider(scrapy.Spider):
    name = 'idx'
    allowed_domain = "https://www.idx.co.id"
    start_urls = "https://www.idx.co.id/en-us/listed-companies/company-profiles/"
    def start_requests(self):
            yield SplashRequest(url=self.start_urls, callback=self.parse, dont_filter=False,
                                endpoint='render.html',
                                args={'wait': 5.0})

    def parse(self, response):
        response_data = response.xpath("//tr")
        for each_response in response_data[1:]:
            items = IdxcrawlingItem()
            items['ticker_symbol'] = each_response.xpath(".//td[2]/text()").get()
            items['company_name'] = each_response.xpath(".//td[3]/a/text()").get()
            items['url'] = (urljoin(self.allowed_domain, each_response.xpath(".//td[3]/a/@href").get()))
            items['listing_date'] = each_response.xpath(".//td[4]/text()").get()
            items['crawled_at'] = datetime.today().strftime('%Y-%m-%d')
            yield items
