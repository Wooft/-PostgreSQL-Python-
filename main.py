import json
import os
import pathlib
import psycopg2


def DelTable():
    cur.execute("""
    DROP TABLE NumPhone;
    DROP TABLE client;
    """)

def getPath():
    path  = pathlib.Path.cwd()
    return path
def dataInput():
    client_data = []
    client_data.append(input("Введите имя клиента: "))
    client_data.append(input("Введите фамилию клиента: "))
    client_data.append(input("Введите email клиента: "))
    return client_data
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
def CreateDataBase(): ## Задание №1 Функция, создающая структуру БД (таблицы)
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
        for items in elements[1]:
            addNumber(items, keys)

def addManualClient(): ## Задание 2 Функция, позволяющая добавить нового клиента вручную
    print('Добавление нового клиента')
    listNumbers = []
    clientdata = dataInput()
    cur.execute("""
    INSERT INTO client (name, lastname, email) VALUES (%s, %s, %s) RETURNING id;
    """, (clientdata[0], clientdata[1], clientdata[2])
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

def addNumber(number, client_id): ##Задание 3 Функция, позволяющая добавить номер телефона для клиента по его id
    cur.execute("""
    INSERT INTO NumPhone (PhoneNumber, Client_id) VALUES (%s, %s);
    """, (number, client_id)
                )

def FindPhones(Clien_ID):
    cur.execute("""
            SELECT * from NumPhone WHERE Client_id=%s
        """, (Clien_ID,))
    print(cur.fetchall())
def changeClientData():##Функция, позволяющая изменить данные о клиенте
    print('Изменение данных клиента')
    data = findClient()
    clientdata = dataInput()
    p_number=input("Введите номер телефона клиента: ")
    cur.execute("""
        UPDATE client SET name=%s, lastname=%s, email=%s WHERE id=%s; 
    """, (clientdata[0], clientdata[1], clientdata[2], data[0][0]))
    FindPhones(data[0][0])
    client_id = int(input("Введите ID записи с номером телефона, которую хотите обновить (Первый столбец): "))
    cur.execute("""
        UPDATE NumPhone SET PhoneNumber=%s WHERE id=%s;
    """, (p_number, client_id))

def delPhoneNumber(): ##Функция, позволяющая удалить телефон для существующего клиента
    print('Удаление номера телефона клиента')
    data = findClient()
    FindPhones(data[0][0])
    client_id = int(input("Введите ID записи с номером телефона, которую хотите удалить (Первый столбец): "))
    cur.execute("""
            DELETE FROM NumPhone WHERE id=%s;
            """, (client_id,))

def delClient(): ##Функция, позволяющая удалить существующего клиента
    print('Удаление данных клиента')
    data = findClient()
    print(data)
    answer = input("Вы хотите удалить данные этого клиента? (Да/Нет) ")
    if answer.lower() == 'да':
        cur.execute("""
                    DELETE FROM NumPhone WHERE id=%s;
                    """, (data[0][0],))
        cur.execute("""
                    DELETE FROM client WHERE id=%s;
                    """, (data[0][0], ))
    else:
        pass


def findClient(): ##Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    print('Для того чтобы найти клиента в базе данных, необходимо ввести информацию')
    answer = int(input('Если вы хотите найти клиента по имени, введите 1, если по Фамилии, введите 2, если по email - ведите 3 если по номеру телефона, введите 4: '))
    fdata = input('Введите данные для поиска: ')
    if answer == 1:
        cur.execute("""
                        SELECT id, name, lastname, email FROM client
                        WHERE name=%s
                        """, (fdata,))
    if answer == 2:
        cur.execute("""
                        SELECT id, name, lastname, email FROM client
                        WHERE lastname=%s
                        """, (fdata,))
    if answer == 3:
        cur.execute("""
                        SELECT id, name, lastname, email FROM client
                        WHERE email=%s
                        """, (fdata,))
    if answer == 4:
        cur.execute("""
                        SELECT id, PhoneNumber FROM NumPhone
                        WHERE PhoneNumber=%s
                        """, (fdata,))
        outd = cur.fetchone()
        cur.execute("""
                        SELECT id, name, lastname, email FROM client
                        WHERE id=%s
                        """, (outd[0],))
    out = cur.fetchall()
    return out
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
        DelTable() #Очистка таблиц
        CreateDataBase() #Создание структуры БД
        addClient() #Добавление клиентов из json файла
        addManualClient() #Добавление клиента в ручном режиме
        selectTable() #вывод содержимого таблиц
        print(findClient()) #функция поиска клиента по введенным данным
        changeClientData() #Измененение данных клиента
        selectTable()  # вывод содержимого таблиц
        delPhoneNumber() #Удаление номера телефона
        selectTable()  # вывод содержимого таблиц
        delClient() #Удаление клиента
        selectTable() #вывод содержимого таблиц
conn.close()