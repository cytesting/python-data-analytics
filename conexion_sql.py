"""
Module to connect to database
"""
import logging
import subprocess

from decouple import config

from sqlalchemy import create_engine

from procesos_pandas import parte_uno_challenge, parte_dos_challenge, parte_tres_challenge

engine = create_engine(config('DATABASE_URL'))

DATABASE_NAME = config('DATABASE_NAME')

def create_table():
    """ Crear las tablas """
    subprocess.run(['psql', '-d', DATABASE_NAME, '-f', 'db_script.sql'], check=True)

def populate_db():
    """ Insertar datos """
    datos1 = parte_uno_challenge()
    datos2 = parte_dos_challenge()
    datos3 = parte_tres_challenge()
    try:
        datos1.to_sql('tabla_unificada', con=engine, if_exists='append', index=False)
        datos2.to_sql('registros_categoria', con=engine, if_exists='append', index=False)
        datos3.to_sql('registros_cine', con=engine, if_exists='append', index=False)
        logging.info('All data saved to db...')
    except:
        logging.error('Could not connect to database')

def check_db():
    """ Comprobar y testear """
    print(engine.execute("SELECT * FROM registros_categoria").fetchall())

check_db()
