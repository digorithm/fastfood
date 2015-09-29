import scrapy
import sys
sys.path.append("../../../../fastfood/")

from fastfood.extractor.items import ReceitasJaItem
from fastfood.extractor.utils import strip_tags


# TODO: few recipes have a list of ingredients for each part of the recipe, i'm not handling it yet

class ReceitasJa(scrapy.Spider):
    name = 'receitas_ja'
    allowed_domain = ['receitasja.com']

    start_urls = []
    recipe_urls = []
    """
    with open('receitas_rapidas_urls.txt') as f:
        data = f.read()
        start_urls = data.split('\n')
        del start_urls[-1]
    """
    
    start_urls = ['http://www.receitasja.com/page/' + str(page) for page in xrange(1,41)]

    def parse(self,response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_page_recipe_links)

    def parse_page_recipe_links(self, response):
        recipe_links = response.css('.entry-title a::attr(href)').extract()
        for recipe in recipe_links:
            yield scrapy.Request(recipe, callback=self.parse_recipe_page)

    def parse_recipe_page(self, response):

        item = ReceitasJaItem()

        for sel in response.css('.page-header a::text'):
            item['title'] = sel.extract()
        
        ingredients = response.css('.entry-content ul').extract()[0].split('</li>')
        del ingredients[-1]
        ingredients = map(strip_tags, ingredients)
        item['ingredients'] = ingredients
        
        steps = response.css('.entry-content ul').extract()[1].split('</li>')
        del steps[-1]
        steps = map(strip_tags, steps)
        item['steps'] = steps

        yield item
