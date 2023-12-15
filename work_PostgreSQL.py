import psycopg2
from pprint import pprint


def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        lastname VARCHAR(40),
        email VARCHAR(150)
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Phone(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    return


def delete_db(cur):
    cur.execute("""
        DROP TABLE Clients, Phone CASCADE;
        """)


def add_phone(cur, client_id, tel):
    cur.execute("""
        INSERT INTO phone(number, client_id)
        VALUES (%s, %s)
        """, (tel, client_id))
    return client_id


def add_client(cur, name=None, lastname=None, email=None, tel=None):
    cur.execute("""
        INSERT INTO clients(name, lastname, email)
        VALUES (%s, %s, %s)
        """, (name, lastname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if tel is None:
        return id
    else:
        add_phone(cur, id, tel)
        return id


def update_client(cur, id, name=None, surname=None, email=None):
    cur.execute("""
        SELECT * from clients
        WHERE id = %s
        """, (id, ))
    info = cur.fetchone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET name = %s, lastname = %s, email =%s 
        where id = %s
        """, (name, surname, email, id))
    return id


def delete_phone(cur, number):
    cur.execute("""
        DELETE FROM phone
        WHERE number = %s
        """, (number, ))
    return number


def delete_client(cur, id):
    cur.execute("""
        DELETE FROM phone
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE FROM clients 
        WHERE id = %s
       """, (id,))
    return id


def find_client(cur, name=None, surname=None, email=None, tel=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number like %s
            """, (name, surname, email, tel))
    return cur.fetchall()



with psycopg2.connect(database="client_db", user="postgres",
                      password="qwerty") as conn:
    with conn.cursor() as curs:

        delete_db(curs)

        create_db(curs)

        add_client(curs, "Александр", "Иванов", "ai@mail.ru")
        add_client(curs, "Ольга", "Петрова", "op@mail.ru", 79694598299)
        add_client(curs, "Алексей", "Смирнов", "as@mail.ru", 79197003050)
        add_client(curs, "Андрей", "Семёнов", "as@mail.ru", 79197430019)
        add_client(curs, "Мария", "Шварц", "msh@mail.ru", 79069530532)
        add_client(curs, "Алёна", "Иванова", "ai@mail.ru", 79253501033)
        add_client(curs, "Максим", "Дуров", "ad@mail.ru")

        print("Данные в таблицах")
        curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone p ON c.id = p.client_id
            ORDER by c.id
            """)
        pprint(curs.fetchall())

        add_phone(curs, 2, 79264587644)
        add_phone(curs, 1, 79253535353)

        curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone p ON c.id = p.client_id
            ORDER by c.id
            """)
        pprint(curs.fetchall())

        update_client(curs, 4, "Тима", None, 'tim@mail.ru')

        delete_phone(curs, '79253535353')
        curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phone p ON c.id = p.client_id
            ORDER by c.id
            """)
        pprint(curs.fetchall())

        delete_client(curs, 2)
        curs.execute("""
                        SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                        LEFT JOIN phone p ON c.id = p.client_id
                        ORDER by c.id
                        """)
        pprint(curs.fetchall())

        pprint(find_client(curs, 'Максим'))

        pprint(find_client(curs, None, None, 'as@mail.ru'))

        pprint(find_client(curs, 'Мария', 'Шварц', 'msh@mail.ru'))

        pprint(find_client(curs, 'Алексей', 'Смирнов', 'as@mail.ru', '79197003050'))

        pprint(find_client(curs, None, None, None, '79253501033'))