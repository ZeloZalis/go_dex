import psycopg2
from decouple import config
from lib.GET import call_db

def table_check():
    try:
        con = call_db()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM pokemon')
        value = cursor.fetchone()
        if type(value) == tuple:
            print('\n------------------------------')
            print('La base de datos está cargada.')
            print('------------------------------')
        else:
            print('\n----------------------------')
            print('La base de datos está vacía.')
            print('----------------------------')
        con.close()
    except Exception as e:
        print(f'Error {e}')

def pokemon_show():
    try:
        con = call_db()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM pokemon')
        pokemon_list = cursor.fetchall()
        for n in pokemon_list:
            print(f'Num {n[1]}: {n[2]}')
        con.close()
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')

def pokemon_search():

    pass

def moves_search():

    pass

def fast_moves_show():
    try:
        con = call_db()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM fast_moves')
        pokemon_list = cursor.fetchall()
        for n in pokemon_list:
            print(f"{n[1]}: {n[2]} type.")
        con.close()
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')

def charged_moves_show():
    con = call_db()
    cursor = con.cursor()
    try:
        con = call_db()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM charge_moves')
        pokemon_list = cursor.fetchall()
        for n in pokemon_list:
            print(f"{n[1]}: {n[2]} type.")
        con.close()
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')

def reset_tables():
    try:
        con = call_db()
        tables = [
            'pokemon',
            'fast_moves',
            'charge_moves'
        ]
        cursor = con.cursor()
        for n in tables:
            cursor.execute(f"TRUNCATE {n} RESTART IDENTITY CASCADE")
        con.commit()
        print('\n--------------------------------------')
        print('Todas las tablas han sido reiniciadas.')
        print('--------------------------------------')
        con.close()
    except Exception as e:
        print(f'Error: {e}')