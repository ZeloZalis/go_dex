from lib.GET import initialization
from lib.functions import *

class Option:
    def __init__(self):
        self.answer = '1'
answer = Option()

options = [
    '\nWelcome to the interactive menu of the Pokédex GO, what do you want to do?',
    '1. Check the status of the tables.',
    '2. Show the list of Pokémon.',
    '3. Search for a Pokémon.',
    '4. Show the list of Fast moves.',
    '5. Show the list of Charged moves.',
    '6. Search for a Fast/Charged move.',
    '7. Load the database tables.',
    '8. Reset the database tables.',
    '9. Exit.'
]

def Table_check():
    con = call_db()
    try:
        tables = [
            'pokemon',
            'fast_moves',
            'charged_moves',
            'pokemon_fast_moves',
            'pokemon_charged_moves'
        ]
        cursor = con.cursor()
        for n in tables:
            cursor.execute(f"SELECT EXISTS (SELECT * FROM information_schema.tables WHERE table_name = '{n}')")
            value = cursor.fetchone()[0]
            if value == False:
                print('\n-------------------------------------------------------')
                print("The tables necessary to run this program doesn't exist.")
                print("-------------------------------------------------------")
                response = input("\nDo you want to create them?\n(Wouldn't be able to continue if not)\n(Y/N)\n").lower()
                if response == 'y':
                    Create_table()
                elif response == 'n':
                    return answer.answer == '0'
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        con.close()

while answer.answer != '0':
    def Keep_going():
        option = input('\nReturn to menu.\n(Y/N)\n')
        option.lower()
        try: 
            if option == 'n':
                answer.answer = '0'
        except Exception as e:
            print(f'Error: {e}')
    
    checking_tables = Table_check()
    if checking_tables == False:
        break
    for n in options:
        print(n)
    select = input('')
    if select == '1':
        Table_status()
        Keep_going()
    elif select == '2':
        Show_pokemon_list()
        Keep_going()
    elif select == '3':
        Search_pokemon()
        Keep_going()
    elif select == '4':
        Show_fast_moves_list()
        Keep_going()
    elif select == '5':
        Show_charged_moves_list()
        Keep_going()
    elif select == '6':
        Search_moves()
        Keep_going()
    elif select == '7':
        initialization()
        Keep_going()
    elif select == '8':
        Reset_tables()
        Keep_going()
    elif select == '9':
        print('\n---------')
        print('Good bye.')
        print('---------')
        break
    else:
        print('\n---------------')
        print('Invalid option.')
        print('---------------')