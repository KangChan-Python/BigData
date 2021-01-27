

from scrapy.spiders import Spider
from scrapy_splash import SplashRequest


class MySpider(Spider):
    name = 'splashspider'

    # 1. SCRAPING
    def start_requests(self):
        yield SplashRequest(
            url ='http://quotes.toscrape.com/js',
            callback = self.parse
        )

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text' : quote.css("span.text::text").extract_first(),
                'author' : quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract(),
            
            }