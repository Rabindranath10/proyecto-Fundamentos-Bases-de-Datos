from datetime import datetime
from fastapi import APIRouter, HTTPException
from config.db import conn, engine
from models.proyecto import proyectos  # Asegúrate de tener la tabla 'proyectos' correctamente definida en models/proyecto.py
from schemas.proyecto import Proyectos  # Esquema para los datos del proyecto
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import SQLAlchemyError

proyecto = APIRouter()

@proyecto.post("/proyectos")
def create_proyecto(proyecto_data: Proyectos):
    # Validar los campos obligatorios
    if not proyecto_data.nombre or not proyecto_data.direccion or proyecto_data.activo is None:
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    # Asignar valores por defecto si no se proporcionan
    created_at = proyecto_data.created_at if proyecto_data.created_at else datetime.now()

    # Preparar la consulta de inserción
    insert_query = insert(proyectos).values(
        created_at=created_at,
        nombre=proyecto_data.nombre,
        direccion=proyecto_data.direccion,
        activo=proyecto_data.activo
    )

    try:
        # Ejecutar la inserción usando SQLAlchemy Core
        with engine.connect() as conn:
            result = conn.execute(insert_query)  # Ejecuta la consulta de inserción
            conn.commit()  # Hacer commit explícito de la transacción
            return {"id": result.inserted_primary_key[0], "message": "Proyecto creado exitosamente"}
    except SQLAlchemyError as e:
        print(f"Error al insertar proyecto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar proyecto: {e}")
    

@proyecto.get("/proyectos/{id}")
def get_proyecto(id: int):
    try:
        # Ejecutar la consulta usando `.mappings()` para obtener un diccionario
        with engine.connect() as conn:  # Usar conexión con el engine
            result = conn.execute(select(proyectos).where(proyectos.c.id_proyecto == id)).mappings().first()
        
        if result:
            return dict(result)  # Si `result` ya es un diccionario, esta línea lo convierte correctamente
        else:
            return {"error": "Proyecto no encontrado"}
    except Exception as e:
        print(f"Error al obtener proyecto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener proyecto: {e}")
    
@proyecto.delete("/proyectos/{id}")
def delete_proyecto(id: int):
    try:
        with engine.connect() as conn:
            # Ejecuta la consulta de eliminación
            result = conn.execute(delete(proyectos).where(proyectos.c.id_proyecto == id))

            # Verifica si alguna fila fue afectada
            if result.rowcount > 0:
                conn.commit()  # Confirmar la eliminación en la base de datos
                return {"message": "Proyecto eliminado exitosamente"}
            else:
                return {"error": "Proyecto no encontrado"}
    except Exception as e:
        print(f"Error al eliminar proyecto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar proyecto: {e}")

@proyecto.put("/proyectos/{id}")
def update_proyecto(id: int, proyecto_data: Proyectos):
    try:
        with engine.connect() as conn:
            # Preparamos la consulta de actualización
            update_query = update(proyectos).where(proyectos.c.id_proyecto == id).values(
                nombre=proyecto_data.nombre,
                direccion=proyecto_data.direccion,
                activo=proyecto_data.activo,
                created_at=proyecto_data.created_at if proyecto_data.created_at else datetime.now()
            )

            # Ejecuta la consulta de actualización
            result = conn.execute(update_query)

            # Verifica si alguna fila fue afectada
            if result.rowcount > 0:
                conn.commit()  # Confirmar la actualización en la base de datos
                return {"message": "Proyecto actualizado exitosamente"}
            else:
                return {"error": "Proyecto no encontrado"}

    except Exception as e:
        print(f"Error al actualizar proyecto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar proyecto: {e}")