"""
Módulo para conectarse con la base de datos
"""
import logging
import subprocess

from decouple import config
import sqlalchemy

from procesos_pandas import obtener_datos

engine = sqlalchemy.create_engine(config('DATABASE_URL'))

DATABASE_NAME = config('DATABASE_NAME')

def crear_tablas():
    """ Crear las tablas sql """
    subprocess.run(['psql', '-d', DATABASE_NAME, '-f', 'db_script.sql'], check=True)
    logging.info('Se crearon las tablas en la base de datos...')

def insertar_datos():
    """ Insertar datos a la base de datos """
    datos = obtener_datos()
    try:
        datos[0].to_sql('tabla_unificada', con=engine, if_exists='append', index=False)
        datos[1].to_sql('registros_categoria', con=engine, if_exists='append', index=False)
        datos[2].to_sql('registros_cine', con=engine, if_exists='append', index=False)
        logging.info('Se guardó todo en la base de datos...')
    except sqlalchemy.exc.OperationalError:
        logging.error('No se pudo conectar a la base de datos')

def main():
    """ Ejecuta todos los scripts del proyecto """
    crear_tablas()
    insertar_datos()

if __name__ == '__main__':
    main()
