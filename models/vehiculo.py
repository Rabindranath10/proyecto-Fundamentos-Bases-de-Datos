from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Float
from config.db import meta, engine




vehiculos = Table(
    "vehiculos", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_vehiculo", Integer, primary_key=True),
    Column("created_at", TIMESTAMP),
    Column("modelo", String(255)),
    Column("marca", String(255)),
    Column("placa", String(255)),
    Column("rendimiento", String(255)),
    Column("galonaje", Float),
    Column("tipo_combustible", String(255)),  # Agregado last_login
)

meta.create_all(engine)