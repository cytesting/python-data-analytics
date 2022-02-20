"""
Module to connect to database
"""
import logging
import subprocess

from decouple import config

import sqlalchemy

from procesos_pandas import datos_pandas

engine = sqlalchemy.create_engine(config('DATABASE_URL'))

DATABASE_NAME = config('DATABASE_NAME')

def crear_tablas():
    """ Crear las tablas """
    subprocess.run(['psql', '-d', DATABASE_NAME, '-f', 'db_script.sql'], check=True)

def insertar_datos():
    """ Insertar datos """
    datos = datos_pandas()
    try:
        datos[0].to_sql('tabla_unificada', con=engine, if_exists='replace', index=False)
        datos[1].to_sql('registros_categoria', con=engine, if_exists='replace', index=False)
        datos[2].to_sql('registros_cine', con=engine, if_exists='replace', index=False)
        logging.info('All data saved to db...')
    except sqlalchemy.exc.OperationalError:
        logging.error('Could not connect to database')

def revisar_db():
    """ Comprobar y testear """
    print(engine.execute("SELECT * FROM tabla_unificada").fetchone())
    print(engine.execute("SELECT * FROM registros_categoria").fetchone())
    print(engine.execute("SELECT * FROM registros_cine").fetchone())

insertar_datos()
