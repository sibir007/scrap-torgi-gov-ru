import os
import typing
from urllib import request
import scrapy
from scrapy.http import TextResponse, Request
import json
from typing import Optional, Any, List, Dict, Generator
from urllib import parse
from torgi_gov_ru import util 
import items


class SearchformSpider(scrapy.Spider):
    name = "searchform"
    allowed_domains = ["torgi.gov.ru"]
    search_form_json_file = 'spiders/search_form.v3 copy.json'
    # base url for request https://torgi.gov.ru/new/api/public/lotcards/search? 
    # "scheme" + "host" + "filename" from search_form.v3.json
    # request_url_base_str: str
    # dict: key - "namme", value - "default" from search_form.v3 "form" item  
    # request_query_dict: dict[str, str]
    
    # start_urls = ["https://torgi.gov.ru/new/api/public/lotcards/search?dynSubjRF=12&lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&text=Жилой дом&byFirstVersion=true&withFacets=true&size=10&sort=firstVersionPublicationDate,desc"]

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        self.logger.debug(f'kwargs: {kwargs:}')
        # self.logger.debug(f'in __init__{os.getcwd() }')
        if name is not None:
            self.name = name
        elif not getattr(self, "name", None):
            raise ValueError(f"{type(self).__name__} must have a name")
        self.logger.debug(os.getcwd())    
        
        request_url_base_str, request_query_dict = util.get_request_url_base_str_and_request_query_dict_from_search_forv_v3_file(self.search_form_json_file) 
        
        self.logger.debug('util.get_request_url_base_str_and_request_query_dict_from_search_forv_v3_file(self.search_form_json_file) called')
        self.logger.debug(f'request_url_base_str: {request_url_base_str}')
        self.logger.debug(f'request_query_dict: {request_query_dict}')
        
        self.request_url_base_str: str = request_url_base_str
        update_query_dict, update_self_dict = util.unpack_dict(pattern_dict=request_query_dict, unpacked_dict=kwargs)
        
        self.logger.debug(f'update_query_dict: {update_query_dict}')
        self.logger.debug(f'update_self_dict: {update_self_dict}')
        
        wraped_update_query_dict = util.wrap_update_query_dict(update_query_dict)
        
        self.logger.debug(f'wraped_update_query_dict: {wraped_update_query_dict}')
        
        updated_request_query_dict = util.update_request_query_dict(request_query_dict, wraped_update_query_dict)
        self.logger.debug(f'updated_request_query_dict: {updated_request_query_dict}')
        
        updated_request_query_dict_whit_defaul_value = util.fill_required_query_dict_keys_default_values_if_they_not_set(updated_request_query_dict, self.search_form_json_file)
        
        self.logger.debug(f'updated_request_query_dict_whit_defaul_value: {updated_request_query_dict_whit_defaul_value}')
        
        self.request_query_dict: Dict[str, List[str]] = updated_request_query_dict_whit_defaul_value
        # self.logger.debug(f'updated_request_query_dict: {updated_request_query_dict}')
        
        # self.request_query_dict.update(wraped_update_query_dict)

        self.__dict__.update(update_self_dict)
        if not hasattr(self, "start_urls"):
            self.start_urls: List[str] = []
        statr_url = util.get_query_url(self.request_url_base_str, self.request_query_dict)
        self.logger.debug(f'statr_url: {statr_url}')
        self.start_urls.append(statr_url)
        self.notices_url = util.get_notices_url_from_search_form_v3_file(self.search_form_json_file)
        self.base_filename_headers = util.get_base_filename_headers_from_search_form_v3_file(self.search_form_json_file)
        self.notices_filename_headers = util.get_notices_filename_headers_from_search_form_v3_file(self.search_form_json_file)
        self.notices_cache = {}
    
    # def start_requests(self):
    #     yield Request('https://torgi.gov.ru/new/api/public/lotcards/search?lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&byFirstVersion=true&withFacets=true&size=10&sort=firstVersionPublicationDate,desc', self.parse_single_response, headers=self.base_filename_headers)
    
    def parse(self, response: TextResponse) -> Generator:
        resp_str: str = response.text
        resp_dict: Dict = json.loads(resp_str)
        self.total_pages = resp_dict['totalPages']
        self.total_elements = resp_dict['totalElements']
        
        yield from self.parse_lotcards_page(response)        
        for page_num in range(1, self.total_pages -1):
            self.request_query_dict['page'] = [str(page_num)]
            query_url = util.get_query_url(self.request_url_base_str, self.request_query_dict)
            yield Request(query_url, callback=self.parse_lotcards_page, headers=self.base_filename_headers)
        # yield resp_dict
        
        
    def parse_single_response(self, response: TextResponse) -> Generator:
        """пишет в файл content одного запроса"""
        resp_str: str = response.text
        resp_dict: Dict = json.loads(resp_str)
        yield resp_dict

        
        
                
    def parse_lotcards_page(self, response: TextResponse) -> Generator:
        resp_str: str = response.text
        resp_dict: Dict = json.loads(resp_str)
        resp_dict_content: List[Dict[str, Any]] = resp_dict['content']
        for v in resp_dict_content:
            noticeNumber = v['noticeNumber']
            lotNumber = v['lotNumber']
            if (raw_notace_item:=self.notices_cache.get(noticeNumber, None)):
                yield from self.parse_lot(raw_notace_item, lotNumber)                        
            query_url = f'{self.notices_url}/{noticeNumber}'
            headers = self.notices_filename_headers
            headers['Referer'] = f"https://torgi.gov.ru/new/public/notices/view/{noticeNumber}"

            yield Request(query_url, 
                          self.parse_notice, 
                          headers=headers, 
                          cb_kwargs={'lotNumber': lotNumber})
            # item = {
            #     'noticeNumber': v['noticeNumber'],
            #     'lotNumber': v['lotNumber'],
            # }
            # yield item        # pass

    
    def parse_notice(self, response: TextResponse, lotNumber: str):
        notice_str: str = response.text
        notice_dict: Dict = json.loads(notice_str)
        noticeNumber: str = notice_dict['noticeNumber']
        raw_notice_item = self.get_raw_notice_item(notice_dict)
        # raw_notice_item = items.NoticeItem(notice_dict)
        self.notices_cache[noticeNumber] = raw_notice_item
        yield from self.load_notaces_attachments(notice_dict)
        yield from self.parse_lot(raw_notice_item, lotNumber)
        
    def get_raw_notice_item(notice_dict: Dict):
        return {}
        
        
    def parse_lot(raw_notice_item: items.NoticeItem, lotNumber:str) -> Generator:
        yield
    
    def load_notaces_attachments(notice_dict: Dict) -> Generator:
        
        yield
    
    def get_response_request_heades_and_response_data_to_feed_items_v1(self, response: TextResponse) -> Generator:
        req: Request = typing.cast(Request, response.request)
        req_headers: Dict[str, str] = {k:v for k,v in req.headers.to_unicode_dict().items()}
        res_heades: Dict[str, str] = {k:v for k,v in response.headers.to_unicode_dict().items()}
        resp_str: str = response.text
        resp_dict: Dict = json.loads(resp_str)
        item = {
            'request_headers': req_headers,
            'response_headers': res_heades,
            'response_data': resp_dict
        }
        yield item        # pass
    # json()['content']


        # content: list = response.json()['content'] 
        # for item in content:
        #     yield item
        # yield 
        # with open('response.json', 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(response.json(), ensure_ascii=False, indent=4))
        # pass
    # def _get_reqest_url(self, query_kw) -> str:
    #     request_url_base_str, request_query_dict = util.get_request_url_base_str_and_request_query_dict_from_v3_s_form_file('search_form.v3.json') 
        
        
    #     sharch_form_dict: dict = util.load_dict_from_json_file('search_form.v3.json')
    #     request_url_base_str: str = sharch_form_dict['request_url_base']
        
    #     request_query_str: str = self._get_reqest_query_str(sharch_form_dict)
    #     return f'{request_url_base_str}?{request_query_str}'

    # def _get_reqest_query_str(self, sharch_form_dict: dict) -> str:
    #     pass

        
