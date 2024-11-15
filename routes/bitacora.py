from datetime import datetime
from fastapi import APIRouter, HTTPException
from config.db import conn, engine
from models.bitacora import bitacora
from schemas.bitacora import Bitacora
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import SQLAlchemyError


bitacoras = APIRouter()


@bitacoras.post("/bitacora")
def create_bitacora(entry: Bitacora):
    # Validar los campos obligatorios
    required_fields = [
        entry.comentario, entry.km_inicial, entry.km_final, entry.num_galones, 
        entry.costo, entry.tipo_gasolina, entry.id_usuario, 
        entry.id_gasolinera, entry.id_vehiculo, entry.id_proyecto
    ]
    if any(field is None for field in required_fields):
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    # Asignar valores por defecto si faltan
    created_at = entry.created_at if entry.created_at else datetime.now()

    # Preparar la consulta de inserción
    insert_query = insert(bitacora).values(
        created_at=created_at,
        comentario=entry.comentario,
        km_inicial=entry.km_inicial,
        km_final=entry.km_final,
        num_galones=entry.num_galones,
        costo=entry.costo,
        tipo_gasolina=entry.tipo_gasolina,
        id_usuario=entry.id_usuario,
        id_gasolinera=entry.id_gasolinera,
        id_vehiculo=entry.id_vehiculo,
        id_proyecto=entry.id_proyecto
    )

    try:
        with engine.connect() as conn:
            # Ejecutar la inserción
            result = conn.execute(insert_query)
            conn.commit()  # Confirmar la transacción
            return {"id": result.inserted_primary_key[0], "message": "Bitácora creada exitosamente"}
    except SQLAlchemyError as e:
        print(f"Error al insertar en bitácora: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar en bitácora: {e}")

@bitacoras.get("/bitacora/{id}")
def get_bitacora(id: int):
    try:
        # Usar el motor para establecer una conexión segura
        with engine.connect() as conn:
            # Construir y ejecutar la consulta
            result = conn.execute(select(bitacora).where(bitacora.c.id_bitacora == id)).mappings().first()

        # Validar si se encontraron resultados
        if result:
            return dict(result)
        else:
            raise HTTPException(status_code=404, detail="Bitácora no encontrada")

    except SQLAlchemyError as e:
        print(f"Error al obtener bitácora: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener bitácora: {e}")
    
@bitacoras.delete("/bitacora/{id}")
@bitacoras.delete("/bitacora/{id}")
def delete_bitacora(id: int):
    try:
        with engine.connect() as conn:
            # Construir la consulta de eliminación
            delete_query = delete(bitacora).where(bitacora.c.id_bitacora == id)

            # Ejecutar la consulta
            result = conn.execute(delete_query)

            # Confirmar la eliminación si se afectó alguna fila
            if result.rowcount > 0:
                conn.commit()
                return {"message": "Bitácora eliminada exitosamente"}
            else:
                raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    except SQLAlchemyError as e:
        print(f"Error al eliminar Bitácora: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar Bitácora: {e}")
    
@bitacoras.put("/bitacora/{id}")
def update_bitacora(id: int, bita: Bitacora):
    try:
        with engine.connect() as conn:
            # Preparar la consulta de actualización
            update_query = update(bitacora).where(bitacora.c.id_bitacora == id).values(
                comentario=bita.comentario,
                km_inicial=bita.km_inicial,
                km_final=bita.km_final,
                num_galones=bita.num_galones,
                costo=bita.costo,
                tipo_gasolina=bita.tipo_gasolina,
                id_usuario=bita.id_usuario,
                id_vehiculo=bita.id_vehiculo,
                id_gasolinera=bita.id_gasolinera,
                id_proyecto=bita.id_proyecto
            )

            # Ejecutar la actualización
            result = conn.execute(update_query)

            # Confirmar si alguna fila fue actualizada
            if result.rowcount > 0:
                conn.commit()
                return {"message": "Bitácora actualizada exitosamente"}
            else:
                raise HTTPException(status_code=404, detail="Bitácora no encontrada")
    except SQLAlchemyError as e:
        print(f"Error al actualizar bitácora: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar bitácora: {e}")