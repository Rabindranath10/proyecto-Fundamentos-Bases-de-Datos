from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from config.db import meta, engine




gasolineras = Table(
    "gasolineras", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_gasolinera", Integer, primary_key=True),
    Column("created_at", TIMESTAMP),
    Column("nombre", String(255)),
    Column("direccion", String(255)),
  
)

meta.create_all(engine)