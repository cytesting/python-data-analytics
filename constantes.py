""" 
Constantes para procesar archivos en pandas
"""

def obtener_urls():
    """ Crea un diccionario de categorías y rutas """
    urlbase = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/'
    rutas = [
        '01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv',
        '392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv',
        '4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv',
    ]
    categorias = ['bibliotecas_populares', 'cines', 'museos']
    urls = [urlbase + item for item in rutas]
    return dict(zip(categorias, urls))

class Constantes:
    DICT_MESES = {
        'January': 'enero',
        'February': 'febrero',
        'March': 'marzo',
        'April': 'abril',
        'May': 'mayo',
        'June': 'junio',
        'July': 'julio',
        'August': 'agosto',
        'September': 'septiembre',
        'October': 'octubre',
        'November': 'noviembre',
        'December': 'diciembre'
    }


    COLUMNAS = [
        'cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia',
        'localidad', 'nombre', 'direccion', 'cp', 'telefono', 'mail', 'web', 'fuente',
         'pantallas', 'butacas', 'espacio_incaa'
    ]

    COLUMNAS_DB = [
        'cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia', 'localidad',
        'nombre', 'domicilio', 'codigo_postal', 'numero_de_telefono', 'mail', 'web', 'fuente',
        'pantallas', 'butacas', 'espacio_incaa'
    ]

    DICT_COLUMNAS = dict(zip(COLUMNAS, COLUMNAS_DB))

    DICT_URLS = obtener_urls()
    