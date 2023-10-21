import psycopg2

try:
    connection = psycopg2.connect(
        user = 'postgres',
        password = '199811',
        host = '127.0.0.1',
        port = '5432',
        database = 'pokedex'
    )
    print('Connection succesful.')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM pokemon')
    pokemon = cursor.fetchall()
    for pokemons in pokemon:
        print(pokemons)
except Exception as e:
    print(e)
finally:
    print('The connection has ended.')