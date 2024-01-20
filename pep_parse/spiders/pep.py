import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        table = response.xpath('//*[@id="numerical-index"]')
        all_peps = table.css('a[href^="pep-"]')
        for pep in all_peps:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        number_name = response.css('h1.page-title::text').get()
        number = number_name.partition(' – ')[0].lstrip('PEP ')
        name = number_name[(number_name.find('–') + 2):]
        data = {
            'number': number,
            'name': name,
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
