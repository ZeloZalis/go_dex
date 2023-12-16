# M.F.S.P
#### My First Smol Project

## Information
As the title says, this is a smol project where I put into practice SQL and GET data from APIs.
Its free to use for anyone who found this usefull, but its a very simple script.

## Requeriments
- [pgAdmin4](https://www.pgadmin.org/download/ "pgAdmin4")
- [PostgreSQL](https://www.postgresql.org/download/ "PostgreSQL")
- [Python 3.11+](https://www.python.org/downloads/ "Python 3.11+")

## Objetives
- Practice SQL
- Practice GET data from APIs
- Practice Environment Variables

## API Used
[PoGo API](https://pogoapi.net/documentation/ "PoGo API")

## How to Use
After having everything installed, you need to follow a couple of steps before making this script works well.
1. First at all, you need to open your pgAdmin4 and setup your user (it will give you the next information: User, Password, Host, Port).
2. Install the packages contained in [requirements.txt](https://github.com/ZeloZalis/go_dex/blob/main/requirements.txt).
3. Now you need to create your database, I would recommend, if you are using this, call it "pokedex" or something like that.

![](https://i.imgur.com/YqMfpDZ.png)

3. After this, you would need to open the script [GET.py](https://github.com/ZeloZalis/go_dex/blob/main/lib/GET.py "GET.py") in any IDE of your preference.
4. Now you will need to change the information in the call_db() function, replace the next values with the information pgAdmin4 gave you before.

![](https://i.imgur.com/YeIB9wv.png)

Make sure the data is in str, for example:

![](https://i.imgur.com/bYzMyBz.png)

After those steps you should be able to execute the script, so you will need to go to [app.py](https://github.com/ZeloZalis/go_dex/blob/main/app.py) and run it, automatically it will connect to your DB and check if you have the tables created, if not, it will create it and then you can upload the information of each pokémon using the options in the menu.
