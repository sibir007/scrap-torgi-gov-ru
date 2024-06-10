from typing import Iterable, Dict, Generator, NoReturn, Set, Tuple, List, FrozenSet, Union, Any, Callable
from util import logging_configure, load_dict_or_list_from_json_file, write_dict_or_list_to_json_file
from util import get_data_generator_from_dict_iterable

import logging
import typing


logger = logging.getLogger(__name__)


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


    
def feed_customizing(search_form_v3: Dict, raw_feed_item: Dict, parsed_feed_item: Dict) -> Dict:
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
            logger.error(f'process_dict_customizing(): dict_path не определён, имя поля модели: {field_name}')
            return
        
        # проверяем, что dict_path типа "list"
        if not isinstance(dict_path, list):
            # dict_path не правильного типа
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_path не правильного типа: {type(dict_path).__name__}, должен быть "list", имя поля модели: {field_name}')
            return
        
        # получаем dect_key_path
        if (dict_key_path:=value_scrap_type.get('dict_key_path', None)) == None:
            # dict_key_path не определён
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_key_path не определён, имя поля модели: {field_name}')
            return
        
        # проверяем, что dict_key_path типа "list"
        if not isinstance(dict_key_path, list):
            # dict_key_path не правильного типа
            # пишем лог, выходим 
            logger.error(f'process_dict_customizing(): dict_key_path не правильного типа: {type(dict_path).__name__}, должен быть "list", имя поля модели: {field_name}')
            return
        
        # # объединяеяем dict_path и dict_key_path
        # dict_path.extend(dict_key_path)
        # # получаем dict_key
        try:
            dict_key = get_value_from_dict_based_on_path_except_if_absent(raw_feed_item, dict_key_path)
        except:
            # ошибка получения занчения из dict
            # пишем лог, присваиваем dict_key дефолт значение модеи 
            logger.warning(f'process_dict_customizing(): ошибка получения занчения из raw_feed_item, dict_key_path: [{", ".join(dict_key_path)}], имя поля модели: {field_name}')
            dict_key = _get_field_model_default_value(model_field_model)
        
        # проверяем тип dict_key
        if not isinstance(dict_key, str):
            # ошибка типа dict_key
            # пишем лог, выходим
            logger.error(f'process_dict_customizing(): ошибка типа dict_key: {type(dict_key).__name__}, должен быть "str", имя поля модели: {field_name}')
            return
        # объединяем dict_path dict_key
        dict_path.extend(['available_values', 'values', dict_key, 'name'])
        # получаем custom значение из словаря
        
        try:
            dict_value = get_value_from_dict_based_on_path_except_if_absent(search_form_v3, dict_path)
        except:
            # ошибка получения занчения из dict
            # пишем лог, выходим
            logger.error(f'process_dict_customizing(): ошибка получения занчения из словаря, dict_path: [{", ".join(dict_path)}], имя поля модели: {field_name}')
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

        # сразу получаем destination  dict куда будет добавляться 
        # custom значение
        if (destinations_list:=_get_destinations(model_field_name, model_field_model, parsed_feed_item)) == None:
            # ошибка получения destinations
            # логи прописаны в _get_destination(), выходим
            return
        # получаем layout, если в роцессе получение возникли ошибки 
        # то вернётся None
        if (default_value:= _get_field_model_default_value(model_field_model)) == None:
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
            logger.info(f'feed_customizing(): value_scrap_type не определён, имя поля модели: {field_name}')
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

def _get_field_model_default_value(field_model:Dict):
    def_val = field_model['field_types']['default_value']
    if isinstance(def_val, dict) or isinstance(def_val, list):
        def_val = def_val.copy()
        
    return def_val
        
def parsing_raw_data_relative_to_data_model_v2(search_form_v3: Dict, raw_data: Dict)-> Dict: 
    """принимпет search_form.v3 и прогоняет по ней
     lot_card,  возвращает dict являющийсчся отрожением lot_card относительно
     feed_items_model_v_2
    """ 
    feed_model = search_form_v3['feed']['types']['dict']
    references = search_form_v3['references']

    def _check_compliance_model_field_type(field_value, field_model: Dict, parent_fields_names: List[str]):
        """проверки что тип field_value есть field_types модели"""

        field_value_type = type(field_value).__name__
        logger.debug(f'in _check_compliance_model_field_type(): {parent_fields_names}')
        return field_value_type in field_model['field_types']['types']
        
    def _make_dict_type_cast(field_value: Dict, field_model: Dict, field_name: str, parent_fields_names: List[str]):
        # проверяем соответств типа field_value типу определённому 
        # в field_model field_type поле
        if _check_compliance_model_field_type(field_value, field_model, parent_fields_names):
            #  field_value тип соответствует field_type модели 
            #  ничего не делаем, присваем field_value res_value
            res_value = field_value
        # в противном случе проверяем существование и значениея 
        # casting_key в field_model
        elif key_name:=field_model.get('casting_key', None):
            # casting_key существует, 
            # определяем значение casting_key в field_value 
            if (key_value:= field_value.get(key_name, None)) != None:
                # field_value имеет значение casting_key, 
                # проверяем соответствие его field_type модели
                if _check_compliance_model_field_type(key_value, field_model, parent_fields_names):
                    # тип key_value соответствует типу определённому в модели
                    # присваеваем его значение res_value 
                    res_value = key_value
                else:
                    # тип key_value не соотвествует типу определённоу в модели 
                    # пишем log
                    #   присваеваем res_value значение по умолчанию
                    logger.warning(f'_make_dict_type_cast(): ошибка приведение тип поля {".".join(parent_fields_names)}, после приведения неверное значение типа')
                    res_value = _get_field_model_default_value(field_model)
            else:
                # field_value не имеет значение casting_key, 
                # пишем log
                #   присваеваем res_value значение по умолчанию
                logger.warning(f'_make_dict_type_cast(): ошибка приведение тип поля {".".join(parent_fields_names)}, key_value модеди отсутствует приводимом dict данных')
                res_value = _get_field_model_default_value(field_model)
        else:
            # атребут casting_key отсутствует в модели или 
            # его значение равно пустому значению,
            # могут быть два варианта:
            # 1. dict является элементом списка поля и отсутствие casting_key
            # означает, что не нужно делать ни каких привдений
            if "list" in field_model['field_types']['types']:
                res_value = field_value
            else:
                # 2. ошибка, нужно делать приведение dict, но casting_key отсутствует   
                # пишем log присваеваем res_value значение по умолчанию
                logger.warning(f'_make_dict_type_cast(): ошибка приведение типа поля {".".join(parent_fields_names)}, атребут casting_key отсутствует в модели или его значение равно пустому значению')
                res_value = _get_field_model_default_value(field_model)
        return res_value
    
    def _make_list_type_cast(field_value: List, field_model: Dict, field_name: str, parent_fields_names: List[str]):
        """приведение списка к типу определённому в модели поля field_types,
        итоговый тип может быть только str, соответственно исходные типы
        элементов списка могут быть только простыми типами либо полученными
        напрямую при parse_list_model() либо приведение типа dict 
        содержащихся в списке, опять же при parse_list_model()  
        """
        
        # проверяем что полученное значение типа list
        if not isinstance(field_value, list):
            # полученное значение не типа list
            # пишем лог, возвращаем дефолт для модели
            logger.error(f'_make_list_type_cast():ошибка - поле: [{", ".join(parent_fields_names)}] не является типом "list"')
            return _get_field_model_default_value(field_model) 
            
        # проверяем что field_types содержит тип list
        # тогда ничего приводить не нужно, осравляем list
        if 'list' in field_model['field_types']['types']:
            # list является типом поля модели, 
            # возвращаем исходное значение
            return field_value
        
        # list не является типом поля модели, 
        # выполняем приведение.
        # приведённым значением типа list может быть только 
        # строка объяденяющая все единичные простые занчения листа
        # проверим есть ли str в списке field_types
        if not ('str' in field_model['field_types']['types']):
            # str не является типом поля модели - ошибка
            # пишем лог, возвращыем дефолтное значение для поля
            logger.error(f'_make_list_type_cast(): ошибока - "str" не является типом поля модели, поле: [{", ".join(parent_fields_names)}]')
            # logger.error(f'ошибка приведение типа "list" поля [{", ".join(parent_fields_names)}], str не является типом поля модели')
            return _get_field_model_default_value(field_model) 
            
        # str есть в field_types модели
        # объединяем значения списка в троку
        str_val = ""
        for item in field_value:
            # проверяем что item имеет простой тип
            if isinstance(item, list) or isinstance(item, dict):
                # item не простого типа - ошибка
                # пишем лог, пропускаем значение
                logger.error(f'_make_list_type_cast(): элемента списка имеет тип {type(item).__name__}, поле: [{", ".join(parent_fields_names)}]')
                continue
            str_val += item
        # приведение закончено, возвращаем заныение
        return str_val
    
    def field_values_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """конверктация типа field_value в тип указанный в field_type модели"""

        # проверяем соответствие типа field_value типу определённому 
        # в field_model field_type поле
        # определяем тип field_value
        field_value_type = type(field_value).__name__
        if _check_compliance_model_field_type(field_value, field_model, parent_field_names):
            #  field_value тип соответствует field_type модели 
            #  ничего не делаем, присваем field_value res_value
            res_value = field_value
        else:
            #  field_value тип не соответствует field_type модели 
            # делаем приведение типа в зависимости от типа field_value
            if field_value_type == 'dict':
                # производим приведение типа field_value типу модели 
                res_value = _make_dict_type_cast(field_value, field_model, field_name, parent_field_names)
            elif field_value_type == 'list':
                # производим приведение типа field_value типу модели 
                res_value = _make_list_type_cast(field_value, field_model, field_name, parent_field_names)
            else:
                # если тип поля простой или list и он не соответствует 
                # field_type модели то пишем log b присваеваем res_value 
                # значение по умолчанию модели
                logger.warning(f'тип {field_value_type} поля {".".join(parent_field_names)} не соответствует field_types {", ".join(field_model["field_types"]["types"])} модели')
                res_value = _get_field_model_default_value(field_model)
        return res_value

    def parse_list_model(parent_field_model: Dict, field_name: str, list_model: Dict, data: List, parent_field_names: List[str]) -> List:
        res_list = []
        for item in data:
            # определяем тип элемента списка
            item_type = type(item).__name__
            logger.debug(f'in parse_list_model(): item type {item_type}')
            # проверяем зарегистриван ли тип в типах лист модели
            if (model:=list_model['types'].get(item_type, None)):
                # тип элемента списка зарегистрирован 
                # в типах модели списка
                # действуем в зависимости от типа элемента
                if model['type'] == 'dict':
                    # тип элемента dict 
                    # вызываем parse_dict_model(), 
                    dict_value = parse_dict_model(model, item, parent_field_names)
                    # исключаем словари с пустыми exclusion key 
                    if dict_value:=exclusion_of_empty_values(dict_value, parent_field_model, field_name, parent_field_names):
                        # проводим приведение типа если необходимо
                        dict_value = _dict_value_conversion(dict_value, parent_field_model, field_name, parent_field_names)
                        # результат аппендим в res_list
                        res_list.append(dict_value) 
                elif model['type'] == 'list':
                    # тип элемента list 
                    # вызываем parse_list_model(), 
                    # результат аппендим в res_list
                    res_list.append(parse_list_model(parent_field_model, field_name, model, item, parent_field_names)) 
                else:
                    # простой тип
                    # аппендим в res_list как есть
                    value = _simple_type_value_conversion(item, parent_field_model, field_name, parent_field_names)
                    res_list.append(value) 
            else:
                # тип элемента списка не зарегистрирован 
                # в типах модели списка
                # пишеь log, аппендим 'type not definet in model'
                logger.warning(f'тип {item_type} элемента list поля [{".".join(parent_field_names)}] не зарегистрирован в типах модели list')
                # logger.warning(f'имя поля: {field_name}, элемент: {item}')
                res_list.append(_get_field_model_default_value(parent_field_model))
        # res =  field_values_type_conversion(res_list, parent_field_model, field_name, parent_field_names)
        # возвращаем результирующий список
        return res_list
    
    
    def field_values_shape_reduction(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """изменение формы field_value в зависимости от значения
        поля модели value_scrap_type
        {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
        direct - значение берётся то которое вычисляется по умолчению None
        dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
        ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
        """
        return field_value
    
    def exclusion_of_empty_values(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
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
        if type(field_value).__name__ == 'dict':
            # field_value есть dict
            # проверяем что поле exclusion_key есть в модели
            if exc_key:=field_model.get('exclusion_key', None):
                # поле exclusion_key есть в модели
                # проверяем что проверяемый dict содержит ключ с именеи 
                # значения exclusion_key
                if (exc_key_val:=field_value.get(exc_key, None)) != None:
                    # field_value содержит ключ с именем значения exclusion_key
                    # проверяем значение exclusion_key в field_value
                    if not (exc_key_val == "" or exc_key_val == "-"):
                        logger.debug(f'exclusion_of_empty_values() exc_key_val: {exc_key_val}')
                        
                        #  exclusion_key в field_value содержит не пустое
                        # значение, возвращаем field_value
                        return field_value
                    else:
                        logger.debug(f'exclusion_of_empty_values() exc_key_val: {exc_key_val}')
                         #  exclusion_key в field_value содержит пустое
                        # значение, возвращаем None
                        return None
                else:
                    # field_value не содержит ключ с именем 
                    # значения exclusion_key. Пишем предупреждение в log
                    # возвращаем field_value
                    logger.warning(f'ошибка exclusion_of_empty_values(): field_value с именем: [{", ".join(parent_field_names)}] не содержил ключа exclusion_key: {exc_key} модели')
                    return field_value
            else:
                # поле exclusion_key отутствует в модели, значит проверка
                # не нужно, возвращаем field_value
                return field_value
        else:
            # field_value не dict
            # возвращаем field_value
            return field_value
            
                
    def boolen_type_value_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """
        преобразование bool занчение в str эквивалент для возможности 
        обращения к справочнику и замены true на "Да", false на "Нет
        """

        field_value_type = type(field_value).__name__
        logger.debug(f'in boolen_type_value_conversion(): field_value_type: {field_value_type}')
        if field_value_type == 'bool':
            res_value = 'true' if field_value else 'false'
        else:
            res_value = field_value
        return res_value                
    
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
        
    # def layout_formatting_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> str:
    #     # получаем layout
    #     if not _get_layout()
    
    
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
        
        
    def value_scrap_type_conversion(field_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]):
        """конвертация  field_value по значению поля value_scrap_type модели.
        возможные значения value_scrap_type
        {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
        direct - нет преобразования. Данное тип не указываем в модели
        dict - field_value подставляется в словарь по ссылке dict_path, 
        полученное заначение записывается в поле
        ref - из field_value делается ссылка путём подставления 
        его в заданное место в ref и уже оно записывается в поле"""
        
        # сначала проверяем наличие и значение поля value_scrap_type в моделе
        # данное поле может отсутствовать в моделе или быть пустое - 
        # direct вариант 
        if value_scrap_type_value:=field_model.get('value_scrap_type', None):
            # value_scrap_type ключ есть в модели
            # действуем в зависимости от типа
            if scrap_type:=value_scrap_type_value.get('type', None):
                # есть ключь "type" и он не пустой
                if scrap_type == 'dict':
                    # проверяем правильность форрмата dict scrap_type
                    if _check_dict_scrap_type(value_scrap_type_value):
                        # value_scrap_type_value правильного формата
                        res_value = dict_scrap_type_conversion(field_value, field_model, field_name, parent_field_names)
                    else:
                        # value_scrap_type_value не правильного формата
                        # пишем log, возвращаем field_value без конвертации
                        logger.error(f'ошибка value_scrap_type_conversion(): тип dict value_scrap_type_value не правильного формата, field_value path: {".".join(parent_field_names)}') 
                        res_value = field_value
                        
                elif scrap_type == 'layout_formatting':
                    # получаем layout
                    if layout:=_get_layout(field_name, value_scrap_type_value, search_form_v3):
                        # layout получен
                        # оборачиваем field_value
                        format_items_dict = safesub()
                        # в полученном layout должно быть место {item}
                        format_items_dict['item'] = field_value
                        res_value = layout.format_map(format_items_dict)
                    else:
                        # ошибка получения layout
                        # пишем лог, отставляем  field_value без conversion
                        logger.error(f'value_scrap_type_conversion(): ошибка получения layout, field_value path: {".".join(parent_field_names)}') 
                        res_value = field_value

                    # res_value = layout_formatting_scrap_type_conversion(field_value, field_model, field_name, parent_field_names)
                else:
                    # не поддерживаемый тип, пишем лог и возвращаем
                    #  field_value без конвертации
                    logger.error(f'value_scrap_type_conversion(): не поддерживаемый scrap_type тип: {scrap_type} , field_value path: {".".join(parent_field_names)}') 
                    res_value = field_value
            else:
                # ключь "type" отсутствует или он пустой - ошибка
                logger.error(f'value_scrap_type_conversion(): ключь "type" отсутствует или он пустой , field_value path: {".".join(parent_field_names)}') 
                res_value = field_value
        else:
            # value_scrap_type ключ отсутствует в моделе
            # конвертация не требуется
            res_value = field_value
        return res_value    
        
    
    def _simple_type_value_conversion(res_value: Any, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
        # преобразуем bool значение в строку, нужно для обращения к справочнику
        res = boolen_type_value_conversion(res_value, field_model, field_name, parent_field_names)

        # корректируем полученное значени по полю модели value_scrap_type
        # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
        # direct - значение берётся то которое вычисляется по умолчению None
        # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
        # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
            
        res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
        # проверяем на путое значение для списка словарей
        # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

        return res

        
        
        
        
    def _dict_value_conversion(res_value: Dict, field_model: Dict, field_name: str, parent_field_names: List[str]) -> Any:
        """конвертация dict занчениея относлительно  модели поля"""
        # корректируем полученное значение по 
        # значениям "field_type", "casting_key" модели поля
        # 
        res = _make_dict_type_cast(res_value, field_model, field_name, parent_field_names)
        
        # res_value = field_values_type_conversion(res_value, field_model, field_name, parent_field_names)
        # res_value = field_values_shape_reduction(res_value, field_model, field_name, parent_field_names)

        # преобразуем bool значение в строку, нужно для обращения к справочнику
        res = boolen_type_value_conversion(res, field_model, field_name, parent_field_names)

        # корректируем полученное значени по полю модели value_scrap_type
        # {"type": "direct"}, {"type": "dict", "dict_path": []}, {"type": "ref", "ref": ""} 
        # direct - значение берётся то которое вычисляется по умолчению None
        # dict - вычисленное значение подставляется в словарь по ссылке dict_path, полученное заначение записывается в поле
        # ref - из вычисленного значения делается ссылка путём подставления его в заданное место в ref и уже оно записывается в поле
            
        res = value_scrap_type_conversion(res, field_model, field_name, parent_field_names)
        # проверяем на путое значение для списка словарей
        # res_value = exclusion_of_empty_values(res_value, field_model, field_name, parent_field_names)

        return res


            
        
    def get_field_value(field_model: Dict, 
                         field_name: str, 
                         data: Dict,
                         parent_field_names: List[str]): 
        parent_field_names.append(field_name)
        # проверяем есть ли поле в данных
        if (field_value:=data.get(field_name, None)) != None:
            # поле есть в данных
            # проверяем что тип поля присутсвует 
            # в зарегистрированных типах модели
            field_type = type(field_value).__name__
            if field_model_type:=field_model['types'].get(field_type, None):
                # тип данных зарегистрирован в типах модели
                # действуем в зависимости от типа поля
                if field_type == 'dict':
                    # если поле типа dict вызываем parse_dict_model()
                    res_value = parse_dict_model(field_model_type, field_value, parent_field_names)
                    
                    res_value = _dict_value_conversion(res_value, field_model, field_name, parent_field_names)
                    
                elif field_type == 'list':
                    # если поле типа list вызываем parse_list_model()
                    res_value = parse_list_model(field_model, field_name, field_model_type, field_value, parent_field_names)
                    res_value = _make_list_type_cast(res_value, field_model, field_name, parent_field_names)
                else:
                    # если поле обычного типа - берём его значение
                    # делаем конвертацию
                    res_value = _simple_type_value_conversion(field_value,field_model,field_name,parent_field_names)                    
            else:
                # тип данных не зарегистрирован в типах модели
                # пишеь log, присваиваем результату значение по умолчанию для типа
                logger.warning(f'get_field_value(): тип {field_type} поля {".".join(parent_field_names)} не зарегистрирован в типах модели')
                res_value = _get_field_model_default_value(field_model)
        else:
            # поля нет в данных
            # присваиваем результату значение по умолчанию для типа
            logger.debug(f'get_field_value(): field name: {".".join(parent_field_names)} нет в данных')
            res_value = _get_field_model_default_value(field_model)
        
        return res_value


    
    def parse_dict_model(dict_model: Dict, data: Dict, parent_field_names: List[str] = []) -> Dict:
        
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
        res_dict = {
                _get_field_to_feeded_name(dict_model_fields[field_name], field_name): 
                get_field_value(dict_model_fields[field_name], field_name, data, parent_field_names.copy())
                for field_name in to_feeded_fields_name 
                }
        
        return res_dict

    return parse_dict_model(feed_model, raw_data)

# def customization_feed(search_form_v3: Dict, parsed_feed_item: Dict):
    


def test_model_parsing_v_1():
        
    search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')

    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/05.06.24_20-05-18.items.json')
    raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])
    # raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])

    res_list = []
    for data in raw_data_gen:
        res_list.append(parsing_raw_data_relative_to_data_model_v2(search_form_dict, data))



    write_dict_or_list_to_json_file('feed/05.06.24_20-05-18.items_parsed_v2.json', res_list)
    # write_dict_or_list_to_json_file('feed/parsed_content_13.json', res_list)



def test_model_parsing_v_1_1():
        
    search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')

    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/test_items.json')
    raw_data_dict_list = load_dict_or_list_from_json_file('feed/06.06.24_08-07-52.items.json')
    # raw_data_dict_list = load_dict_or_list_from_json_file('feed/05.06.24_20-05-18.items.json')
    raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])
    # raw_data_gen = get_data_generator_from_dict_iterable(raw_data_dict_list, [])

    res_list = []
    for data in raw_data_gen:
        parsed_data = parsing_raw_data_relative_to_data_model_v2(search_form_dict, data)
        feed_customizing(search_form_dict, data, parsed_data,)
        res_list.append(parsed_data)



    write_dict_or_list_to_json_file('feed/05.06.24_20-05-18.items_parsed_v2.json', res_list)
    # write_dict_or_list_to_json_file('feed/parsed_content_13.json', res_list)
        
        
def test_model_parsing_v_2():
    search_form_dict = load_dict_or_list_from_json_file('spiders/search_form.v3.json')
    
    raw_data_dict = load_dict_or_list_from_json_file('feed/raw_feed_item.json')


    parsed_content =  parsing_raw_data_relative_to_data_model_v2(search_form_dict, raw_data_dict)
    write_dict_or_list_to_json_file('feed/parsed_content_1.json', parsed_content)
    feed_customizing(search_form_dict, raw_data_dict, parsed_content)
    write_dict_or_list_to_json_file('feed/parsed_content_2_custom.json', parsed_content)


def test_get_model():
    model = get_feed_model_v2_from_feed_items_file('feed/06.06.24_08-07-52.items.json', [])
    write_dict_or_list_to_json_file('feed_items_modelv2_2.json', model)
    

if __name__ == '__main__':
    logging_configure(logger, logging.WARNING)
    # test_model_parsing_v_2()
    test_model_parsing_v_1_1()
    # test_model_parsing_v_1()
    # test_get_model()
    