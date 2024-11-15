from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from config.db import meta, engine
from cryptography.fernet import Fernet

key=Fernet.generate_key()
f=Fernet(key)

usuarios = Table(
    "usuarios", meta,  # Cambiado a "usuarios" para coincidir con la base de datos
    Column("id_usuario", Integer, primary_key=True),
    Column("created_at", TIMESTAMP),
    Column("nombre", String(255)),
    Column("apellido", String(255)),
    Column("password", String(255)),
    Column("id_rol", Integer),
    Column("activo", Integer),
    Column("username", String(255)),
    Column("last_login", TIMESTAMP),  # Agregado last_login
)

meta.create_all(engine)
