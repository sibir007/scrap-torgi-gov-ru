# from ast import If
# from curses import wrapper
# from curses.ascii import SI
# from email.policy import default
# from lib2to3.pytree import convert
# from math import lgamma
# import re
# from tabnanny import check
# from tkinter import N
# from turtle import st
# from types import new_class
from typing import Iterable, Dict, Generator, Literal, NoReturn, Set, Tuple, List, FrozenSet, Union, Any, Callable
# from unittest.mock import DEFAULT

# import scrapy
# from importlib import simple
from util import logging_configure, load_dict_or_list_from_json_file, write_dict_or_list_to_json_file
from util import get_data_generator_from_dict_iterable, type_str

# from util import SIMPLE_TYPES_LIST, CLASS_TYPES_LIST
from util_parsing_raw_data import get_model_type_none_if_error, get_list_model_list_item_type_none_if_error  
from util_parsing_raw_data import SIMPLE_TYPES_LIST, _get_field_to_feeded_name, CLASS_TYPES_LIST
from util_get_model import get_field_model


import logging
import typing


logger = logging.getLogger(__name__)





def get_item_class_mapping(search_form_v3: Dict, root_class_name: str = 'root'):
    
    
    def get_class_field_layout():
        field_layout = {
            # human readable name из модели поля
            'hr_name': '',
            # raw name из dict модели 
            'r_name': '',
            'type': '',
        }
        return field_layout

    
    def get_filed_class_field_layout(field_model: Dict, field_name: str, parrent_class_path: List, field_type: str) -> Union[Dict, None]:
        """отдаёт заполненный макет поля класса"""
        
        filed_layout = get_class_field_layout()        
        filed_layout['hr_name'] = field_model['human_readable_name']
        filed_layout['r_name'] = field_name
        filed_layout['type'] = field_type
        
        # class_name = get_class_name(feed_model, field_model, field_name, parrent_path,)
        return filed_layout

    
    def get_class_layout():
        class_layout = {
            # имя вычисляемое get_class_name(), являющеесе ключём класса 
            'class_name': '',
            # human readable name из модели поля
            'hr_name': '',
            # raw name из dict модели
            'r_name': '',
            # на всякий случай, в будущем может понадобиться
            'random_name': '',
            'type': '',
            'path': [],
            'fields': {},
            'foreign_key_fields': []
        }
        return class_layout
    
    # def check_class_type(field_model: Dict, field_name: str, parrent_path: List, class_type: Literal['dict', 'list_dict', 'list_simple']) -> bool:
    #     """осуществляем проверку переданного в class_type литерала
    #     и вычисленного на основании field_model
    #     ошибочные ситуации:
    #     1. ошибка при получении типа модели
    #     2. тип модели относится к простому типу
    #     3. тип переданного в class_type литерале не соответствует вычисленному
    #     допустимые литералы для class_type:
    #     1. 'dict'
    #     2. 'list_dict'
    #     3. 'list_simple'
    #     на данный момент не допустимые литералы для class_type:
    #     1. 'list_list' и производные от него
    #     """
    #     logger.debug(f"-----> {check_class_type.__name__}(): field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #     # получаем тип моди
    #     if not (model_type:=get_model_type_none_if_error(root_feed_fields, field_name, parrent_path)):
    #         # при получении типа модели возникли ошибки
    #         # логи прописаны в get_model_type_none_if_error()
    #         # возвращаем False
    #         logger.error(f"{check_class_type.__name__}(): ошибка при получении типа модели, field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     # проверяем что тип модели вростой тип
    #     if model_type in SIMPLE_TYPES_LIST:
    #         # ошибка - тип модели простой тип
    #         # пишем лог, возвращаем False
    #         logger.error(f"{check_class_type.__name__}(): ошибка - тип модели простой тип: {model_type}, field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     # проверяем условие для 'dict' типа
    #     if model_type == 'dict':
    #         if model_type == class_type:
    #             return True
    #         # ошибочная ситуация, переданный class_type не
    #         # соответствует вычисленному по field_model
    #         # пишем лог, возвращаем False
    #         logger.error(f"{check_class_type.__name__}(): переданный class_type: '{class_type}', не соотверствует вычисленному '{model_type}', field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     if model_type != 'list':
    #         # ошибка не поддерживаемы тип подели класса
    #         logger.error(f"{check_class_type.__name__}(): не поддерживаемы тип модели класса: {model_type}, допустимые типы: 'dict', 'list_dict', 'list_simple'; field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     # вычисленный тип 'list', получаем тип листа
    #     if not (list_model_type:=get_list_model_list_item_type_none_if_error(field_model, field_name, parrent_path)):
    #         # ошибка при получении типа лист модели
    #         logger.error(f"{check_class_type.__name__}(): ошибка при получении типа '{model_type}' модели, field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     if list_model_type in SIMPLE_TYPES_LIST:
    #         if class_type == 'list_simple':
    #             return True
    #         # ошибочная ситуация, переданный class_type не
    #         # соответствует вычисленному по field_model
    #         # пишем лог, возвращаем False
    #         logger.error(f"{check_class_type.__name__}(): переданный class_type: '{class_type}', не соотверствует вычисленному 'list_simple', field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     if list_model_type == 'dict':
    #         if class_type == 'list_dict':
    #             return True
    #         # ошибочная ситуация, переданный class_type не
    #         # соответствует вычисленному по field_model
    #         # пишем лог, возвращаем False
    #         logger.error(f"{check_class_type.__name__}(): переданный class_type: '{class_type}', не соотверствует вычисленному 'list_dict', field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #         return False
    #     # ошибочная ситуация, не поддерживаемый тип list модели
    #     logger.error(f"{check_class_type.__name__}(): не поддерживаемый тип '{list_model_type}' list модели, поддерживаемые типы 'dict', 'simple'; field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
    #     return False
    #     # calculated_class_type = calculate_class_type(field_model, field_name, parrent_path)
    
    def get_filled_class_layout(field_model: Dict, field_name: str, calass_name: str, parrent_path: List, class_type: Literal['dict', 'list_dict', 'list_simple'], random_name: str = '') -> Union[Dict, None]:
        """отдаёт заполненный макет класса, тип класса вычисляется 
        внутри функции, "class_type" параметр передающийся извне 
        используется для проверки правильности задания типа
        """
        
        # # проверяем соответствие class_type типу field_model
        # if not check_class_type(field_model, field_name, parrent_path, class_type):
        #     # ошибка - несоответствие class_type типу модели
        #     logger.error(f"{get_filled_class_layout.__name__}(): несоответствие class_type: '{class_type}' типу модели, field_name: {field_name}, parrent_path: {', '.join(parrent_path)}")
        #     return None
        class_layout = get_class_layout()        
        class_layout['class_name'] = calass_name
        class_layout['hr_name'] = field_model['human_readable_name']
        class_layout['r_name'] = field_name
        class_layout['type'] = class_type
        # class_name = get_class_name(feed_model, field_model, field_name, parrent_path,)
        return class_layout
    

    def get_field_dict_model_for_simple_list_type(list_field_model: Dict, list_field_name: str):
        """создание из simple list - dict list с одним полем имени соответствующем
        данному листу и типом листа, для запуска через make_class()"""
        # создадим модель поля для simple поля list
        field_dict_model_for_list_item = get_field_model() 
        field_dict_model_for_list_item['visible'] = list_field_model['visible']
        field_dict_model_for_list_item['feed'] = list_field_model['feed']
        field_dict_model_for_list_item['feed_human_readable_name'] = list_field_model['feed_human_readable_name']
        field_dict_model_for_list_item['human_readable_name'] = list_field_model['human_readable_name']
        field_dict_model_for_list_item['value_scrap_type'] = list_field_model['value_scrap_type']
        field_dict_model_for_list_item['field_types'] = {"types": ["str"], "default_value": ""}
        field_dict_model_for_list_item['casting_key'] = ''
        field_dict_model_for_list_item['exclusion_key'] = ''
        field_dict_model_for_list_item['types'] = {"str": {"type": "str"}}
    
        # создадим новую модель типа dict для list
        field_dict_model_for_list = get_field_model()
        field_dict_model_for_list['visible'] = list_field_model['visible']
        field_dict_model_for_list['feed'] = list_field_model['feed']
        field_dict_model_for_list['feed_human_readable_name'] = list_field_model['feed_human_readable_name']
        field_dict_model_for_list['human_readable_name'] = list_field_model['human_readable_name']
        field_dict_model_for_list['value_scrap_type'] = list_field_model['value_scrap_type']
        field_dict_model_for_list['field_types'] = {"types": ["dict"], "default_value": ""}
        field_dict_model_for_list['casting_key'] = ''
        field_dict_model_for_list['exclusion_key'] = ''
        dict_types = {
            "dict": { 
                "type": "dict", 
                "fields": {
                    list_field_name: field_dict_model_for_list_item
                    }
                }
            }
            
        field_dict_model_for_list['types'] = dict_types
        return field_dict_model_for_list
    
    def make_class(field_dict_type_model: Dict, model_field_name: str, class_mapping: Dict, parrent_class_path: List[str], class_type: Literal['dict', 'list_dict', 'list_simple']):
        """создаёт сласс типа 'dict', добавляет его в class_mapping dict
        root_feed_fields: Dict = search_form_v3['feed']['types']['dict']['fields']
        """
        dict_model_fields: Dict = field_dict_type_model['types']['dict']['fields']
        
        # определяем имя класса
        class_suffix = _get_field_to_feeded_name(field_dict_type_model, model_field_name)

        parrent_class_path.append(class_suffix)
        
        class_name = '_'.join(parrent_class_path)
        
        
        # class_name = get_class_name(field_dict_type_model, model_field_name, parrent_class_path, class_mapping)
        # получаем class_layout, выполняем проверку 
        if not (class_layout:= get_filled_class_layout(field_dict_type_model, model_field_name, class_name, parrent_class_path, class_type)):
            # ошибка при созднаии class_layout, пишем лог, выходим без модификации  class_mapping
            logger.error(f"{make_class.__name__}(): ошибка при созднаии class_layout, класс типа 'dict' для field_name: {model_field_name}, parrent_path: {', '.join(parrent_class_path)} не создан")
            return
        # записываем класс в class_mapping
        class_mapping[class_name] = class_layout
        # class_layout создан, заполняем его поля
        # параллельно заполняем 'foreign_key_fields'
        # сначала выполняем проход по полям dict  feed_model
        # определяем их тип и действуем в зависимости от типа
        parrent_class_path_copy = parrent_class_path.copy()
        # parrent_class_path_copy.append(model_field_name)
            
        for field_mame, field_model in dict_model_fields.items():
            # определяем тип поля, действуем в зависимости от типа
            if not (field_model_type:=get_model_type_none_if_error(field_model, field_mame, parrent_class_path_copy)):
                # ошибка при определении типа модели
                # пишем лог, пропускаем поле
                logger.error(f"{make_class.__name__}(): ошибка при определении типа модели поля: {field_mame}, parrent_path: {', '.join(parrent_class_path_copy)}, поле пропущено для добавлеие в класс")
                continue
            # далее действуем в заисимости от типа модели
            if field_model_type in SIMPLE_TYPES_LIST:
                # тип поля - простой тип
                # получаем  поле класса
                class_field = get_filed_class_field_layout(field_model, field_mame, parrent_class_path_copy, field_model_type)
                # получаем имя поля в зависимости от статуса "feed_human_readable_name"
                class_field_name = _get_field_to_feeded_name(field_model, field_mame)
                # записываем поле в class_layout
                class_layout['fields'][class_field_name] = class_field
                # проверяем на "foreign_key_field": true
                if (item_class_binding:=field_model.get('item_class_binding', None)):
                    if (item_class_binding('foreign_key_field', None)):
                        class_layout['foreign_key_fields'].append(class_field_name)
                continue
            if field_model_type == 'dict':
                # запускаем создание класса типа dict
                make_class(field_model, field_mame, class_mapping, parrent_class_path_copy, 'dict')
                continue
            if field_model_type == 'list':
                # определяем тип листа и действуем в зависимости от него
                if not (list_model_type:=get_list_model_list_item_type_none_if_error(field_model, field_mame, parrent_class_path_copy)):
                    # ошибка при определении типа модели лица
                    # пишем лог, пропускаем поле
                    logger.error(f"{make_class.__name__}(): ошибка при определении list_model_type поля: {field_mame}, parrent_path: {', '.join(parrent_class_path_copy)}, поле пропущено для добавлеие в class_mapping")
                    continue
                if list_model_type in SIMPLE_TYPES_LIST:
                    new_dict_model_for_simple_list = get_field_dict_model_for_simple_list_type(field_model, field_mame)
                    make_class(new_dict_model_for_simple_list, field_mame, class_mapping, parrent_class_path_copy, 'list_simple')
                    continue


                    
                # поле простого типа вкючаем его в класс
        # соответственно для каждого поля производим группировку простых полей
        # и полей классов подлежащей дикт модели
        # поля получаем поутём обхода полей dict feed_model
        # могут быть 2-а типа полей:
        # 1. обычные, доступные через 'key' словоря
        #   1.1. обычные поля класса, модели полей простых типов
        #   1.2. сложные поля - классы, модели полей с типами 'dict' и 'list'
        # 2. экстар поля - доступные через ["item_class_binding"]["extra_fields"] 
        #  field_model объекта, могут быть только у класса
            
    # root_fields: Dict = feed_model['fields']
    # root_dict_fields: Dict = feed_model['fields']
    # создадим field_model обёртку root класса
    
    class_mappping = {}
    root_feed_fields: Dict = search_form_v3['feed']['types']['dict']['fields']
    custom_feed_fields = search_form_v3['custom_feed_model']['fields']

    root_field_model = get_field_model()
    # на всякий случай
    root_field_model['visible'] = True
    root_field_model['feed'] = True
    root_field_model['feed_human_readable_name'] = True
    root_field_model['human_readable_name'] = root_class_name
    # зададим правильный тип для модели
    root_field_model['field_types']['types'] = ['dict']
    # положим 'types' root_field_model 'types' search_form_v3['feed'], 
    # т.е. dict c root полями
    root_field_model['types'] = search_form_v3['feed']['types']
    # запустим получение root dict класса и трансформации class_mappping
    make_class(root_field_model, root_class_name, class_mappping, [], 'dict') 
    
    
    return class_mappping

if __name__ == '__main__':
    logging_configure(logger, logging.WARNING)
    # test_model_parsing_v_2()
    # test_model_parsing_v_1()
    # test_get_model()
    # test_model_parsing_v_1_1()
    # convert_parsed_feed_to_class_items_test()