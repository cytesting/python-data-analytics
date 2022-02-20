-- Longitudes máximas:
-- [('cod_localidad', 8), ('id_provincia', 2), ('id_departamento', 5), ('categoria', 34),
-- ('provincia', 53), ('localidad', 39), ('nombre', 118), ('domicilio', 100), ('código postal', 9),
-- ('número de teléfono', 24), ('mail', 65), ('web', 116)]
-- integer PRIMARY KEY DEFAULT nextval('serial') = postgresql

DROP TABLE IF EXISTS "tabla_unificada";
DROP TABLE IF EXISTS "registros_categoria";
DROP TABLE IF EXISTS "registros_cine";

CREATE TABLE "tabla_unificada" (
    "id" serial NOT NULL PRIMARY KEY,
    "cod_localidad" varchar(20),
    "id_provincia" varchar(5),
    "id_departamento" varchar(10),
    "categoria" varchar(50),
    "provincia" varchar(100),
    "localidad" varchar(60),
    "nombre" varchar(200),
    "domicilio" varchar(150),
    "codigo_postal" varchar(20),
    "numero_de_telefono" varchar(50),
    "mail" varchar(100),
    "web" varchar(150),
    "fecha_descarga" date not null
);

CREATE TABLE "registros_categoria" (
    "categoria" varchar(100),
    "numero_registros" integer,
    "tipo" varchar(100),
    "provincia" varchar(100),
    "fuente" varchar(100),
    "fecha_descarga" date not null
);

CREATE TABLE "registros_cine" (
    "provincia" varchar(100),
    "pantallas" integer,
    "butacas" integer,
    "espacio_incaa" integer,
    "fecha_descarga" date not null
);
