# import operator

import util
import logging

logger = logging.getLogger(__name__)
# class safesub(dict):

#     def __missing__(self, key):
#         return '{' + key + '}'
# test_layout = "test_layout: name1: {name1}, name2: {name2}"
# item1 = {'name1': 'dima'}
# item2 = {'name1': 'dima', 'name2': 'vasua'}
# item4 = {'name1': 'dima', 'name3': 'vasua'}
# item3 = {}
# test_str1 = test_layout.format_map(safesub(item1))
# test_str2 = test_layout.format_map(safesub(item2))
# test_str3 = test_layout.format_map(safesub(item3))
# test_str4 = test_layout.format_map(safesub(item4))
# print(f'test_str1: {test_str1}')
# print(f'test_str2: {test_str2}')
# print(f'test_str3: {test_str3}')
# print(f'test_str4: {test_str4}')
# from ast import Try


classes = {
    "lot": {
        "type": "dict",
        "path": [],
        "fields": ["ID_лота", "Номер_извещения", "Номер_лота"],
        "extra_fields": {}
    },
    "lot_characteristics": {
        "type":'dict_list',
        "path": ["Характеристики_лота"],
        "fields": ["Значение", "Наименование", "Ед.изм."],
        "extra_fields": {
            "ID_лота": []
        }
    },
    "lot_lotImages": {
        "type":'simple_list',
        "path": ["Изображениея_лота"],
        "fields": ["Изображениея_лота"],
        "extra_fields": {
            "ID_лота": []
        }
    },
    
}


def logger_wrap(fun):
    fun_name = fun.__name__
    logger_name = 

# print(str(True))
# print(str(100))
# print(str(129292.888128e1))
# print(str(type(None).__name__))

# logger.
def test_function():
    logger.debug(f'in test function __name__: {test_function.__name__}')


if __name__ == '__main__':
    util.logging_configure(logger, logging.DEBUG)
    # tes\
        
    test_function()