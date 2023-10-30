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


    # type_map = {}
    # for type_data in data_types:
    #     if type_data['form'] == 'Normal':
    #         type_map[type_data['pokemon_name']] = type_data['type']

    # cursor = con.cursor()

    # for stats_data in data_stats:
    #     if stats_data['form'] == 'Normal':
    #         pokemon_name = stats_data['pokemon_name']
    #         type = type_map.get(pokemon_name, None)
    #         if type:
    #             atk, hp, defense = stats_data['atk'], stats_data['hp'], stats_data['def']
    #             dexnum = stats_data['dex']
    #             pokename = stats_data['pokemon_name']

    #             if len(type) == 1:
    #                 query = """INSERT INTO pokemon (dexnum, pokename, poketype1, pokeatk, pokehp, pokedef) VALUES (%s,%s,%s,%s,%s,%s)"""
    #                 cursor.execute(query, (dexnum, pokename, type[0], atk, hp, defense))
    #             else:
    #                 # El Pokémon tiene dos tipos
    #                 query = """INSERT INTO pokemon (dexnum, pokename, poketype1, poketype2, pokeatk, pokehp, pokedef) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    #                 cursor.execute(query, (dexnum, pokename, type[0], type[1], atk, hp, defense))
    # con.commit()
    # print('Se han agregado los valores correctamente.')
    # con.close()


    for n in data_stats: #buco el mimo pokemon en las 3 apis
        if n['form'] == 'Normal': # Si no es un pokémon de evento:
            for i in data_moves:
                if i['form'] == 'Normal' and i['pokemon_name'] == n['pokemon_name']:
                    for k in data_types:
                        if k['form'] == 'Normal' and k['pokemon_name'] == i['pokemon_name']: #ete e la ultima api
                            if len(k['type']) == 1:
                                query = """INSERT INTO pokemon (dexnum, pokename, poketype1, pokeatk, pokehp, pokedef) VALUES (%s, %s, %s, %s, %s, %s)"""
                                record_insert = (n['pokemon_id'], n['pokemon_name'], k['type'], n['base_attack'], n['base_stamina'], n['base_defense']) 
                                cursor.execute(query, record_insert)
                            else:
                                query = """INSERT INTO pokemon (dexnum, pokename, poketype1, poketype2, pokeatk, pokehp, pokedef) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                                record_insert = (n['pokemon_id'], n['pokemon_name'], k['type'], k['type'][1], n['base_attack'], n['base_stamina'], n['base_defense'])
                                cursor.execute(query, record_insert)
                        for h in i['fast_moves']:
                            query22 = """SELECT * FROM pokemon WHERE pokename = (%s)"""
                            insert_query12 = (n['pokemon_name'])
                            cursor.execute(query22, insert_query12)
                            pokemon = cursor.fetchone()
                            print(pokemon)
                            query_fast = """INSERT INTO pokemon_fast_attacks (id_pokemon, id_fast_attack) VALUES (%s, %s)"""
                            # cursor.execute("INSERT INTO pokemon_fast_attacks (id_pokemon, id_fast_attack) VALUES (%s, %s)", (pokemon_idpokemon, fast_moves_id))
    con.commit()
    con.close()
pokemon_upload()