import json
import os
import pathlib
import pprint
import psycopg2


def DelTable():
    cur.execute("""
    DROP TABLE NumPhone;
    DROP TABLE client;
    """)

def getPath():
    path  = pathlib.Path.cwd()
    return path

def NumInput():
    while type:
        answer = input('Введите количество номеров телефона клиента: ')  # Ввод числа
        try:
            getTempNumber = int(answer)
        except ValueError:  # Проверка на ошибку неверного формата (введены буквы)
            print('"' + answer + '"' + ' - не является числом')
        else:
            break
    return int(answer)

def openClients():
    pathfile = os.path.join(getPath(), 'data.json')
    data = {}
    with open(pathfile, 'r') as file:
        data = json.load(file)
    return data
def CreateDataBase(): ## Функция, создающая структуру БД (таблицы)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                lastname VARCHAR(40),
                email VARCHAR(40)
                );
            CREATE TABLE IF NOT EXISTS NumPhone(
                id SERIAL PRIMARY KEY,
                PhoneNumber VARCHAR(20),
                Client_id INTEGER NOT NULL REFERENCES client(id)
                );
            """)
def addClient(): ## Заполнение таблиц базовыми данными
    data = openClients()
    for keys, elements in data.items():
        cur.execute("""
        INSERT INTO client (name, lastname, email) VALUES (%s, %s, %s);
        """, (elements[0][0], elements[0][1], elements[0][2])
                    )
        if len(elements[1]) == 1:
            addNumber(elements[1], keys)
        else:
            for items in elements[1]:
                addNumber(items, keys)

def addManualClient(): ## Функция, позволяющая добавить нового клиента
    listNumbers = []
    cur.execute("""
    INSERT INTO client (name, lastname, email) VALUES (%s, %s, %s) RETURNING id;
    """, (input("Введите имя клиента: "), input("Введите фамилию клиента: "), input("Введите email клиента: "))
                )
    client_id = cur.fetchall()
    answer = NumInput()
    if answer == 1:
        number = input("Введите номер телефона клиента: ")
        addNumber(number, client_id[0][0])
    else:
        for i in range(int(answer)):
            number = input("Введите номер телефона клиента: ")
            listNumbers.append(number)
    for elements in listNumbers:
        addNumber(elements, client_id[0][0])

def addNumber(number, client_id):
    cur.execute("""
    INSERT INTO NumPhone (PhoneNumber, Client_id) VALUES (%s, %s);
    """, (number, client_id)
                )

def selectTable():
    cur.execute("""
    SELECT * FROM client;
    """)
    print(cur.fetchall())
    cur.execute("""
    SELECT * from NumPhone
    """)
    print(cur.fetchall())

# def writefile():
#     data = {"1": [("Феликс", "Туров", "saugillicrouce-8344@yopmail.com"), ["8(921)286-09-49"]],
#      "2": [("Альберт", "Воронов", "cruzessulluffe-2867@yopmail.com"), ("8(921)896-42-23", "8(911)852-87-37")],
#      "3": [("Пахомов", "Глеб", "japeujucibru-1874@yopmail.com"), ["8(921)908-80-60"]],
#      "4": [("Джема", "Семёнова", "bautroufracrafe-5864@yopmail.com"), ["8(921)396-91-45"]],
#      "5": [("Лира", "Кузнецова", "demaupougreikou-8496@yopmail.com"), ["8(921)324-26-46"]]}
#     with open(os.path.join(getPath(), 'data.json'), 'w', encoding='utf-8') as outfile:
#         json.dump(data, outfile, ensure_ascii=False)

with psycopg2.connect(database="Homework_0", user="postgres", password="Shambala") as conn:
    with conn.cursor() as cur:
        DelTable()
        CreateDataBase()
        addClient()
        addManualClient()
        selectTable()
conn.close()