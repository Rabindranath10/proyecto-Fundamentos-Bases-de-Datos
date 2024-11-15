from datetime import datetime
from fastapi import APIRouter
from config.db import conn
from models.logs import log
from schemas.log import Log


log = APIRouter()

@log.post("/logs")
def create_proyecto(lo: Log):
    # Cifrar la contraseña antes de guardarla
    # Asignar valores por defecto si faltan
    created_at = lo.created_at if lo.created_at else datetime.now()
  
    
    # Preparar la consulta de inserción
    insert_query = log.insert().values(
        created_at=created_at,
        descripcion=lo.descripcion,
        id_usr=lo.id_usr
        
    )
    
    try:
        # Ejecutar la inserción y capturar el ID insertado
        result = conn.execute(insert_query)
        conn.commit()  # Asegurarse de hacer commit para guardar los cambios
        return {"id": result.inserted_primary_key[0], "message": "Log created successfully"}
    except Exception as e:
        print(f"Error al insertar Log: {e}")
        return {"error": str(e)}