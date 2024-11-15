from datetime import datetime
from fastapi import APIRouter, HTTPException
from config.db import conn, engine
from models.gasolinera import gasolineras
from schemas.gasolinera import Gasolinera
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete, update


gasolinera = APIRouter()

@gasolinera.post("/gasolinera")
def create_gasolinera(gasolina: Gasolinera):
    # Validar los campos obligatorios
    if not gasolina.nombre or not gasolina.direccion:
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    # Asignar valores por defecto si faltan
    created_at = gasolina.created_at if gasolina.created_at else datetime.now()

    # Preparar la consulta de inserción
    insert_query = insert(gasolineras).values(
        created_at=created_at,
        nombre=gasolina.nombre,
        direccion=gasolina.direccion
    )

    try:
        with engine.connect() as conn:
            # Ejecutar la inserción
            result = conn.execute(insert_query)
            conn.commit()  # Asegurarse de hacer commit para guardar los cambios
            return {"id": result.inserted_primary_key[0], "message": "Gasolinera creada exitosamente"}
    except SQLAlchemyError as e:
        print(f"Error al insertar gasolinera: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar gasolinera: {e}")
    
@gasolinera.get("/gasolinera/{id}")
def get_gasolinera(id: int):
    try:
        # Ejecutar la consulta para obtener una gasolinera específica
        with engine.connect() as conn:
            result = conn.execute(select(gasolineras).where(gasolineras.c.id_gasolinera == id)).mappings().first()
        
        if result:
            return dict(result)  # Retornar los datos como diccionario
        else:
            return {"error": "Gasolinera no encontrada"}
    except SQLAlchemyError as e:
        print(f"Error al obtener gasolinera: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener gasolinera: {e}")
    
@gasolinera.delete("/gasolinera/{id}")
def delete_gasolinera(id: int):
    try:
        with engine.connect() as conn:
            # Ejecutar la consulta de eliminación
            result = conn.execute(delete(gasolineras).where(gasolineras.c.id_gasolinera == id))

            # Verificar si alguna fila fue afectada
            if result.rowcount > 0:
                conn.commit()  # Confirmar la eliminación en la base de datos
                return {"message": "Gasolinera eliminada exitosamente"}
            else:
                return {"error": "Gasolinera no encontrada"}
    except SQLAlchemyError as e:
        print(f"Error al eliminar gasolinera: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar gasolinera: {e}")
    
@gasolinera.put("/gasolinera/{id}")
def update_gasolinera(id: int, gasolina: Gasolinera):
    try:
        with engine.connect() as conn:
            # Preparar la consulta de actualización
            update_query = (
                update(gasolineras)
                .where(gasolineras.c.id_gasolinera == id)
                .values(
                    nombre=gasolina.nombre,
                    direccion=gasolina.direccion
                )
            )
            
            # Ejecutar la consulta de actualización
            result = conn.execute(update_query)

            # Verificar si alguna fila fue afectada
            if result.rowcount > 0:
                conn.commit()  # Confirmar los cambios
                return {"message": "Gasolinera actualizada exitosamente"}
            else:
                return {"error": "Gasolinera no encontrada"}
    except SQLAlchemyError as e:
        print(f"Error al actualizar gasolinera: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar gasolinera: {e}")