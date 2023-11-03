import requests
import json
import psycopg2

def call_db():
    con = psycopg2.connect(
        user = 'postgres',
        password = '199811',
        host = '127.0.0.1',
        port = '5432',
        database = 'pokedex'
    )
    return con

#Función para cargar a la tabla los ataques rápidos
def fast_move_upload():
    con = call_db()
    getting = requests.get('https://pogoapi.net/api/v1/fast_moves.json')
    data = getting.json()
    cursor = con.cursor()
    insert_query = """ INSERT INTO fast_moves (name, type, power, energy, speed) VALUES (%s,%s,%s,%s,%s)"""
    for n in data:
        record_to_insert = (n['name'], n['type'], n['power'], n['energy_delta'], n['duration'])
        cursor.execute(insert_query, record_to_insert)
    con.commit()
    print('Se han agregado los valores correctamente.')
    con.close()

def charge_move_upload():
    con = call_db()
    getting = requests.get('https://pogoapi.net/api/v1/charged_moves.json')
    data = getting.json()
    cursor = con.cursor()
    insert_query = """INSERT INTO charge_moves (name, type, power, energy) VALUES (%s,%s,%s,%s)"""
    for n in data:
        record_to_insert = (n['name'], n['type'], n['power'], n['energy_delta'])
        cursor.execute(insert_query, record_to_insert)
    con.commit()
    print('Se han agregado los valores correctamente.')
    con.close()

def pokemon_upload():
    con = call_db()
    cursor = con.cursor()
    getting_moves = requests.get('https://pogoapi.net/api/v1/current_pokemon_moves.json')
    getting_stats = requests.get('https://pogoapi.net/api/v1/pokemon_stats.json')
    getting_types = requests.get('https://pogoapi.net/api/v1/pokemon_types.json')
    data_moves = getting_moves.json()
    data_stats = getting_stats.json()
    data_types = getting_types.json()
    for n in data_stats:
        if n['form'] == 'Normal':
            for i in data_moves:
                if i['form'] == 'Normal' and i['pokemon_name'] == n['pokemon_name']:
                    for k in data_types:
                        if k['form'] == 'Normal' and k['pokemon_name'] == i['pokemon_name']:
                            if len(k['type']) == 1:
                                query = """INSERT INTO pokemon (dexnum, pokename, poketype1, pokeatk, pokehp, pokedef) VALUES (%s, %s, %s, %s, %s, %s)"""
                                record_insert = (n['pokemon_id'], n['pokemon_name'], k['type'][0], n['base_attack'], n['base_stamina'], n['base_defense']) 
                                cursor.execute(query, record_insert)
                                print('Se ha cargado el pokémon con 1 tipo.')
                                con.commit()
                            elif len(k['type']) == 2:
                                query = """INSERT INTO pokemon (dexnum, pokename, poketype1, poketype2, pokeatk, pokehp, pokedef) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                                record_insert = (n['pokemon_id'], n['pokemon_name'], k['type'][0], k['type'][1], n['base_attack'], n['base_stamina'], n['base_defense'])
                                cursor.execute(query, record_insert)
                                print('Se ha cargado el pokémon con 2 tipos.')
                                con.commit()
    con.close()

def fk_table_upload_fast_attack():
    con = call_db()
    cursor = con.cursor()
    getting_moves = requests.get('https://pogoapi.net/api/v1/current_pokemon_moves.json')
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
                            cursor.execute(f"INSERT INTO pokemon_fast_attacks (id_pokemon, id_fast_attack) VALUES ({n[0]}, {m[0]})")
                            print(f"Se ha cargado el ataque {i} en {n[2]}")
                            con.commit()
    con.close()

def fk_table_upload_charge_attack():
    con = call_db()
    cursor = con.cursor()
    getting_moves = requests.get('https://pogoapi.net/api/v1/current_pokemon_moves.json')
    data_moves = getting_moves.json()
    cursor.execute("SELECT * FROM pokemon")
    pokemon_list = cursor.fetchall()
    cursor.execute("SELECT * FROM charge_moves")
    charge_attack_list = cursor.fetchall()
    for n in pokemon_list:
        for k in data_moves:
            if k['form'] == 'Normal' and k['pokemon_name'] == n[2]:
                for i in k['charged_moves']:
                    for m in charge_attack_list:
                        if i == m[1]:
                            cursor.execute(f"INSERT INTO pokemon_charge_attacks (id_pokemon, id_charge_attack) VALUES ({n[0]}, {m[0]})")
                            print(f"Se ha cargado el ataque {i} en {n[2]}")
                            con.commit()
    con.close()