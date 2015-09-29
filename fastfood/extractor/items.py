import scrapy


class ReceitasRapidasItem(scrapy.Item):
    
    title = scrapy.Field()
    steps = scrapy.Field()
    ingredients = scrapy.Field()

class ReceitasJaItem(scrapy.Item):
    
    title = scrapy.Field()
    steps = scrapy.Field()
    ingredients = scrapy.Field()

