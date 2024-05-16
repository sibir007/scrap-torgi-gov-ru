from urllib import request
import scrapy
from scrapy.http import TextResponse, Request
import json
from typing import Optional, Any, List
from urllib import parse
from torgi_gov_ru import util 


class SearchformSpider(scrapy.Spider):
    name = "searchform"
    search_form_json_file = 'search_form.v3.json'
    allowed_domains = ["torgi.gov.ru"]
    request_url_base_str: str
    request_query_dict: dict
    
    # start_urls = ["https://torgi.gov.ru/new/api/public/lotcards/search?dynSubjRF=12&lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&text=Жилой дом&byFirstVersion=true&withFacets=true&size=10&sort=firstVersionPublicationDate,desc"]

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        if name is not None:
            self.name = name
        elif not getattr(self, "name", None):
            raise ValueError(f"{type(self).__name__} must have a name")
        # self.__dict__.update(kwargs)
        request_url_base_str, request_query_dict = util.get_request_url_base_str_and_request_query_dict_from_v3_s_form_file(self.search_form_json_file) 
        self.request_url_base_str: str = request_url_base_str
        self.request_query_dict: dict = request_query_dict
        self.request_query_dict.update(kwargs)
        if not hasattr(self, "start_urls"):
            self.start_urls: List[str] = []
    
    def start_requests(self):
        yield Request(self.request_url, self.parse)
    
    def parse(self, response: TextResponse):
        content: list = response.json()['content'] 
        for item in content:
            yield item
        # yield 
        # with open('response.json', 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(response.json(), ensure_ascii=False, indent=4))
        # pass
    def _get_reqest_url(self, query_kw) -> str:
        request_url_base_str: str, request_query_dict: dict = util.get_request_url_base_str_and_request_query_dict_from_v3_s_form_file('search_form.v3.json') 
        
        
        sharch_form_dict: dict = util.load_dict_from_json_file('search_form.v3.json')
        request_url_base_str: str = sharch_form_dict['request_url_base']
        
        request_query_str: str = self._get_reqest_query_str(sharch_form_dict)
        return f'{request_url_base_str}?{request_query_str}'

    def _get_reqest_query_str(self, sharch_form_dict: dict) -> str:
        pass

        
