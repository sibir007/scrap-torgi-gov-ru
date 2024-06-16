from email.policy import default
from lib2to3.pytree import convert
from math import lgamma
import re
from tabnanny import check
from tkinter import N
from turtle import st
from typing import Iterable, Dict, Generator, Literal, NoReturn, Set, Tuple, List, FrozenSet, Union, Any, Callable
from unittest.mock import DEFAULT

import scrapy
from util import logging_configure, load_dict_or_list_from_json_file, write_dict_or_list_to_json_file
from util import get_data_generator_from_dict_iterable

import logging
import typing

SIMPLE_TYPES_LIST = ['int', 'float', 'bool', 'str']

logger = logging.getLogger(__name__)

def type_str(value: Any) -> str:
    return type(value).__name__

# def fill_model_v3_item_class_bindings(model_v_3: Dict) -> None:
#     """заполняет отредактированную модель item_class_binding полями"""

#     dict_model: Dict = model_v_3['feed']['types']['dict']

#     def _get_item_class_binding_template() -> Dict:
#         template = {
#                 "field_type": "",
#                 "membership": []
#                     }
#         return template
    
#     def _fill_field(field_name: str, field_model: Dict, parent_field_names: List[str]):
#         """заполняет item_class_binding поле модели поля и всх потомков"""
#         # записываем шаблон поля
        
#         field_model['item_class_binding'] = _get_item_class_binding_template()
#         # получаем "types" модели
#         try:
#             types_path = ['field_types', 'types']
#             types = get_value_from_dict_based_on_path_except_if_absent(field_model, types_path)
#         except:
#             # ошибка полученияе field_types, неправильный формат field_model
#             # пишем лог, записываем в field_type error, выходим
#             logger.error(f'_fill_field(): ошибка полученияе field_types, неправильный формат field_model, имя поля: {field_name}, парентс [{", ".join(parent_field_names)}], types_path: [{", ".join(types_path)}]') 
#             field_model['item_class_binding']['field_type'] = 'error'
#             return
#         # проверяем поле "types" модели, действуем в зависимости от того
#         # простое оно или нет
#         if "list" in types:
#             # если тип лист, то действуем в зависимости от 
#             # типа его элементов для этого проверяем поле type_for_list
#             try:
#                 type_for_list_path = ['field_types', 'type_for_list']
#                 type_for_list = get_value_from_dict_based_on_path_except_if_absent(field_model, type_for_list_path)
#             except:
#                 # ошибка полученияе type_for_list, неправильный формат field_model
#                 # пишем лог, записываем в field_type error, выходим
#                 logger.error(f'_fill_field(): ошибка полученияе type_for_list, неправильный формат field_model, имя поля: {field_name}, парентс [{", ".join(parent_field_names)}], type_for_list_path: [{", ".join(type_for_list_path)}]') 
#                 field_model['item_class_binding']['field_type'] = 'error'
#                 return
#             # проверяем  тип list
#             if type_for_list == 'list':
#                 # считаем данную ситуацию ошибкой
#                 # пишем лог, пишем ошибку  field_type
#                 # выходим
#                 logger.error(f'_fill_field(): не верный тип для типа list, "type_for_list" не может быть "list", имя поля: {field_name}, парентс [{", ".join(parent_field_names)}]') 
#                 field_model['item_class_binding']['field_type'] = 'error'
#                 return
#             elif type_for_list == 'dict':
#                 # пишем 'field_type': 'class'
#                 # запускаем _fill_model_fields()
#                 try:
#                     # получаем  "fields" из 'dict' листа
#                     dict_model_path = ['types', 'list', 'types', 'dict']
#                     dict_model = get_value_from_dict_based_on_path_except_if_absent(field_model, dict_model_path)
#                     field_model['item_class_binding']['field_type'] = 'class'
#                     _fill_dict_model(dict_model, field_name, parent_field_names)
#                     return
#                 except:
#                     # ошибка получения 'dict_model' из 'типов листа 
#                     # пишем лог, записываем в field_type error, выходим
#                     logger.error(f'_fill_field(): ошибка получения "dict_model" из типов листа, неправильный формат field_model, имя поля: {field_name}, парентс [{", ".join(parent_field_names)}], dict_model_path: [{", ".join(dict_model_path)}]') 
#                     field_model['item_class_binding']['field_type'] = 'error'
#                     return
#             else:
#                 # у листа простой тип
#                 parent_field_names.append(field_name)
#                 class_name = "_".join(parent_field_names)
#                 field_model['item_class_binding']['field_type'] = 'member'
#                 field_model['item_class_binding']['membership'].append(class_name)        
#                 return
#         elif 'dict' in types:
#             pass
#             return
#         else:
#             # поле простое, соответственно оно является членом класса.
#             # имя класса создаём путём конкатенации parent_field_names 
#             # через "_"
#             class_name = "_".join(parent_field_names)
#             # пишем занчения в 'item_class_binding'
#             field_model['item_class_binding']['field_type'] = 'member'
#             field_model['item_class_binding']['membership'].append(class_name)
        
#     def _fill_dict_model(dict_model: Dict, model_fields_field_name: str, paretn_fields_name: List[str]):
#         # олучаем fields
#         try:
#             dict_model_fields_path = ['fields']
#             fields = get_value_from_dict_based_on_path_except_if_absent(dict_model, dict_model_fields_path)
#         except:
#             # ошибка полученияе fields из dict модели
#             # пишем лог, записываем в field_type error, выходим
#             logger.error(f'_fill_model_fields(): ошибка полученияе fields из dict модели, имя поля: model_fields_field_name: {model_fields_field_name}, paretn_fields_name [{", ".join(paretn_fields_name)}], dict_model_fields_path: [{", ".join(dict_model_fields_path)}]') 
#             return
#         for field_name, field_model in fields.items():
#             paretn_fields_name_copy = paretn_fields_name.copy()
#             paretn_fields_name_copy.append(model_fields_field_name)
#             _fill_field(field_name, field_model, paretn_fields_name_copy)
    
#     _fill_dict_model(dict_model, 'lot', [])


# def get_item_class_binding(search_forrm_v_3: Dict) -> Dict:
#     res_dict = {}
#     feed_model = search_forrm_v_3['feed']['types']['dict']

#     def get_bindings_templat() -> Dict:
#         bindings_templat = {
#             "type": "",
#             "path": [],
#             "fields": [],
#             "extra_fields": {}
#         }
#         return bindings_templat


#     def simple_list_bindings(parent_field_name: str, feed_dict_model: Dict, bindings: Dict, path: List[str], extra_fields: Dict):
#         copy_path_for_name = path.copy()
#         copy_path_for_name.append(parent_field_name)
#         class_name = "_".join(copy_path_for_name)
#         bindings[class_name] = get_bindings_templat()
#         bindings[class_name]['type'] = 'simple_list'


#     def dict_type_bindings(parent_field_name: str, field_dict_model: Dict, feed_dict_model: Dict, bindings: Dict, path: List[str], extra_fields: Dict, dict_type: str):
#         copy_path_for_name = path.copy()
#         copy_path_for_name.append(parent_field_name)
#         class_name = "_".join(copy_path_for_name)
#         bindings[class_name] = get_bindings_templat()
#         bindings[class_name]['type'] = dict_type
#         for field_name, field_maodel in field_dict_model['fields'].items():
#             # сначала проверяем занчение "feed" модели поля,
#             # если False - поле пропускаем
#             if not field_maodel['feed']:
#                 continue
#             # получаем binding тип поля
#             binding_type = field_maodel['item_class_binding']['type']
#             # действуем в зависимости от типа
#             if binding_type == 'member':
#                 # поле является членом класса, поэтому его нужно
#                 # добавить в поля класса, 
#                 # имя поля берётся в зависимости
#                 # от значения "feed_human_readable_name", если True то
#                 # записывается human_readable_name
#                 if field_maodel["feed_human_readable_name"]:
#                     field_name = field_maodel["human_readable_name"]
#                 # аппендим field_name в "fields" класса
#                 bindings['fields'].append(field_name)
#             elif binding_type == 'simple_list':
#                 # поле является классом 'simple_list',
#                 # т.е. в поле содержится лист с простыми занчениями
#                 # запускаем simple_list_bindings
#                 path_copy = path.copy()
#                 path_copy.append(parent_field_name)
#                 class_extra_fields = field_maodel['item_class_binding']["extra_fields"]
#                 simple_list_bindings(field_name, feed_dict_model, bindings, path_copy, class_extra_fields)
#             elif binding_type == 'dict_list':
#                 # поле является классом 'dict_list',
#                 # т.е. в поле содержится лист со словорями (dict)
#                 # запускаем simple_list_bindings
#                 pass
#     # res_dict['lot'] = 


def get_feed_model_v2_from_feed_items_file(feed_items_file: str, path: List[str]) -> Dict:
    """принимает feed_items_file и path до target elements list, возвращает feed_model dict"""

    feed_items_v1_list = typing.cast(List[Dict], load_dict_or_list_from_json_file(feed_items_file))
    return get_feed_model_v2_from_feed_items_list(feed_items_v1_list, path)


def get_feed_model_v2_from_feed_items_list(data: Union[Dict, List], path: List[str] = []) -> Dict:
    """принимае дата структуру List[Dict], возвращает модель этой структуры"""


    def get_value_dict_type():
        field_attr = {
            # модель будет иметь два типа полей:
            # 1. поля созданные на основании парсинга данных
            # 2. поля добавленные в модель, т.е. не содержащиеся в данных
            # поля второго типа должны быть производными от полей 1-го типа и 
            # должны формироваться после парсинго данных, для разделения полей
            # вводим аттребут "field_type": {"type": "data"} - введённые в 
            # модель на основании данных и 
            # "field_type": {"type": "custom", 
            #               "destinations_paths": [[]]}
            # введённые произвольно
            # поле "field_type": {"type": "data"}, по умолчанию None
            # "field_type": {"type": "custom"} вводится вручную при
            # описании custom модели
            # для отобразения поля на сайте, для его выбора
                    "visible": False,
            # False - поле не попадает в feed
                    "feed": False,
            # True - качестве ключа для поля будет использоваться значение 
            # из human_readable_name, в противном случае key value 
                    "feed_human_readable_name": False,
                    "human_readable_name": "",
            # {"type": "direct"}, {"type": "dict", "dict_path": []}, 
            # {"type": "layout_formatting", 
            #  "layout_path": [],
            #  "layout_format_feed_items_paths": {
            #                      "raw_feed": {'name1': [path]},
            #                      "search_form": {}
            #                   }
            #               } - 
            # }
            # direct - значение берётся то которое вычисляется
            # dict - вычисленное значение подставляется в словарь по ссылке 
            # dict_path, полученное заначение записывается в поле
            # layout_formatting - значение поля подставляется в layout,
            # находимый по пути "layout_path" и полученное значение 
            # записывается в поле,
            # "layout_format_feed_items_paths" поле применимо только в 
            # контексте  "field_type": {"type": "custom"}, по данному полю
            # ищутся элементы для встаки в layout
                    "value_scrap_type": {},
            # определяет какие типы могут данных могут присваиваться полю и значение 
            # по умолчанию в случае если фактический тип данных не соответствует установленному 
            # или если данное поле отсутсвует в данных
                    "field_types": {"types": ["str"], "default_value": ""}, 
            # если тип данных dict, а field_types просой тип, то сюда записываестя
            # кей в ктором записаны данные для присваиванюя полю
                    "casting_key": "",
            # если данные list[dict], то exclusion_key это кей в словаре который нужно 
            # проверять на пустое значение. Если exclusion_key пустой или None весь 
            # dict исключаестя из итогового list  
                    "exclusion_key": "",
            # типы которые бывают у данного поля в исходных данных, данные типы 
            # не обязательно попадают в итоговое значение и могут быть каститься 
            # до другого типа при парсинге через модель
                    "types": {
                        }
                    }
        return field_attr

    def get_dict_type(dict_item: Dict):
        res_dict_type = {'type': 'dict', 'fields': {}}
        for item_key, item_value in dict_item.items():
            value_dict_type = get_value_dict_type()
            item_value_type = type(item_value).__name__
            if item_value_type == 'dict':
                value_dict_type['types'][item_value_type] = get_dict_type(item_value)
            elif item_value_type == 'list':
                value_dict_type['types'][item_value_type] = get_list_type(item_value)
            else:
                value_dict_type['types'][item_value_type] = get_simple_type(item_value_type)
            # value_dict_type['types'][item_value_type] = value_dict_type
            res_dict_type['fields'][item_key] = value_dict_type
        return res_dict_type         
                    
    def get_simple_type(field_type: str) -> Dict:
        return {'type': field_type}


    def get_list_type(item_iterable: Iterable) -> Any:
            # logger.debug('in get_list_type(item_iterable: Iterable)')
        res_list_type: Dict = {'type': 'list', 'types': {}}
        for item in item_iterable:
            if (target_type:=type(item).__name__) == 'dict':
                # logger.debug(f'in if (target_type:=type(item).__name__) == "dict": target_type: {target_type}')
                item_dict_type: Dict = get_dict_type(item)
                # print(item_dict_type)
                # logger.debug(f'item_dict_type: {item_dict_type}')
                if (saved_item_dict_type:=res_list_type['types'].get('dict', None)) != None:
                    # logger.debug(f'if (saved_item_dict_type:=res_list_type[types].get(dict, None)) != None:')
                    merge_dict_type_in_saved_item_dict_type(saved_item_dict_type, item_dict_type)
                else:
                    res_list_type['types']['dict'] = item_dict_type
            elif target_type == 'list':
                item_list_type = get_list_type(item)
                if (saved_item_list_type:=res_list_type['types'].get('list', None)) != None:
                    merge_list_type_in_saved_item_list_type(saved_item_list_type, item_list_type)
                else:
                    res_list_type['types']['list'] = item_list_type
            else:
                res_list_type['types'][target_type] = get_simple_type(target_type)
        return res_list_type   

                
    def merge_list_type_in_saved_item_list_type(saved_item_list_type: Dict, item_list_type: Dict) -> Dict:
        item_list_type_types: Dict = item_list_type['types']
        saved_item_list_type_types: Dict = saved_item_list_type['types']
        for type_key, type_value in item_list_type_types.items():
            # провеяем есть ли сливаемый тип в сохранённых типах
            if (saved_type:=saved_item_list_type_types.get(type_key, None)) == None:
                # сливаемый тип в сохранённых типах отсутствует - просто добавляем сливаемый тип в сохранённые
                saved_item_list_type_types[type_key] = type_value
            else:
                # сливаемый тип в сохранённых типах есть
                # действуем в зависимости от типа сливаемого типа

                if type_key == 'dict':
                    # если тип dict закускаем слияние dict типов
                    merge_dict_type_in_saved_item_dict_type(saved_type, type_value)
                elif type_key == 'list':
                    # если тип list закускаем слияние list типов
                    merge_list_type_in_saved_item_list_type(saved_type, type_value)
                else:
                    # если тип простой ничего не делаем
                    pass
                    
                
        return saved_item_list_type
        
        
    def merge_dict_type_in_saved_item_dict_type(saved_item_dict_type: Dict, item_dict_type: Dict) -> Dict:
        # print(f'saved_item_dict_type {saved_item_dict_type}')
        dict_type = {
            'type': "dict",
            'field': {
                'some_field': {
                            "visible": False,
                            "feed": False,
                            "feed_human_readable_name": True,
                            "human_readable_name": "",
                            "types": {
                                'dict': {
                                        'type': "dict",
                                        'field': {
                                            'some_field': {
                                                        "visible": False,
                                                        "feed": False,
                                                        "feed_human_readable_name": "true",
                                                        "human_readable_name": "",
                                                        "types": {
                                                            'dict': {
                                                                
                                                            }
                                                            }
                                            }
                                        }
                                    }
                                }
                }
            }
        }
        item_dict_type_fields: Dict = item_dict_type['fields']
        saved_item_dict_type_fields: Dict = saved_item_dict_type['fields']
        for fields_name, field_value in item_dict_type_fields.items():
            # сначала проверяем есть ли в сохранённом dict_type поле с именем из сливаемого типа
            if (saved_field_value:=saved_item_dict_type_fields.get(fields_name, None)) == None:
                
                # в сохранённом dict_type поле с именем из сливаемого типа отсутствуем -добаляем поле в сохранённый dict_type
                saved_item_dict_type_fields[fields_name] = field_value
            else:
                # в сохранённом dict_type поле с таким именем есть
                # проверяем есть ли в сохранённом поле тип сливаемого поля
                field_value_types=list(field_value['types'].keys())
                for field_value_type in field_value_types:
                    
                    if (saved_field_value_type:=saved_field_value['types'].get(field_value_type, None)) == None:

                        # тип сливаемого поля в типах сохранённого поля отсутствует - добавляем новый тип в типы сохранённого поля    
                        saved_field_value['types'][field_value_type] = field_value['types'][field_value_type]
                    else:
                        # тип сливаемого поля в типах сохранённого поля есть - действуем в зависимости от типа поля
                        if field_value_type == 'dict':
                            # если тип dict то закускаем сливание типов сохранённого и сливаемого поля     
                            merge_dict_type_in_saved_item_dict_type(saved_field_value_type, field_value['types'][field_value_type])
                        elif field_value_type == 'list':
                            # если тип list то закускаем сливание типов сохранённого и сливаемого поля
                            merge_list_type_in_saved_item_list_type(saved_field_value_type, field_value['types'][field_value_type])     
                        else:
                            # если тип простой то ничего не делаем, он уже присутствует
                            pass
                        
        return saved_item_dict_type
    


    response_data_generator: List = typing.cast(List, get_data_generator_from_dict_iterable(data, path))

    res_model = get_list_type(response_data_generator)
    

   
    return res_model





def _get_layout(field_name: str, 
            value_scrap_type: Dict, 
            search_form_v3: Dict
            ) -> Union[str, None]:
    """возвращает layout строку из dict, по данному пути, при ошибке возвращает None"""
    
    if layout_path:=value_scrap_type.get('layout_path', None):
        # layout_path существует и он не пустой
        if isinstance(layout_path, list):
            # layout_path правильного типа
            # пытаемся получить layout из search_form_v3 по указанному layout_path
            try:
                layout = get_value_from_dict_based_on_path_except_if_absent(search_form_v3, layout_path) 
            except Exception as e:
                # ошибка при звлечении значения из search_form_v3 
                #  пишем лог, возвращаем None
                logger.error(f'_get_layout(): ошибка при извлечении значения из search_form_v3, путь [{", ".join(layout_path)}] не существует, имя поля модели: {field_name}')
                return None    
            # проверяем тип layout - должен быть "str" 
            if isinstance(layout, str):
                # значение layout правильного типа 
                return layout
            else:
                # значение layout не правильного типа
                #  пишем лог, возвращаем None
                logger.error(f'_get_layout(): значение layout не правильного типа: {type(layout).__name__}, должен быть str')
                return None
        else:
            # layout_path не правильного типа
            # пишем лог, возвращаем None
            logger.error(f'_get_layout(): layout_path не правильного типа: {type(layout_path.__name__)}, должен быть "list"')
            return None
    else:
        # layout_path не существует или он пустой - ошибка
        # пишем лог, возвращаем None
        logger.error(f'_get_layout(): layout_path не существует или он пустой, имя поля модели: {field_name}')
        return None


class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'


    
def feed_customizing(search_form_v3: Dict, raw_feed_item: Dict, parsed_feed_item: Dict):
    """получает search_form_v3 dict, сырой feed_item и парсед через модель feed_item,
    производит customizing parsed_feed_item по custom_feed_model search_form_v3 

    Args:
        search_form_v3 (Dict): search_form_v3
        raw_feed_item (Dict): сырой feed_item 
        parsed_feed_item (Dict): парсед через дата модель feed_item 

    Returns:
        Dict: customized parsed_feed_item 
    """
    
    
    
        
    def process_dict_customizing(model_field_name: str, 
                                  model_field_model: Dict, 
                                  value_scrap_type: Dict, 
                                  search_form_v3: Dict, 
                                  raw_feed_item: Dict,
                                  parsed_feed_item: Dict):
        """заныение для custom полей берётся из словаря по пути "dict_path" """
        
        
        
        # сразу получаем destination  dict куда будет добавляться 
        # custom значение
        if (destinations_list:=_get_destinations(model_field_name, model_field_model, parsed_feed_item)) == None:
            # ошибка получения destinations
            # логи прописаны в _get_destination(), выходим
            return
        # проверяем dict_path
        if (dict_path:= value_scrap_type.get('dict_path', None).copy()) == None:
            # dict_path не определён
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_path не определён, имя поля модели: {model_field_name}')
            return
        
        # проверяем, что dict_path типа "list"
        if not isinstance(dict_path, list):
            # dict_path не правильного типа
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_path не правильного типа: {type(dict_path).__name__}, должен быть "list", имя поля модели: {model_field_name}')
            return
        
        # получаем dect_key_path
        if (dict_key_path:=value_scrap_type.get('dict_key_path', None)) == None:
            # dict_key_path не определён
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_key_path не определён, имя поля модели: {model_field_name}')
            return
        
        # проверяем, что dict_key_path типа "list"
        if not isinstance(dict_key_path, list):
            # dict_key_path не правильного типа
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_key_path не правильного типа: {type(dict_path).__name__}, должен быть "list", имя поля модели: {model_field_name}')
            return
        
        # # объединяеяем dict_path и dict_key_path
        # dict_path.extend(dict_key_path)
        # # получаем dict_key
        try:
            dict_key = get_value_from_dict_based_on_path_except_if_absent(raw_feed_item, dict_key_path)
        except:
            # ошибка получения занчения из dict
            # считаем, что запрашиваемый элемент не существует в raw_feed
            # пишем лог, присваиваем dict_key дефолт значение модеи 
            logger.info(f'process_dict_customizing(): path: [{", ".join(dict_key_path)}] не существует в raw_feed_item, имя поля модели: {model_field_name}')
            dict_key = get_model_default_value_for_model_type(model_field_model, model_field_name, [])
        
        # проверяем тип dict_key
        if not isinstance(dict_key, str):
            # ошибка типа dict_key
            # пишем лог, выходим
            logger.error(f'process_dict_customizing(): ошибка типа dict_key: {type(dict_key).__name__}, должен быть "str", имя поля модели: {model_field_name}')
            return
        # объединяем dict_path dict_key
        dict_path.extend(['available_values', 'values', dict_key, 'name'])
        # получаем custom значение из словаря
        
        try:
            dict_value = get_value_from_dict_based_on_path_except_if_absent(search_form_v3, dict_path)
        except:
            # ошибка получения занчения из dict
            # пишем лог, выходим
            logger.error(f'process_dict_customizing(): ошибка получения занчения из словаря, dict_path: [{", ".join(dict_path)}], имя поля модели: {model_field_name}')
            return
        # пгулчаем 
        custom_name = _get_field_to_feeded_name(model_field_model, model_field_name)
        # пишем в destination custom значение 
        for destination in destinations_list:
            destination[custom_name]  = dict_value
        # return parsed_feed_item
 
 
 
    def _get_destinations(model_field_name: str, model_field_model: Dict, parsed_feed_item: Dict) -> Union[List[Dict],None]:

        if (destinations_paths:=model_field_model['field_type'].get('destinations_paths', None)) == None:
            # destinations_paths отсутствует - ошибка
            # пишем лог, выходим
            logger.error(f'_get_destinations(): "destinations_paths" отсутствует, имя поля модели: {model_field_name}')
            return None
        # проверяем тип - должен быть list
        if not isinstance(destinations_paths, list):
            # тип не правильный
            # пишем error log и выходим
            logger.error(f'_get_destinations(): не правильный тип destinations_paths: {type(destinations_paths).__name__}, должен быть "list", имя поля модели: {model_field_name}')
            return None
        # TODO: переделать на get_value_from_dict_based_on_path_create_if_absent() 
        # получаем список destination
        destination_list = []
        for destination_path in destinations_paths:
            if not isinstance(destination_path, list):
                # тип не правильный
                # пишем error log и пропускаем
                logger.error(f'_get_destinations(): не правильный тип destination_path: {type(destination_path).__name__}, должен быть "list", имя поля модели: {model_field_name}')
                continue
            try:
                destination = get_value_from_dict_based_on_path_except_if_absent(parsed_feed_item, destination_path)
            except:
                # ошибка при получении destination из  parsed_feed_item
                # по destination_path, пишем лог, пропускаем
                logger.error(f'_get_destinations(): ошибка при получении destination из parsed_feed_item по destinations_paths: [{", ".join(destination_path)}], имя поля модели: {model_field_name}')
                continue
            # проверяем тип destination - должен быть dict
            if not isinstance(destination, dict):
                #  не правильный тип destination
                # пишем лог, пропускаем
                logger.error(f'_get_destinations(): ошибка типа destination: {type(destination).__name__}, должен быть "dict", destinations_paths: [{", ".join(destination_path)}], имя поля модели: {model_field_name}')
                continue
            destination_list.append(destination)
            # проверяем что destination_list не пустой
        if not destination_list:
            # destination_list пустой - ошибка
            # пишем лог, выходим
            logger.error(f'_get_destinations(): destination_list пустой, destinations_paths: [{[", ".join(destination_path) for destination_path in destinations_paths]}], имя поля модели: {model_field_name}')
            return None
        return destination_list
        
    
    def process_layout_formatting_customizing(model_field_name: str, 
                                            model_field_model: Dict,
                                            value_scrap_type: Dict, 
                                            search_form_v3: Dict, 
                                            raw_feed_item: Dict,
                                            parsed_feed_item: Dict):
        
        def _set_format_items(field_name: str, 
                        format_items_sours: Dict, 
                        format_feed_items: Dict, 
                        feed_item_or_search_form: Dict) -> None:
            """получает из format_items_sours (либо "raw_feed", либо "search_form")
            format items элементы, записывает их в format_feed_items dict, 
            в случае ошибок 
            пишет логи
            """
            for format_feed_item_name, format_feed_item_value_path in format_items_sours.items():
                # проверяем формат format_feed_item_value_path - должет быть list
                if isinstance(format_feed_item_value_path, list):
                    # тип правильный 
                    # пробуем получить значение из feed_item dict по format_feed_item_value_path
                    try:
                        format_feed_item_value = get_value_from_dict_based_on_path_except_if_absent(feed_item_or_search_form, format_feed_item_value_path)
                    except Exception as e:
                        # ошибка получения занчения из dict по path
                        # пишем лог, пропускаем данный format items
                        logger.error(f'_set_format_items_from_raw_feed(): ошибка: "{e}" получения занчения из feed_item по pathlayout_format_feed_items_paths: [{", ".join}]  не существует или он не пустой, имя поля модели: {field_name}')
                    else:
                        # получение значения из feed_item dict по path
                        # прошло без ошибок, создам format item  
                        # в format_feed_items dict
                        format_feed_items[format_feed_item_name] = format_feed_item_value
                        # запишем дебаг лог
                        logger.debug(f'_set_format_items_from_raw_feed(): получено занчения из feed_item по pathlayout_format_feed_items_paths: [{", ".join(format_feed_item_value_path)}], создали format item: {format_feed_item_name}:{format_feed_item_value}, имя поля модели {field_name}')
                        
                else:
                    # формат не правильный
                    # пишем лог, пропускаем данный format items
                    logger.error(f'_set_format_items_from_raw_feed(): не верный тип format_feed_item_value_path: {type(format_feed_item_value_path).__name__}, должен быть "lict", имя поля модели: {field_name}, имя поля raw_feed: {format_feed_item_name}')
            
        def _get_layout_format_items(field_name: str, 
                        value_scrap_type: Dict, 
                        search_form_v3: Dict, 
                        raw_feed_item: Dict) -> Dict:
            """возвращает dict из name=value элементы форматирования layout,
            в случае ошибок при получении возвращает None, который должен проверяться
            вызывающей функцией
            """
            # создаём экзумпляр safesub который будет подставляться 
            # в format_map()
            format_feed_items = safesub()
            # получаем layout_format_feed_items_paths
            if layout_format_feed_items_paths:=value_scrap_type.get('layout_format_feed_items_paths', None):
                # layout_format_feed_items_paths существует и он не пустой
                # получаем значения "name:value" из raw_feed
                if raw_feed:=layout_format_feed_items_paths.get('raw_feed', None):
                    # raw_feed существует и он не пустой, получаем format_feed_items
                    # из raw_feed
                    _set_format_items(field_name,
                                        raw_feed,
                                        format_feed_items,
                                        raw_feed_item)
                else:
                    # raw_feed не существует или он пустой
                    # пишем инфо лог
                    logger.info(f'_get_layout_format_items(): raw_feed format_items отсутствуюе, имя поля модели: {field_name}')
                    
                # получаем значения "name:value" из "search_form" элемента "layout_format_feed_items_paths" 
                if search_form:=layout_format_feed_items_paths.get('search_form', None):
                    # "search_form" существует и он не пустой, получаем format_feed_items
                    # из "search_form"
                    _set_format_items(field_name,
                                        search_form,
                                        format_feed_items,
                                        search_form_v3)
                else:
                    # raw_feed не существует или он пустой
                    # пишем инфо лог
                    logger.info(f'_get_layout_format_items(): "search_form" format_items отсутствуют, имя поля модели: {field_name}')
                
                return format_feed_items
            else:
                # layout_format_feed_items_paths не существует или он пустой
                # считаем данную ситуацию возможной, например если нам не нужно 
                # форматировано layout
                # пишем инфо лог, возвращаем пустой format_feed_items
                logger.info(f'_get_layout_format_items(): layout_format_feed_items_paths не существует или он не пустой, имя поля модели: {field_name}')
                return format_feed_items    
        
        
        # сразу получаем destination  dict куда будет добавляться 
        # custom значение
        if (destinations_list:=_get_destinations(model_field_name, model_field_model, parsed_feed_item)) == None:
            # ошибка получения destinations
            # логи прописаны в _get_destinations(), выходим
            return
        # получаем layout, если в роцессе получение возникли ошибки 
        # то вернётся None
        if (layout:=_get_layout(model_field_name, value_scrap_type, search_form_v3)) == None:
            # None, ошибка получения layout
            # логи прописаны в  _get_layout()
            # выходим, ничего не делая
            return
        # layout есть, получаем layout_format_items
        # мы всегда получаем экземпляр layout_format_items dict
        # даже если в процессе получения  format_items произошли ошибки
        # поэтому проверку на None не делаем 
        layout_format_items = _get_layout_format_items(model_field_name, value_scrap_type, search_form_v3, raw_feed_item)
        formated_layout = layout.format_map(layout_format_items)
        custom_name = _get_field_to_feeded_name(model_field_model, model_field_name)
        # пишем в destination custom значение 
        for destination in destinations_list:
            destination[custom_name] = formated_layout
        # return parsed_feed_item
    
    def process_default_value_customizing(model_field_name: str, 
                                        model_field_model: Dict,
                                        value_scrap_type: Dict, 
                                        search_form_v3: Dict, 
                                        raw_feed_item: Dict,
                                        parsed_feed_item: Dict):
        """если в custom_feed_model указано поле со 
        статусом "feed": true но "value_scrap_type" для
        него не определён - мы добавляем данное поле в feed
        с дефолтным занчением для данной модели поля"""

        # сразу получаем destination  dict куда будет добавляться 
        # custom значение
        if (destinations_list:=_get_destinations(model_field_name, model_field_model, parsed_feed_item)) == None:
            # ошибка получения destinations
            # логи прописаны в _get_destination(), выходим
            return
        # получаем layout, если в роцессе получение возникли ошибки 
        # то вернётся None
        if (default_value:= get_model_default_value_for_model_type(model_field_model, model_field_name, [])) == None:
            # None, ошибка получения default_value
            # пишем логи
            # выходим, ничего не делая
            logger.error(f'process_default_value_customizing(): ошибка получения default_value, имя поля модели: {field_name}')
            return
        # default_value есть
        # получаем custom_name
        custom_name = _get_field_to_feeded_name(model_field_model, model_field_name)
        # пишем в destination custom значение 
        for destination in destinations_list:
            destination[custom_name] = default_value
        # return parsed_feed_item
    
    
    def _get_direct_value(model_field_name: str, 
                        model_field_model: Dict,
                        value_scrap_type: Dict, 
                        search_form_v3: Dict, 
                        raw_feed_item: Dict,
                        parsed_feed_item: Dict):
        #  получаем value_sourse и value_path
        if not (value_path:=value_scrap_type.get('value_path', None)):
            # ошибка полученияv value_path
            # пишем лог, выходим
            logger.error(f'_get_direct_value(): ошибка полученияv value_path: не существует или пустойб имя поля модели: {model_field_name}')
            return None
        # получаем тип источника "raw_feed", "parsed_feed", search_form_v3
        if not (sours_type:=value_path.get('type', None)):
            # ошибка полученияv sours_type
            # пишем лог, выходим
            logger.error(f'_get_direct_value(): ошибка полученияv sours_type: не существует или пустойб имя поля модели: {model_field_name}')
            return None
        # получаем путь в к значению
        if not (path:=value_path.get('path', None)):
            # ошибка полученияv path
            # пишем лог, выходим
            logger.error(f'_get_direct_value(): ошибка полученияv path: не существует или пустойб имя поля модели: {model_field_name}')
            return None
        sours = raw_feed_item if sours_type == "raw_feed" else parsed_feed_item if sours_type == "parsed_feed" else search_form_v3
        try:
            target_value = get_value_from_dict_based_on_path_except_if_absent(sours, path)
        except:
            # ошибка при получении value из sours
            # пишем лог, пропускаем
            logger.error(f'_get_direct_value(): ошибка при получении value из: {sours_type} по path: [{", ".join(path)}], имя поля модели: {model_field_name}')
            return None
        return target_value
            
        
        
    def process_direct_value_customizing(model_field_name: str, 
                                        model_field_model: Dict,
                                        value_scrap_type: Dict, 
                                        search_form_v3: Dict, 
                                        raw_feed_item: Dict,
                                        parsed_feed_item: Dict):
        """занчение для custom поля берётся по пути "direct_path"
        "value_scrap_type" модели поля
        """
        # сразу получаем destination  dict куда будет добавляться 
        # custom значение
        if (destinations_list:=_get_destinations(model_field_name, model_field_model, parsed_feed_item)) == None:
            # ошибка получения destinations
            # логи прописаны в _get_destination(), выходим
            return
        # получаем т
        # получаем layout, если в роцессе получение возникли ошибки 
        # то вернётся None
        if (direct_value:= _get_direct_value(model_field_name, model_field_model, value_scrap_type, search_form_v3, raw_feed_item, parsed_feed_item )) == None:
            # None, ошибка получения direct_value
            # пишем логи
            # выходим, ничего не делая
            logger.error(f'process_direct_value_customizing(): ошибка получения direct_value, имя поля модели: {field_name}')
            return
        # direct_value есть
        # получаем custom_name
        custom_name = _get_field_to_feeded_name(model_field_model, model_field_name)
        # пишем в destination custom значение 
        for destination in destinations_list:
            destination[custom_name] = direct_value
        # return parsed_feed_item
    
    
    custom_feed_model_fields: Dict = search_form_v3['custom_feed_model']['fields']
    # field_names_to_customizing = _get_to_feeded_fields(custom_feed_model)
    for field_name, field_model in custom_feed_model_fields.items():
        if not field_model['feed']:
            continue
        # проверяем что value_scrap_type определн
        if (value_scrap_type_type:=(value_scrap_type:=field_model['value_scrap_type']).get('type', None)) == None:
            # value_scrap_type не определён - 
            # берём дефолтное значение модели, 
            # на всякий случай пишем лог - 
            logger.info(f'{feed_customizing.__name__}(): value_scrap_type не определён, имя поля модели: {field_name}')
            process_default_value_customizing(field_name, field_model, value_scrap_type, search_form_v3, raw_feed_item, parsed_feed_item)
        
        # value_scrap_type определён - действуем в зависимости от типа
        elif value_scrap_type_type == 'layout_formatting':
            process_layout_formatting_customizing(field_name, field_model, value_scrap_type, search_form_v3, raw_feed_item, parsed_feed_item)
        elif value_scrap_type_type == 'dict':
            process_dict_customizing(field_name, field_model, value_scrap_type, search_form_v3, raw_feed_item, parsed_feed_item)        
        elif value_scrap_type_type == 'direct':
            process_direct_value_customizing(field_name, field_model, value_scrap_type, search_form_v3, raw_feed_item, parsed_feed_item)
        else:
            # не известный value_scrap_type тип 
            # пишем лог, ничего не делаем
            logger.warning(f'feed_customizing(): не известный value_scrap_type тип: {value_scrap_type_type}, имя поля модели: {field_name}')
    
    
def _get_to_feeded_fields(dict_model_fields: Dict) -> List[str]:
    """получает model поля dict и возвращает список имён полей,
    модели которых помечены "feed": True
    """
    to_feeded_fields = [
                        field 
                        for field, value
                        in dict_model_fields.items()
                        if value['feed']
                        ]
    return to_feeded_fields

def _get_field_to_feeded_name(field_model: Dict, field_name: str) -> str:
    """получает модель поля и его имя - возвращает human_readable_name 
    поля если 'feed_human_readable_name': True
    """

    # return field_name
    return field_model['human_readable_name'] if field_model['feed_human_readable_name'] else  field_name

def get_value_from_dict_based_on_path_except_if_absent(target_dict:Dict, path: List[str]) -> Any:
    """получает dict и путь до требуемого значения - возвращает значение из
    по указанному пути если указанный путь не существует выбрасвыет исключение,
    которое должно обрабатываться в вызывающей функции
    """
    target: Dict = target_dict
    # кидает исключение, обрабатывать вызывающей функцией
    for item in path:
        target = target[item]
    return target

# TODO: доработать
def get_value_from_dict_based_on_path_create_if_absent(target_dict:Dict, path: List[str], value_if_absent: Any, raise_if_exist: bool = True) -> Any:
    """получает dict и путь до требуемого значения - возвращает значение
    по указанному пути, если указанный путь не существует создаёт его
    при необходимости переопределяет значение на dict если на пути попадается 
    другой тип. Если raise_if_exist=True то всесто переопределения
    выбрасвыет исключение, которое должно обрабатываться в вызывающей функции
    """
    
    # это всё не работает
    target: Dict = target_dict
    # кидает исключение, обрабатывать вызывающей функцией
    for item in path:
        target = target[item]
    return target


DEFAULT_VALUES_FOR_TYPES = {
    'str': lambda : '',
    'int': lambda : None,
    'float': lambda : None,
    'bool': lambda : None,
    'list': lambda : [],
    'dict': lambda : {},
    'NoneType': lambda : None
}

def get_model_type(field_model:Dict, field_name: str, parent_fields_names: List[str]):
    # определяем таргет тип
    logger.debug(f"enter -> {get_model_type.__name__}(): field_name: {field_name}, parent_fields_names: {', '.join(parent_fields_names)}")
    model_types = field_model['field_types']['types']
    if (len(model_types) > 2) or (len(model_types) == 0):
        logger.debug(f"{get_model_type.__name__}():if (len(model_types) > 2) or (len(model_types) == 0): len(model_types): {len(model_types)}")
        # ошибка формата model_types, типов может быть максимум два NoneType
        # и любой другой
        logger.error(f'{get_model_type.__name__}():  ошибка формата ["field_types"]["types"], типов болше 2-х или 0, имя поля: {field_name}, парентс: [{", ".join(parent_fields_names)}]') 
        return "NoneType"
    if (len(model_types) == 2) and (not ("NoneType" in model_types)):
        logger.debug(f"{get_model_type.__name__}():if (len(model_types) == 2) and (not ('NoneType' in model_types)): len(model_types): {len(model_types)}")
        # ошибка формата model_types, типов может быть максимум два NoneType
        # и любой другой 
        logger.error(f'{get_model_type.__name__}(): ошибка формата ["field_types"]["types"], если типа 2 то второй должен быть NoneType, имя поля: {field_name}, парентс: [{", ".join(parent_fields_names)}]') 
        # logger.error(f'get_model_type(): ошибка формата model_types, если типа 2 то второй должен быть NoneType, имя поля: {field_model["human_readable_name"]}') 
        return "NoneType"
    if (len(model_types) == 2):
        logger.debug(f"{get_model_type.__name__}():if (len(model_types) == 2):: len(model_types): {len(model_types)}")
        model_type = "NoneType"
        for item_type in model_types:
            if item_type != "NoneType":
                logger.debug(f"{get_model_type.__name__}():if item_type != 'NoneType': item_type: {item_type}")
                model_type = item_type
        if model_type == "NoneType": 
            logger.debug(f"{get_model_type.__name__}():if model_type == 'NoneType': item_type: {item_type}")
            logger.error(f'{get_model_type.__name__}(): ошибка формата ["field_types"]["types"], модель имеет только NoneType, имя поля: {field_name}, парентс: [{", ".join(parent_fields_names)}]') 
        return model_type
    logger.debug(f"{get_model_type.__name__}():model_types[0]: {model_types[0]}")
    return model_types[0]
    
def get_model_type_none_if_error(field_model:Dict, field_name: str, parent_fields_names: List[str]):
    # определяем таргет тип
    model_types = field_model['field_types']['types']
    if (len(model_types) > 2) or (len(model_types) == 0):
        # ошибка формата model_types, типов может быть максимум два NoneType
        # и любой другой
        logger.error(f'get_model_type_none_if_error():  ошибка формата ["field_types"]["types"], типов болше 2-х или 0, имя поля: {field_name}, парентс: [{", ".join(parent_fields_names)}]') 
        return None
    if (len(model_types) == 2) and (not ("NoneType" in model_types)):
        # ошибка формата model_types, типов может быть максимум два NoneType
        # и любой другой 
        logger.error(f'get_model_type_none_if_error(): ошибка формата ["field_types"]["types"], если типа 2 то второй должен быть NoneType, имя поля: {field_name}, парентс: [{", ".join(parent_fields_names)}]') 
        return None
    if (len(model_types) == 2):
        model_type = "NoneType"
        for item_type in model_types:
            if item_type != "NoneType":
                model_type = item_type
        if model_type == "NoneType": 
            logger.error(f'get_model_type_none_if_error(): ошибка формата ["field_types"]["types"], модель имеет только NoneType, имя поля: {field_name}, парентс: [{", ".join(parent_fields_names)}]') 
            return None
        return model_type
    else:
        return model_types[0]

def get_list_model_list_item_type(field_model: Dict, field_name: str, parent_fields_names):
    """возвращает тип элемента списка,
    для этого тип модели должне быть 'list'
    """
    # проверяем, что модель типа 'list'
    if not (model_type:=get_model_type(field_model, field_name, parent_fields_names)) == 'list':
        logger.error(f'get_list_model_list_item_type: модель имеет тип: {model_type}, должен быть "list", имя поля: {field_name}, паретс: [{", ".join(parent_fields_names)}]') 
        return 'NoneType'
    # получаем тип элемента списка
    if (item_type:=field_model['field_types'].get('type_for_list', None)) == None:
        # ошибка, type_for_list не определён
        logger.error(f'get_list_model_list_item_type: type_for_list не определён, имя поля:  имя поля: {field_name}, паретс: [{", ".join(parent_fields_names)}]') 
        return 'NoneType'
    return item_type

def get_model_default_value_for_model_type(field_model:Dict, field_name: str, parent_fields_names: List[str]):
    model_type =  get_model_type(field_model, field_name, parent_fields_names)
    default_value = DEFAULT_VALUES_FOR_TYPES[model_type]()
        
    return default_value

def get_model_default_value_for_list_item(field_model:Dict, field_name: str, parent_fields_names: List[str]):
    item_type = get_list_model_list_item_type(field_model, field_name, parent_fields_names)
    default_value = DEFAULT_VALUES_FOR_TYPES[item_type]()
        
    return default_value        

def get_model_default_value(field_model:Dict, field_name: str, parent_fields_names: List[str], belonging: Literal['field', 'list']):
    if belonging == 'field':
        return get_model_default_value_for_model_type(field_model, field_name, parent_fields_names)
    elif belonging == 'list':
        return get_model_default_value_for_list_item(field_model, field_name, parent_fields_names)
    else:
        # ошибка dict_belonging
        logger.error(f'get_model_default_value() ошибка, неизвестное значение dict_belonging: {belonging}, может быть: "field" | "list"')
        return None
        
        
# def parsing_raw_data_relative_to_data_model_v2(search_form_v3: Dict, raw_data: Dict)-> Dict: 
#     """принимпет search_form.v3 и прогоняет по ней
#      lot_card,  возвращает dict являющийсчся отрожением lot_card относительно
#      feed_items_model_v_2
#     """ 
#     feed_model = search_form_v3['feed']['types']['dict']
#     references = search_form_v3['references']

#     def _check_compliance_model_field_type(field_value, field_model: Dict, parent_fields_names: List[str]):
#         """проверки что тип field_value есть field_types модели"""

#         field_value_type = type(field_value).__name__
#         logger.debug(f'in _check_compliance_model_field_type(): {parent_fields_names}')
#         return field_value_type in field_model['field_types']['types']
        
#     def _make_dict_type_cast(field_value: Dict, field_model: Dict, field_name: str, parent_fields_names: List[str]):
#         # проверяем соответств типа field_value типу определённому 
#         # в field_model field_type поле
#         if _check_compliance_model_field_type(field_value, field_model, parent_fields_names):
#             #  field_value тип соответствует field_type модели 
#             #  ничего не делаем, присваем field_value res_value
#             res_value = field_value
#         # в противном случе проверяем существование и значениея 
#         # casting_key в field_model
#         elif key_name:=field_model.get('casting_key', None):
#             # casting_key существует, 
#             # определяем значение casting_key в field_value 
#             if (key_value:= field_value.get(key_name, None)) != None:
#                 # field_value имеет значение casting_key, 
#                 # проверяем соответствие его field_type модели
#                 if _check_compliance_model_field_type(key_value, field_model, parent_fields_names):
#                     # тип key_value соответствует типу определённому в модели
#                     # присваеваем его значение res_value 
#                     res_value = key_value
#                 else:
#                     # тип key_value не соотвествует типу определённоу в модели 
#                     # пишем log
#                     #   присваеваем res_value значение по умолчанию
#                     logger.warning(f'_make_dict_type_cast(): ошибка приведение тип поля {".".join(parent_fields_names)}, после приведения неверное значение типа')
#                     res_value = _get_model_default_value(field_model)
#             else:
#                 # field_value не имеет значение casting_key, 
#                 # пишем log
#                 #   присваеваем res_value значение по умолчанию
#                 logger.warning(f'_make_dict_type_cast(): ошибка приведение тип поля {".".join(parent_fields_names)}, key_value модеди отсутствует приводимом dict данных')
#                 res_value = _get_model_default_value(field_model)
#         else:
#             # атребут casting_key отсутствует в модели или 
#             # его значение равно пустому значению,
#             # могут быть два варианта:
#             # 1. dict является элементом списка поля и отсутствие casting_key
#             # означает, что не нужно делать ни каких привдений
#             if "list" in field_model['field_types']['types']:
#                 res_value = field_value
#             else:
#                 # 2. ошибка, нужно делать приведение dict, но casting_key отсутствует   
#                 # пишем log присваеваем res_value значение по умолчанию
#                 logger.warning(f'_make_dict_type_cast(): ошибка приведение типа поля {".".join(parent_fields_names)}, атребут casting_key отсутствует в модели или его значение равно пустому значению')
#                 res_value = _get_model_default_value(field_model)
#         return res_value
    
#     def _make_list_type_cast(field_value: List, field_model: Dict, field_name: str, parent_fields_names: List[str]):
#         """приведение списка к типу определённому в модели поля field_types,
#         итоговый тип может быть только str, соответственно исходные типы
#         элементов списка могут быть только простыми типами либо полученными
#         напрямую при parse_list_model() либо приведение типа dict 
#         содержащихся в списке, опять же при parse_list_model()  
#         """
        
#         # проверяем что полученное значение типа list
#         if not isinstance(field_value, list):
#             # полученное значение не типа list
#             # пишем лог, возвращаем дефолт для модели
#             logger.error(f'_make_list_type_cast():ошибка - поле: [{", ".join(parent_fields_names)}] не является типом "list"')
#             return _get_model_default_value(field_model) 
            
#         # проверяем что field_types содержит тип list
#         # тогда ничего приводить не нужно, осравляем list
#         if 'list' in field_model['field_types']['types']:
#             # list является типом поля модели, 
#             # возвращаем исходное значение
#             return field_value
        
#         # list не является типом поля модели, 
#         # выполняем приведение.
#         # приведённым значением типа list может быть только 
#         # строка объяденяющая все единичные простые занчения листа
#         # проверим есть ли str в списке field_types
#         if not ('str' in field_model['field_types']['types']):
#             # str не является типом поля модели - ошибка
#             # пишем лог, возвращыем дефолтное значение для поля
#             logger.error(f'_make_list_type_cast(): ошибока - "str" не является типом поля модели, поле: [{", ".join(parent_fields_names)}]')
#             # logger.error(f'ошибка приведение типа "list" поля [{", ".join(parent_fields_names)}], str не является типом поля модели')
#             return _get_model_default_value(field_model) 
            
#         # str есть в field_types модели
#         # объединяем значения списка в троку
#         str_val = ""
#         for item in field_value:
#             # проверяем что item имеет простой тип
#             if isinstance(item, list) or isinstance(item, dict):
#                 # item не простого типа - ошибка
#                 # пишем лог, пропускаем значение
#                 logger.error(f'_make_list_type_cast(): элемента списка имеет тип {type(item).__name__}, поле: [{", ".join(parent_fields_names)}]')
#                 continue
#             str_val += item
#         # приведение закончено, возвращаем заныение
#         return str_val
    
#     def field_values_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
#         """конверктация типа field_value в тип указанный в field_type модели"""

#         # проверяем соответствие типа field_value типу определённому 
#         # в field_model field_type поле
#         # определяем тип field_value
#         field_value_type = type(field_value).__name__
#         if _check_compliance_model_field_type(field_value, field_model, parent_field_names):
#             #  field_value тип соответствует field_type модели 
#             #  ничего не делаем, присваем field_value res_value
#             res_value = field_value
#         else:
#             #  field_value тип не соответствует field_type модели 
#             # делаем приведение типа в зависимости от типа field_value
#             if field_value_type == 'dict':
#                 # производим приведение типа field_value типу модели 
#                 res_value = _make_dict_type_cast(field_value, field_model, field_name, parent_field_names)
#             elif field_value_type == 'list':
#                 # производим приведение типа field_value типу модели 
#                 res_value = _make_list_type_cast(field_value, field_model, field_name, parent_field_names)
#             else:
#                 # если тип поля простой или list и он не соответствует 
#                 # field_type модели то пишем log b присваеваем res_value 
#                 # значение по умолчанию модели
#                 logger.warning(f'тип {field_value_type} поля {".".join(parent_field_names)} не соответствует field_types {", ".join(field_model["field_types"]["types"])} модели')
#                 res_value = _get_model_default_value(field_model)
#         return res_value

#     def parse_list_model(parent_field_model: Dict, field_name: str, list_model: Dict, data: List, parent_field_names: List[str]) -> List:
#         res_list = []
#         for item in data:
#             # определяем тип элемента списка
#             item_type = type(item).__name__
#             logger.debug(f'in parse_list_model(): item type {item_type}')
#             # проверяем зарегистриван ли тип в типах лист модели
#             if (model:=list_model['types'].get(item_type, None)):
#                 # тип элемента списка зарегистрирован 
#                 # в типах модели списка
#                 # действуем в зависимости от типа элемента
#                 if model['type'] == 'dict':
#                     # тип элемента dict 
#                     # вызываем parse_dict_model(), 
#                     dict_value = parse_dict_model(model, item, parent_field_names)
#                     # исключаем словари с пустыми exclusion key 
#                     if dict_value:=exclusion_of_empty_values(dict_value, parent_field_model, field_name, parent_field_names):
#                         # проводим приведение типа если необходимо
#                         dict_value = _dict_value_conversion(dict_value, parent_field_model, field_name, parent_field_names)
#                         # результат аппендим в res_list
#                         res_list.append(dict_value) 
#                 elif model['type'] == 'list':
#                     # тип элемента list 
#                     # вызываем parse_list_model(), 
#                     # результат аппендим в res_list
#                     res_list.append(parse_list_model(parent_field_model, field_name, model, item, parent_field_names)) 
#                 else:
#                     # простой тип
#                     # аппендим в res_list как есть
#                     value = _simple_type_value_conversion(item, parent_field_model, field_name, parent_field_names)
#                     res_list.append(value) 
#             else:
#                 # тип элемента списка не зарегистрирован 
#                 # в типах модели списка
#                 # пишеь log, аппендим 'type not definet in model'
#                 logger.warning(f'тип {item_type} элемента list поля [{".".join(parent_field_names)}] не зарегистрирован в типах модели list')
#                 # logger.warning(f'имя поля: {field_name}, элемент: {item}')
#                 res_list.append(_get_model_default_value(parent_field_model))
#         # res =  field_values_type_conversion(res_list, parent_field_model, field_name, parent_field_names)
#         # возвращаем результирующий список
#         return res_list
    
    
#     def field_values_shape_reduction(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
#         """изменение формы field_value в зависимости от значения
#         поля модели value_scrap_type
#         {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
#         direct - значение берётся то которое вычисляется по умолчению None
#         dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
#         ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
#         """
#         return field_value
    
#     def exclusion_of_empty_values(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
#         """проверка field_value на значение поля exclusion_key модели,
#         поле может иметь значение только если проверяемое field_value 
#         словарь (dict) и только в том случае если данный словарь 
#         являествя элементом некого списка (list[dict]), в данном контексте 
#         проверяемы exclusion_key это имя ключа словаря, ключевого атребута
#         в котором содержится значение определяющее саму сущьность словаря,
#         без которого сам dict теряет смысл. Например в списке покупок может быть
#         запись
#         {'наименование товара': 'картофель', 'кол-во': ''}
#         в данном примере ''кол-во' некий атребут без которого веся сущьность
#         покупи 'картофель' теряет смысл - поэтому её нужно исключить из
#         списка вообще.
#         Функция проверяет наличие exclusion_key - если его нет или его значение 
#         в field_value не пустое то возвращиет field_value, 
#         в противнос случае проверяет значение
#         exclusion_key в field_value и если там содержится пустое значение ("" или "-")
#         то возвращает None, который должен проверяться в parse_list_model()
#         при добавлении значения в список
#         """
#         # проверяем что field_value есть dict
#         if type(field_value).__name__ == 'dict':
#             # field_value есть dict
#             # проверяем что поле exclusion_key есть в модели
#             if exc_key:=field_model.get('exclusion_key', None):
#                 # поле exclusion_key есть в модели
#                 # проверяем что проверяемый dict содержит ключ с именеи 
#                 # значения exclusion_key
#                 if (exc_key_val:=field_value.get(exc_key, None)) != None:
#                     # field_value содержит ключ с именем значения exclusion_key
#                     # проверяем значение exclusion_key в field_value
#                     if not (exc_key_val == "" or exc_key_val == "-"):
#                         logger.debug(f'exclusion_of_empty_values() exc_key_val: {exc_key_val}')
                        
#                         #  exclusion_key в field_value содержит не пустое
#                         # значение, возвращаем field_value
#                         return field_value
#                     else:
#                         logger.debug(f'exclusion_of_empty_values() exc_key_val: {exc_key_val}')
#                          #  exclusion_key в field_value содержит пустое
#                         # значение, возвращаем None
#                         return None
#                 else:
#                     # field_value не содержит ключ с именем 
#                     # значения exclusion_key. Пишем предупреждение в log
#                     # возвращаем field_value
#                     logger.warning(f'ошибка exclusion_of_empty_values(): field_value с именем: [{", ".join(parent_field_names)}] не содержил ключа exclusion_key: {exc_key} модели')
#                     return field_value
#             else:
#                 # поле exclusion_key отутствует в модели, значит проверка
#                 # не нужно, возвращаем field_value
#                 return field_value
#         else:
#             # field_value не dict
#             # возвращаем field_value
#             return field_value
            
                
#     def boolen_type_value_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
#         """
#         преобразование bool занчение в str эквивалент для возможности 
#         обращения к справочнику и замены true на "Да", false на "Нет
#         """

#         field_value_type = type(field_value).__name__
#         logger.debug(f'in boolen_type_value_conversion(): field_value_type: {field_value_type}')
#         if field_value_type == 'bool':
#             res_value = 'true' if field_value else 'false'
#         else:
#             res_value = field_value
#         return res_value                
    
#     def dict_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
#         """ конвертация  field_value по значению 'dict' поля value_scrap_type модели """

#         # проверим, что тип field_value - str
#         if not isinstance(field_value, str):
#             # field_value не str
#             # пишем log, возвращаем field_value без конвертации
#             logger.error(f'ошибка dict_scrap_type_conversion: тип field_value не str, field_value path: {".".join(parent_field_names)}') 
#             return field_value
#         t_path: List = field_model['value_scrap_type']['dict_path'].copy()
#         t_path.extend(['available_values', 'values', field_value, 'name'])
#         try:            
#             res_value = get_value_from_dict_based_on_path_except_if_absent(search_form_v3, t_path)
#         except Exception as e:
#             # ошибка получения заначения из словаря по t_path
#             #  пишем log, возвращаем field_value без конвертации
#             logger.error(f'ошибка: {e}, dict_scrap_type_conversion: ошибка получения заначения из словаря по t_path: [{".".join(t_path)}] , field_value path: {".".join(parent_field_names)}') 
#             return field_value
#         return res_value
        
#     # def layout_formatting_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> str:
#     #     # получаем layout
#     #     if not _get_layout()
    
    
#     def _check_dict_scrap_type(dict_scrap_type: Dict):
#         """проверка на корректность типа dict_scrap_type"""
#         # это должно быть словарь типа {'type': 'dict', 'dict_path': []}
#         if ['type', 'dict_path'] != list(dict_scrap_type.keys()):
#             return False
#         if dict_scrap_type['type'] != 'dict':
#             return False
#         if not isinstance(dict_scrap_type['dict_path'], list):
#             return False
#         for item in dict_scrap_type['dict_path']:
#             if not isinstance(item, str):
#                 return False
#         return True
        
        
#     def value_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
#         """конвертация  field_value по значению поля value_scrap_type модели.
#         возможные значения value_scrap_type
#         {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
#         direct - нет преобразования. Данное тип не указываем в модели
#         dict - field_value подставляется в словарь по ссылке dict_path, 
#         полученное заначение записывается в поле
#         ref - из field_value делается ссылка путём подставления 
#         его в заданное место в ref и уже оно записывается в поле"""
        
#         # сначала проверяем наличие и значение поля value_scrap_type в моделе
#         # данное поле может отсутствовать в моделе или быть пустое - 
#         # direct вариант 
#         if value_scrap_type_value:=field_model.get('value_scrap_type', None):
#             # value_scrap_type ключ есть в модели
#             # действуем в зависимости от типа
#             if scrap_type:=value_scrap_type_value.get('type', None):
#                 # есть ключь "type" и он не пустой
#                 if scrap_type == 'dict':
#                     # проверяем правильность форрмата dict scrap_type
#                     if _check_dict_scrap_type(value_scrap_type_value):
#                         # value_scrap_type_value правильного формата
#                         res_value = dict_scrap_type_conversion(field_value, field_model, field_name, parent_field_names)
#                     else:
#                         # value_scrap_type_value не правильного формата
#                         # пишем log, возвращаем field_value без конвертации
#                         logger.error(f'ошибка value_scrap_type_conversion(): тип dict value_scrap_type_value не правильного формата, field_value path: {".".join(parent_field_names)}') 
#                         res_value = field_value
                        
#                 elif scrap_type == 'layout_formatting':
#                     # получаем layout
#                     if layout:=_get_layout(field_name, value_scrap_type_value, search_form_v3):
#                         # layout получен
#                         # оборачиваем field_value
#                         format_items_dict = safesub()
#                         # в полученном layout должно быть место {item}
#                         format_items_dict['item'] = field_value
#                         res_value = layout.format_map(format_items_dict)
#                     else:
#                         # ошибка получения layout
#                         # пишем лог, отставляем  field_value без conversion
#                         logger.error(f'value_scrap_type_conversion(): ошибка получения layout, field_value path: {".".join(parent_field_names)}') 
#                         res_value = field_value

#                     # res_value = layout_formatting_scrap_type_conversion(field_value, field_model, field_name, parent_field_names)
#                 else:
#                     # не поддерживаемый тип, пишем лог и возвращаем
#                     #  field_value без конвертации
#                     logger.error(f'value_scrap_type_conversion(): не поддерживаемый scrap_type тип: {scrap_type} , field_value path: {".".join(parent_field_names)}') 
#                     res_value = field_value
#             else:
#                 # ключь "type" отсутствует или он пустой - ошибка
#                 logger.error(f'value_scrap_type_conversion(): ключь "type" отсутствует или он пустой , field_value path: {".".join(parent_field_names)}') 
#                 res_value = field_value
#         else:
#             # value_scrap_type ключ отсутствует в моделе
#             # конвертация не требуется
#             res_value = field_value
#         return res_value    
        
    
#     def _simple_type_value_conversion(res_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
#         # преобразуем bool значение в строку, нужно для обращения к справочнику
#         res = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)

#         # корректируем полученное значени по полю модели value_scrap_type
#         # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
#         # direct - значение берётся то которое вычисляется по умолчению None
#         # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
#         # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
            
#         res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
#         # проверяем на путое значение для списка словарей
#         # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

#         return res

        
        
        
        
#     def _dict_value_conversion(res_value: Dict, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
#         """конвертация dict занчениея относлительно  модели поля"""
#         # корректируем полученное значение по 
#         # значениям "field_type", "casting_key" модели поля
#         # 
#         res = _make_dict_type_cast(res_value, field_model, field_name, parent_field_names)
        
#         # res_value = field_values_type_conversion(res_value, field_model, field_name, parent_field_names)
#         # res_value = field_values_shape_reduction(res_value, field_model, field_name, parent_field_names)

#         # преобразуем bool значение в строку, нужно для обращения к справочнику
#         res = boolen_type_value_conversion(res, field_model, field_name, parent_field_names)

#         # корректируем полученное значени по полю модели value_scrap_type
#         # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
#         # direct - значение берётся то которое вычисляется по умолчению None
#         # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
#         # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
            
#         res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
#         # проверяем на путое значение для списка словарей
#         # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

#         return res


            
        
#     def get_field_value(field_model: Dict, 
#                          field_name: str, 
#                          data: Dict,
#                          parent_field_names: List[str]): 
#         parent_field_names.append(field_name)
#         # проверяем есть ли поле в данных
#         if (field_value:=data.get(field_name, None)) != None:
#             # поле есть в данных
#             # проверяем что тип поля присутсвует 
#             # в зарегистрированных типах модели
#             field_type = type(field_value).__name__
#             if field_model_type:=field_model['types'].get(field_type, None):
#                 # тип данных зарегистрирован в типах модели
#                 # действуем в зависимости от типа поля
#                 if field_type == 'dict':
#                     # если поле типа dict вызываем parse_dict_model()
#                     res_value = parse_dict_model(field_model_type, field_value, parent_field_names)
                    
#                     res_value = _dict_value_conversion(res_value, field_model, field_name, parent_field_names)
                    
#                 elif field_type == 'list':
#                     # если поле типа list вызываем parse_list_model()
#                     res_value = parse_list_model(field_model, field_name, field_model_type, field_value, parent_field_names)
#                     res_value = _make_list_type_cast(res_value, field_model, field_name, parent_field_names)
#                 else:
#                     # если поле обычного типа - берём его значение
#                     # делаем конвертацию
#                     res_value = _simple_type_value_conversion(field_value,field_model,field_name,parent_field_names)                    
#             else:
#                 # тип данных не зарегистрирован в типах модели
#                 # пишеь log, присваиваем результату значение по умолчанию для типа
#                 logger.warning(f'get_field_value(): тип {field_type} поля {".".join(parent_field_names)} не зарегистрирован в типах модели')
#                 res_value = _get_model_default_value(field_model)
#         else:
#             # поля нет в данных
#             # присваиваем результату значение по умолчанию для типа
#             logger.debug(f'get_field_value(): field name: {".".join(parent_field_names)} нет в данных')
#             res_value = _get_model_default_value(field_model)
        
#         return res_value


    
#     def parse_dict_model(dict_model: Dict, data: Dict, parent_field_names: List[str] = []) -> Dict:
        
#         dict_model_fields = dict_model['fields']
#         dif_field_names = set(data.keys()) - set(dict_model_fields.keys())
#         if dif_field_names:
#             # for key in dict_model_fields.keys():
#             #     logger.warning(f'model_key: {key}')
#             # logger.error(f"model['type'] == 'dict': model_field: [{','.join(dict_model['fields'].keys())}]")
#             # logger.error(f"data['type'] == 'dict': data_field: [{','.join(data.keys())}]")

#             for field_name in dif_field_names:
#                 logger.warning(f'parse_dict_model(): field_name: {field_name} not in model, parent_field_names: {parent_field_names}')
#         to_feeded_fields_name: List[str] = _get_to_feeded_fields(dict_model_fields)
#         # мы отправляем в получение значения все поля не проверяя
#         # есть ли они в полученных данных
#         res_dict = {
#                 _get_field_to_feeded_name(dict_model_fields[field_name], field_name): 
#                 get_field_value(dict_model_fields[field_name], field_name, data, parent_field_names.copy())
#                 for field_name in to_feeded_fields_name 
#                 }
        
#         return res_dict

#     return parse_dict_model(feed_model, raw_data)

# def customization_feed(search_form_v3: Dict, parsed_feed_item: Dict):
        
def parsing_raw_data_relative_to_data_model_v2_var2(search_form_v3: Dict, raw_data: Dict)-> Dict: 
    """принимпет search_form.v3 и прогоняет по ней
     lot_card,  возвращает dict являющийсчся отрожением lot_card относительно
     feed_items_model_v_2
     в отличии от вар 1 будет исходить из того что "field_types" имеет только 
     одно возможное значени и  None, т.е. все простые типы нужно кастить
    """ 
    feed_model = search_form_v3['feed']['types']['dict']
    references = search_form_v3['references']

    def _check_compliance_model_type_value_type(field_value, field_model: Dict, field_name: str, parent_fields_names: List[str]) -> bool:
        """проверки что тип field_value есть в field_types модели
        (в отличии от проверки соответствия типа значения элемента списка в 
        _check_compliance_model_type_value_type_for_list_item_value())
        
        в данной модели у field_model могут быть только два допустимых 
        типа: NoneType и любой другой, т.е. допустимы: одно значение напр [str]
        или два значения где второе значение NoneType: [int, NoneType].
        Т.е. поле может иметь только один тип NoneType.
        Здесь не выполняется проверка соответствия для значений являющихся
        элементами списка, только значения являющиеся занчением поля
        
         """
        # определяем тип поля
        field_value_type = type(field_value).__name__
        # получаем тип подели
        field_model_type = get_model_type(field_model, field_name, parent_fields_names)
        # field_model['field_types']['types']
        return field_value_type  == field_model_type
            
    def _check_compliance_model_type_value_type_for_list_item_value(list_item_value, field_model: Dict, field_name: str, parent_fields_names: List[str]) -> bool:
        """проверки что тип list_item_value есть type_for_list модели
        (в отличии от проверки значения типа поля значению типа модели в
        _check_compliance_model_type_value_type()) 
        в данной модели у value могут быть только два допустимых 
        типа: NoneType и любой другой, т.е. допустимы: одно значение напр [str]
        или два значения где второе значение NoneType: [int, NoneType].
        Т.е. поле может иметь только один тип NoneType.
         """
        # определяем тип поля
        list_item_type = type(list_item_value).__name__
        # получаем тип подели
        list_item_model_type: str = get_list_model_list_item_type(field_model, field_name, parent_fields_names)
        
        return list_item_type == list_item_model_type

    def check_compliance_model_type(value: Any, field_model: Dict, field_name: str, parent_fields_names: List[str], belonging: Literal['field', 'list']) -> Union[bool, None]:
        if belonging == 'field':
            if _check_compliance_model_type_value_type(value, field_model, field_name, parent_fields_names):
            #  field_value тип соответствует field_type модели 
            #  ничего не делаем, присваем field_value res_value
                return True
            else:
                return False
        elif belonging == 'list':
            if _check_compliance_model_type_value_type_for_list_item_value(value, field_model, field_name, parent_fields_names):
            #  field_value тип соответствует field_type модели 
            #  ничего не делаем, присваем field_value res_value
                return True
            else:
                return False
        else:
            # ошибка dict_belonging
            logger.error(f'_check_compliance_model_type() ошибка, неизвестное значение dict_belonging: {belonging}, может быть: "field" | "list"')
            return None     

    def simple_value_conversion_for_simple_type_model_field(data_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
        # осуществляем приведение к типу модели
        res_value = make_simple_type_cast(data_value, field_model, field_name, parent_field_names, 'field')
        # осуществляем boolen_type_value_conversion
        res_value = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)
        # осуществляем value_scrap_type конвертацию
        # позвращаем полученное значение
        return value_scrap_type_conversion(res_value, field_model, field_name, parent_field_names)

    def make_simple_type_cast(item_value: Any, field_model: Dict, field_name: str, parent_fields_names: List[str], simple_type_belonging: Literal['field', 'list']):
        """приведение простых типов для всех значений: 
        int->float
        int->str
        float->str
        bool->str
        """
        cast_map = {
            'str': {
                'types': ['int', 'float', 'bool'],
                'default': ''
                },
            'float': {
                'types': ['int'],
                'default': None
            },
            'int': {
                'types': ['float'],
                'default': None
            },
            'bool': {
                'types': ['str', 'int', 'float'],
                'default': None
            }
                
        }
        
        # определяем таргет тип
        if simple_type_belonging == 'field':
            model_type = get_model_type(field_model, field_name, parent_fields_names)
        elif simple_type_belonging == 'list':
            model_type = get_list_model_list_item_type(field_model, field_name, parent_fields_names)
        else:
            # ошьбка simple_type_belonging
            logger.error(f'make_simple_type_cast() ошибка, неизвестное значение simple_type_belonging: {simple_type_belonging}, может быть: "field" | "list"')
            return None
        
        item_value_type = type(item_value).__name__ 
        
        # не соответсвие field_value_type и  model_type должно провериться
        # на преидущем этапе, здесь они должны не соответствовать друг другу
        # но на всякий случаем делаем проверку ещё раз
        if item_value_type == model_type:
            return item_value
        # приведение
        if model_type == 'str':
            if not (item_value_type in cast_map['str']['types']):
                # ошибка приведение типа, field_value_type нельзя привести к типу 'str'
                logger.error(f'make_simple_type_cast(): ошибка приведение типа, field_value_type ({item_value_type}) нельзя привести к типу "str", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
                return DEFAULT_VALUES_FOR_TYPES[model_type]()
            return str(item_value)
        if model_type == 'int':
            if not (item_value_type in cast_map['int']['types']):
                # ошибка приведение типа, field_value_type нельзя привести к типу 'int'
                logger.error(f'make_simple_type_cast(): ошибка приведение типа, field_value_type ({item_value_type}) нельзя привести к типу "int", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
                return DEFAULT_VALUES_FOR_TYPES[model_type]()
            # приведение к int возможно только из float, поэтому пишем предупреждение
            logger.warning(f'make_simple_type_cast(): field_value_type ({item_value_type}) приводится к типу "int", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
            return int(item_value)
        if model_type == 'float':
            if not (item_value_type in cast_map['float']['types']):
                # ошибка приведение типа, field_value_type нельзя привести к типу 'int'
                logger.error(f'make_simple_type_cast(): ошибка приведение типа, field_value_type ({item_value_type}) нельзя привести к типу "float", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
                return DEFAULT_VALUES_FOR_TYPES[model_type]()
            return float(item_value)
        if model_type == 'bool':
            if not (item_value_type in cast_map['bool']['types']):
                # ошибка приведение типа, field_value_type нельзя привести к типу 'int'
                logger.error(f'make_simple_type_cast(): ошибка приведение типа, field_value_type ({item_value_type}) нельзя привести к типу "bool", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
                return DEFAULT_VALUES_FOR_TYPES[model_type]()
            return bool(item_value)
        # ошибка приведения, не известное значение model_type 
        logger.error(f'make_simple_type_cast(): ошибка приведения, не известное значение model_type: ({model_type}), имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
        return None
        
    
    # def _make_field_simple_type_cast(field_value: Any, field_model: Dict, field_name: str, parent_fields_names: List[str]):
    #     """приведение простых типов для значений присваивающихся полям:
    #     int->float
    #     int->str
    #     float->str
    #     bool->str
    #     """
    #     cast_map = {
    #         'str': {
    #             'types': ['int', 'float', 'bool'],
    #             'default': ''
    #             },
    #         'float': {
    #             'types': ['int'],
    #             'default': None
    #         },
    #         'int': {
    #             'types': ['float'],
    #             'default': None
    #         },
    #         'bool': {
    #             'types': ['str', 'int', 'float'],
    #             'default': None
    #         }
                
    #     }
        
    #     # определяем таргет тип
    #     model_type = get_model_type(field_model)
        
    #     field_value_type = type(field_value).__name__ 
        
    #     # не соответсвие field_value_type и  model_type должно провериться
    #     # на преидущем этапе, здесь они должны не соответствовать друг другу
    #     # но на всякий случаем делаем проверку ещё раз
    #     if field_value_type == model_type:
    #         # если есть соответствие то пишем log и возвращаем field_value
    #         # без приведения
    #         logger.warning(f'_make_simple_type_cast(): типы field_value и field_model соответствуют друг друго, здесь это ошибка , имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #         return field_value
    #     # приведение
    #     if model_type == 'str':
    #         if not (field_value_type in cast_map['str']['types']):
    #             # ошибка приведение типа, field_value_type нельзя привести к типу 'str'
    #             logger.error(f'_make_simple_type_cast(): ошибка приведение типа, field_value_type ({field_value_type}) нельзя привести к типу "str", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #             return DEFAULT_VALUES_FOR_TYPES[model_type]()
    #         return str(field_value)
    #     if model_type == 'int':
    #         if not (field_value_type in cast_map['int']['types']):
    #             # ошибка приведение типа, field_value_type нельзя привести к типу 'int'
    #             logger.error(f'_make_simple_type_cast(): ошибка приведение типа, field_value_type ({field_value_type}) нельзя привести к типу "int", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #             return DEFAULT_VALUES_FOR_TYPES[model_type]()
    #         # приведение к int возможно только из float, поэтому пишем предупреждение
    #         logger.warning(f'_make_simple_type_cast(): field_value_type ({field_value_type}) приводится к типу "int", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #         return int(field_value)
    #     if model_type == 'float':
    #         if not (field_value_type in cast_map['float']['types']):
    #             # ошибка приведение типа, field_value_type нельзя привести к типу 'int'
    #             logger.error(f'_make_simple_type_cast(): ошибка приведение типа, field_value_type ({field_value_type}) нельзя привести к типу "float", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #             return DEFAULT_VALUES_FOR_TYPES[model_type]()
    #         return float(field_value)
    #     if model_type == 'bool':
    #         if not (field_value_type in cast_map['bool']['types']):
    #             # ошибка приведение типа, field_value_type нельзя привести к типу 'int'
    #             logger.error(f'_make_simple_type_cast(): ошибка приведение типа, field_value_type ({field_value_type}) нельзя привести к типу "bool", имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #             return DEFAULT_VALUES_FOR_TYPES[model_type]()
    #         return bool(field_value)
    #     # ошибка приведения, не известное значение model_type 
    #     logger.error(f'_make_simple_type_cast(): ошибка приведения, не известное значение model_type: ({model_type}), имя поля: {field_name}, path: [{", ".join(parent_fields_names)}]')
    #     return None
    
        
        
    # def make_dict_type_cast(dict_item: Dict, field_model: Dict, field_name: str, parent_fields_names: List[str], dict_belonging: Literal['field', 'list']):
    #     """приведение к типу модели словаря являющегося элементом списка
    #     (в отличие от значения которое записывается в поле)
    #     """
    #     # проверяем соответств типа dict_list_item типу определённому 
    #     # в type_for_list модели
        
    #     if check:=check_compliance_model_type(dict_item, field_model, field_name, parent_fields_names, dict_belonging):
    #         return dict_item
    #     elif check == None:
    #         return None
             
        
    #     if key_name:=field_model.get('casting_key', None):
    #         # casting_key существует, 
    #         # определяем значение casting_key в field_value 
    #         if (key_value:= dict_item.get(key_name, None)) != None:
    #             # field_value имеет значение casting_key, 
    #             # проверяем соответствие его field_type модели
    #             if check_compliance_model_type(key_value, field_model, field_name, parent_fields_names, dict_belonging):
    #                 # тип key_value соответствует типу определённому в модели
    #                 # присваеваем его значение res_value 
    #                 return key_value
    #             else:
    #                 # тип key_value не соотвествует типу определённоу в модели 
    #                 # пишем log
    #                 #   присваеваем res_value значение по умолчанию
    #                 logger.error(f'make_dict_type_cast(): ошибка приведение тип поля, field_name: {field_name}, parent_fields_names: [{".".join(parent_fields_names)}], после приведения неверное значение типа, dict_belonging: {dict_belonging}')
    #                 return get_model_default_value(field_model, dict_belonging)
    #         else:
    #             # field_value не имеет значение casting_key, 
    #             # пишем log
    #             #   присваеваем res_value значение по умолчанию
    #             logger.error(f'make_dict_type_cast(): ошибка приведение тип поля, field_name: {field_name}, parent_fields_names: {".".join(parent_fields_names)}, key_value модеди отсутствует приводимом dict данных, dict_belonging: {dict_belonging}')
    #             return get_model_default_value(field_model, dict_belonging)
    #     else:
    #         # атребут casting_key отсутствует в модели или 
    #         # его значение равно пустому значению,
    #         # шибка, нужно делать приведение dict, но casting_key отсутствует   
    #         # пишем log присваеваем res_value значение по умолчанию
    #         logger.error(f'make_dict_type_cast(): ошибка приведение типа поля, field_name: {field_name}, parent_fields_names: {".".join(parent_fields_names)}, атребут casting_key отсутствует в модели или его значение равно пустому значению, dict_belonging: {dict_belonging}')
    #         return get_model_default_value(field_model, dict_belonging)
        
     
    def dict_value_conversion_for_simple_type_model_field(dict_value: Dict, field_model: Dict, field_name: str, parent_fields_names: List[str]):
        """конвиет метод для dict valu при присваивании его полю
        простого типа
        """
        res_value = make_dict_type_cast(dict_value, field_model, field_name, parent_fields_names, 'field')
        res_value = boolen_type_value_conversion(res_value, field_model, field_name, parent_fields_names)
        # осуществляем value_scrap_type конвертацию
        # позвращаем полученное значение
        return value_scrap_type_conversion(res_value, field_model, field_name, parent_fields_names)
                    
        
    def make_dict_type_cast(dict_value: Dict, field_model: Dict, field_name: str, parent_fields_names: List[str], belonging: Literal['field', 'list']):
        """приведение к типу модели словаря являющегос значением поля
        (в отличие от словаря являющегося элементом списка)
        """
        # проверяем существование и значениея 
        # casting_key в field_model
        if key_name:=field_model.get('casting_key', None):
            # casting_key существует, 
            # определяем значение casting_key в field_value 
            if (key_value:= dict_value.get(key_name, None)) != None:
                # field_value имеет значение casting_key, 
                # проверяем соответствие его field_type модели
                if check_compliance_model_type(key_value, field_model, field_name, parent_fields_names, belonging):
                    # тип key_value соответствует типу определённому в модели
                    # присваеваем его значение res_value 
                    res_value = key_value
                else:
                    # тип key_value не соотвествует типу определённоу в модели 
                    # пишем log
                    #   присваеваем res_value значение по умолчанию
                    logger.error(f'make_dict_type_cast(): ошибка приведение тип поля: {field_name}, парентс: {".".join(parent_fields_names)}, после приведения неверное значение типа: {type_str(key_value)}, belonging: {belonging}')
                    res_value = get_model_default_value(field_model, field_name, parent_fields_names, belonging)
            else:
                # field_value не имеет значение casting_key, 
                # пишем log
                #   присваеваем res_value значение по умолчанию
                logger.error(f'make_dict_type_cast(): ошибка приведение тип поля: {field_name}, парентс: {".".join(parent_fields_names)}, key_value модели отсутствует приводимом dict данных, belonging: {belonging}')
                res_value = get_model_default_value(field_model, field_name, parent_fields_names, belonging)
        else:
            # атребут casting_key отсутствует в модели или 
            # его значение равно пустому значению,
            # шибка, нужно делать приведение dict, но casting_key отсутствует   
            # пишем log присваеваем res_value значение по умолчанию
            logger.error(f'make_dict_type_cast(): ошибка приведение типа поля: {field_name}, парентс: {".".join(parent_fields_names)}, атребут casting_key отсутствует в модели или его значение равно пустому значению, belonging: {belonging}')
            res_value = get_model_default_value(field_model, field_name, parent_fields_names, belonging)
        return res_value
    
    # def make_list_type_cast(field_value: List, field_model: Dict, field_name: str, parent_fields_names: List[str]):
    #     """приведение списка к типу определённому в модели поля field_types,
    #     итоговый тип может быть только str, соответственно исходные типы
    #     элементов списка могут быть только простыми типами либо полученными
    #     напрямую при parse_list_model() либо приведение типа dict 
    #     содержащихся в списке, опять же при parse_list_model()  
    #     """
        
    #     # проверяем что полученное значение типа list
    #     if not isinstance(field_value, list):
    #         # полученное значение не типа list
    #         # пишем лог, возвращаем дефолт для модели
    #         logger.error(f'make_list_type_cast():ошибка - поле: [{", ".join(parent_fields_names)}] не является типом "list"')
    #         return get_model_default_value(field_model, 'field') 
            
    #     # проверяем что field_types содержит тип list
    #     # тогда ничего приводить не нужно, осравляем list
    #     if 'list' in field_model['field_types']['types']:
    #         # list является типом поля модели, 
    #         # возвращаем исходное значение
    #         return field_value
        
    #     # list не является типом поля модели, 
    #     # выполняем приведение.
    #     # приведённым значением типа list может быть только 
    #     # строка объяденяющая все единичные простые занчения листа
    #     # проверим есть ли str в списке field_types
    #     if not ('str' in field_model['field_types']['types']):
    #         # str не является типом поля модели - ошибка
    #         # пишем лог, возвращыем дефолтное значение для поля
    #         logger.error(f'make_list_type_cast(): ошибка - "str" не является типом поля модели, поле: [{", ".join(parent_fields_names)}]')
    #         # logger.error(f'ошибка приведение типа "list" поля [{", ".join(parent_fields_names)}], str не является типом поля модели')
    #         return get_model_default_value(field_model, 'field') 
            
    #     # str есть в field_types модели
    #     # объединяем значения списка в троку
    #     str_val = ""
    #     for item in field_value:
    #         # проверяем что item имеет простой тип
    #         if isinstance(item, list) or isinstance(item, dict):
    #             # item не простого типа - ошибка
    #             # пишем лог, пропускаем значение
    #             logger.error(f'make_list_type_cast(): элемента списка имеет тип {type(item).__name__}, поле: [{", ".join(parent_fields_names)}]')
    #             continue
    #         str_val += item
    #     # приведение закончено, возвращаем заныение
    #     return str_val
    
    # def field_values_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
    #     """конверктация типа field_value в тип указанный в field_type модели"""

    #     # проверяем соответствие типа field_value типу определённому 
    #     # в field_model field_type поле
    #     # определяем тип field_value
    #     field_value_type = type(field_value).__name__
    #     if _check_compliance_model_type_value_type(field_value, field_model, parent_field_names):
    #         #  field_value тип соответствует field_type модели 
    #         #  ничего не делаем, присваем field_value res_value
    #         res_value = field_value
    #     else:
    #         #  field_value тип не соответствует field_type модели 
    #         # делаем приведение типа в зависимости от типа field_value
    #         if field_value_type == 'dict':
    #             # производим приведение типа field_value типу модели 
    #             res_value = make_field_dict_type_cast(field_value, field_model, field_name, parent_field_names)
    #         elif field_value_type == 'list':
    #             # производим приведение типа field_value типу модели 
    #             res_value = make_list_type_cast(field_value, field_model, field_name, parent_field_names)
    #         else:
    #             # если тип поля простой или list и он не соответствует 
    #             # field_type модели то пишем log b присваеваем res_value 
    #             # значение по умолчанию модели
    #             logger.warning(f'тип {field_value_type} поля {".".join(parent_field_names)} не соответствует field_types {", ".join(field_model["field_types"]["types"])} модели')
    #             res_value = _get_model_default_value(field_model)
    #     return res_value

    # def parse_list_model(parent_field_model: Dict, field_name: str, list_model: Dict, data: List, parent_field_names: List[str]) -> List:
    #     res_list = []
    #     for item in data:
    #         # делаем проверку на пустые и None значения
    #         if (item == "") or (item == None):
    #             continue
    #         # определяем тип элемента списка
    #         item_type = type(item).__name__
    #         logger.debug(f'in parse_list_model(): item type {item_type}')
    #         # проверяем зарегистриван ли тип в типах лист модели
    #         if (model:=list_model['types'].get(item_type, None)):
    #             # тип элемента списка зарегистрирован 
    #             # в типах модели списка
    #             # действуем в зависимости от типа элемента
    #             if model['type'] == 'dict':
    #                 # тип элемента dict 
    #                 # вызываем parse_dict_model(), 
    #                 res_value = parse_dict_model(model, item, parent_field_names)
    #                 # исключаем словари с пустыми exclusion key 
    #                 if res_value:=exclusion_of_empty_values(res_value, parent_field_model, field_name, parent_field_names):
    #                     # проводим приведение типа если необходимо
    #                     res_value = make_dict_type_cast(res_value, parent_field_model, field_name, parent_field_names, 'list')
    #                     res_value = value_conversion(res_value, parent_field_model, field_name, parent_field_names)
    #                     # результат аппендим в res_list
    #                     res_list.append(res_value) 
    #             elif model['type'] == 'list':
    #                 # тип элемента list 
    #                 # вызываем parse_list_model(), 
    #                 # результат аппендим в res_list
    #                 # list_value = 
    #                 res_list.append(parse_list_model(parent_field_model, field_name, model, item, parent_field_names)) 
    #             else:
    #                 # простой тип
    #                 # аппендим в res_list как есть
    #                 value = make_simple_type_cast(item, parent_field_model, field_name, parent_field_names, 'list')
    #                 value = value_conversion(value, parent_field_model, field_name, parent_field_names)
    #                 res_list.append(value) 
    #         else:
    #             # тип элемента списка не зарегистрирован 
    #             # в типах модели списка
    #             # пишеь log, аппендим 'type not definet in model'
    #             logger.warning(f'тип {item_type} элемента list поля [{".".join(parent_field_names)}] не зарегистрирован в типах модели list')
    #             # logger.warning(f'имя поля: {field_name}, элемент: {item}')
    #             res_list.append(get_model_default_value(parent_field_model, 'list'))
    #     # res =  field_values_type_conversion(res_list, parent_field_model, field_name, parent_field_names)
    #     # возвращаем результирующий список
    #     return res_list
    
    def join_list_values_for_simple_type(list_parsed_values: List, field_model: Dict, field_name: str, parent_field_names: List[str]) -> List[str]:
        """объединяет в единый список список полученный после
        парсинга arse_list_model_for_simple_type()
        """
        res_str_list = []
        
        for item in list_parsed_values:
            item_type = type_str(item)
            if item_type in SIMPLE_TYPES_LIST:
                res_val = simple_value_conversion_for_simple_type_model_field(item, field_model, field_name, parent_field_names)
                res_str_list.append(str(res_val))
            if item_type == 'dict':
                res_val = dict_value_conversion_for_simple_type_model_field(item, field_model, field_name, parent_field_names)
                res_str_list.append(str(res_val))
            if item_type == 'list':
                res_list = join_list_values_for_simple_type(item, field_model, field_name, parent_field_names)
                res_str_list.extend(res_list)
                # res_str_list.extend(join_list_values_for_simple_type()    
        return res_str_list
    
    
    def parse_list_data(list_data: List, list_model: Dict, field_name: str, parent_field_names: List[str], nesting_level = 0) -> List:
        logger.debug(f"----->{parse_list_data.__name__}(): field_name: {field_name}, parent_field_names: [{', '.join(parent_field_names)}]")

        res_list = []
        for item in list_data:
            # действуем в зависимости от типа item
            item_type = type_str(item)
            logger.debug(f"{parse_list_data.__name__}(): for item in list_data: item_type: {item_type}, field_name: {field_name}, parent_field_names: [{', '.join(parent_field_names)}]")
            # проверяем есть тип элемента в типах листа
            if (item_type_model:=list_model['types'].get(item_type, None)) == None:
                logger.debug(f"{parse_list_data.__name__}(): if (item_type_model:=list_model['types'].get(item_type, None)) == None: item_type: {item_type}, field_name: {field_name}, parent_field_names: [{', '.join(parent_field_names)}]")
                # ошибка - тип элемента списка отсутствует в модели листа
                # пишем лог, продолжаем
                logger.error(f'parse_list_model(): ошибка - тип элемента списка "{item_type}" отсутствует в модели листа, путь: [{", ".join(parent_field_names)}], nesting_level: {nesting_level} ')
                continue
            if item_type in SIMPLE_TYPES_LIST:
                logger.debug(f"{parse_list_data.__name__}(): if item_type in SIMPLE_TYPES_LIST: item_type: {item_type}, field_name: {field_name}, parent_field_names: [{', '.join(parent_field_names)}]")
                res_list.append(item)
            if item_type == 'dict':
                logger.debug(f"{parse_list_data.__name__}(): if item_type == 'dict': item_type: {item_type}, field_name: {field_name}, parent_field_names: [{', '.join(parent_field_names)}]")
                dict_list_item = parse_dict_data(item_type_model, item, parent_field_names)
                res_list.append(dict_list_item)
            if item_type == 'list':
                logger.debug(f"{parse_list_data.__name__}(): if item_type == 'list': item_type: {item_type}, field_name: {field_name}, parent_field_names: [{', '.join(parent_field_names)}]")
                # на данном этапе считаем данное состояние ошибкой
                # пишем лог, пропускаем значение
                # TODO: рассмотереть возможность делать list модель с типом list
                logger.error(f'parse_list_model(): недопустимый тип элемента "{item_type}" для лист модели списка, путь: [{", ".join(parent_field_names)}], nesting_level: {nesting_level} ')
                continue
                list_list_item = parse_list_data(item, item_type_model, field_name, parent_field_names, nesting_level+1)
                res_list.append(list_list_item)
        return res_list
    
    def make_simple_type_items_list_type_field_cast(list_parsed_values: List, field_model: Dict, field_name: str, parent_fields_names: List[str]) -> List:
        """приведение типа элемента листа к типу листа"""
        
        res_list = []
        if (list_type:=get_list_model_list_item_type(field_model, field_name, parent_fields_names)) == 'NoneType':
            # ошибка определения list_item типа
            # логи прописаны в get_list_model_list_item_type()
            # возвращаем дефолтное значение для типа модели
            return get_model_default_value_for_model_type(field_model, field_name, parent_fields_names)
        
        for list_item in list_parsed_values:
            list_item_type = type_str(list_item)
            if list_item_type in SIMPLE_TYPES_LIST:
                cast_list_item = make_simple_type_cast(list_item, field_model, field_name, parent_fields_names, 'list')
                if cast_list_item:
                    res_list.append(cast_list_item)
            elif list_item_type == 'dict':
                cast_list_item = make_dict_type_cast(list_item, field_model, field_name, parent_fields_names, 'list')
                if cast_list_item:
                    res_list.append(cast_list_item)
            else:
                # item_type == 'list'
                # на данном этапе считаем данное состояние ошибкой
                # пишем лог, пропускаем значение
                # TODO: рассмотереть возможность делать list модель с типом list
                logger.error(f'make_simple_type_items_list_type_field_cast(): недопустимый тип элемента "{list_item_type}" для лист модели списка, путь: [{", ".join(parent_fields_names)}]')
        
        return res_list
    
    def make_simple_type_items_list_type_field_scrap_type_conversion(list_parsed_values: List, field_model: Dict, field_name: str, parent_fields_names: List[str]) -> List:
        """scrap_type_conversion элемента листа, проводится посли кастинга
        поэтому все значения должны соответствовать типу модели,
        поэтому проверку типов не делаем"""
        
        logger.debug(f"-----> {make_simple_type_items_list_type_field_scrap_type_conversion.__name__}(): field_name: {field_name}, parent_fields_names: {', '.join(parent_fields_names)}")
        res_list = []
        for list_item in list_parsed_values:
            scrap_type_list_item = value_scrap_type_conversion(list_item, field_model, field_name, parent_fields_names)
            logger.debug(f"{make_simple_type_items_list_type_field_scrap_type_conversion.__name__}(): for list_item in list_parsed_values: field_name: {field_name}, parent_fields_names: {', '.join(parent_fields_names)}")
            # исключаем пустые значения
            if scrap_type_list_item:
                logger.debug(f"{make_simple_type_items_list_type_field_scrap_type_conversion.__name__}(): if scrap_type_list_item: field_name: {field_name}, parent_fields_names: {', '.join(parent_fields_names)}")
                res_list.append(scrap_type_list_item)

        logger.debug(f"<----- {make_simple_type_items_list_type_field_scrap_type_conversion.__name__}(): field_name: {field_name}, parent_fields_names: {', '.join(parent_fields_names)}")
        return res_list
    
    def make_simple_type_items_list_type_field_boolen_conversion(list_parsed_values: List, field_model: Dict, field_name: str, parent_fields_names: List[str]) -> List:
        """boolen_conversion элемента листа, проводится посли кастинга
        поэтому все значения должны соответствовать типу модели,
        поэтому проверку типов не делаем"""

        res_list = []
        for list_item in list_parsed_values:
            bool_corr_list_item = boolen_type_value_conversion(list_item, field_model, field_name, parent_fields_names)
            # исключаем пустые значения
            if bool_corr_list_item:
                res_list.append(bool_corr_list_item)

        return res_list
    
    
    def simple_type_items_list_type_field_convertion(list_parsed_values: List, field_model: Dict, field_name: str, parent_fields_names: List[str]) -> List:
        """приведение типа и scrap_type_conversion элементов листа простого типа"""

        res_list = make_simple_type_items_list_type_field_cast(list_parsed_values, field_model, field_name, parent_fields_names) 
        res_list = make_simple_type_items_list_type_field_boolen_conversion(res_list, field_model, field_name, parent_fields_names)
        res_list = make_simple_type_items_list_type_field_scrap_type_conversion(res_list, field_model, field_name, parent_fields_names) 

        return res_list
    
    def exclusion_dicts_with_empty_values_from_list(list_parsed_values: List, list_type: str, field_model: Dict, field_name: str, parent_field_names: List[str]) -> List:

        res_list = []
        for list_item in list_parsed_values:
            exc_list_item = exclusion_dict_with_empty_values(list_item, field_model, field_name, parent_field_names)
            if exc_list_item:
                res_list.append(exc_list_item)

        return res_list
    # def field_values_shape_reduction(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
    #     """изменение формы field_value в зависимости от значения
    #     поля модели value_scrap_type
    #     {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
    #     direct - значение берётся то которое вычисляется по умолчению None
    #     dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
    #     ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
    #     """
    #     return field_value
    
    def exclusion_dict_with_empty_values(dict_value: Dict, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """проверка field_value на значение поля exclusion_key модели,
        поле может иметь значение только если проверяемое field_value 
        словарь (dict) и только в том случае если данный словарь 
        являествя элементом некого списка (list[dict]), в данном контексте 
        проверяемы exclusion_key это имя ключа словаря, ключевого атребута
        в котором содержится значение определяющее саму сущьность словаря,
        без которого сам dict теряет смысл. Например в списке покупок может быть
        запись
        {'наименование товара': 'картофель', 'кол-во': ''}
        в данном примере ''кол-во' некий атребут без которого веся сущьность
        покупи 'картофель' теряет смысл - поэтому её нужно исключить из
        списка вообще.
        Функция проверяет наличие exclusion_key - если его нет или его значение 
        в field_value не пустое то возвращиет field_value, 
        в противнос случае проверяет значение
        exclusion_key в field_value и если там содержится пустое значение ("" или "-")
        то возвращает None, который должен проверяться в parse_list_model()
        при добавлении значения в список
        """
        # проверяем что field_value есть dict
        if (data_type:=type_str(dict_value)) == 'dict':
            # field_value есть dict
            # проверяем что поле exclusion_key есть в модели
            if exc_key:=field_model.get('exclusion_key', None):
                # поле exclusion_key есть в модели
                # проверяем что проверяемый dict содержит ключ с именеи 
                # значения exclusion_key
                if (exc_key_val:=dict_value.get(exc_key, None)) != None:
                    # field_value содержит ключ с именем значения exclusion_key
                    # проверяем значение exclusion_key в field_value
                    if not (exc_key_val == "" or exc_key_val == "-"):
                        logger.debug(f'exclusion_dict_with_empty_values() exc_key_val: {exc_key_val}')
                        
                        #  exclusion_key в field_value содержит не пустое
                        # значение, возвращаем field_value
                        return dict_value
                    else:
                        logger.debug(f'exclusion_dict_with_empty_values() exc_key_val: {exc_key_val}')
                         #  exclusion_key в field_value содержит пустое
                        # значение, возвращаем None
                        return None
                else:
                    # field_value не содержит ключ с именем 
                    # значения exclusion_key. Пишем предупреждение в log
                    # возвращаем field_value
                    logger.warning(f'exclusion_dict_with_empty_values(): field_value с именем: [{", ".join(parent_field_names)}] не содержил ключа exclusion_key: {exc_key} модели')
                    return dict_value
            else:
                # поле exclusion_key отутствует в модели, значит проверка
                # не нужно, возвращаем field_value
                return dict_value
        else:
            # ошибочная ситуация здесь могут быть только dict значения
            # data не dict
            # пишем лог возвращаем дефолт для типа листа
            logger.error(f'exclusion_dict_with_empty_values(): тип данных "{data_type}", в данной функции может быть только "dict", path: {", ".join(parent_field_names)}')
            default_value_for_model = get_model_default_value_for_list_item(field_model, field_name, parent_field_names)
            return default_value_for_model
            
                
    def boolen_type_value_conversion(data_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """
        преобразование bool занчение в str эквивалент для возможности 
        обращения к справочнику и замены true на "Да", false на "Нет
        """

        data_value_type = type_str(data_value)
        logger.debug(f'in boolen_type_value_conversion(): field_value_type: {data_value_type}')
        if data_value_type == 'bool':
            return  'true' if data_value else 'false'
        else:
            return data_value
    
    def dict_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """ конвертация  field_value по значению 'dict' поля value_scrap_type модели """

        # проверим, что тип field_value - str
        if not isinstance(field_value, str):
            # field_value не str
            # пишем log, возвращаем field_value без конвертации
            logger.error(f'ошибка dict_scrap_type_conversion: тип field_value не str, field_value path: {".".join(parent_field_names)}') 
            return field_value
        t_path: List = field_model['value_scrap_type']['dict_path'].copy()
        t_path.extend(['available_values', 'values', field_value, 'name'])
        try:            
            res_value = get_value_from_dict_based_on_path_except_if_absent(search_form_v3, t_path)
        except Exception as e:
            # ошибка получения заначения из словаря по t_path
            #  пишем log, возвращаем field_value без конвертации
            logger.error(f'ошибка: {e}, dict_scrap_type_conversion: ошибка получения заначения из словаря по t_path: [{".".join(t_path)}] , field_value path: {".".join(parent_field_names)}') 
            return field_value
        return res_value
        
    # # def layout_formatting_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> str:
    # #     # получаем layout
    # #     if not _get_layout()
    
    
    def _check_dict_scrap_type(dict_scrap_type: Dict):
        """проверка на корректность типа dict_scrap_type"""
        # это должно быть словарь типа {'type': 'dict', 'dict_path': []}
        if ['type', 'dict_path'] != list(dict_scrap_type.keys()):
            return False
        if dict_scrap_type['type'] != 'dict':
            return False
        if not isinstance(dict_scrap_type['dict_path'], list):
            return False
        for item in dict_scrap_type['dict_path']:
            if not isinstance(item, str):
                return False
        return True
        
        
    def value_scrap_type_conversion(data_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """конвертация  data_value по значению поля value_scrap_type модели.
        возможные значения value_scrap_type
        {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
        direct - нет преобразования. Данное тип не указываем в модели
        dict - data_value подставляется в словарь по ссылке dict_path, 
        полученное заначение записывается в поле
        ref - из data_value делается ссылка путём подставления 
        его в заданное место в ref и уже оно записывается в поле"""
        logger.debug(f"-----> {value_scrap_type_conversion.__name__}(): field_name: {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
        
        
        # сначала проверяем наличие и значение поля value_scrap_type в моделе
        # данное поле может отсутствовать в моделе или быть пустое - 
        # direct вариант 
        if value_scrap_type_value:=field_model.get('value_scrap_type', None):
            logger.debug(f"{value_scrap_type_conversion.__name__}(): if value_scrap_type_value:=field_model.get('value_scrap_type', None): {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
            # value_scrap_type ключ есть в модели
            # действуем в зависимости от типа
            if scrap_type:=value_scrap_type_value.get('type', None):
                logger.debug(f"{value_scrap_type_conversion.__name__}(): if scrap_type:=value_scrap_type_value.get('type', None): scrap_type: {scrap_type}, field_name: {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
                # есть ключь "type" и он не пустой
                
                # выполним проверку на простоту тип
                data_value_type = type_str(data_value)
                if not data_value_type in SIMPLE_TYPES_LIST:
                    logger.debug(f"{value_scrap_type_conversion.__name__}(): if not data_value_type in SIMPLE_TYPES_LIST: data_value_type: {data_value_type}, field_name: {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
                    # ошибочное состояние - тип данных не протой
                    # пишем лог, присваеваем data_value дефолтное значение
                    logger.error(f'{value_scrap_type_conversion.__name__}(): ошибка сложный тип данных "{data_value_type}, данные должны быть простого типа, path: {".".join(parent_field_names)}"')
                    data_value = DEFAULT_VALUES_FOR_TYPES[data_value_type]()
                
                if scrap_type == 'dict':
                    logger.debug(f"{value_scrap_type_conversion.__name__}(): if scrap_type == 'dict': scrap_type: {scrap_type}, field_name: {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
                    # проверяем правильность форрмата dict scrap_type
                    if _check_dict_scrap_type(value_scrap_type_value):
                        # value_scrap_type_value правильного формата
                        res_value = dict_scrap_type_conversion(data_value, field_model, field_name, parent_field_names)
                    else:
                        # value_scrap_type_value не правильного формата
                        # пишем log, возвращаем data_value без конвертации
                        logger.error(f'ошибка value_scrap_type_conversion(): тип dict value_scrap_type_value не правильного формата, data_value path: {".".join(parent_field_names)}') 
                        res_value = data_value
                        
                elif scrap_type == 'layout_formatting':
                    logger.debug(f"{value_scrap_type_conversion.__name__}(): elif scrap_type == 'layout_formatting': {scrap_type}, field_name: {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
                    # получаем layout
                    if layout:=_get_layout(field_name, value_scrap_type_value, search_form_v3):
                        # layout получен
                        # оборачиваем data_value
                        format_items_dict = safesub()
                        # в полученном layout должно быть место {item}
                        format_items_dict['item'] = data_value
                        res_value = layout.format_map(format_items_dict)
                    else:
                        # ошибка получения layout
                        # пишем лог, отставляем  data_value без conversion
                        logger.error(f'value_scrap_type_conversion(): ошибка получения layout, data_value path: {".".join(parent_field_names)}') 
                        res_value = data_value

                    # res_value = layout_formatting_scrap_type_conversion(data_value, field_model, field_name, parent_field_names)
                else:
                    # не поддерживаемый тип, пишем лог и возвращаем
                    #  data_value без конвертации
                    logger.error(f'value_scrap_type_conversion(): не поддерживаемый scrap_type тип: {scrap_type} , data_value path: {".".join(parent_field_names)}') 
                    res_value = data_value
            else:
                logger.debug(f"{value_scrap_type_conversion.__name__}(): else if scrap_type:=value_scrap_type_value.get('type', None): scrap_type: {scrap_type}, field_name: {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
                # ключь "type" отсутствует или он пустой - ошибка
                logger.error(f'{value_scrap_type_conversion.__name__}(): ключь "type" отсутствует или он пустой , data_value path: {".".join(parent_field_names)}') 
                res_value = data_value
        else:
            logger.debug(f"{value_scrap_type_conversion.__name__}(): else if value_scrap_type_value:=field_model.get('value_scrap_type', None): {field_name}, parent_field_names: [{','.join(parent_field_names)}]")
            
            # value_scrap_type ключ отсутствует в моделе
            # конвертация не требуется
            res_value = data_value
        return res_value    
    
    
    
    
    # # def _field_simple_type_value_conversion(res_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
    # #     """конвертация простого типа значения принадлежащего полю
    # #     в отличии от значения являющегося элементом списка
    # #     """
    # #     # проверяем соответствие типа заначение поля типу модели поля
    # #     if not _check_compliance_model_type_value_type(res_value, field_model, parent_field_names):
    # #         # производим приведение типа для простых типов
    # #         res_value =  _make_field_simple_type_cast(res_value, field_model, field_name, parent_field_names)
            
    # #     # преобразуем bool значение в строку, нужно для обращения к справочнику
    # #     res = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)

    # #     # если  послe _make_simple_type_cast() мы получили None то 
    # #     # мы не будем провдить его value_scrap_type_conversion()
    # #     # даже если она предусмотренна моделью поля
    # #     if res != None:

    # #         # корректируем полученное значени по полю модели value_scrap_type
    # #         # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
    # #         # direct - значение берётся то которое вычисляется по умолчению None
    # #         # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
    # #         # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
                
    # #         res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
    # #         # проверяем на путое значение для списка словарей
    # #         # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

    # #     return res

    # # def value_conversion(res_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
    # #     """конвертация любого занчениея по 'bool' и value_scrap_type занчениям"""
        
    # #     # преобразуем bool значение в строку, нужно для обращения к справочнику
    # #     res = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)
        
    # #     # корректируем полученное значени по полю модели value_scrap_type
    # #     # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
    # #     # direct - значение берётся то которое вычисляется по умолчению None
    # #     # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
    # #     # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
            
    # #     res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
    # #     # проверяем на путое значение для списка словарей
    # #     # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

    # #     return res

    # # def _field_dict_value_conversion(res_value: Dict, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
    #     """конвертация dict занчениея, которое является значением поля
    #     (в отличии от dict, который является элементом списка"""
    #     # корректируем полученное значение по 
    #     # значениям "field_type", "casting_key" модели поля
    #     # 
    #     res = make_field_dict_type_cast(res_value, field_model, field_name, parent_field_names)
        
    #     # res_value = field_values_type_conversion(res_value, field_model, field_name, parent_field_names)
    #     # res_value = field_values_shape_reduction(res_value, field_model, field_name, parent_field_names)

    #     # преобразуем bool значение в строку, нужно для обращения к справочнику
    #     res = boolen_type_value_conversion(res, field_model, field_name, parent_field_names)

    #     # корректируем полученное значени по полю модели value_scrap_type
    #     # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
    #     # direct - значение берётся то которое вычисляется по умолчению None
    #     # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
    #     # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
            
    #     res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
    #     # проверяем на путое значение для списка словарей
    #     # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

    #     return res

            
    def get_field_value_v_2(field_model: Dict, 
                            field_name: str, 
                            data: Dict,
                            parent_field_names: List[str]): 
        logger.debug(f"-----> {get_field_value_v_2.__name__}(): field_name: {field_name}, parent_field_names: {parent_field_names}")
        # возможны следущие варианты для 
        # 1. тип field_model простой
        #   1.1. дата типы простые
        #       - приведение типа к типу модели
        #   1.2. дата типы dict 
        #       - приведение типа к типу модели на основании casting_keys
        #   1.3. дата типы list 
        #       1.3.1 - элементы простые значения - объединяются в строку, тип подели должен быть str
        #       1.3.2 - элементы dict - на основании casting_keys превращаются в единичное значение и объединяются в строку, тип подели должен быть str
        # 2. тип field_model dict
        #   2.1. дата типы простые - на данный момент ошибка
        #   2.2. дата типы dict
        #   2.3. дата типы list - на данный момент ошибка
        # 3. тип field_model list
        #   3.1. дата типы простые
        #   3.2. дата типы dict
        #   3.3. дата типы list 
        
        model_type: str = get_model_type(field_model, field_name, parent_field_names)
        model_default_value: Union[int, float, bool, str, list, dict] = DEFAULT_VALUES_FOR_TYPES[model_type]()
        # для этого определяем тип модули
        logger.debug(f"{get_field_value_v_2.__name__}(): model_type: {model_type}")
        
        if model_type == 'NoneType':
            logger.debug(f"{get_field_value_v_2.__name__}(): if  model_type == 'NoneType': model_type: {model_type}")
            
            # ошибка в определении типа подели,
            # логи прописаны в get_model_type()
            # возвращаем дефолтное значение для модели
            return model_default_value
        parent_field_names.append(field_name)
        # parent_field_names = parent_field_names.copy() выплнена в parsing_dict
        # проверяем есть ли поле в данных
        if (data_value:=data.get(field_name, None)) != None:
            logger.debug(f"{get_field_value_v_2.__name__}(): if (data_value:=data.get(field_name, None)) != None:")
            # поле есть в данных
            # проверяем что тип поля присутсвует 
            # в зарегистрированных типах модели
            data_value_type = type_str(data_value)
            logger.debug(f"{get_field_value_v_2.__name__}(): if (data_value:=data.get(field_name, None)) != None: data_value_type: {data_value_type}")
            if field_model_type:=field_model['types'].get(data_value_type, None):
                logger.debug(f"{get_field_value_v_2.__name__}(): if field_model_type:=field_model['types'].get(data_value_type, None)")
                # будем действовоать в зависимости от типа  модели
                # он иожет быть 3-х видов:
                # 1. простой: int, float, bool, str
                # 2. dict
                # 3. list
                
                # 1. простой: int, float, bool, str
                if model_type in SIMPLE_TYPES_LIST:
                    logger.debug(f"{get_field_value_v_2.__name__}(): if model_type in SIMPLE_TYPES_LIST: model_type: {model_type}")
                    
                    # для простого типа рассматриваем следующие варианты
                    # типов получаемых данных
                    # 1. простой тип
                    # 2. dict
                    # 3. list - ошибочное состояние на данный момент
                    #   3.1 list item - простой тип
                    #   3.2 list item - dict
                    #   3.3 list item - list
                
                    # 1. простой тип
                    if data_value_type in SIMPLE_TYPES_LIST:
                        logger.debug(f"{get_field_value_v_2.__name__}(): if data_value_type in SIMPLE_TYPES_LIST: data_value_type: {data_value_type}")
                        # make_simple_type_cast()
                        # boolen_type_value_conversion()
                        # value_scrap_type_conversion()
                        return simple_value_conversion_for_simple_type_model_field(data_value, field_model, field_name, parent_field_names)
                        # # осуществляем приведение к типу модели
                        # res_value = make_simple_type_cast(data_value, field_model, field_name, parent_field_names, 'field')
                        # # осуществляем boolen_type_value_conversion
                        # res_value = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)
                        # # осуществляем value_scrap_type конвертацию
                        # # позвращаем полученное значение
                        # return value_scrap_type_conversion(res_value, field_model, field_name, parent_field_names)

                    # 2. dict
                    if data_value_type == 'dict':
                        logger.debug(f"{get_field_value_v_2.__name__}(): if data_value_type == 'dict': data_value_type: {data_value_type}")
                        dict_model = field_model_type
                        res_dict = parse_dict_data(dict_model, data_value, parent_field_names)
                        
                        # make_field_dict_type_cast()
                        # boolen_type_value_conversion()
                        # value_scrap_type_conversion()
                        return dict_value_conversion_for_simple_type_model_field(res_dict, field_model, field_name, parent_field_names)
                        # res_value = make_field_dict_type_cast(res_dict, field_model, field_name, parent_field_names)
                        # res_value = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)
                        # # осуществляем value_scrap_type конвертацию
                        # # позвращаем полученное значение
                        # return value_scrap_type_conversion(res_value, field_model, field_name, parent_field_names)
                    
                    # ошибочное состояние на данный момент
                    # допустимые дипы данных для простого типа модели
                    # только SIMPLE и "dict"
                    # пишем лог
                    # позвращаем дефолтное значение для типа модели
                    # logger.debug(f"else if data_value_type == 'dict': data_value_type: {data_value_type}")
                    # logger.error(f'{get_field_value_v_2.__name__}(): ошибочный тип данных "{data_value_type}" - для тип модели "{model_type}" возможено только тип данных "dict", path: [{", ".join(parent_field_names)}]')
                    # return model_default_value
                    # 3. list - пока считаем ошибочнм состоянием и не используем в модели
                    if data_value_type == 'list':
                        # list data может допукаться в модель типа str,
                        # т.к. предполагается join все значения листа в строку
                        #  поэтому осуществляем проверку типа модели на 
                        # соответствие типу str
                        if model_type != 'str':
                            # ошибка, модель должна быть типа str
                            # пишем лог, возвращаем дефолтное значение для модели поля
                            logger.error(f'get_field_value_v_2(): не допустимый тип модели "{model_type}", для типа данных "list" - тип модели должен быть "str", path: [{", ".join(parent_field_names)}]')
                            return model_default_value
                        list_model = field_model_type
                        res_list = parse_list_data(data_value, list_model, field_name, parent_field_names)
                        res_list_str = join_list_values_for_simple_type(res_list, field_model, field_name, parent_field_names)
                        return ", ".join(res_list_str)
                
                # 2. dict
                if model_type == 'dict':
                    logger.debug(f"{get_field_value_v_2.__name__}(): if model_type == 'dict': model_type: {model_type}")
                    # на данный момент считаем возжные только
                    # толь dict тип данных для модели данного типа
                    if data_value_type != 'dict':
                        logger.debug(f"{get_field_value_v_2.__name__}(): if data_value_type != 'dict': data_value_type: {data_value_type}")
                        # ошибочное значение data_value_type для dict типа модели
                        # пишем лог, возвращаем дефолтное значение для модели 
                        logger.error(f'{get_field_value_v_2.__name__}(): ошибочный тип данных "{data_value_type}" - для тип модели "dict" возможено только тип данных "dict", path: [{", ".join(parent_field_names)}]')
                        return model_default_value
                    return parse_dict_data(field_model_type, data_value, parent_field_names)

                # 3. list
                if model_type == 'list':
                    logger.debug(f"{get_field_value_v_2.__name__}(): if model_type == 'list': model_type: {model_type}")
                    # проверяем data_value_type - он может быть только list
                    if data_value_type != 'list':
                        logger.debug(f"{get_field_value_v_2.__name__}(): if data_value_type != 'list': data_value_type: {data_value_type}")
                        # в занном случае заворачиваем единичное значение в лист
                        # отправляем дальше в обработку
                        data_value = [data_value]
                        # # ошибочное значение data_value_type для list типа модели
                        # # пишем лог, возвращаем дефолтное значение для модели 
                        # logger.error(f'get_field_value_v_2(): ошибочный тип данных "{data_value_type}" - для тип модели "list" возможено только тип данных "list", path: [{", ".join(parent_field_names)}]')
                        # return model_default_value
                    # list_model = field_model_type
                    res_list = parse_list_data(data_value, field_model_type, field_name, parent_field_names)
                    # определяем тип листа (simple или dict)
                    if (list_type:=get_list_model_list_item_type(field_model, field_name, parent_field_names)) == 'NoneType':
                        logger.debug(f"(list_type:=get_list_model_list_item_type(field_model_type, field_name, parent_field_names)) == 'NoneType': list_type: {list_type}")
                        # ошибка определения list_item типа
                        # логи прописаны в get_list_model_list_item_type()
                        # возвращаем дефолтное значение для типа модели
                        return model_default_value
                    # действуем в зависимости от типа листа
                    if list_type in SIMPLE_TYPES_LIST:
                        logger.debug(f"{get_field_value_v_2.__name__}(): if list_type in SIMPLE_TYPES_LIST: list_type: {list_type}")
                        res_list = simple_type_items_list_type_field_convertion(res_list, field_model, field_name, parent_field_names)
                        # простой тип листа
                        return res_list
                    if list_type == 'dict':
                        logger.debug(f"{get_field_value_v_2.__name__}(): if list_type == 'dict': list_type: {list_type}")
                        res_list = exclusion_dicts_with_empty_values_from_list(res_list, list_type, field_model, field_name, parent_field_names)
                        return res_list
                    # TODO: рассмотереть возможность делать list модель с типом list
                    # ошибка - не поддерживаемый тип элемента листа
                    # пишем лог, возвращаем дефолтное значение для модели
                    logger.error(f'{get_field_value_v_2.__name__}(): не поддерживаемый тип "{list_type}" элемента листа, paht {".".join(parent_field_names)}')
                    return model_default_value
            else:
                logger.debug(f"{get_field_value_v_2.__name__}(): else if field_model_type:=field_model['types'].get(data_value_type, None): field_model_type: {field_model_type}")
                # тип данных не зарегистрирован в типах модели
                # пишеь log, присваиваем результату значение по умолчанию для типа
                logger.warning(f'{get_field_value_v_2.__name__}(): тип {data_value_type} поля {".".join(parent_field_names)} не зарегистрирован в типах модели')
                return model_default_value
        else:
            logger.debug(f"{get_field_value_v_2.__name__}(): else if (data_value:=data.get(field_name, None)) != None:")
            # поля нет в данных
            # присваиваем результату значение по умолчанию для типа
            return model_default_value
       
    # def get_field_value(field_model: Dict, 
    #                      field_name: str, 
    #                      data: Dict,
    #                      parent_field_names: List[str]): 
        
    #     # возможны следущие варианты field_value
    #     # 1. тип field_model простой
    #     #   1.1. дата типы простые
    #     #   1.2. дата типы dict
    #     #   1.3. дата типы list
    #     # 2. тип field_model dict
    #     #   2.1. дата типы простые
    #     #   2.2. дата типы dict
    #     #   2.3. дата типы list
    #     # 3. тип field_model list
    #     #   3.1. дата типы простые
    #     #   3.2. дата типы dict
    #     #   3.3. дата типы list
        
        
    #     parent_field_names.append(field_name)
        
    #     # проверяем есть ли поле в данных
    #     if (field_value:=data.get(field_name, None)) != None:
    #         # поле есть в данных
    #         # проверяем что тип поля присутсвует 
    #         # в зарегистрированных типах модели
    #         field_type = type(field_value).__name__
    #         if field_model_type:=field_model['types'].get(field_type, None):
    #             # тип данных зарегистрирован в типах модели
    #             # действуем в зависимости от типа поля
    #             if field_type == 'dict':
    #                 # если поле типа dict вызываем parse_dict_model()
    #                 res_value = parse_dict_model(field_model_type, field_value, parent_field_names)
    #                 res_value = make_dict_type_cast(res_value, field_model, field_name, parent_field_names, 'field')
    #                 return  value_conversion(res_value, field_model, field_name, parent_field_names)
                    
    #             elif field_type == 'list':
    #                 # если поле типа list вызываем parse_list_model()
    #                 res_value = parse_list_model(field_model, field_name, field_model_type, field_value, parent_field_names)
    #                 res_value = make_list_type_cast(res_value, field_model, field_name, parent_field_names)
    #             else:
    #                 # если поле простого типа - берём его значение
    #                 # делаем конвертацию
    #                 res_value = _field_simple_type_value_conversion(field_value,field_model,field_name,parent_field_names)                    
    #         else:
    #             # тип данных не зарегистрирован в типах модели
    #             # пишеь log, присваиваем результату значение по умолчанию для типа
    #             logger.warning(f'get_field_value(): тип {field_type} поля {".".join(parent_field_names)} не зарегистрирован в типах модели')
    #             res_value = _get_model_default_value(field_model)
    #     else:
    #         # поля нет в данных
    #         # присваиваем результату значение по умолчанию для типа
    #         logger.debug(f'get_field_value(): field name: {".".join(parent_field_names)} нет в данных')
    #         res_value = _get_model_default_value(field_model)
        
    #     return res_value


    
    def parse_dict_data(dict_model: Dict, data: Dict, parent_field_names: List[str] = []) -> Dict:
        logger.debug(f"----->{parse_dict_data.__name__}(): parent_field_names: [{', '.join(parent_field_names)}]")
        dict_model_fields = dict_model['fields']
        dif_field_names = set(data.keys()) - set(dict_model_fields.keys())
        if dif_field_names:
            # for key in dict_model_fields.keys():
            #     logger.warning(f'model_key: {key}')
            # logger.error(f"model['type'] == 'dict': model_field: [{','.join(dict_model['fields'].keys())}]")
            # logger.error(f"data['type'] == 'dict': data_field: [{','.join(data.keys())}]")

            for field_name in dif_field_names:
                logger.warning(f'parse_dict_model(): field_name: {field_name} not in model, parent_field_names: {parent_field_names}')
        to_feeded_fields_name: List[str] = _get_to_feeded_fields(dict_model_fields)
        # мы отправляем в получение значения все поля не проверяя
        # есть ли они в полученных данных
        res_dict = {}
        for field_name in to_feeded_fields_name:
            res_dict_key = _get_field_to_feeded_name(dict_model_fields[field_name], field_name)
            logger.debug(f"{parse_dict_data.__name__}(): for field_name in to_feeded_fields_name: field_name: {field_name}, parents: [{', '.join(parent_field_names)}]")
            res_dict_value = get_field_value_v_2(dict_model_fields[field_name], field_name, data, parent_field_names.copy())
            res_dict[res_dict_key] = res_dict_value     
        
        logger.debug(f"<----- {parse_dict_data.__name__}(): parent_field_names: [{', '.join(parent_field_names)}]")
                 
        # res_dict = {
        #         _get_field_to_feeded_name(dict_model_fields[field_name], field_name): 
        #         get_field_value_v_2(dict_model_fields[field_name], field_name, data, parent_field_names.copy())
        #         for field_name in to_feeded_fields_name 
        #         }
        
        return res_dict

    return parse_dict_data(feed_model, raw_data)
    


def test_model_parsing_v_1():
        
    search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')

    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/05.06.24_20-05-18.items.json')
    raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])
    # raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])

    res_list = []
    for data in raw_data_gen:
        res_list.append(parsing_raw_data_relative_to_data_model_v2_var2(search_form_dict, data))



    write_dict_or_list_to_json_file('feed/05.06.24_20-05-18.items_parsed_v2.json', res_list)
    # write_dict_or_list_to_json_file('feed/parsed_content_13.json', res_list)



def test_model_parsing_v_1_1():
        
    search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')

    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/test_items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    raw_data_dict_list = load_dict_or_list_from_json_file('feed/05.06.24_20-05-18.items.json')
    raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])
    # raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])

    res_list = []
    for data in raw_data_gen:
        parsed_data = parsing_raw_data_relative_to_data_model_v2_var2(search_form_dict, data)
        feed_customizing(search_form_dict, data, parsed_data,)
        res_list.append(parsed_data)



    write_dict_or_list_to_json_file('feed/05.06.24_20-05-18.items_parsed_v4.json', res_list)
    # write_dict_or_list_to_json_file('feed/parsed_content_13.json', res_list)
def test_model_parsing_v_2_1():
        
    search_form_dict = load_dict_or_list_from_json_file('spiders/test_model.json')

    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/test_items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    raw_data_dict_list = load_dict_or_list_from_json_file('feed/05.06.24_20-05-18.items.json')
    raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])
    # raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])

    res_list = []
    for data in raw_data_gen:
        parsed_data = parsing_raw_data_relative_to_data_model_v2_var2(search_form_dict, data)
        # feed_customizing(search_form_dict, data, parsed_data,)
        res_list.append(parsed_data)



    write_dict_or_list_to_json_file('feed/05.06.24_20-05-18.items_parsed_v4.json', res_list)
    # write_dict_or_list_to_json_file('feed/parsed_content_13.json', res_list)
        
        
        
def test_model_parsing_v_2():
    search_form_dict = load_dict_or_list_from_json_file('spiders/test_model.json')
    
    raw_data_dict = load_dict_or_list_from_json_file('feed/raw_feed_item.json')

    # print(raw_data_dict)

    parsed_content =  parsing_raw_data_relative_to_data_model_v2_var2(search_form_dict, raw_data_dict)
    # write_dict_or_list_to_json_file('feed/parsed_content_3.json', parsed_content)
    feed_customizing(search_form_dict, raw_data_dict, parsed_content)
    write_dict_or_list_to_json_file('feed/parsed_content_3_custom.json', parsed_content)


def test_get_model():
    model = get_feed_model_v2_from_feed_items_file('feed/05.06.24_20-05-18.items.json', [])
    # model = get_feed_model_v2_from_feed_items_file('feed/06.06.24_08-07-52.items.json', [])
    write_dict_or_list_to_json_file('feed_items_modelv2_3.json', model)
    

if __name__ == '__main__':
    logging_configure(logger, logging.WARNING)
    # test_model_parsing_v_2()
    # test_model_parsing_v_1_1()
    # test_model_parsing_v_1()
    # test_get_model()
    test_model_parsing_v_1_1()