from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from config.db import meta, engine




proyectos = Table(
    "proyectos", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_proyecto", Integer, primary_key=True),
    Column("created_at", TIMESTAMP),
    Column("nombre", String(255)),
    Column("direccion", String(255)),
    Column("activo", Integer),
  
)

meta.create_all(engine)