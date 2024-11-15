from datetime import datetime
from fastapi import APIRouter, HTTPException
from config.db import conn, engine
from models.vehiculo import vehiculos
from schemas.vehiculo import Vehiculos
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import SQLAlchemyError


vehiculo = APIRouter()

@vehiculo.post("/vehiculos")
def create_vehiculo(vehiculo_data: Vehiculos):
    # Validar los campos obligatorios
    if not vehiculo_data.modelo or not vehiculo_data.marca or not vehiculo_data.placa or not vehiculo_data.rendimiento or not vehiculo_data.galonaje or not vehiculo_data.tipo_combustible:
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    # Asignar valores por defecto si no se proporcionan
    created_at = vehiculo_data.created_at if vehiculo_data.created_at else datetime.now()

    # Preparar la consulta de inserción
    insert_query = insert(vehiculos).values(
        created_at=created_at,
        modelo=vehiculo_data.modelo,
        marca=vehiculo_data.marca,
        placa=vehiculo_data.placa,
        rendimiento=vehiculo_data.rendimiento,
        galonaje=vehiculo_data.galonaje,
        tipo_combustible=vehiculo_data.tipo_combustible
    )

    try:
        # Ejecutar la inserción usando SQLAlchemy Core
        with engine.connect() as conn:
            result = conn.execute(insert_query)
            conn.commit()  # Hacer commit explícito de la transacción
            return {"id": result.inserted_primary_key[0], "message": "Vehículo creado exitosamente"}
    except Exception as e:
        print(f"Error al insertar vehículo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar vehículo: {e}")
    
@vehiculo.get("/vehiculos/{id}")
def get_vehiculo(id: int):
    try:
        # Ejecuta la consulta usando `.mappings()` para obtener el vehículo como un diccionario
        with engine.connect() as conn:
            result = conn.execute(select(vehiculos).where(vehiculos.c.id_vehiculo == id)).mappings().first()
        
        if result:
            return dict(result)  # Si result es un diccionario, esta línea lo devuelve como un diccionario
        else:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    except Exception as e:
        print(f"Error al obtener vehículo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener vehículo: {e}")
    
@vehiculo.delete("/vehiculos/{id}")
def delete_vehiculo(id: int):
    try:
        with engine.connect() as conn:
            # Ejecuta la consulta de eliminación
            result = conn.execute(delete(vehiculos).where(vehiculos.c.id_vehiculo == id))

            # Verifica si alguna fila fue afectada
            if result.rowcount > 0:
                conn.commit()  # Confirmar la eliminación en la base de datos
                return {"message": "Vehículo eliminado exitosamente"}
            else:
                return {"error": "Vehículo no encontrado"}
    except Exception as e:
        print(f"Error al eliminar vehículo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar vehículo: {e}")
    


@vehiculo.put("/vehiculos/{id}")
def update_vehiculo(id: int, vehiculo_data: Vehiculos):
    try:
        with engine.connect() as conn:
            # Preparamos la consulta de actualización
            update_query = update(vehiculos).where(vehiculos.c.id_vehiculo == id).values(
                modelo=vehiculo_data.modelo,
                marca=vehiculo_data.marca,
                placa=vehiculo_data.placa,
                rendimiento=vehiculo_data.rendimiento,
                galonaje=vehiculo_data.galonaje,
                tipo_combustible=vehiculo_data.tipo_combustible
            )

            # Ejecuta la consulta de actualización
            result = conn.execute(update_query)

            # Verifica si alguna fila fue afectada
            if result.rowcount > 0:
                conn.commit()  # Confirmar la actualización en la base de datos
                return {"message": "Vehículo actualizado exitosamente"}
            else:
                return {"error": "Vehículo no encontrado"}

    except Exception as e:
        print(f"Error al actualizar vehículo: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar vehículo: {e}")