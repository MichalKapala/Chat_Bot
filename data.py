import sqlite3

connection = sqlite3.connect('Pytania.db')
c = connection.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS przywitanie(poczatek TEXT, pytanie TEXT, odpowiedz TEXT)')

def dodawanie(pytanie, odpowiedz):
    id=''
    for i in pytanie:
        if i != ' ':
            id += i
        else: break;

    c.execute("INSERT INTO przywitanie (poczatek, pytanie, odpowiedz)  VALUES (?, ?, ? )", (id, pytanie, odpowiedz))
    connection.commit()

pytanie = ''
odpowiedz = ''

while pytanie != 'Koniec':
    print("Dodaj pytanie:  ", end='')
    pytanie = input()
    print("Dodaj odzpowiedz:  ", end='')
    odpowiedz = input()
    dodawanie(pytanie, odpowiedz)


connection.close()
c.close()