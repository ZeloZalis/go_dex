import psycopg2
from decouple import config
from lib.GET import call_db
import string

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
    con = call_db()
    cursor = con.cursor()
    try:
        look_for = input('\nIngresa el nombre del Pokémon:\n')
        cursor.execute(f"SELECT * FROM pokemon WHERE pokename = '{look_for.capitalize()}'")
        found = cursor.fetchone()
        cursor.execute(f"SELECT * FROM pokemon_fast_attacks WHERE id_pokemon = {found[0]}")
        fast_moves = cursor.fetchall()
        fast_list = []
        cursor.execute(f"SELECT * FROM pokemon_charge_attacks WHERE id_pokemon = {found[0]}")
        charged_moves = cursor.fetchall()
        charged_list = []
        for n in fast_moves:
            cursor.execute(f"SELECT * FROM fast_moves WHERE id = {n[1]}")
            fattack = cursor.fetchone()
            fast_list.append(fattack[1])
        for n in charged_moves:
            cursor.execute(f"SELECT * FROM charge_moves WHERE id = {n[1]}")
            cattack = cursor.fetchone()
            charged_list.append(cattack[1])
        if found[4] != None:
            print('\n------------------------')
            print(f"Nombre: {found[2]}\nTipos: {found[3]}/{found[4]}\nATK: {found[5]}\nHP: {found[6]}\nDEF: {found[7]}")
            print(f"Ataques rápidos: {fast_list}")
            print(f"Ataques cargados: {charged_list}")
            print('------------------------')
        else:
            print('\n------------------------')
            print(f"Nombre: {found[2]}\nTipo: {found[3]}\nATK: {found[5]}\nHP: {found[6]}\nDEF: {found[7]}")
            print('------------------------')
    except Exception as e:
        print(f'Error: {e}')
    con.close()

def moves_search():
    con = call_db()
    cursor = con.cursor()
    try:
        look_for = input('\nIngresa el nombre del ataque rápido:\n')
        cursor.execute(f"SELECT * FROM fast_moves WHERE name = '{string.capwords(look_for)}'")
        found = cursor.fetchone()
        if found is None:
            cursor.execute(f"SELECT * FROM charge_moves WHERE name = '{string.capwords(look_for)}'")
            charged_info = cursor.fetchone()
            print("\nAtaque Cargado.")
            print("-----------------")
            print(f"Nombre: {charged_info[1]}\nTipo: {charged_info[2]}\nDaño: {charged_info[3]}\nEnergía: {charged_info[4]}")
            print("-----------------")
        else:
            print("\nAtaque rápido.")
            print("-----------------")
            print(f"Nombre: {found[1]}\nTipo: {found[2]}\nDaño: {found[3]}\nEnergía: {found[4]}\nVelocidad: {found[5]}")
            print("-----------------")
    except Exception as e:
        print(f'Error: {e}')
    con.close()

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