import scrapy

class CompanyprofilescrawlItem(scrapy.Item):
    Company_Name = scrapy.Field()
    Security_Code = scrapy.Field()
    Office_address = scrapy.Field()
    Email = scrapy.Field()
    Country = scrapy.Field()
    Phone = scrapy.Field()
    Fax = scrapy.Field()
    NPWP = scrapy.Field()
    Company_Website = scrapy.Field()
    IPO_Date = scrapy.Field()
    Board = scrapy.Field()
    Sector = scrapy.Field()
    Sub_Sector = scrapy.Field()
    Registrar = scrapy.Field()
    Corporate_Secretary = scrapy.Field()
    Director = scrapy.Field()
    Subsidiary = scrapy.Field()


