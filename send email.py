cont = [
        [
            "Mary",
            "flyletter23@gmail.com"
        ],
        [
            "Michael",
            "natashka42@googlemail.com"
        ],
        [
            "Kate",
            "natalya9448@yandex.ru"
        ]
    ]
dict_cont = {}
for i in cont:
    dict_cont[i[0]] = i[1]
for key, value in dict_cont.items():
    email = value
    print(email)



