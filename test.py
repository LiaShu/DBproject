# -*- coding: utf-8 -*-
data = [('flyletter23@gmail.com', 'Кухонные полотенца', 'Постирайте в машинке.'),
        ('flyletter23@gmail.com', 'Посуда', 'Перед сном вымойте.'),
        ('liashu2023@gmail.com', 'Кухонный стол', 'Протирайте стол.'),
        ('natalya9448@yandex.ru', 'Кухонный стол', 'Протирайте стол.'),
        ('liashu2023@gmail.com', 'Миски домашних питомцев', 'Большинство мисок можно мыть в посудомоечной машине. '),
        ('natalya9448@yandex.ru', 'Кухонные шкафчики', 'Протрите тряпкой с чистящим средством. '),
        ('flyletter23@gmail.com', 'Кухонные шкафчики', 'Протрите тряпкой с чистящим средством. ')]

dict_task = {}
final_list = []
for i in data:
     list_i = list(i)
     final_list.append(list_i)
for j in final_list:
     email = j[0]
     value = j[1::]
     if email not in dict_task.keys():
          dict_task[email] = value
     else:
          new_value = j[1::]
          f_val = dict_task.get(email) + new_value
          dict_task[email] = f_val
print(dict_task)
for k, v in dict_task.items():
    email = k
    task = v

#      list_test.append(i[0])
#      list_test.append(list(i[1:]))
#      final_list.append(list_test)
# list_name = list_test[::2]
# list_task = list_test[1::2]
# print(final_list)
