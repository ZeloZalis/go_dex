import requests
import json
import psycopg2
from decouple import config

def call_db():
    con = psycopg2.connect(
        user = config('SQL_user'),
        password = config('SQL_password'),
        host = config('SQL_host'),
        port = config('SQL_port'),
        database = config('SQL_database')
    )
    return con

def Create_table():
    con = call_db()
    try:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (id SERIAL PRIMARY KEY, dexnum INTEGER UNIQUE NOT NULL, name TEXT NOT NULL, type1 TEXT NOT NULL, type2 TEXT, atk INTEGER NOT NULL, hp INTEGER NOT NULL, def INTEGER NOT NULL)""")
        con.commit()
        print("Tabla pokemon creada.")
        cursor.execute("""CREATE TABLE IF NOT EXISTS fast_moves (id SERIAL PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, power INTEGER NOT NULL, energy INTEGER NOT NULL, speed INTEGER NOT NULL)""")
        con.commit()
        print("Tabla fast_moves creada.")
        cursor.execute("""CREATE TABLE IF NOT EXISTS charged_moves (id SERIAL PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, power INTEGER NOT NULL, energy INTEGER NOT NULL)""")
        con.commit()
        print("Tabla charged_moves creada.")
        cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon_fast_moves (id_pokemon INT NOT NULL, id_fast_moves INT NOT NULL, PRIMARY KEY (id_pokemon, id_fast_moves), FOREIGN KEY (id_pokemon) REFERENCES pokemon (id), FOREIGN KEY (id_fast_moves) REFERENCES fast_moves (id))""")
        con.commit()
        print("Tabla pokemon_fast_moves creada.")
        cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon_charged_moves (id_pokemon INT NOT NULL, id_charged_moves INT NOT NULL, PRIMARY KEY (id_pokemon, id_charged_moves), FOREIGN KEY (id_pokemon) REFERENCES pokemon (id), FOREIGN KEY (id_charged_moves) REFERENCES charged_moves (id))""")
        con.commit()
        print("Tabla pokemon_charged_moves creada.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

def fast_moves_upload():
    con = call_db()
    try:
        getting = requests.get(config('API_fast_moves'))
        data = getting.json()
        cursor = con.cursor()
        insert_query = """ INSERT INTO fast_moves (name, type, power, energy, speed) VALUES (%s,%s,%s,%s,%s)"""
        for n in data:
            record_to_insert = (n['name'], n['type'], n['power'], n['energy_delta'], n['duration'])
            cursor.execute(insert_query, record_to_insert)
            print(f"Se ha cargado {n['name']} a la base de datos.")
        con.commit()
        print('\n---------------------------------------------------------------------------')
        print('Se han agregado todos los ataques rápidos a la base de datos correctamente.')
        print('---------------------------------------------------------------------------\n')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

def charged_moves_upload():
    con = call_db()
    try:
        getting = requests.get(config('API_charged_moves'))
        data = getting.json()
        cursor = con.cursor()
        insert_query = """INSERT INTO charged_moves (name, type, power, energy) VALUES (%s,%s,%s,%s)"""
        for n in data:
            record_to_insert = (n['name'], n['type'], n['power'], n['energy_delta'])
            cursor.execute(insert_query, record_to_insert)
            print(f"Se ha cargado {n['name']} a la base de datos.")
        con.commit()
        print('\n----------------------------------------------------------------------------')
        print('Se han agregado todos los ataques cargados a la base de datos correctamente.')
        print('----------------------------------------------------------------------------\n')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

def pokemon_upload():
    con = call_db()
    try:
        cursor = con.cursor()
        getting_stats = requests.get(config('API_stats'))
        getting_types = requests.get(config('API_types'))
        data_stats = getting_stats.json()
        data_types = getting_types.json()
        for n in data_stats:
            if n['form'] == 'Normal':
                for k in data_types:
                    if k['form'] == 'Normal' and k['pokemon_name'] == n['pokemon_name']:
                        if len(k['type']) == 1:
                            query = """INSERT INTO pokemon (dexnum, name, type1, atk, hp, def) VALUES (%s, %s, %s, %s, %s, %s)"""
                            record_insert = (n['pokemon_id'], n['pokemon_name'], k['type'][0], n['base_attack'], n['base_stamina'], n['base_defense']) 
                            cursor.execute(query, record_insert)
                            print(f"{n['pokemon_name']} ha sido cargado correctamente.")
                        elif len(k['type']) == 2:
                            query = """INSERT INTO pokemon (dexnum, name, type1, type2, atk, hp, def) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                            record_insert = (n['pokemon_id'], n['pokemon_name'], k['type'][0], k['type'][1], n['base_attack'], n['base_stamina'], n['base_defense'])
                            cursor.execute(query, record_insert)
                            print(f"{n['pokemon_name']} ha sido cargado correctamente.")
        con.commit()
        print('\n-------------------------------------------------------------------')
        print('Se han agregado todos los Pokémon a la base de datos correctamente.')
        print('-------------------------------------------------------------------\n')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

def fk_table_upload_fast_moves():
    con = call_db()
    try:
        cursor = con.cursor()
        getting_moves = requests.get(config('API_Pokemon_Moves'))
        data_moves = getting_moves.json()
        cursor.execute("SELECT * FROM pokemon")
        pokemon_list = cursor.fetchall()
        cursor.execute("SELECT * FROM fast_moves")
        fast_attack_list = cursor.fetchall()
        for n in pokemon_list:
            for k in data_moves:
                if k['form'] == 'Normal' and k['pokemon_name'] == n[2]:
                    for i in k['fast_moves']:
                        for m in fast_attack_list:
                            if i == m[1]:
                                cursor.execute(f"INSERT INTO pokemon_fast_moves (id_pokemon, id_fast_moves) VALUES ({n[0]}, {m[0]}) ON CONFLICT (id_pokemon, id_fast_moves) DO NOTHING")
                                print(f"Se ha cargado el ataque {i} en {n[2]}.")
        con.commit()
        print('\n------------------------------------------------------------------')
        print('Se ha vinculado los ataques rápidos con los Pokémon correctamente.')
        print('------------------------------------------------------------------\n')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

def fk_table_upload_charged_moves():
    con = call_db()
    try:
        cursor = con.cursor()
        getting_moves = requests.get(config('API_Pokemon_Moves'))
        data_moves = getting_moves.json()
        cursor.execute("SELECT * FROM pokemon")
        pokemon_list = cursor.fetchall()
        cursor.execute("SELECT * FROM charged_moves")
        charged_moves_list = cursor.fetchall()
        for n in pokemon_list:
            for k in data_moves:
                if k['form'] == 'Normal' and k['pokemon_name'] == n[2]:
                    for i in k['charged_moves']:
                        for m in charged_moves_list:
                            if i == m[1]:
                                cursor.execute(f"INSERT INTO pokemon_charged_moves (id_pokemon, id_charged_moves) VALUES ({n[0]}, {m[0]}) ON CONFLICT (id_pokemon, id_charged_moves) DO NOTHING")
                                print(f"Se ha cargado el ataque {i} en {n[2]}.")
        con.commit()
        print('\n-------------------------------------------------------------------')
        print('Se ha vinculado los ataques cargados con los Pokémon correctamente.')
        print('-------------------------------------------------------------------\n')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

def initialization():
    call_db()
    print('Iniciando...\n')
    fast_moves_upload()
    charged_moves_upload()
    pokemon_upload()
    fk_table_upload_fast_moves()
    fk_table_upload_charged_moves()
    print('.')
    print('..')
    print('...\n')
    print('----------------------------------------------------------------')
    print('Se han cargado todos los datos a la base de datos correctamente.')
    print('----------------------------------------------------------------')
