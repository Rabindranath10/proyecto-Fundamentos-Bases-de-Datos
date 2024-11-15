# config/db.py
import pg8000
from sqlalchemy import create_engine, MetaData
from urllib.parse import urlparse

# URL de conexión de Supabase (reemplaza con tu contraseña real)
DATABASE_URL = "postgresql+pg8000://postgres.hvkeastftvmpwppzfyei:italocarcamo@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Extraer las partes de la URL
result = urlparse(DATABASE_URL)

# Establecer la conexión con pg8000
conn = pg8000.connect(user=result.username, password=result.password, host=result.hostname,
                      port=result.port, database=result.path[1:])

# Crear un cursor
cursor = conn.cursor()

# Realizar una consulta simple
try:
    cursor.execute("SELECT NOW()")
    current_time = cursor.fetchone()
    print(f"La hora actual desde la base de datos es: {current_time[0]}")
finally:
    # Cerrar la conexión y cursor de forma segura
    cursor.close()
    conn.close()

# Definir MetaData y crear el motor de conexión con SQLAlchemy usando pg8000
meta = MetaData()
engine = create_engine(DATABASE_URL)
