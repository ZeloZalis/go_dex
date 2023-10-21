import requests
import json
import psycopg2

getting = requests.get('https://pogoapi.net/api/v1/fast_moves.json')
data = getting.json()
# print(data)
# print(type(data))
# print(type(data[0]))

#De esta forma agarro un dato normal, se puede hacer ['form'], ['pokemon_id'], ['pokemon_name'], ['type'] éste último devuelve una lista
# name = ['name']
# type = ['type']
# power = ['power']
# energy = ['energy_delta']
# speed = ['duration']

# print(len(data))
# for datos in data:
#     print(datos['name'])

#Función para cargar a la tabla los ataques rápidos
def fast_move_upload():
    con = psycopg2.connect(
        user = 'postgres',
        password = '199811',
        host = '127.0.0.1',
        port = '5432',
        database = 'pokedex'
    )
    cursor = con.cursor()
    insert_query = """ INSERT INTO fast_moves (name, type, power, energy, speed) VALUES (%s,%s,%s,%s,%s)"""
    for n in data:
        record_to_insert = (n['name'], n['type'], n['power'], n['energy_delta'], n['duration'])
        cursor.execute(insert_query, record_to_insert)
    con.commit()
    print('Se han agregado los valores correctamente.')
    con.close()
fast_move_upload()