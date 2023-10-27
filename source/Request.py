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
    con = psycopg2.connect(
        user = 'postgres',
        password = '199811',
        host = '127.0.0.1',
        port = '5432',
        database = 'pokedex'  
    )
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
    con = psycopg2.connect(
        user = 'postgres',
        password = '199811',
        host = '127.0.0.1',
        port = '5432',
        database = 'pokedex'
    )
    getting_moves = requests.get('https://pogoapi.net/api/v1/current_pokemon_moves.json')
    getting_stats = requests.get('https://pogoapi.net/api/v1/pokemon_stats.json')
    getting_types = requests.get('https://pogoapi.net/api/v1/pokemon_types.json')
    data_moves = getting_moves.json()
    data_stats = getting_stats.json()
    data_types = getting_types.json()


    type_map = {}
    for type_data in data_types:
        if type_data['form'] == 'Normal':
            type_map[type_data['pokemon_name']] = type_data['type']

    cursor = con.cursor()

    for stats_data in data_stats:
        if stats_data['form'] == 'Normal':
            pokemon_name = stats_data['pokemon_name']
            type = type_map.get(pokemon_name, None)
            if type:
                atk, hp, defense = stats_data['atk'], stats_data['hp'], stats_data['def']
                dexnum = stats_data['dex']
                pokename = stats_data['pokemon_name']

                if len(type) == 1:
                    query = """INSERT INTO pokemon (dexnum, pokename, poketype1, pokeatk, pokehp, pokedef) VALUES (%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(query, (dexnum, pokename, type[0], atk, hp, defense))
                else:
                    # El Pokémon tiene dos tipos
                    query = """INSERT INTO pokemon (dexnum, pokename, poketype1, poketype2, pokeatk, pokehp, pokedef) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(query, (dexnum, pokename, type[0], type[1], atk, hp, defense))

    con.commit()
    print('Se han agregado los valores correctamente.')
    con.close()









    # for n in data_stats:
    #     if n['form'] == 'Normal':
    #         for i in data_moves:
    #             if i['form'] == 'Normal' and i['pokemon_name'] == n['pokemon_name']:
    #                 for k in data_types:
    #                     if k['form'] == 'Normal' and k['pokemon_name'] == i['pokemon_name']:
    #                         if len(n['type']) == 1:
    #                             query = """INSERT INTO pokemon (dexnum, pokename, poketype1, pokeatk, pokehp, pokedef) VALUES (%s,%s,%s,%s,%s,%s)"""
    #                         else:
    #                             query = """INSERT INTO pokemon (dexnum, pokename, poketype1, poketype2, pokeatk, pokehp, pokedef) VALUES (%s,%s,%s,%s,%s,%s,%s)"""