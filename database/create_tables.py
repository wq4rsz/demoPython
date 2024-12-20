import psycopg2
from psycopg2 import sql
from config import db_config

conn = psycopg2.connect(
    dbname='postgres',
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
)

conn.autocommit = True
cur = conn.cursor()

db_name = db_config['dbname']
cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
exists = cur.fetchone()

if not exists:
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"Database '{db_name}' created successfully!")
else:
    print(f"Database '{db_name}' already exists.")

cur.close()
conn.close()

conn = psycopg2.connect(
    dbname=db_config['dbname'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
)

cur = conn.cursor()

create_tables_sql = '''
CREATE TABLE IF NOT EXISTS public.materials
(
    id_material serial NOT NULL,
    title_material character varying(50) COLLATE pg_catalog."default",
    mtype_id integer NOT NULL,
    picture character varying(500) COLLATE pg_catalog."default",
    price money,
    storage_quantity integer,
    min_quantity integer,
    pack_quantity integer,
    unit character(2) COLLATE pg_catalog."default",
    CONSTRAINT materials_pkey PRIMARY KEY (id_material),
    CONSTRAINT materials_title_material_key UNIQUE (title_material)
);

CREATE TABLE IF NOT EXISTS public.materials_suppliers
(
    material_id integer NOT NULL,
    supplier_id integer NOT NULL,
    CONSTRAINT materials_suppliers_material_id_suppliers_id_key UNIQUE (material_id, supplier_id)
);

CREATE TABLE IF NOT EXISTS public.mtype
(
    id_mtype serial NOT NULL,
    title_mtype character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT mtype_pkey PRIMARY KEY (id_mtype)
);

CREATE TABLE IF NOT EXISTS public.stype
(
    id_stype serial NOT NULL,
    title_stype character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT stype_pkey PRIMARY KEY (id_stype)
);

CREATE TABLE IF NOT EXISTS public.suppliers
(
    id_supplier serial NOT NULL,
    title_supplier character varying(50) COLLATE pg_catalog."default",
    stype_id integer NOT NULL,
    inn character(10) COLLATE pg_catalog."default",
    rating integer,
    bdate date,
    CONSTRAINT suppliers_pkey PRIMARY KEY (id_supplier),
    CONSTRAINT suppliers_inn_key UNIQUE (inn),
    CONSTRAINT suppliers_title_supplier_key UNIQUE (title_supplier)
);

ALTER TABLE IF EXISTS public.materials
    ADD CONSTRAINT materials_mtype_id_fkey FOREIGN KEY (mtype_id)
    REFERENCES public.mtype (id_mtype) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.materials_suppliers
    ADD CONSTRAINT materials_suppliers_material_id_fkey FOREIGN KEY (material_id)
    REFERENCES public.materials (id_material) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.materials_suppliers
    ADD CONSTRAINT materials_suppliers_suppliers_id_fkey FOREIGN KEY (supplier_id)
    REFERENCES public.suppliers (id_supplier) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.suppliers
    ADD CONSTRAINT suppliers_stype_id_fkey FOREIGN KEY (stype_id)
    REFERENCES public.stype (id_stype) MATCH SIMPLE
    ON UPDATE NO ACTION;

'''

with conn.cursor() as cur:
    cur.execute(create_tables_sql)
    conn.commit()

cur.close()
conn.close()


