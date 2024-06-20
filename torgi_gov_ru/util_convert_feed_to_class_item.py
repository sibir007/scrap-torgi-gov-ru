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


import logging
import typing


logger = logging.getLogger(__name__)



def convert_parsed_feed_to_class_items(class_name: str, parsed_feed: Dict, class_mapping: Dict):
    

    def make_field_grupping(class_name: str, parsed_data: Dict, parent_class_path: List['str']):
        logger.debug(f"-----> {make_field_grupping.__name__}(): class_name: {class_name}, parent_class_path: [{', '.join(parent_class_path)}]")
        
        simple_field_dict = {}
        class_field_list = []
        
        
        logger.debug(f"{make_field_grupping.__name__}(): parsed_data_type: {type_str(parsed_data)}")
        for field_name, field_value in parsed_data.items():
            logger.debug(f"{make_field_grupping.__name__}(): for field_name, field_value in parsed_data.items(): field_name: {field_name}, class_name: {class_name}, parent_class_path: [{', '.join(parent_class_path)}]")
            # определяем тип данных
            field_value_type = type_str(field_value)
            if field_value_type in SIMPLE_TYPES_LIST:
                logger.debug(f"{make_field_grupping.__name__}(): if field_value_type in SIMPLE_TYPES_LIST: field_value_type: {field_value_type}, class_name: {class_name}, parent_class_path: [{', '.join(parent_class_path)}]")
            # добавляем данные в dict
                simple_field_dict[field_name] = field_value
                continue
            if field_value_type in CLASS_TYPES_LIST:
                logger.debug(f"{make_field_grupping.__name__}(): if field_value_type in SIMPLE_TYPES_LIST: field_value_type: {field_value_type}, class_name: {class_name}, parent_class_path: [{', '.join(parent_class_path)}]")
                class_field_list.append((field_name, field_value))
                continue
            # не поддерживаемый тип данных
            # пишем лог, пропускаем
            logger.error(f"{make_field_grupping.__name__}(): не поддерживаемый тип данных: {field_value_type}, class_name: {class_name}, parent_class_path: {'.'.join(parent_class_path)}")
        return simple_field_dict, class_field_list

    def get_foreign_key_fields_dict(class_name: str, parsed_feed_item: Dict,  parent_class_path: List['str'], class_mapping: Dict) -> Dict:
        return {}
    
    def get_item_class_implementation(class_mapping: Dict, class_name: str) -> type:
        class custom_dict(dict):
            def __init__(self, item):
                item['class_name'] = class_name
                super().__init__(item)
        return custom_dict
    
    
    def prepare_new_feed_item_and_call_convert_parsed_feed_item_to_class_item(
        field_name: str, 
        class_name: str, 
        parent_class_path: List['str'],
        feed_item_to_prepare_field_name: str,
        feed_item_to_prepare: Dict, 
        item_class_mapping: Dict,
        foreign_key_fields: Dict
        ) -> Generator[Dict, None, None]:
        parent_class_path_copy = parent_class_path.copy()
        parent_class_path_copy.append(field_name)
        new_class_name = class_name + '_' + feed_item_to_prepare_field_name
        foreign_key_fields_copy = foreign_key_fields.copy()
        yield from convert_parsed_feed_item_to_class_item(
            feed_item_to_prepare_field_name, 
            new_class_name, 
            feed_item_to_prepare, 
            parent_class_path_copy,
            item_class_mapping,
            foreign_key_fields_copy
            )
    
    def get_dict_wrapper_for_simple_list_item(key_name: str, wrappered_item):
        
        return {key_name: wrappered_item}
        
    
    def convert_parsed_feed_item_to_class_item(
        field_name: str, 
        class_name: str, 
        parsed_feed_item: Dict, 
        parent_class_path: List['str'],
        item_class_mapping: Dict,
        foreign_key_fields: Dict
        ) -> Generator[Dict, None, None]:
        # получаем dict: поля со значениями для класса и лист (имя, dict) типов сласса
        simple_field_dict, class_field_list = make_field_grupping(class_name, parsed_feed_item, parent_class_path)
        # добавляем поля внешних ключей foreign_key_fields  
        simple_field_dict.update(foreign_key_fields)
        # получаем имплементацию Item класса, создам экземпляр, возворащаем
        yield get_item_class_implementation(item_class_mapping, class_name)(simple_field_dict)
        # получаем поля внешних ключей текущего класса
        current_class_foreign_key_fields = get_foreign_key_fields_dict(class_name, parsed_feed_item, parent_class_path, item_class_mapping)
        # обновляем foreign_key_fields для передаче потомкам
        foreign_key_fields.update(current_class_foreign_key_fields)
        # конвертируем остальные классы
        for descendant_field_name, descendant_class in class_field_list:
            # определяем тип
            descendant_class_value_type = type_str(descendant_class)
            # действуем в зависимости от типа
            if descendant_class_value_type == 'dict':
                yield from prepare_new_feed_item_and_call_convert_parsed_feed_item_to_class_item(
                    field_name,
                    class_name,
                    parent_class_path,
                    descendant_field_name,
                    descendant_class,
                    item_class_mapping,
                    foreign_key_fields
                )
                continue
            if descendant_class_value_type == 'list':
                for item in descendant_class:
                    # по заданным условиям все элементы листа должны быть
                    # одного типа, проверка этого осуществляется на предидущих
                    # этапах, поэтому здесь мы полагаем что это условие 
                    # выполнено и не проверяем здесь.
                    # определение типа выполеняем для запуска соответствующего 
                    # обработчика
                    item_type = type_str(item)
                    if item_type in SIMPLE_TYPES_LIST:
                        # обернём элемент в dict с ключём descendant_field_name 
                        wrappered_item = get_dict_wrapper_for_simple_list_item(descendant_field_name, item)
                        yield from prepare_new_feed_item_and_call_convert_parsed_feed_item_to_class_item(
                            field_name,
                            class_name,
                            parent_class_path,
                            descendant_field_name,
                            wrappered_item,
                            item_class_mapping,
                            foreign_key_fields
                        )
                        continue
                    if item_type == 'dict':
                        yield from prepare_new_feed_item_and_call_convert_parsed_feed_item_to_class_item(
                            field_name,
                            class_name,
                            parent_class_path,
                            descendant_field_name,
                            item,
                            item_class_mapping,
                            foreign_key_fields
                        )
                        continue
                    # ошибочное состояние - 'list' не может быть типом листа
                    logger.error(f"{convert_parsed_feed_item_to_class_item.__name__}(): ошибочное состояние - типЖ '{item_type}' не может быть типом листа")

    yield from convert_parsed_feed_item_to_class_item(class_name, class_name, parsed_feed , [], class_mapping, {})
    
    

def convert_parsed_feed_to_class_items_test():
    parsed_item = load_dict_or_list_from_json_file('custom_raw_feed_item.json')
    for item in convert_parsed_feed_to_class_items("lot", parsed_item, {}):
        print(item)




if __name__ == '__main__':
    logging_configure(logger, logging.WARNING)
    # test_model_parsing_v_2()
    # test_model_parsing_v_1_1()
    # test_model_parsing_v_1()
    # test_get_model()
    # test_model_parsing_v_1_1()
    convert_parsed_feed_to_class_items_test()