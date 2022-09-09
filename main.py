import psycopg2
from psycopg2._psycopg import cursor

def DelTable():
    pass


def CreateTable():
    cur.execute("""
            CREATE TABLE IF NOT EXISTS course(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40),
                lastname VARCHAR(40),
                email VARCHAR(40)
            );
            """)




with psycopg2.connect(database="Homework_0", user="postgres", password="Shambala") as conn:
    with conn.cursor() as cur:
        CreateTable()
conn.close()