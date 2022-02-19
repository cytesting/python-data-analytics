"""
Module to connect to database
"""

import subprocess
from decouple import basicConfig

# TODO: import dfs from pandas_process file
# TODO: use logging and python-decouple

from sqlalchemy import create_engine

engine = create_engine(config('DATABASE_URL'))

def create_table():
    """ Crear las tablas """
    subprocess.run(['psql', '-d', 'leonardo', '-f', 'postres.sql'], check=True)

def populate_db():
    """ Insertar datos """
    #df = pd.DataFrame({'nombre' : ['Jobbto', 'Karlek'], 'origen': ['USA', 'Suecia']})
    #df.to_sql('postres', con=engine, if_exists='append', index=False)

def check_db():
    """ Comprobar y testear """
    print(engine.execute("SELECT nombre, origen FROM postres").fetchall())
