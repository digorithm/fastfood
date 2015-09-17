import scrapy

from HTMLParser import HTMLParser

"""
first version of the first crawler.
I'm learning how to use scrapy, so
this may be extremely poor coded. 
the target website didn't help as well
Other crawlers will be better;

"""

class ReceitasRapidasItem(scrapy.Item):
    
    title = scrapy.Field()
    steps = scrapy.Field()
    ingredients = scrapy.Field()

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    new_text = ' '.join(s.get_data().splitlines())
    return new_text


class ReceitasRapidasSpider(scrapy.Spider):
    name = 'receitas_rapidas'
    allowed_domain = ['receitasrapidas.com']

    start_urls = [
            'http://www.receitasrapidas.com/arroz/arroz-de-tamboril-e-camarao/',
            'http://www.receitasrapidas.com/arroz/arroz-simples/',
            'http://www.receitasrapidas.com/doces-e-sobremesas/bolos-e-tortas-doces/folar-da-pascoa-da-beira-litoral/',
            'http://www.receitasrapidas.com/doces-e-sobremesas/receitas-sobremesas/pudim-de-leite-condensado/',
            'http://www.receitasrapidas.com/receitas-de-marisco/camarao-frito-com-cerveja/',
            'http://www.receitasrapidas.com/doces-e-sobremesas/quindim/',
            'http://www.receitasrapidas.com/doces-e-sobremesas/receitas-sobremesas/pudim-caseiro/',
            'http://www.receitasrapidas.com/doces-e-sobremesas/bolos-e-tortas-doces/biscoitos-de-chocolate/',
            'http://www.receitasrapidas.com/doces-e-sobremesas/folhados-de-gila/']

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
