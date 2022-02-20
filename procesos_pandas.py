"""
Este módulo importa los archivos csv y los procesa con pandas
"""

from datetime import datetime
import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from constantes import Constantes

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

DICT_URLS = Constantes.DICT_URLS
DICT_MESES = Constantes.DICT_MESES
DICT_COLUMNAS = Constantes.DICT_COLUMNAS

class PandasCSV:
    """ Crea y procesa archivos csv """
    ruta_archivos_csv = []
    def importar_archivos_csv():
        """
        Crea archivos tipo: museos/2021-noviembre/museos-03-11-2021
        """
        for categoria in DICT_URLS:
            folder, archivo = PandasCSV.formatear_nombre_folder(categoria)
            ubicacion = folder.joinpath(archivo)
            PandasCSV.ruta_archivos_csv.append(str(ubicacion))
            if not os.path.exists(folder):
                os.makedirs(folder)
            contenido = PandasCSV.descargar_contenido(categoria)
            PandasCSV.guardar_contenido(ubicacion, contenido)

    def guardar_contenido(ubicacion, contenido):
        """ Guarda contenido en archivo """
        try:
            with open(ubicacion, 'w', encoding='latin-1') as archivo_csv:
                archivo_csv.write(contenido)
                logging.info('Se guardaron los archivos csv')
        except OSError:
            logging.error(f'No se pudo guardar el archivo {ubicacion}')

    def descargar_contenido(categoria):
        """ Descarga contenido remoto """
        try:
            response = requests.get(DICT_URLS[categoria])
            logging.info(f'Archivo {categoria}. Status code: {response.status_code}')
            return response.text
        except requests.exceptions.ConnectionError:
            logging.error('No se pudo establecer conexión')

    def formatear_nombre_folder(categoria):
        """ Crea las rutas de archivos a partir del timestamp y categoría """
        now = datetime.now()
        fecha = now.strftime('%d-%m-%Y')
        annio = now.strftime('%Y')
        mes = DICT_MESES[now.strftime('%B')]
        folder = Path(f'{categoria}/{annio}-{mes}/')
        archivo = f'{categoria}-{fecha}'
        return folder, archivo

    def formatear_columnas(dataframe):
        """ Pasa las columnas a minúsculas y elimina tildes """
        def repl(matchobj):
            if matchobj.group(0) == 'á': return 'a'
            if matchobj.group(0) == 'é': return 'e'
            if matchobj.group(0) == 'í': return 'i'
            if matchobj.group(0) == 'ó': return 'o'
            else: return 'u'
        patron = '[áéíóú]'
        dataframe.columns = dataframe.columns.str.lower()
        dataframe.columns = dataframe.columns.str.replace(patron, repl, regex=True)

    def crear_dataframe(archivo_csv, columnas):
        """
        Crea un dataframe a partir de un archivo csv
        """
        now = datetime.now()
        fecha = now.strftime('%d-%m-%Y')
        dataframe = pd.read_csv(archivo_csv)
        PandasCSV.formatear_columnas(dataframe)
        dataframe = dataframe.rename(columns=DICT_COLUMNAS)
        dataframe = dataframe.filter(items=columnas)
        dataframe['fecha_descarga'] = fecha
        logging.info(f'Se creó el dataframe de {archivo_csv}')
        return dataframe

    def concadenar_dataframes(lista_dataframes):
        """
        Une dataframes en un dataframe
        """
        dataframe = pd.concat(lista_dataframes, ignore_index=True)
        return dataframe

def parte_uno_challenge():
    """
    Parte 1 del challenge
    Normalizar toda la información de Museos, Salas de Cine y Bibliotecas
    Populares, para crear una única tabla que contenga:
    cod_localidad, id_provincia, id_departamento, categoría, provincia, localidad,
    nombre, domicilio, código postal, número de teléfono, mail, web
    """
    PandasCSV.importar_archivos_csv()
    archivos = PandasCSV.ruta_archivos_csv
    columnas = ['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
        'localidad', 'nombre', 'domicilio', 'codigo_postal', 'numero_de_telefono', 'mail', 'web']
    lista_dataframes = []
    for ruta in archivos:
        lista_dataframes.append(PandasCSV.crear_dataframe(ruta, columnas))
    return PandasCSV.concadenar_dataframes(lista_dataframes)

def formatear_series(series):
    """ Convierte pandas series en dataframe """
    dataframe = series.to_frame()
    dataframe.columns = ['numero_registros']
    dataframe = dataframe.reset_index()
    dataframe.rename(columns={'categoria': 'nombre'}, inplace=True)
    dataframe['tipo'] = 'categoria'
    dataframe['provincia'] = np.nan
    return dataframe

def parte_dos_challenge():
    """
    Parte 2 del challenge
    Procesar los datos conjuntos para poder generar una tabla con la siguiente
    información:
    Cantidad de registros totales por categoría
    Cantidad de registros totales por fuente
    Cantidad de registros por provincia y categoría
    """
    columnas = ['categoria', 'fuente', 'provincia']
    PandasCSV.importar_archivos_csv()
    archivos = PandasCSV.ruta_archivos_csv
    lista = []
    for ruta in archivos:
        lista.append(PandasCSV.crear_dataframe(ruta, columnas))
    dataframe = PandasCSV.concadenar_dataframes(lista)
    categoria = dataframe.groupby('categoria')['categoria'].count()
    fuente = dataframe.groupby('fuente')['fuente'].count()
    provincia_categoria = dataframe.groupby(['provincia', 'categoria'], as_index=False).size()
    catdf = formatear_series(categoria)
    fuentedf = formatear_series(fuente)
    provincia_categoria.rename(columns={'size': 'numero_registros', 'categoria': 'nombre'}, inplace=True)
    provincia_categoria['tipo'] = 'categoria'
    datos = [catdf, fuentedf, provincia_categoria]
    return pd.concat(datos, ignore_index=True, sort=False)


def parte_tres_challenge():
    """
    Parte 3 del challenge
    Procesar la información de cines para poder crear una tabla que contenga:
    Provincia
    Cantidad de pantallas
    Cantidad de butacas
    Cantidad de espacios INCAA
    """
    folder, archivo = PandasCSV.formatear_nombre_folder('cines')
    archivo_csv = folder.joinpath(archivo)
    columnas = ['provincia', 'pantallas', 'butacas', 'espacio_incaa']
    datos_cine = PandasCSV.crear_dataframe(archivo_csv, columnas)
    diccionario = {'si': 1, 'SI': 1}
    lambda_filter = lambda val: diccionario.get(val, 0)
    datos_cine['espacio_incaa'] = datos_cine['espacio_incaa'].apply(lambda_filter)
    grupo_provincia = datos_cine.groupby('provincia', as_index=False)
    numero_pantallas = grupo_provincia['pantallas'].sum()
    numero_butacas = grupo_provincia['butacas'].sum()
    numero_espacios_incaa = grupo_provincia['espacio_incaa'].sum()
    lista = [numero_pantallas, numero_butacas, numero_espacios_incaa]
    unidos = numero_pantallas.merge(numero_butacas, on='provincia')
    return unidos.merge(numero_espacios_incaa, on='provincia')

def datos_pandas():
    """ retorna datos de las tres partes del challenge """
    datos1 = parte_uno_challenge()
    datos2 = parte_dos_challenge()
    datos3 = parte_tres_challenge()
    return [datos1, datos2, datos3]
