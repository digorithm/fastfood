import scrapy


class ReceitasRapidasItem(scrapy.Item):
    
    title = scrapy.Field()
    steps = scrapy.Field()
    ingredients = scrapy.Field()
