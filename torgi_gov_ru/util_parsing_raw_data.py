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
from os import name
from typing import Iterable, Dict, Generator, Literal, NoReturn, Set, Tuple, List, FrozenSet, Union, Any, Callable
# from unittest.mock import DEFAULT

# import scrapy
# from importlib import simple
from util import logging_configure, load_dict_or_list_from_json_file, write_dict_or_list_to_json_file
from util import get_data_generator_from_dict_iterable, type_str

# from util import SIMPLE_TYPES_LIST, CLASS_TYPES_LIST


import logging
import typing

SIMPLE_TYPES_LIST = ['int', 'float', 'bool', 'str']
CLASS_TYPES_LIST = ['list', 'dict']

DEFAULT_VALUES_FOR_TYPES = {
    'str': lambda : '',
    'int': lambda : None,
    'float': lambda : None,
    'bool': lambda : None,
    'list': lambda : [],
    'dict': lambda : {},
    'NoneType': lambda : None
}

logger = logging.getLogger(__name__)


def get_feed_model_from_search_file(search_file: Dict) -> Dict:
    """получение полей feed модели"""

    return search_file['feed']['types']['dict']['field']

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


    # TODO: доделать конвертацию  destinations_paths
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
    
    def _check_field_dict_or_list_dict(field_name: str, field_model: Dict) -> Union[None, Literal['list', 'dict']]:
        """проверяет, что поле является dict или list dict, None если False,
        'list' или 'dict' если True 
        """
        
        if (fiel_type:=get_model_type_none_if_error(field_model, field_name, [])) == None:

           
    
    def _get_dict_fields_from_field_model(field_name: str, field_model: Dict):
        """поучает модель поля, выдаёт поля словаря поля,
        поле должно быть типа dict или list типа  dict, в противном случае None
        """
        if field_model
    
    def _convert_destination_path(model_field_name: str, destinations_path: List[str], search_form_v3: Dict) -> Union[List['str'], None]: 
        """преобразует destinations_path в ключах модели в destinations_path в ключах parsed_feed_item"""
        res_path = []
        field_model_fields = get_feed_model_from_search_file(search_form_v3)
        for field_name in destinations_path:
            # проверяем наличие поля в модели
            if (field_model:=field_model_fields.get(field_name, None)) == None:
                # нет такого поля в feed модели
                # пишем лог, возвращаем None
                logger.error(f"{feed_customizing.__name__}():{_convert_destination_path.__name__}(): поля '{field_name}' в feed модели, model_field_name: {model_field_name}")
                return None
            # выполняем проверку, что модель типа dict или list dict
            if (model_type:=get_model_type_none_if_error(field_model, field_name, [])) == None:
                # ошибка типа модели поля
                logger.error(f"{feed_customizing.__name__}():{_convert_destination_path.__name__}(): ошибка типа модели поля '{field_name}'")
                return None
            if model_type != 'dict':
                if model_type == 'list':
                    if (model_type:=get_list_model_list_item_type_none_if_error(field_model, field_name, [])) == None:
                        # ошибка типа модели поля
                        logger.error(f"{feed_customizing.__name__}():{_convert_destination_path.__name__}(): ошибка типа лист модели поля '{field_name}'")
                        return None
                    if model_type != 'dict':
                        # ошибка типа модели поля
                        logger.error(f"{feed_customizing.__name__}():{_convert_destination_path.__name__}(): ошибка типа лист модели поля '{field_name}'")
                        return None
                # ошибка типа модели поля
                logger.error(f"{feed_customizing.__name__}():{_convert_destination_path.__name__}(): ошибка типа лист модели поля '{field_name}'")
                return None
            
            field_model_fields = _get_dict_fields_from_field_model(field_name, field_model)
            name_for_path = _get_field_to_feeded_name(field_model_fields, field_name)
            res_path.append(name_for_path)
        return res_path


 
    def _get_destinations(model_field_name: str, model_field_model: Dict, parsed_feed_item: Dict, search_form_v3: Dict) -> Union[List[Dict],None]:

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
            # конвертируем destination_path по модели в converted_destination_path по parsed_feed_item
            if (convert_destination_path:=_convert_destination_path(model_field_name, destination_path, search_form_v3)) == None:
                # ошибка конвертации destination_path
                # пишем error log и пропускаем
                logger.error(f'{_get_destinations.__name__}(): ошибка конвертации destination_path, имя поля модели: {model_field_name}')
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



def get_model_type(field_model:Dict, field_name: str, parent_fields_names: List[str]):
    """определяем тип моделе, на основании поля ['field_types']['types'] 
    ошибочные ситуации:
    1. (len(model_types) > 2) or (len(model_types) == 0) 
    2. (len(model_types) == 2) and (not ("NoneType" in model_types))
    3.  оба элемента model_types == "NoneType"
    возвращается "NoneType"
    """
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
    """определяем тип моделе, на основании поля ['field_types']['types'] 
    ошибочные ситуации:
    1. (len(model_types) > 2) or (len(model_types) == 0) 
    2. (len(model_types) == 2) and (not ("NoneType" in model_types))
    3.  оба элемента model_types == "NoneType"
    возвращается None
    """
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


def get_list_model_list_item_type_none_if_error(field_model: Dict, field_name: str, parent_fields_names):
    """возвращает тип элемента списка,
    для этого тип модели должне быть 'list'
    """
    # проверяем, что модель типа 'list'
    if not (model_type:=get_model_type(field_model, field_name, parent_fields_names)) == 'list':
        logger.error(f'get_list_model_list_item_type: модель имеет тип: {model_type}, должен быть "list", имя поля: {field_name}, паретс: [{", ".join(parent_fields_names)}]') 
        return None
    # получаем тип элемента списка
    if (item_type:=field_model['field_types'].get('type_for_list', None)) == None:
        # ошибка, type_for_list не определён
        logger.error(f'get_list_model_list_item_type: type_for_list не определён, имя поля:  имя поля: {field_name}, паретс: [{", ".join(parent_fields_names)}]') 
        return None
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
        """приведение типа элемента листа к типу листа, в целях дальнйшего упрощения приведения 
        типов простых элементов листа, на данном этапе все элементы приводим к типу "str", т.е. 
        итоговый лисп простых типов может быть только типа "str" """
        
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
                    res_list.append(str(cast_list_item))
            elif list_item_type == 'dict':
                cast_list_item = make_dict_type_cast(list_item, field_model, field_name, parent_fields_names, 'list')
                if cast_list_item:
                    res_list.append(str(cast_list_item))
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



    # write_dict_or_list_to_json_file('feed/05.06.24_20-05-18.items_parsed_v4.json', res_list)
    write_dict_or_list_to_json_file('feed/parsed_content_13.json', res_list)

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
    search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')
    # search_form_dict = load_dict_or_list_from_json_file('spiders/test_model.json')
    
    raw_data_dict = load_dict_or_list_from_json_file('feed/raw_test_item.json')

    # print(raw_data_dict)

    parsed_content =  parsing_raw_data_relative_to_data_model_v2_var2(search_form_dict, raw_data_dict)
    # write_dict_or_list_to_json_file('feed/parsed_content_3.json', parsed_content)
    feed_customizing(search_form_dict, raw_data_dict, parsed_content)
    write_dict_or_list_to_json_file('feed/parsed_content_4_custom.json', parsed_content)

if __name__ == '__main__':
    logging_configure(logger, logging.WARNING)
    test_model_parsing_v_2()
    # test_model_parsing_v_1_1()
    # test_model_parsing_v_1()
    # test_get_model()
    # test_model_parsing_v_1_1()
    # convert_parsed_feed_to_class_items_test()