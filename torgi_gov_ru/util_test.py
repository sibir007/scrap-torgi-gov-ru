class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'
test_layout = "test_layout: name1: {name1}, name2: {name2}"
item1 = {'name1': 'dima'}
item2 = {'name1': 'dima', 'name2': 'vasua'}
item4 = {'name1': 'dima', 'name3': 'vasua'}
item3 = {}
test_str1 = test_layout.format_map(safesub(item1))
test_str2 = test_layout.format_map(safesub(item2))
test_str3 = test_layout.format_map(safesub(item3))
test_str4 = test_layout.format_map(safesub(item4))
print(f'test_str1: {test_str1}')
print(f'test_str2: {test_str2}')
print(f'test_str3: {test_str3}')
print(f'test_str4: {test_str4}')