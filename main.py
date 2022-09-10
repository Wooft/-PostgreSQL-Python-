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
                PhoneNumber VARCHAR(12),
                Client_id INTEGER NOT NULL REFERENCES client(id)
                );
            """)
def addClient(): ## Функция, позволяющая добавить нового клиента
    data = openClients()
    for keys, elements in data.items():
        name = elements[0]
        lastname = elements[1]
        email = elements[2]
        cur.execute("""
        INSERT INTO client (name, lastname, email) VALUES (%s, %s, %s);
        """, (name, lastname, email)
                    )

def addNumber(number, client_id):
    cur.execute("""
    INSERT INTO NumPhone (PhoneNumber, Client_id) VALUES (%s, %s, %s);
    """, (number, client_id)
                )

def selectTable():
    cur.execute("""
    SELECT * FROM client;
    """)
    print(cur.fetchall())

with psycopg2.connect(database="Homework_0", user="postgres", password="Shambala") as conn:
    with conn.cursor() as cur:
        DelTable()
        CreateDataBase()
        addClient()
        selectTable()
conn.close()