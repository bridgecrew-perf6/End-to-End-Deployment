import scrapy

class IdxcrawlingItem(scrapy.Item):
    ticker_symbol = scrapy.Field()
    company_name = scrapy.Field()
    url = scrapy.Field()
    listing_date = scrapy.Field()
    crawled_at = scrapy.Field()



