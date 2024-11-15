from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from config.db import meta, engine




log = Table(
    "log", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_log", Integer, primary_key=True),
    Column("created_at", TIMESTAMP),
    Column("descripcion", String(255)),
    Column("id_usuario", Integer),
  
)

meta.create_all(engine)