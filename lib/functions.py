import psycopg2
from decouple import config
from GET import call_db

def table_check():
    
    pass

def pokemon_show():
    con = call_db()
    cursor = con.cursor()
    try:
        cursor.execute('SELECT * FROM pokemon')
        pokemon_list = cursor.fetchall()
        for n in pokemon_list:
            print(f'Num {n[1]}: {n[2]}')
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')
    con.close()

def pokemon_search():

    pass

def moves_search():

    pass

def fast_moves_show():
    con = call_db()
    cursor = con.cursor()
    try:
        cursor.execute('SELECT * FROM fast_moves')
        pokemon_list = cursor.fetchall()
        for n in pokemon_list:
            print(f"{n[1]}: {n[2]} type.")
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')
    con.close()

def charged_moves_show():
    con = call_db()
    cursor = con.cursor()
    try:
        cursor.execute('SELECT * FROM charge_moves')
        pokemon_list = cursor.fetchall()
        for n in pokemon_list:
            print(f"{n[1]}: {n[2]} type.")
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')
    con.close()

def reset_tables():
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
    print('Todas las tablas han sido reiniciadas.')
    con.close()