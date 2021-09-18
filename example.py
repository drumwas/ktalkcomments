import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin



class MagrebComments(scrapy.Spider):
    name = 'magreb'
    page_number=2
    allowed_domains=['kenyatalk.com']
    start_urls =['https://kenyatalk.com/index.php?search/6727644/']

    custom_settings={
        'DOWNLOAD_DELAY':3,
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }


    ## def a parse to follow the links

    

    def parse(self, response):

        for item in response.xpath('//li[@class="block-row block-row--separated  js-inlineModContainer"]'):
            yield {#comment
                    'comment':item.xpath('.//div[@class="contentRow-snippet"]/text()').get(),
                    #date
                    'date':item.xpath('.//time/@datetime').get(),
                    #forum
                    'forum':item.xpath('.//li[contains(.,"Forum")]/a/text()').get(),
                    #post
                    'post':item.xpath('.//ul[@class="listInline listInline--bullet"]/li[2]/text()').get()
            }
            
        # base_url='https://kenyatalk.com'
        # next_page=response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get()
        # final_url=urljoin(base_url, next_page)
        # cont_url=response.xpath('//a[@class="button--link button"]/@href').get()
        after_page=LinkExtractor(restrict_xpaths=['//a[@class="pageNav-jump pageNav-jump--next"]','//a[@class="button--link button"]']).extract_links(response)[0]

        if after_page.url is not None:
            yield response.follow(after_page, callback=self.parse)

