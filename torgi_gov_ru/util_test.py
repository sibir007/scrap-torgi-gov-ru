# import operator
from inspect import getmembers
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
        "class_name": "",
        "hr_name": '',
        "r_name": '',
        'random_name': '',
        "type": "dict",
        "path": [],
        "fields": {
            "ID_лота": {
                'hr_name': 'ID_лота',
                "r_name": "ID_лота",
                "type": "str"
            }, 
            "Номер_извещения": {
                "name": "Номер_извещения",
                "type": "str"
            }, 
            "Номер_лота": {
                "name": "Номер_лота",
                "type": "int"
            }
        },
        "foreign_key_fields": {}
    },
    "lot_Характеристики_лота": {
        "type":'list_dict',
        "path": ["Характеристики_лота"],
        "fields": {
            "Значение": {
                "name": "Значение",
                "type": "str"
            },
            "Наименование": {
                "name": "Наименование",
                "type": "str"
            },
            "Ед.изм.": {
                "name": "Ед.изм.",
                "type": "str"
            },
        },
        "foreign_key_fields": {}
    },
    "lot_Изображениея_лота": {
        "type":'simple_list',
        "path": ["Изображениея_лота"],
        "fields": {
            "Изображениея_лота": {
                "name": "Изображениея_лота",
                "type": "str"
            }
        },
        "foreign_key_fields": {}
    },
    
}


# def logger_wrap(fun):
#     fun_name = fun.__name__
#     logger_name = logger.name

# print(str(True))
# print(str(100))
# print(str(129292.888128e1))
# print(str(type(None).__name__))

# logger.
def test_function():
    logger.debug(f'in test function __name__: {test_function.__name__}')


def test2():
    a = 5
    b = 6
    context = dir()
    for item in context:
        print(item)


def function_for_test():
    test2()



if __name__ == '__main__':
    # util.logging_configure(logger, logging.DEBUG)
    # # tes\
        
    # test_function()
    
    # test_dict = {'key1': 'value1', 'key2': 'value2'}

    # print(dict(test_dict))
    function_for_test()
    # for item in dir():
    #     print( item)