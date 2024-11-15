from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Float
from config.db import meta, engine




bitacora = Table(
    "bitacora", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_bitacora", Integer, primary_key=True),
    Column("created_at", TIMESTAMP),
    Column("comentario", String(255)),
    Column("km_inicial", Integer),
    Column("km_final", Integer),
    Column("num_galones", Float),
    Column("costo", Float),
    Column("tipo_gasolina", String(255)),
    Column("id_usuario", Integer),
    Column("id_gasolinera", Integer),
    Column("id_vehiculo", Integer),
    Column("id_proyecto", Integer),

)

meta.create_all(engine)