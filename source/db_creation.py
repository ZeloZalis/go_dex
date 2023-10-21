import psycopg2

con = psycopg2.connect(
    database = "pokedex_go",
    user = 'postgres',
    password = '199811'
)
con.autocommit = True

cursor = con.cursor()
cursor.execute('''CREATE database mydb''')
print('Database has been created.')
con.close()