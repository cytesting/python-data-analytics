# Data analytics con python

## Acerca del proyecto

Se trata de crear una base de datos postgresql con información procesada con la librería
pandas de python.

## Instalación

Crear entorno virtual python con virtualenv o venv. Instalar las dependencias:

```
source venv/bin/activate
pip install -r requirements
```

## Configuración de la base de datos

Para acceder a la base de datos Postgres se requiere nombre del usuario, contraseña y nombre
de la base de datos. Hay que crear un archivo **.env** con la siguientes variables de
entorno para la conexión con la base de datos:

```
[settings]
DATABASE_URL=postgresql://<usuario>:<contraseña>@localhost:5432/<nombre_de_la_db>
DATABASE_NAME=<nombre_de_la_db>
```

## Ejecución

Activar el entorno virtual (unix) y ejecutar el archivo conexion_sql.py:

```
source venv/bin/activate
python conexion_sql.py
```

Se pueden ver los logs en el archivo **app.log**

## Herramientas

* Python
* Pandas
* SQLAlchemy
* Postgresql
* Entorno Linux
