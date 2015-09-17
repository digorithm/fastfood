import scrapy
import sys
sys.path.append("../../../../fastfood/")

from fastfood.extractor.items import ReceitasRapidasItem
from fastfood.extractor.utils import strip_tags

"""
first version of the first crawler.
I'm learning how to use scrapy, so
this may be extremely poor coded. 
the target website didn't help as well
Other crawlers will be better;

"""

class ReceitasRapidasSpider(scrapy.Spider):
    name = 'receitas_rapidas'
    allowed_domain = ['receitasrapidas.com']

    start_urls = []
    with open('receitas_rapidas_urls.txt') as f:
        data = f.read()
        start_urls = data.split('\n')
        del start_urls[-1]

    def parse(self,response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_recipe_page)

    def parse_recipe_page(self, response):

        item = ReceitasRapidasItem()

        for sel in response.css('.entry-title a::text'):
            item['title'] = sel.extract()
        
        for sel in response.css('.entry-content ol'):
            steps = sel.extract().split('</li>')
            del steps[-1]
            steps = map(strip_tags, steps)
            item['steps'] = steps
        
        if len(response.css('.entry-content ul'))>1:
            ingredients = response.css('.entry-content ul')[1].extract().split('</li>')
            del ingredients[-1]
            ingredients = map(strip_tags, ingredients)
        
            item['ingredients'] = ingredients

        yield item
