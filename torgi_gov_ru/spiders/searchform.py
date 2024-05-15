import scrapy
from scrapy.http import TextResponse, Request
# import 


class SearchformSpider(scrapy.Spider):
    name = "searchform"
    allowed_domains = ["torgi.gov.ru"]
    start_urls = ["https://torgi.gov.ru/new/api/public/lotcards/search?dynSubjRF=12&lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&text=Жилой дом&byFirstVersion=true&withFacets=true&size=10&sort=firstVersionPublicationDate,desc"]

    def parse(self, response: TextResponse):
        with open('response.txt', 'w', encoding='utf-8') as f:
            f.write(response.text,)
        # pass
