
# from tkinter.messagebox import NO
# from re import X
# from attr import field
# from networkx import difference
from tkinter import NO
from uu import Error
from playwright.sync_api import sync_playwright, Browser, Page, Request, Response
from typing import Iterable, Dict, Generator, NoReturn, Set, Tuple, List, FrozenSet, Union, Any, Callable
import typing
from urllib import parse, request
from lxml import html
from contextlib import contextmanager
import pickle
import json
import os
from pathlib import Path
import lxml
# import brotli
import shutil
import pydlib as dl
from datetime import datetime
import logging
from collections import defaultdict

# from importlib import simple



logger = logging.getLogger(__name__)

def logging_configure(logger, log_level: int):
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    fm = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fm)
    logger.addHandler(ch)




"""data time example
now = datetime.datetime.now()  # Get the current datetime object
formatted_date = now.strftime("%d.%m.%y_%H-%M-%S")
"""

def get_curent_date_time() -> str:
    now = datetime.now()  # Get the current datetime object
    formatted_date = now.strftime("%d.%m.%y_%H-%M-%S")
    return formatted_date

VZLJOT_PROXY = {
  'http': 'http://SibiryakovDO:vzlsoFia1302@proxy:3128',
  'https': 'http://SibiryakovDO:vzlsoFia1302@proxy:3128',
}
BACKUP_DIR = 'backup/'
NEW_PYBLIC_LINK = 'https://torgi.gov.ru/new/public'
NEW_PYBLIC_LOTS_REG_LINK = 'https://torgi.gov.ru/new/public/lots/reg'
HEADERS_DIR = 'headers/'
HEADERS_FILE_EXTENSION = '.headers.json'
COOKIES_DIR = 'coodies/'
COOKIES_FIEL_EXTENSION = '.cookies'
GENERAL_COOKIES_FILE_NAME = 'general' + COOKIES_FIEL_EXTENSION
UBUNTY_HEADERS_JSON_FILE = 'ubuntu_chromium_version_122.0.6261.128.headers.json'
EXCEL_LINK = 'https://torgi.gov.ru/new/api/public/lotcards/export/excel?lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&biddEndFrom=&biddEndTo=&pubFrom=&pubTo=&aucStartFrom=&aucStartTo=&text=&amoOrgCode=&npa=&byFirstVersion=true&sort=firstVersionPublicationDate,desc'
EXCEL_LINK_DICT = {
	"GET": {
		"scheme": "https",
		"host": "torgi.gov.ru",
		"filename": "/new/api/public/lotcards/export/excel",
		"query": {
			"lotStatus": "PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER",
			"biddEndFrom": "",
			"biddEndTo": "",
			"pubFrom": "",
			"pubTo": "",
			"aucStartFrom": "",
			"aucStartTo": "",
			"catCode": "7",
			"text": "",
			"amoOrgCode": "",
			"npa": "",
			"byFirstVersion": "true",
			"sort": "firstVersionPublicationDate,desc"
		},
		"remote": {
			"Address": "95.167.245.141:443"
		}
	}
}
TORGI_GOV_SEARSH_LINK = 'https://torgi.gov.ru/new/api/public/lotcards/search?lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&byFirstVersion=true&withFacets=true&size=10&sort=firstVersionPublicationDate,desc'
TORGI_GOV_SEARSH_DICT = {
	"GET": {
		"scheme": "https",
		"host": "torgi.gov.ru",
		"filename": "/new/api/public/lotcards/search",
		"query": {
			"lotStatus": "PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER",
			"byFirstVersion": "true",
			"withFacets": "true",
			"size": "10",
			"sort": "firstVersionPublicationDate,desc"
		},
		"remote": {
			"Address": "95.167.245.141:443"
		}
	}
}
TORGI_GOV_SEARSH_DICT2 = {
    "GET": {
        "scheme": "https",
        "host": "torgi.gov.ru",
        "filename": "/new/api/public/lotcards/search",
        "query": {
            "dynSubjRF": "12",
            "lotStatus": "PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER",
            "text": "жилой дом",
            "byFirstVersion": "true",
            "withFacets": "true",
            "size": "10",
            "sort": "firstVersionPublicationDate,desc"
        },
        "remote": {
            "Address": "95.167.245.141:443"
        }
    }
}

TORGI_GOV_NOTICES_URL = 'https://torgi.gov.ru/new/api/public/notices/noticeNumber/23000051770000000058'

TORGI_GOV_QUERY2 = {
            "lotStatus": "PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER",
            "text": "жилой дом",
            "size": "10",
        }
TORGI_GOV_QUERY2_STR = """-a lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER -a text="жилой дом" -a size=10"""
VZLJOT_PROXY = {
  'http': 'http://SibiryakovDO:vzlsOfia1302@proxy:3128',
  'https': 'http://SibiryakovDO:vzlsOfia1302@proxy:3128',
}
TORGI_GOV_QUERY3_STR = '-a lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER  -a size=10 -a some_extra_key=some_extra_value -a text="Жилой дом" -a dynSubjRF=12,80 -a catCode=7'

NEW_API_PUBLIC_NOTICES_NOTICENUMBE = {
	"GET": {
		"scheme": "https",
		"host": "torgi.gov.ru",
		"filename": "/new/api/public/notices/noticeNumber/23000051770000000058",
		"remote": {
			"Address": "95.167.245.141:443"
		}
	},
 "Response Headers (406 B)": {
		"headers": [
			{
				"name": "Cache-Control",
				"value": "no-cache, no-store, max-age=0, must-revalidate"
			},
			{
				"name": "Connection",
				"value": "keep-alive"
			},
			{
				"name": "Content-Type",
				"value": "application/json"
			},
			{
				"name": "Date",
				"value": "Sun, 19 May 2024 10:19:56 GMT"
			},
			{
				"name": "Expires",
				"value": "0"
			},
			{
				"name": "Pragma",
				"value": "no-cache"
			},
			{
				"name": "Server",
				"value": "nginx"
			},
			{
				"name": "Strict-Transport-Security",
				"value": "max-age=31536000 ; includeSubDomains"
			},
			{
				"name": "Transfer-Encoding",
				"value": "chunked"
			},
			{
				"name": "X-Content-Type-Options",
				"value": "nosniff"
			},
			{
				"name": "X-Frame-Options",
				"value": "SAMEORIGIN"
			},
			{
				"name": "X-XSS-Protection",
				"value": "1; mode=block"
			}
		]
	
}
}

# HTTP/1.1 200 
# Server: nginx
# Date: Sun, 19 May 2024 10:19:56 GMT
# Content-Type: application/json
# Transfer-Encoding: chunked
# Connection: keep-alive
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Cache-Control: no-cache, no-store, max-age=0, must-revalidate
# Pragma: no-cache
# Expires: 0
# Strict-Transport-Security: max-age=31536000 ; includeSubDomains
# X-Frame-Options: SAMEORIGIN

url_parts = ('scheme', 'netloc', 'path', 'params', 'query', 'fragment')
linc = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D1%83%D0%B7%D0%B5%D0%BB+%D1%83%D1%87%D1%91%D1%82%D0%B0&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'

@contextmanager
def pretty_print(fun_name: Callable):
    print(f'----------{fun_name.__name__}----------')
    yield
    print('-------------------------------')



def print_dict(d: dict, level: int = 0):
    shift = 4
    for k, v in d.items():
        print(level*4*' ' + f'{k}: {v}')
    

def print_unquoted_url(url: str):
    with pretty_print(print_unquoted_url):
        linc_unquot = parse.unquote_plus(url)
        print(linc_unquot)
    

def print_parsed_url(url: str):
    with pretty_print(print_parsed_url):
        linc_unquot = parse.unquote_plus(url)
        linc_parsed = parse.urlparse(linc_unquot)
        linc_parsed_dict = linc_parsed._asdict()
        query_str = linc_parsed_dict['query']
        del linc_parsed_dict['query']
        query_dict = parse.parse_qs(query_str)
        print_dict(linc_parsed_dict)
        print('query - ')
        print_dict(query_dict, level=1)



def parse_raw_headers_from_file_to_dict(file: str) -> dict:
    header_dict = {}
    with open(file, 'rt') as f:
        for line in f:
            ind = line.find(':')
            head, tail = line[:ind], line[ind+1:]
            header_dict[head.strip()] = tail.strip()
    return header_dict

# def parse_raw_headers_from_file_to_dict_and_write_json_to_file(fname_from: str, fname_to: str = 'test-header.json'):
#     """
#     """
#     h_dict = parse_raw_headers_to_dict(fname_from)
#     write_header_dict_to_json_file(fname_to, h_dict)
                

def get_netloc(linc: str) -> str:
    """return netloc frome linc string

    Args:
        linc (str): linc, url

    Returns:
        str: netloc
    """
    parse_linc = parse.urlparse(linc)
    return parse_linc.netloc

        
        
def write_headers_frome_file_to_file_as_dict(hfile: str, fname: str = 'test'):
    hdict = parse_raw_headers_from_file_to_dict(hfile)
    write_header_dect_to_file(hdict=hdict, fname=fname)
   
   
def load_header_dict(fname: str) -> dict:
    """load from file header dict

    Args:
        fname (str): file name

    Returns:
        dict: header dict
    """
    with open(fname, 'rb') as f:
        hdict = pickle.load(f)
    return hdict

def load_dict_or_list_from_json_file(fname: str) -> Union[Dict, List]:
    """load from json file header dict

    Args:
        fname (str): file name

    Returns:
        dict: header dict
    """
    logger.debug(f'in load_dict_from_json_file(fname: str) os.getcwd(): {os.getcwd()}')
    with open(fname, 'rt', encoding='utf-8') as f:
        data = f.read()
        hdict = json.loads(data)
    return hdict

def write_header_dect_to_file(hdict: dict, fname: str = 'test'):
    """write headers in dict to file

    Args:
        hdict (dict): dect headers
        fname (str, optional): file name. Defaults to 'test'.
    """
    with open(f'{fname}.headers', 'wb') as f:
        pickle.dump(hdict, f)


def write_dict_or_list_to_json_file(fname: str, obj: Union[List, Dict]):
    """load to json file header dict

    Args:
        fname (str): file name
        hdict (dict): header dict
    """
    with open(fname, 'wt', encoding='utf-8') as f:
        json_str = json.dumps(obj, indent=4, ensure_ascii=False)
        f.write(json_str)
        

def write_unquoted_link_in_file(link: str, fname: str = 'unqoted-lincs.txt'):
    """write unquoted link to file

    Args:
        link (str): linc to write
        fname (str, optional): file name. Defaults to 'unqoted-lincs.txt'.
       
    """
    unquoted_link = parse.unquote_plus(link)
    with open(fname, 'at') as f:
        f.write(unquoted_link)

def cookies_file_name_frome_link(link: str) -> str:
    """return cookies file name frome link

    Args:
        link (str): linck

    Returns:
        str: cookies file name
    """
    return get_netloc(link) + COOKIES_FIEL_EXTENSION




# def decompress_brotli_from_file_to_file(fname_from: str, fname_to):
#     with open(fname_from, 'rb') as fr:
#         with open(fname_to, 'wb') as fw:
#             fw.write(brotli.decompress(fr.read()))

def test_quoting():
    search_link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={searchString}&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber={pageNumber}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'
    search_link_unquoted = parse.unquote_plus(search_link)
    print(search_link_unquoted)
    print(parse.quote(search_link_unquoted))
    'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={searchString}&morphology=on&search-filter=Дате размещения&pageNumber={pageNumber}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'

# write_headers_frome_file_to_file_as_dict('windows-chrome-headers.txt', 'windows-chrome-headers.txt')
# parse_raw_headers_to_dict('windows-chrome-headers.txt')
# parse_raw_headers_from_file_to_dict_and_write_json_to_file('windows-chrome-headers.txt', 'windows-chrome-headers.json')
                    # # НАЧАЛО----------------------- Работа с query --------------------------------
                    # link2 =          'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D1%83%D0%B7%D0%B5%D0%BB+%D1%83%D1%87%D1%91%D1%82%D0%B0&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'
                    # link2_unquoted = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=узел учёта&morphology=on&search-filter=Дате размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1'
                    # linc2_quoted_plus = 'https%3A%2F%2Fzakupki.gov.ru%2Fepz%2Forder%2Fextendedsearch%2Fresults.html%3FsearchString%3D%D1%83%D0%B7%D0%B5%D0%BB+%D1%83%D1%87%D1%91%D1%82%D0%B0%26morphology%3Don%26search-filter%3D%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F%26pageNumber%3D1%26sortDirection%3Dfalse%26recordsPerPage%3D_10%26showLotsInfoHidden%3Dfalse%26sortBy%3DUPDATE_DATE%26fz44%3Don%26fz223%3Don%26af%3Don%26ca%3Don%26pc%3Don%26pa%3Don%26currencyIdGeneral%3D-1'
                    # link2_parsed = parse.urlparse(link2)
                    # link2_query = link2_parsed.query
                    # link2_query_unquoted = parse.unquote_plus(link2_query)
                    # link2_query_unquoted_parsed = parse.parse_qs(link2_query_unquoted)
                    # print_dict(link2_query_unquoted_parsed)
                    # link2_query_unquoted_parsed_back = parse.urlencode(link2_query_unquoted_parsed, doseq=True)
                    # print()
                    # print(link2_query_unquoted_parsed_back)
                    # print()

                    # link2_back = link2_parsed._replace(query=link2_query_unquoted_parsed_back).geturl()
                    # print(link2_back)
                    # print(link2==link2_back)

                    # # КОНЕЦ----------------------- Работа с query --------------------------------


def get_request_response_headers(link: str, browser: str = 'firefox') -> Tuple[Dict[str, str], Dict[str, str]]:
    """accept link return tuple response request headers dicts

    Args:
        link (str): link
        browser (str): browser type 
    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: tuple reqvest response headers dict
    """
    resp_headers: Dict[str, str]
    req_headers: Dict[str, str]
    # cookies: 
    with sync_playwright() as p:
        # p.chromium.launch(headless=False, slow_mo=50)
        browser_impl: Browser = getattr(p, browser).launch(headless=False, slow_mo=50)
        page: Page = browser_impl.new_page()
        
        response: Union[Response, None]= page.goto(link)
        if not response:
            raise RuntimeError('page.goto(link) return None value')
        resp_headers = response.all_headers()
        req_headers = response.request.all_headers()
        browser_impl.close()
        

    return req_headers, resp_headers

# for d in get_request_response_headers(NEW_PYBLIC_LOTS_REG_LINK):
#      print_dict(d)
# # print()
def _get_request_json_response_dicts_dict_calback(result: list) -> Callable[["Request"], "None"]:
    # result_list = result
    def request_json_response_dicts_list_calback(request):
        response: Union[Response, None] = request.response()
        if not response:
            raise RuntimeError('request.response() return None')
        if response.header_value('content-type') == 'application/json':
            result_dict = {}
            result_dict['request_url'] = request.url
            result_dict['request_headers'] = request.all_headers()
            result_dict['response_headers'] = response.all_headers()
            result_dict['response_json'] = response.json()
            # req_url = request.url
            # resp_json = request.response().json()
            result.append(result_dict)
        # pass
    return request_json_response_dicts_list_calback
        
def get_request_json_response_dicts_list(linc: str, browser: str = 'firefox') -> List[Dict]:
    result: list = []
    with sync_playwright() as p:
        browser_impl: Browser = getattr(p, browser).launch(headless=False, slow_mo=50)
        page: Page = browser_impl.new_page()
        page.on('requestfinished', _get_request_json_response_dicts_dict_calback(result))
        page.goto(linc)
        browser_impl.close()
    return result

# def get_request_json_response_dicts_dict(linc: str, browser: str = 'firefox') -> Dict[str, Dict]:
    
    
    
#     result: dict = {}
#     with sync_playwright() as p:
#         browser_impl: Browser = getattr(p, browser).launch(headless=False, slow_mo=50)
#         page: Page = browser_impl.new_page()
#         page.on("requestfinished", _get_request_json_response_dicts_dict_calback(result))
#         page.goto(linc)
#         browser_impl.close()
#     return result



# TODO: implement
def _get_ownership_form_list__check_version(request_info2_data: dict, fun_version: str) -> bool:
    """проверка соответствии версии функции get_ownership_form_list(fname: str) 
    и версии апи указанной в request_info2.json  файле. Печатае результа в stdout

    Args:
        request_info2_data (dict): request_info2.json dict
        fun_version (str): version get_ownership_form_list()
    Returns:
        Union[True, False]: True or False for caler fun
    """
    return True

def get_ownership(fname: str, return_value: str = 'list') -> Union[List[str], Dict[str, str]]:
    """accept request_info2.json file format and type return value, 
    return list ownership code or dict ownership_code:ownership_name 

    Args:
        fname (str): json file format request_info2.json
        return_value (str) 'list' or 'dict', defaul 'list': return value list [ownership_code] or dict {ownership_code:ownership_name}
    Returns:
        Union[List[str], Dict[str, str]]: list [ownership_code] or dict {ownership_code:ownership_name}
    """
    #version torgi.gov.ru for check
    # version_api = '3.1'
    # ownershp_code_list: list[str]
    # with open(fname, 'rb') as f:
    #     data_json = f.read()
    #     # try
    #     data_dict = json.loads(data_json)
        # # TODO: обработать вызов
        # _get_ownership_form_list__check_version(data_dict, version_api)
        # ownershp_dict_list: list[dict] = data_dict['https://torgi.gov.ru/new/nsi/v1/OWNERSHIP_FORM']['response_json']
        # if return_value == 'dict':
        #     ownershp_result: dict[str, str] = {ownershp_dict['code']: ownershp_dict['name'] for ownershp_dict in ownershp_dict_list}
        # else:
        #     ownershp_result: list[str] = [ownershp_dict['code'] for ownershp_dict in ownershp_dict_list]
    return get_relationship(fname=fname, 
                            url='https://torgi.gov.ru/new/nsi/v1/OWNERSHIP_FORM', 
                            code='code',
                            value='name',
                            return_value=return_value)


def get_relationship(fname: str, url: str, code: str, value: str, return_value: str = 'list') -> Union[List[str], Dict[str, str]]:
    """accept request_info2.json file format, url, code str, value str and type return value, 
    return list relationship code or dict relationship_code:relationship_name 
    url['response_json'] obgect must be form [{code: some_code_value, value:some_value_value, ...}, {}, {}]

    Args:
        fname (str): json file format request_info2.json
        url (str): url str for search in file
        code (str): code str
        value (str): value str
        return_value (str) 'list' or 'dict', defaul 'list': return value list [some_code_value, ...] or dict {some_code_value:some_value_value, ...}
    Returns:
        Union[List[str], Dict[str, str]]: list [some_code_value, some_code_value, ...] or dict {some_code_value:some_value_value, some_code_value:some_value_value, ...}
    """
    #version torgi.gov.ru for check
    version_api = '3.1'
    # ownershp_code_list: list[str]
    with open(fname, 'rb') as f:
        data_json = f.read()
        # try
        data_dict = json.loads(data_json)
        
        # TODO: обработать вызов
        _get_ownership_form_list__check_version(data_dict, version_api)
        
        
        
        relationship_dict_list: List[dict] = data_dict[url]['response_json']
        if return_value == 'dict':
            return {relationship_dict[code]: relationship_dict[value] for relationship_dict in relationship_dict_list}
            # relationship_result: Dict[str, str] = {relationship_dict[code]: relationship_dict[value] for relationship_dict in relationship_dict_list}
        else:
            return [relationship_dict[code] for relationship_dict in relationship_dict_list]
            # relationship_result: List[str] = [relationship_dict[code] for relationship_dict in relationship_dict_list]
    # return relationship_result

def get_dict_values(d: dict, path: str) -> List[Any]:
    return typing.cast(List[Any], dl.get(d, path, sep='`'))

def get_relationship_v2(info2_fname: str, 
                        code_path: str, 
                        code_key: str, 
                        value_path: str, 
                        value_key: str,
                        ) -> Dict[str, str]:
    """accept request_info2.json file format, code_path, code_key, value_path, value_key
    and type return value, return dict {code:value, ...} 

    Args:
        info2_fname (str): json file format request_info2.json
        code_path (str): path to code dict, forma: a`b`c
        code_key (str):  code key
        value_path (str): path to value dict, forma: a`b`c
        value_key (str):  value key
    Returns:
        Dict[str, str]: dict {some_code_value:some_value_value, some_code_value:some_value_value, ...}
    """
    #version torgi.gov.ru for check
    version_api = '3.1'
    # ownershp_code_list: list[str]
    # with open(info2_fname, 'rb') as f:
    #     data_json = f.read()
    #     # try
    #     data_dict = json.loads(data_json)
    data_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(info2_fname))     
    # TODO: обработать вызов
    _get_ownership_form_list__check_version(data_dict, version_api)
    
    
    
    key_list: list[Any] = get_dict_values(data_dict, code_path + '`' + code_key)
    value_list: list[Any] =   get_dict_values(data_dict, value_path + '`' + value_key)
 
    key_value_zip = zip(key_list, value_list)    
    # if return_value == 'dict':
    key_value_dict: dict[str, str] = {key: value for key, value in key_value_zip}
        # else:
            # relationship_result: list[str] = [relationship_dict[code_path] for relationship_dict in relationship_dict_list]
    return key_value_dict

# TODO: доделать версию 3. available_values_hint.values

def get_relationship_v3(info2_fname: str, 
                        path: str, 
                        code_key: str,
                        value_key: str, 
                        parent_key: str
                        ) -> Dict[str, Dict[str, str]]:
    """accept request_info2.json file format, code_path, code_key, value_path, value_key
    and type return value, return dict {code:value, ...} 

    Args:
        info2_fname (str): json file format request_info2.json
        code_path (str): path to code dict, forma: a`b`c
        code_key (str):  code key
        value_path (str): path to value dict, forma: a`b`c
        value_key (str):  value key
    Returns:
        Dict[str, str]: dict {some_code_value:some_value_value, some_code_value:some_value_value, ...}
    """
    #version torgi.gov.ru for check
    version_api = '3.1'
    # ownershp_code_list: list[str]
    # with open(info2_fname, 'rb') as f:
    #     data_json = f.read()
    #     # try
    #     data_dict = json.loads(data_json)
    data_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(info2_fname))     
    # TODO: обработать вызов
    _get_ownership_form_list__check_version(data_dict, version_api)
    
    
    
    dict_list: List[dict] = typing.cast(List[dict], dl.get(data_dict, path, sep='`')) 
    # # for Субъект местонахождения имущества only"
    "--------------разкоментировать для Субъект местонахождения имущества--------------------"
    # dict_list = dict_list[0]['mappingTable']
    # print(len(dict_list))
    # print(path)
    res_dict: dict = {}
    for item in dict_list:
        code_value = dl.get(item, code_key, sep='`')
        value_value = dl.get(item, value_key, sep='`')
        parent_value = dl.get(item, parent_key, sep='`')
        res_dict[code_value] = {'name': value_value, 'parent': parent_value}

            # relationship_result: list[str] = [relationship_dict[code_path] for relationship_dict in relationship_dict_list]
    return res_dict



def _get_key_valu_dicts(code_path, value_path, relationship_dict_list):
    for d in relationship_dict_list:
        target_relationship_key_dict: dict = d
        for key in code_path:
            if not (target_relationship_key_dict := target_relationship_key_dict.get(key, {})):
                break
        if not target_relationship_key_dict:
            continue
        target_relationship_value_dict: dict = d
        for key in value_path:
            if not (target_relationship_value_dict := target_relationship_value_dict.get(key, {})):
                break
        if not target_relationship_value_dict:
            continue
        yield target_relationship_key_dict, target_relationship_value_dict
    #     target_relationship_key_dict_list.append(target_relationship_key_dict)
    #     target_relationship_value_dict_list.append(target_relationship_value_dict)
    #     zip_dict_lists = zip(target_relationship_key_dict_list, target_relationship_value_dict_list)
    # return zip_dict_lists



def write_value_to_dict_in_json_file(fname: str, target_dict_paths: List[str], key_for_insert: str, value_for_insert: Union[list, dict]):
    """принимает json файл, путь и значение для вставки в json
    если target_dict_paths не существуе - создаёт его

    Args:
        fname (str): json file name
        target_dict_paths (List[str]): list string to dict
        key_for_insert (str): key name for insert value
        value_for_insert (Union[str, dict]): list or dict for inserting
    """
    
    with open(fname, 'r+', encoding='utf-8') as f:
        loaded_dict: dict = json.loads(f.read())
        target_dict: dict = loaded_dict
        
        # target: Union[List, Dict]
        for path in target_dict_paths:
            if not path in target_dict.keys():
                target_dict[path] = {}
            target_dict = target_dict[path]
        target_dict[key_for_insert] = value_for_insert
        json_str = json.dumps(loaded_dict, indent=4, ensure_ascii=False)
        f.seek(0)
        f.write(json_str)



def write_value_to_dict_in_json_file_v2(fname: str, path: str, value: Any):
    """принимает json файл, путь и значение для вставки в json
    если target_dict_paths не существуе - создаёт его

    Args:
        fname (str): json file name
        paths (str): path to dict: a`b`c`d
        value_for_insert (Any): Amy valu for inserting
    """
    def dl_update(d: dict, path: str, value: Any, sep: str = '.'):
        """переопределяем dl.update(), разрешаем inverse во flatten"""

        from flatten_dict import flatten, unflatten
        if not dl.has(d, path, sep):
            return d
        keys = tuple(path.split(sep))
        d_flat = flatten(d)
        d_flat[keys] = value
        return unflatten(d_flat)
    
    loaded_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(fname))
    loaded_dict = dl_update(loaded_dict, path, value, sep='`')
    # json_str = json.dumps(loaded_dict, indent=4, ensure_ascii=False)
    write_dict_or_list_to_json_file(fname, loaded_dict)


def write_value_to_dict(target_dict: Dict, path: List[str], value: Any):
    """принимает dict, путь и значение для вставки в json
    если target_dict_paths не существуе - создаёт его, переопределяя
    существующие значения

    Args:
        target_dict (Dict): dict
        paths (List[str]): path to dict
        value_for_insert (Any): Amy valu for inserting
    """
    target_key = path[-1:]
    target_path = path[:len(path)-1]
    for path_item in target_path:
        if not (target_dict:=target_dict.get(path_item, None)):
            pass


def write_value_to_dict_in_json_file_v3(fname: str, path: List[str], value: Any):
    """принимает json файл, путь и значение для вставки в json
    если target_dict_paths не существуе - создаёт его

    Args:
        fname (str): json file name
        paths (List[str]): path to dict
        value_for_insert (Any): Amy valu for inserting
    """
    
    
    def dl_update(d: dict, path: str, value: Any, sep: str = '.'):
        """переопределяем dl.update(), разрешаем inverse во flatten"""

        from flatten_dict import flatten, unflatten
        if not dl.has(d, path, sep):
            return d
        keys = tuple(path.split(sep))
        d_flat = flatten(d)
        d_flat[keys] = value
        return unflatten(d_flat)
    
    loaded_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(fname))
    loaded_dict = dl_update(loaded_dict, path, value, sep='`')
    # json_str = json.dumps(loaded_dict, indent=4, ensure_ascii=False)
    write_dict_or_list_to_json_file(fname, loaded_dict)



def read_data_from_json_file(fname: str, path: str) -> Any:
    data_from_json_file: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(fname))
    value = get_dict_values(data_from_json_file, path)
    return value    
# "request_url": "https://torgi.gov.ru/new/nsi/v1/RELATIONSHIP_BIDD_HINTEXT",

# print(json.dumps(get_relationship('request_info2.json', url='https://torgi.gov.ru/new/nsi/v1/RELATIONSHIP_BIDD_HINTEXT', code='code', value='fullName', return_value='list'), ensure_ascii=False))
# print(json.dumps(get_relationship('request_info2.json', url='https://torgi.gov.ru/new/nsi/v1/RELATIONSHIP_BIDD_HINTEXT', code='code', value='fullName', return_value='dict'), ensure_ascii=False))

FORM_FIELDS = [
    'Поисковый запрос',
    'Нормативный правовой акт',
    'Вид торгов',
    'Вид сделки',
    'Форма проведения торгов',
    'Субъект местонахождения имущества',
    'Местонахождение имущества',
    'Категория',
               ]

def form_field_Нормативный_правовой_акт():
    url = 'https://torgi.gov.ru/new/nsi/v1/RELATIONSHIP_BIDD_HINTEXT'
    t_path = ['form', 'Нормативный правовой акт']
    a_key = 'available_values'
    a_value = get_relationship('request_info2.json', url=url, code='code', value='fullName', return_value='list')
    a_h_key = 'available_values_hint'
    a_h_value = get_relationship('request_info2.json', url=url, code='code', value='fullName', return_value='dict')
    write_value_to_dict_in_json_file(
        'search_form.json',
        t_path, 
        a_key,
        a_value
        )
    write_value_to_dict_in_json_file(
        'search_form.json',
        t_path, 
        a_h_key,
        a_h_value
        )
    
def form_field(searsh_form_file: str, form_field_name: str, info2_file_name:str):
    # with open(info2_file_name) as info2_f:
    # резервная копия
    shutil.copy(searsh_form_file, 'copy.'+searsh_form_file)
    with open(searsh_form_file, encoding='utf-8') as form_file:
        form_dict = json.loads(form_file.read())
        url_key = form_dict['form'][form_field_name]['info2_url']
        aviavailable_values_key = form_dict['form'][form_field_name]['available_values']['key']
        aviavailable_values_hint_key = form_dict['form'][form_field_name]['available_values_hint']['key']
        aviavailable_values_hint_value = form_dict['form'][form_field_name]['available_values_hint']['value']

    v_t_path = ['form', form_field_name, 'available_values']
    v_h_t_path = ['form', form_field_name, 'available_values_hint']
    a_key = 'values'
    a_h_key = 'values'

    a_value = get_relationship(info2_file_name, url=url_key, code=aviavailable_values_key, value=aviavailable_values_hint_value, return_value='list')
    a_h_value = get_relationship(info2_file_name, url=url_key, code=aviavailable_values_hint_key, value=aviavailable_values_hint_value, return_value='dict')
    write_value_to_dict_in_json_file(
        searsh_form_file,
        v_t_path, 
        a_key,
        a_value
        )
    write_value_to_dict_in_json_file(
        searsh_form_file,
        v_h_t_path, 
        a_h_key,
        a_h_value
        )

def form_field_v2(searsh_form_file: str, form_field_name: str, info2_file_name:str):
    # резервная копия
    shutil.copy(searsh_form_file, 'copy.'+searsh_form_file)
    # with open(searsh_form_file, encoding='utf-8') as form_file:
    #     form_dict: dict = json.loads(form_file.read())
    form_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(searsh_form_file))
    url_key = dl.get(form_dict, f'form`{form_field_name}`info2_url', sep='`')
    aviavailable_values_path = dl.get(form_dict, f'form`{form_field_name}`available_values`path', sep='`')
    aviavailable_values_hint_path = dl.get(form_dict, f'form`{form_field_name}`available_values_hint`path', sep='`')
    full_a_v_path = f'{url_key}`{aviavailable_values_path}'
    full_a_v_h_path = f'{url_key}`{aviavailable_values_hint_path}'
    aviavailable_values_key = typing.cast(str, dl.get(form_dict, f'form`{form_field_name}`available_values`key', sep='`')) 
    aviavailable_values_hint_key = typing.cast(str, dl.get(form_dict, f'form`{form_field_name}`available_values_hint`key', sep='`'))


    res: Dict[str, str] = get_relationship_v2(info2_file_name, 
                                  code_path=full_a_v_path, 
                                  code_key=aviavailable_values_key,
                                  value_path=full_a_v_h_path, 
                                  value_key=aviavailable_values_hint_key)

    form_aviavailable_values_path = f'form`{form_field_name}`available_values`values'
    form_aviavailable_values_hint_path = f'form`{form_field_name}`available_values_hint`values'
    write_value_to_dict_in_json_file_v2(
        searsh_form_file,
        form_aviavailable_values_hint_path,
        res
        )
    write_value_to_dict_in_json_file_v2(
        searsh_form_file,
        form_aviavailable_values_path, 
        list(res.keys())
        )

def form_field_v3(searsh_form_v3_file: str, form_field_name: str, info2_file_name:str):
    # резервная копия
    create_a_backup(searsh_form_v3_file)
    # shutil.copy(searsh_form_v3_file, 'copy.'+searsh_form_v3_file)
    # with open(searsh_form_file, encoding='utf-8') as form_file:
    #     form_dict: dict = json.loads(form_file.read())
    form_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(searsh_form_v3_file))
    url_key = dl.get(form_dict, f'form`{form_field_name}`info2_url', sep='`')
    aviavailable_values_key_path = dl.get(form_dict, f'form`{form_field_name}`available_values`key_path', sep='`')
    full_a_v_k_path = f'{url_key}`{aviavailable_values_key_path}'
    aviavailable_values_key_value = typing.cast(str, dl.get(form_dict, f'form`{form_field_name}`available_values`key_value', sep='`'))

    # aviavailable_values_value_path = dl.get(form_dict, f'form`{form_field_name}`available_values`value_path', sep='`')
    # full_a_v_v_path = f'{url_key}`{aviavailable_values_value_path}'
    aviavailable_values_value_value = typing.cast(str, dl.get(form_dict, f'form`{form_field_name}`available_values`value_value', sep='`')) 

    # aviavailable_values_parent_path = dl.get(form_dict, f'form`{form_field_name}`available_values`parent_path', sep='`')
    # full_a_v_p_path = f'{url_key}`{aviavailable_values_value_path}'
    aviavailable_values_parent_value = typing.cast(str, dl.get(form_dict, f'form`{form_field_name}`available_values`parent_value', sep='`'))


    res: Dict[str, Dict[str, str]] = get_relationship_v3(info2_file_name, 
                                  path=full_a_v_k_path, 
                                  code_key=aviavailable_values_key_value,
                                  value_key=aviavailable_values_value_value,
                                  parent_key=aviavailable_values_parent_value
                                  )

    form_dict['form'][form_field_name]['available_values']['values'] = res
    write_dict_or_list_to_json_file(searsh_form_v3_file, form_dict)
    
    
    
def form_field_v2_субьект_местонаходения():
    path = f'https://torgi.gov.ru/new/nsi/v1/DYNAMIC_ATTR_SEARCH_OPTION'
    file_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file('request_info2.json'))
    t_dict = file_dict[path]['response_json'][0]
    path2 = 'mappingTable`code'
    path3 = 'mappingTable`baseAttrValue`name'
    # info2_data1 = read_data_from_json_file('request_info2.json', path + '`' + path2)
    # info2_data2 = read_data_from_json_file('request_info2.json', path + '`' + path3)
    info2_data1 = get_dict_values(t_dict, path2)
    info2_data2 = get_dict_values(t_dict, path3)
    write_dict_or_list_to_json_file('test1.json', info2_data1)
    write_dict_or_list_to_json_file('test2.json', info2_data2)
    zip_info = zip(info2_data1, info2_data2)
    dict_info: dict = {k:v for k,v in zip_info}
    # dict_info_sorted = dict(sorted(dict_info.items()))
    # print_dict(dict_info_sorted)
    search_form_file = 'search_form.v2.json'
    form_aviavailable_values_hint_path = 'form`Субъект местонахождения имущества`available_values_hint`values'
    form_aviavailable_values_path = 'form`Субъект местонахождения имущества`available_values`values' 
    write_value_to_dict_in_json_file_v2(
        search_form_file,
        form_aviavailable_values_hint_path,
        dict_info
        )
    write_value_to_dict_in_json_file_v2(
        search_form_file,
        form_aviavailable_values_path, 
        list(dict_info.keys())
        )

def form_field_v3_субьект_местонаходения_for_response_refernce():
    search_form_file = 'search_form.v3.json'
    request_info2_file = 'request_info2.json'
    path = f'https://torgi.gov.ru/new/nsi/v1/DYNAMIC_ATTR_SEARCH_OPTION'
    request_info2_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(request_info2_file))
    t_dict = request_info2_dict[path]['response_json'][0]
    path2 = ['mappingTable', 'baseAttrValue', 'code']
    path3 = ['mappingTable', 'baseAttrValue', 'name']
    # info2_data1 = read_data_from_json_file('request_info2.json', path + '`' + path2)
    # info2_data2 = read_data_from_json_file('request_info2.json', path + '`' + path3)
    info2_data1 = get_dict_values(t_dict, path2)
    info2_data2 = get_dict_values(t_dict, path3)
    # write_dict_or_list_to_json_file('test1.json', info2_data1)
    # write_dict_or_list_to_json_file('test2.json', info2_data2)
    zip_info = zip(info2_data1, info2_data2)
    dict_info: dict = {k:{'name': v, 'parent': None} for k,v in zip_info}
    # dict_info_sorted = dict(sorted(dict_info.items()))
    # print_dict(dict_info_sorted)
    # form_aviavailable_values_hint_path = 'form`Субъект местонахождения имущества`available_values_hint`values'
    form_aviavailable_values_path = ['references', 'Субъект местонахождения имущества', 'available_values', 'values'] 
    # write_value_to_dict_in_json_file_v2(
    #     search_form_file,
    #     form_aviavailable_values_hint_path,
    #     dict_info
    #     )
    write_value_to_dict_in_json_file_v2(
        search_form_file,
        form_aviavailable_values_path, 
        dict_info
        )



# def check_list_structure(target_list: list, struct: list, target_name_name: str = 'undefined'):
#     pass

def check_dict_structure(target_dict: dict, struct: dict, target_dict_name: str = 'undefined'):
    """получает на вход dict и structur, проверяет соответствие и 
    в некоторых случаях исправляет структуру полученного dict:
    - если элемент структуры отсутствует - вставляет его
    - если элемент структуры присутствует но имеет не правильный 
    тип меняет его (если отсутствует содержание)
    - - если элемент структуры присутствует но имеет не правильный 
    тип но при этом элемент имеет содержание - выводит предупреждение """
    
    def _make_descendants(field: dict, descendants: dict, field_name: str):
        for key in descendants.keys():
            field[key] = descendants[key]['default']()
            logger.debug(f'add descendants field:{field_name}.{key} type {type(field[key])}')
            if (chaild_descendants := descendants[key].get('descendants', None)):
                _make_descendants(field[key], chaild_descendants, f'{field_name}.{key}')
    
    
    def _existen_dict_key_process(dict_name: str, target_dict: dict, key: str, struct: dict):
        if not type(target_dict[key]) == struct['type']:
            if target_dict[key]:
                logger.debug(f'field:{dict_name}.{key} contain not compatible type {type(target_dict[key])}, should be {struct["type"]}')
                return
            else: 
                target_dict[key] = struct['default']()
                logger.debug(f'field:{dict_name}.{key} change type to {struct["type"]}')
                if (descendants := struct.get('descendants', None)) :
                    # print(f'key: {key}')
                    _make_descendants(target_dict[key], descendants, f'{dict_name}.{key}')
        else:
            if (descendants := struct.get('descendants', None)):
                check_dict_structure(target_dict[key], descendants, f'{dict_name}.{key}')
    
    def check_for_consistens(target_dict: dict, struct: dict, target_dict_name: str):            
        for key, value in struct.items():
            if target_dict.get(key, None) is not None:
                    _existen_dict_key_process(target_dict_name, target_dict, key, value)
            else:
                target_dict[key] = struct[key]['default']()
                print(f'add field:{target_dict_name}.{key} type {type(target_dict[key])}')
                if (descendants:=struct[key].get('descendants', None)):
                    # print(f'key: {key}')
                    _make_descendants(target_dict[key], descendants, f'{target_dict_name}.{key}')
            
    def check_for_redundancy(target_dict: dict, struct: dict, target_dict_name: str):
        target_dict_key_set = set(target_dict.keys())
        struct_key_set = set(struct.keys())
        keys_diff = target_dict_key_set - struct_key_set
        if (count:=len(keys_diff)):
            keys_diff_list = list(keys_diff)
            remaining_keys = []
            deleted_keys_count = 0
            logger.debug(f'dict:{target_dict_name} contain {count} redundan fields {keys_diff_list}')
            for key in keys_diff_list:
                if not target_dict[key]:
                    del target_dict[key]
                    deleted_keys_count += 1
                else:
                    remaining_keys.append(key)
            logger.debug(f'remuved redundan fields count {deleted_keys_count}')
            logger.debug(f'remaining redundan fields {remaining_keys}')
            
    
    check_for_redundancy(target_dict, struct, target_dict_name) 
    check_for_consistens(target_dict, struct, target_dict_name)
    
    
FORM_V2_FORM_FIELD_STRUCT = {
            "name": {
                'type': str, 
                "default": lambda : ""
                },
            "required": {
                'type': bool, 
                "default": lambda : False
                },
            "multi_value": {
                'type': bool, 
                "default": lambda : False
                },
            "default": {
                'type': list, 
                "default": lambda : list(), 
            },
            "info2_url": {
                'type': str, 
                "default": lambda : ""
                },
            "available_values": {
                'type': dict, 
                "default": lambda : dict(), 
                'descendants': {
                    "path": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "key": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "values": {
                        'type': list, 
                        "default": lambda : list(), 
                        },
                    },
                },
            "available_values_hint": {
                'type': dict, 
                "default": lambda : dict(), 
                'descendants': {
                    "path": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "key": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "values": {
                        'type': dict, 
                        "default": lambda : dict(), 
                        },
                    },
                },
            "selected_values": {
                'type': list, 
                "default": lambda : list(), 
                },
            "comment": {
                'type': str, 
                "default": lambda : ""
                },
            }

    
FORM_V3_FORM_FIELD_STRUCT = {
            "group": {
                'type': dict, 
                "default": lambda : dict(),
                'descendants': {
                    "name": {
                        'type': str, 
                        "default": lambda : "form"
                        },
                    "parent": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "sort_order": {
                        'type': int,
                        'defoult': lambda : 0
                        }
                    },
                },
            "name": {
                'type': str, 
                "default": lambda : ""
                },
            "required": {
                'type': bool, 
                "default": lambda : False
                },
            "multi_value": {
                'type': bool, 
                "default": lambda : False
                },
            "default": {
                'type': list, 
                "default": lambda : list(), 
            },
            "info2_url": {
                'type': str, 
                "default": lambda : ""
                },
            "available_values": {
                'type': dict, 
                "default": lambda : dict(), 
                'descendants': {
                    "key_path": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "key_value": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "value_path": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "value_value": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "parent_path": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "parent_value": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "values": {
                        'type': dict, 
                        "default": lambda : dict(), 
                        },
                    },
                },
            "selected_values": {
                'type': list, 
                "default": lambda : list(), 
                },
            "comment": {
                'type': str, 
                "default": lambda : ""
                },
            }

FORM_V3_FEED_FIELD_STRUCT = {
            "group": {
                'type': dict, 
                "default": lambda : dict(),
                'descendants': {
                    "name": {
                        'type': str, 
                        "default": lambda : "form"
                        },
                    "parent": {
                        'type': str, 
                        "default": lambda : ""
                        },
                    "sort_order": {
                        'type': int,
                        'defoult': lambda : 0
                        }
                    },
                },
            "name": {
                'type': str, 
                "default": lambda : ""
                },
            "required": {
                'type': bool, 
                "default": lambda : True
                },
            "value": {
                'type': Union[str, dict, list],
                'default': ""
            },
            "default": {
                'type': list, 
                "default": lambda : list(), 
            },
            "comment": {
                'type': str, 
                "default": lambda : ""
                },
            }



def create_a_backup(fname: str):
    """принимает file name - создаёт резурвную копию"""
    date_time = get_formated_curent_date_time()
    shutil.copy(fname, f'{BACKUP_DIR}{date_time}-{fname}')


def check_form_v2_fields_structure(form_v2_fname: str):

    """проеряет структуру поля формы, 
    вставляет недостоющие поля,
    если поле существует, проверяет его тип,
    если тип не верный меняет его тип 
    только в случае если оно пустое, не содержит данных
    если поле не пустое пишет предупреждение в stdout"""
    # global FORM_V2_FORM_FIELD_STRUCT
    create_a_backup(form_v2_fname)
    target_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(form_v2_fname))
    form_dict: dict = target_dict['form']
    for field_name, field in form_dict.items():
        check_dict_structure(field, FORM_V2_FORM_FIELD_STRUCT, field_name)
    write_dict_or_list_to_json_file(form_v2_fname, target_dict)
    # check_form_v2_fields_structure(form_dict)
    # _process_check_structure(form_dict, FORM_V2_FORM_FIELD_STRUCT)
    
def test_check_dict_structure():
    test1 = {
        'name': [],
        'comment': "comment",
        "info2_url": {'key': 'value'},
        'not_struc_key1': '',
        'not_struc_key2': 'value',
        "available_values_hint": {
                "path": {},
                "key": "",
                "values": {
                    "SUCCEED": "Состоялся",
                    "PUBLISHED": "Опубликован",
                    "APPLICATIONS_SUBMISSION": "Прием заявок",
                    "DETERMINING_WINNER": "Определение победителя",
                    "FAILED": "Не состоялся",
                    "CANCELED": "Отменен"
                },
                'not_struc_key3': '',
                'not_struc_key4': 'value',
                'not_struc_key4': [],
                'not_struc_key4': ['value'],
            },
        }
    check_dict_structure(test1, FORM_V2_FORM_FIELD_STRUCT, 'test1')
   
def get_formated_curent_date_time() -> str:
    now = datetime.now()  # Get the current datetime object
    return now.strftime("%d.%m.%y_%H-%M-%S")
    # print(formatted_date)

def print_to_file_os_enveron_var(fname: str):
    with open(fname, 'wt', encoding='utf-8') as f:
        
        json.dump(obj=dict(os.environ.items()), fp=f, ensure_ascii=False, indent=4)
    
def sort_dict_recursiv(target_dict:dict) -> dict:
    new_dict: dict = {}
    for k in sorted(target_dict.keys()):
        if type((value:=target_dict[k])) == dict:
            value = sort_dict_recursiv(value)
        new_dict[k] = value
    return new_dict
      
def form_v2_to_v3():
    target_file_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file('search_form.v3.json'))
    target_dict: dict = target_file_dict['form']
    for k, v in target_dict.items():
        new_item = {}
        new_item['multi_value'] = v.get('multi_value', '')
        new_item['multi_value'] = v.get('multi_value', '')
        new_item['multi_value'] = v.get('multi_value', '')
        new_item['default'] = v.get('default', '')
        new_item['info2_url'] = v.get('info2_url', '')
        new_item['available_values'] = {}
        new_item['available_values']['key_path'] = v['available_values']['path']
        new_item['available_values']['key_value'] = v['available_values']['key']
        new_item['available_values']['value_path'] = v['available_values_hint']['path']
        new_item['available_values']['value_value'] = v['available_values_hint']['key']
        new_item['available_values']['parent_path'] = ''
        new_item['available_values']['parent_value'] = ''
        new_item['available_values']['values'] = {}
        new_item['selected_values'] = v.get('selected_values', '')
        new_item['comment'] = v.get('comment', '')
        
        target_dict[k] = new_item
    write_dict_or_list_to_json_file('search_form.v3.json', target_file_dict)    
    
    
def sort_form_v3_for_group_and_sort_order():
    create_a_backup('search_form.v3.json')
    target_file_dictv3: Dict = typing.cast(Dict, load_dict_or_list_from_json_file('search_form.v3.json'))
    target_groups = target_file_dictv3['groups']
    target_form = target_file_dictv3['form']
    temp_list = []
    for k, v in target_form.items():
        t = target_groups[target_form[k]['group']['name']]['sort_order'], target_form[k]['group']['sort_order'], k
        temp_list.append(t)
    sorted_list = sorted(temp_list)
    rez_dict = {}   
    for _, _, k in sorted_list:
        rez_dict[k] = target_form[k]
    
    target_file_dictv3['form'] = rez_dict
    write_dict_or_list_to_json_file('search_form.v3.json', target_file_dictv3)    


def get_request_url_base_str_and_request_query_dict_from_search_forv_v3_file(search_form_json_file: str) -> Tuple[str, Dict[str, List[str]]]:
    """получает search_form.v3.json, возвращает: 
    1. base_url for request - "scheme" + "host" + "filename" 
    2. query_dict - key - "namme", value - "default" from search_form.v3 "form" item

    Args:
        search_form_json_file (str): search_form.v3.json

    Returns:
        Tuple[str, Dict[str, str]]: (base_url, query_dict) 
    """
    
    search_form_v3_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(search_form_json_file))
    
    base_url: str = get_base_url_from_search_form_v3_dict(search_form_v3_dict)
    query_dict = get_query_dict_from_search_form_v3_dict(search_form_v3_dict)
    return base_url, query_dict


def get_base_url_from_search_form_v3_file(search_form_v3_file: str) -> str:
    """принимает search_form_v3_file - возвращает base_url str"""

    search_form_v3_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(search_form_v3_file))
    return get_base_url_from_search_form_v3_dict(search_form_v3_dict)

def get_notices_url_from_search_form_v3_file(search_form_v3_file: str) -> str:
    """принимает search_form_v3_file - возвращает notices_url str"""

    search_form_v3_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(search_form_v3_file))
    return get_notices_url_from_search_form_v3_dict(search_form_v3_dict)



def get_base_url_from_search_form_v3_dict(search_form_v3_dict: Dict) -> str:
    """принимает search_form_v3_dict - возвращает base_url str"""

    return f"{search_form_v3_dict['scheme']}://{search_form_v3_dict['host']}{search_form_v3_dict['base_filename']['filename']}"

def get_notices_url_from_search_form_v3_dict(search_form_v3_dict: Dict) -> str:
    """принимает search_form_v3_dict - возвращает notices_url str"""

    return f"{search_form_v3_dict['scheme']}://{search_form_v3_dict['host']}{search_form_v3_dict['notices_filename']['filename']}"






def get_query_dict_from_search_form_v3_dict(search_form_v3_dict: dict) -> dict:
    """получает search_form_v3_dict и возвращает:
    query_dict: key - "namme", value - "default" from search_form.v3 "form" item
    

    Args:
        search_form_v3_dict (dict): dict from  search_form.v3.json file

    Returns:
        dict: key - "namme", value - "default" from search_form.v3 "form" item
    """
    form_dict: dict = search_form_v3_dict['form']
    query_dict = {item['name']: [] for item in form_dict.values()}

    return query_dict
        
        
def unpack_dict(pattern_dict: dict, unpacked_dict: dict) -> Tuple[Dict[str, str], Dict[str, str]]:
    """ принимает два dict: "pattern" и "unpacked"
    возвращает два dict созданных на основании "unpacked":
    1. с ключами которые есть в pattern_dict
    2. с ключами которых нет в pattern_dict

    Args:
        pattern_dict (dict): шаблонный dict, на основании которого происходит разделение unpack_dict
        unpacked_dict (dict): разделяемый dict

    Returns:
        True[Dict[str, str], Dict[str, str]]: (dict с ключами которые есть в pattern_dict, dict с ключами которых нет в pattern_dict)
    """
    key_in_dict: dict = {}
    key_out_dict: dict = {}
    for key in unpacked_dict.keys():
        if key in pattern_dict:
            key_in_dict[key] = unpacked_dict[key]
        else:
            key_out_dict[key] = unpacked_dict[key]

    return key_in_dict, key_out_dict
        
def get_query_url(request_url_base_str: str, request_query_dict: Dict[str, List[str]], empty_value: bool = False) -> str:
    """получает "<scheme>://<netloc>/<path>"_str и request_query_dict, возвращает
    "<scheme>://<netloc>/<path>?<query>". Если empty_value=False - то в query не
    включаются ключи с пустыми заначениями ([])

    Args:
        request_url_base_str (str): "<scheme>://<netloc>/<path>"
        request_query_dict (dict): {'name1': ["value1"], 'name2': [], 'name3': ["value1", "value4", ...]}
        empty_value (bool): Если empty_value=False - то в query не включаются ключи с пустыми заначениями ([])
    Returns:
        str: "<scheme>://<netloc>/<path>?<query>"
    """
    request_query_str = get_quey_str_from_v_3_dict(request_query_dict, empty_value=empty_value)
    query_url = f'{request_url_base_str}?{request_query_str}'
    return query_url

def get_quey_str_from_v_3_dict(query_dict: Dict[str, List[str]], empty_value: bool = False) -> str:
    """получает query_dict возвращает query строку. Если empty_value=True
    то в строку уключаются ключи с пустыми занчениями т.е. [], в противном случае
    в строке только не путые занчения

    Args:
        query_dict (dict): query_dict
        empty_value (bool, optional): Влючать или нет пустые значения. Defaults to True.

    Returns:
        str: query string
    """
    query_str_list = []
    for k,v in query_dict.items():
        if v:
            query_str_list.append(f"{k}={','.join(v)}")
        elif empty_value:
            query_str_list.append(f"{k}={','.join(v)}")
    query_str = '&'.join(query_str_list)        
    return query_str


def update_request_query_dict(request_query_dict: Dict[str, List[str]], update_query_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Обновляет request_query_dict значениями из update_query_dict"""
    # test = []
    # test.extend
    for k in update_query_dict.keys():
        if request_query_dict.get(k, None) != None: 
            request_query_dict[k].extend(update_query_dict[k])
    return request_query_dict

def wrap_update_query_dict(update_query_dict:  Dict[str, str]) -> Dict[str, List[str]]:
    """оборачивает value str в list, если value мультивелю
    т.е. в виде 'a,b,c' то split значение оп ','"""

    wraped_update_query_dict = {}
    for k, v in update_query_dict.items():
        logger.debug(f'in wrap_update_query_dict(), v: {v}')
        wraped_update_query_dict[k] = v.split(',')

    return wraped_update_query_dict
# TODO: делать функцию
def fill_required_query_dict_keys_default_values_if_they_not_set(updated_request_query_dict: Dict[str, List[str]], search_forv_v3_file: str) -> Dict[str, List[str]]:
    """получает updated_request_query_dict и в случае если ключи с тебованием
    "required": "true" в """  
    search_form_file_dict: Dict[str, Any] = typing.cast(Dict, load_dict_or_list_from_json_file(search_forv_v3_file))
    search_form_fields_dict: Dict[str, Dict] = search_form_file_dict['form']
    for v in search_form_fields_dict.values():
        if v['required'] == 'true':
            field_name = v['name'] 
            if not updated_request_query_dict[field_name]:
                updated_request_query_dict[field_name].extend(v['default'])
    return updated_request_query_dict

def get_base_filename_headers_from_search_form_v3_file(search_form_v3_json_file:str) -> Dict[str, str]:
    """принимает search_form_v3_json_file - отдаёт base_filename_headers request headers dict"""

    search_form_v3_json_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(search_form_v3_json_file))
    return get_base_filename_headers_from_search_form_v3_dict(search_form_v3_json_dict)

def get_base_filename_headers_from_search_form_v3_dict(search_form_v3_dict: Dict[str,Any]) -> Dict[str, str]:
    """принимает search_form_v3_dict - отдаёт base_filename_headers request headers dict"""

    return search_form_v3_dict['base_filename']['request_headers_for_send']

def get_notices_filename_headers_from_search_form_v3_file(search_form_v3_json_file:str) -> Dict[str, str]:
    """принимает search_form_v3_json_file - отдаёт notices_filename_headers request headers dict"""

    search_form_v3_json_dict: Dict = typing.cast(Dict, load_dict_or_list_from_json_file(search_form_v3_json_file))
    return get_notices_filename_headers_from_search_form_v3_dict(search_form_v3_json_dict)

def get_notices_filename_headers_from_search_form_v3_dict(search_form_v3_dict: Dict[str,Any]) -> Dict[str, str]:
    """принимает search_form_v3_dict - отдаёт notices_filename_headers request headers dict"""
    
    return search_form_v3_dict['notices_filename']['request_headers_for_send']


def get_feed_items_v1_keys_maping_from_feed_items_v1_file(feed_items_v1_file: str) -> Dict[str, List[Tuple[Tuple[str, str],Tuple[str, str]]]]:
    """принимает feeed_items_v1.json файл - возвращает словарь в котором
    ключи str(tuple), tuple из ключей "response_data" dict a value список 
    из Tuple ((biddForm, value_biddForm), (biddType, value_biddType))
    """
    feed_items_v1_list: List = typing.cast(List, load_dict_or_list_from_json_file(feed_items_v1_file))
    
    return get_feed_items_v1_keys_maping_from_feed_items_v1_list(feed_items_v1_list)

def _get_response_data_generator_from_feed_items_v1_list(feed_items_v1_list: List[Dict[str, Any]]) -> Generator[Dict[str, Any], Any, Any]:
# def _get_response_data_generator_from_feed_items_v1_list(feed_items_v1_list: List[Dict[str, Any]]) -> Generator:
    """принимает feed_items_v1_list - возращает генератор feed_item['response_data'] dict"""

    return typing.cast(Generator[Dict[str, Any], Any, Any], (feed_item['response_data'] for feed_item in feed_items_v1_list))


def coroutine(fun: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Generator:
        gen = fun(args, kwargs)
        next(gen)
        return gen
    return wrapper

def get_data_generator_from_dict_iterable(target_iterable: Iterable[Dict], path: List[str] = []) -> Generator:
    """принимает Iterable структуру и путь List - возращает генератор элементов соответствующих путю"""

    if not isinstance(target_iterable, Iterable):
        return 
    # print(path)
    path_len = len(path)
    for item in target_iterable:
        if isinstance(item, list):
            yield from get_data_generator_from_dict_iterable(target_item, path)
        if not path_len:
            yield item
            continue
        if not isinstance(item, dict):
            continue
        target_item: Dict = item
        for i in range(0, path_len):
            # print(i)
            target_item = typing.cast(Dict, target_item.get(path[i], None))
            
            if target_item == None:
                break
            if isinstance(target_item, list):
                yield from get_data_generator_from_dict_iterable(target_item, path[i+1:path_len])
                break
            if not isinstance(target_item, dict) and i != path_len-1:
                break
            if i == path_len-1:
                yield target_item
                
    # return (item for item in target_iterable)



def get_feed_items_v1_keys_maping_from_feed_items_v1_list(feed_items_v1_list: List[Dict]) -> Dict[str, List[Tuple[Tuple[str, str],Tuple[str, str]]]]:
    """принимает feeed_items_v1.json dict - возвращает словарь в котором
    ключи str(tuple), tuple из ключей "response_data" dict a value список 
    из Tuple ((biddForm, value_biddForm), (biddType, value_biddType))
    """
    response_data_gen = _get_response_data_generator_from_feed_items_v1_list(feed_items_v1_list)
    # response_data_gen: Generator[Dict, None, None] = typing.cast(Generator[Dict, None, None], (feed_item['response_data'] for feed_item in feed_items_v1_list))
    
    res_dict = defaultdict(list)
    for response_data in response_data_gen:
        keys_tuple = str(tuple(resp_key for resp_key in sorted(response_data.keys())))
        value = (
            ('biddForm', response_data['biddForm']['name']),
            ('biddType', response_data['biddType']['name'])
            )
        res_dict[keys_tuple].append(value)
    return res_dict

def get_union_keys_set_from_feed_items_file(feed_items_v1_file: str, path: List[str]) -> Set[str]:
    """принимает feeed_items.json файл и путь до некого dict или List[dict] 
    - возвращает union set из ключей указанного dict 
    """
    feed_items_v1_list: List = typing.cast(List, load_dict_or_list_from_json_file(feed_items_v1_file))
    
    return get_union_keys_set_from_feed_items_list(feed_items_v1_list, path)

def get_union_keys_set_from_feed_items_list(feed_items_list: List[Dict], path: List[str]) -> Set[str]:
    """принимает feeed_items list и путь до некого dict или List[dict] 
    - возвращает union set из ключей указанного dict 
    """
    # response_data_gen = (feed_item['response_data'] for feed_item in feed_items_v1_list)
    response_data_gen = get_data_generator_from_dict_iterable(feed_items_list, path)
    # response_data_gen: Generator[Dict, None, None] = typing.cast(Generator[Dict, None, None], (feed_item['response_data'] for feed_item in feed_items_v1_list))
    
    res_set = set()
    for response_data in response_data_gen:
        keys_set = set(resp_key for resp_key in response_data.keys())
        res_set |= keys_set
    return res_set

def get_intersection_keys_from_feed_items_file(feed_items_file: str, path: List[str]) -> Set[str]:
    """принимает feeed_items.json файл - и путь до некого dict или List[dict] 
    - возвращает intersection set из ключей указанного dict
    """
    feed_items_v1_list: List = typing.cast(List, load_dict_or_list_from_json_file(feed_items_file))
    
    return get_intersection_keys_from_feed_items_list(feed_items_v1_list, path)

def get_intersection_keys_from_feed_items_list(feed_items_v1_list: List[Dict], path: List[str]) -> Set[str]:
    """принимает feeed_items list - и путь до некого dict или List[dict] 
    - возвращает intersection set из ключей указанного dict
    """
    # response_data_gen = (feed_item['response_data'] for feed_item in feed_items_v1_list)
    response_data_gen = get_data_generator_from_dict_iterable(feed_items_v1_list, path)
    # response_data_gen: Generator[Dict, None, None] = typing.cast(Generator[Dict, None, None], (feed_item['response_data'] for feed_item in feed_items_v1_list))
    
    res_set = set()
    for response_data in response_data_gen:
        if not res_set:
            res_set = set(resp_key for resp_key in response_data.keys())
            continue
        keys_set = set(resp_key for resp_key in response_data.keys())
        res_set &= keys_set
    return res_set
def get_difference_keys_from_feed_items_file(feed_items_v1_file: str, path: List[str]) -> Set[str]:
    """принимает feeed_items.json file - и путь до некого dict или List[dict] 
    - возвращает difference set из ключей указанного dict
    """
    feed_items_v1_list: List = typing.cast(List, load_dict_or_list_from_json_file(feed_items_v1_file))
    
    return get_difference_keys_from_feed_items_list(feed_items_v1_list, path)

def get_difference_keys_from_feed_items_list(feed_items_v1_list: List[Dict], path: List[str]) -> Set[str]:
    """принимает feeed_items_v1 list dicts - - возвращает intersection set 
    из ключей указанного dict
    """
    # response_data_gen = (feed_item['response_data'] for feed_item in feed_items_v1_list)
    # response_data_gen = _get_response_data_generator_from_feed_items_v1_list(feed_items_v1_list)
    # response_data_gen: Generator[Dict, None, None] = typing.cast(Generator[Dict, None, None], (feed_item['response_data'] for feed_item in feed_items_v1_list))
    
    union_set = get_union_keys_set_from_feed_items_list(feed_items_v1_list, path)
    intersep_set = get_intersection_keys_from_feed_items_list(feed_items_v1_list, path)
    res_set = union_set - intersep_set
    return res_set

                

        
# TODO переделывать под моель 2
def feed_model_traversing(model: Dict, travers_fun: Callable,  init_path: List[str] = []):
    """принимает feed_model dict, и travers_fun коорая применяется к каждому 
    элементу модели, совершает обход всех модел элементов, производит действиве указанное в travers_fun_
    traversing
    пример travers_fun:
    
    def fun_trav(model_el: Dict, path: List[str]):
        if not model_el.get('value', None):
                model_el['value'] = {}
        for t in model_el['types']:
            model_el['value'][t['type']] = path

    добавляет в элемент поле со значением
    """

    def feed_element_model_traversing(model_el: Dict, travers_fun: Callable, init_path: List[str] = []):

        travers_fun(model_el, init_path)
        for k,v in model_el['types'].items():
            if (k == 'dict') or (k == 'list'):
                c_path = init_path.copy()
                feed_model_traversing(v['fields'], travers_fun, c_path)


    for k, v in model.items():
        el_path = k
        c_path = init_path.copy()
        c_path.append(el_path)
        feed_element_model_traversing(v, travers_fun, c_path)

    
def get_union_intersection_difference_from_items_file(items_list_file: str, path: List[str]) -> Dict[str, List[str]]:
    """принимает  item list file и path, возвращиет dict
    targ_dict = {
        'union_set': list(union_set),
        'intersection_set': list(inters_set),
        'difference_set': list(dif_set)
    }
    
    """
    union_set = get_union_keys_set_from_feed_items_file(items_list_file, path)    
    inters_set = get_intersection_keys_from_feed_items_file(items_list_file, path)
    dif_set = get_difference_keys_from_feed_items_file(items_list_file, path)
    targ_dict = {
        'union_set': list(union_set),
        'inters_set': list(inters_set),
        'dif_set': list(dif_set)
    }
    
    return targ_dict
    # write_dict_or_list_to_json_file('feed/un_in_dif.json', targ_dict)




if __name__ == '__main__':
    logging_configure()
    form_field_v3_субьект_местонаходения_for_response_refernce()
    # pass
    # req_url_str, query_dikt = get_request_url_base_str_and_request_query_dict_from_search_forv_v3_file('spiders/search_form.v3 copy.json')
    # url_str = get_query_url(req_url_str, query_dikt, False) 
    # print(url_str)
    # list_dict = get_feed_model_v2_from_feed_items_file('raw_data_dict_list', ['response_data','content'])
    # list_dict = get_feed_model_v1_from_feed_items_file('feed/feed_items_v0.json',['response_data', 'content'])
    # write_dict_or_list_to_json_file('feed/feed_items_lot_card_modelv2_2.json', list_dict)
    # res_data = load_dict_or_list_from_json_file('feed/feed_items.v1.json')
    # list_dict = res_data[0]['response_data']
    # search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/raw_content.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/27.05.24_09-10-05.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/feed_items_v0.json')
    # raw_data_dict = load_dict_or_list_from_json_file('feed/raw_content.json')
    
    # raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, ['content'])

    # res_list = []
    # data = next(raw_data_gen)
    # for data in raw_data_gen:
    # res_list.append(parsing_raw_data_relative_to_data_model_v2(search_form_dict, data))

    
    
    # parsed_content =  parsing_raw_data_relative_to_data_model_v2(search_form_dict, raw_data_dict)
    # print(parsed_content)
    # write_dict_or_list_to_json_file('feed/parsed_content_12.json', parsed_content)
    # write_dict_or_list_to_json_file('feed/parsed_content_7.json', parsed_content)
    # res_data = get_dict_type(list_dict)
    # print(res_data)