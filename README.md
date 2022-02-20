# Data analytics con python

## Instalación

Crear entorno virtual python con virtualenv o venv. Instalar las dependencias:

```
pip install -r requirements
```

## Configuración de la base de datos

Crear un archivo .env con la siguientes variables de entorno:

```
[settings]
DATABASE_URL=postgresql://<usuario>:<contraseña>@localhost:5432/<nombre_de_la_db>
DATABASE_NAME=<nombre_de_la_db>
```

## Ejecución

Ejecutar el archivo conexion_sql.py:

```
python conexion_sql.py
```

