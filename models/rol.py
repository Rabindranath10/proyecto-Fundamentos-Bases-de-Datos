from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from config.db import meta, engine




rol = Table(
    "rol", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_rol", Integer, primary_key=True),
    Column("descripcion", String(255)),

  
)

meta.create_all(engine)