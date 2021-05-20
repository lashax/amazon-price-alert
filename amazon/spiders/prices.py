import scrapy
from scrapy_splash import SplashRequest
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from amazon.items import AmazonItem
from amazon.user_input import AMAZON_URLS


class PricesSpider(scrapy.Spider):
    name = 'prices'
    start_urls = AMAZON_URLS

    def start_requests(self):
        for url in self.start_urls:
            script = """
            function main(splash)
            assert(splash:go(splash.args.url))
            assert(splash:wait(1))
            return {html = splash:html(),}
            end
            """
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response, **kwargs):
        loader = ItemLoader(AmazonItem(), response=response)
        loader.default_output_processor = TakeFirst()

        # Price of an item can be in one of the following xpath
        possible_xpath = ('//*[@id="price_inside_buybox"]/text()',
                           '//*[@id="price"]/text()',
                           '//span/span[@class="a-text-normal"]/text()',
                           '//*[@id="kindle-price"]/text()',
                           '//span[@class="a-button-inner"]/text()'
                           '//a[@href="javascript:void(0)"]/span[2]/text()',
                           '//span[@class="a-size-base a-color-price"]/text()',
                           '//span[@class="a-size-medium a-color-price"]/text()')

        for xpath in possible_xpath:
            value = loader.get_xpath(xpath)
            if value:
                loader.add_value('price', value)
                break

        # If no price was found, assign a default value
        if not loader.get_output_value('price'):
            loader.add_value('price', 'Error: Price not available!')

        loader.add_xpath('_id', '//*[@id="averageCustomerReviews"]/@data-asin')
        loader.add_xpath('name', '//*[@id="productTitle"]/text()')
        loader.add_value('url', response.url)

        yield loader.load_item()
