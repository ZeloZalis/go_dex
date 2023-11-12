from lib.GET import initialization
from lib.functions import *

class Option:
    def __init__(self):
        self.answer = '1'
answer = Option()

options = [
    '\nBienvenido al menú interactivo de la Pokédex GO, ¿qué desea realizar?',
    '1. Revisar el estado de las tablas.',
    '2. Mostrar la lista de Pokémon.',
    '3. Buscar un Pokémon.',
    '4. Buscar un ataque rápido/cargado.',
    '5. Ver la lista de ataques rápidos.',
    '6. Ver la lista de ataques cargados.',
    '7. Cargar las tablas de la base de datos.',
    '8. Resetear las tablas de la base de datos.'
]

while answer.answer != '0':
    def keep_going():
        option = input('\n¿Desea volver al menú?\n(Y/N)\n')
        option.lower()
        try: 
            if option == 'n':
                answer.answer = '0'
        except Exception as e:
            print(f'Error: {e}')

    for n in options:
        print(n)
    select = input('')
    if select == '1': #Revisar el estado de la tabla
        table_check()
        keep_going()
    elif select == '2': #Mostrar la lista de Pokémon
        pokemon_show()
        keep_going()
    elif select == '3': #Buscar un Pokémon
        pokemon_search()
        keep_going()
    elif select == '4': #Buscar un ataque cargado/rápido

        pass
    elif select == '5': #Ver la lista de ataques rápidos
        fast_moves_show()
        keep_going()
    elif select == '6': #Ver la lista de ataques cargados
        charged_moves_show()
        keep_going()
    elif select == '7': #Cargar la base de datos
        initialization()
        keep_going()
    elif select == '8': #Vaciar la base de datos
        reset_tables()
        keep_going()
    else:
        print('\n----------------')
        print('Opción inválida.')
        print('----------------')