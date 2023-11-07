from lib.GET import *
from lib.functions import *

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

while True:
    for n in options:
        print(n)
    select = int(input(''))