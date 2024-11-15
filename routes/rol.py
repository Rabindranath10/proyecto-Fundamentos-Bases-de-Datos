from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.sql import insert
from config.db import engine, meta
from sqlalchemy import select, delete, update

# Definir la tabla con SQLAlchemy Core
rol = Table(
    'rol', meta,
    Column('id_rol', Integer, primary_key=True),
    Column('descripcion', String(255)),
)

# Crear las tablas si no existen
meta.create_all(engine)

# Función para insertar un rol usando SQLAlchemy Core
from fastapi import APIRouter, HTTPException
from schemas.rol import Rol

roles = APIRouter()

@roles.post("/roles")
def create_roles(roli: Rol):
    if not roli.descripcion:
        raise HTTPException(status_code=400, detail="Descripcion es obligatoria")

    # Preparar la consulta de inserción
    insert_query = insert(rol).values(descripcion=roli.descripcion)

    try:
        with engine.connect() as conn:
            result = conn.execute(insert_query)
            conn.commit()  # Hacer commit explícito de la transacción
            return {"id": result.inserted_primary_key[0], "message": "Rol created successfully"}
    except Exception as e:
        print(f"Error al insertar Rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar Rol: {e}")

    
@roles.get("/roles/{id}")
def get_rol(id: int):
    try:
        # Usar 'select' para obtener el rol basado en su 'id_rol'
        query = select(rol).where(rol.c.id_rol == id)

        # Ejecutar la consulta y obtener el resultado
        with engine.connect() as conn:
            result = conn.execute(query).mappings().first()

        if result:
            return dict(result)  # Devuelve el resultado como un diccionario
        else:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
    except Exception as e:
        print(f"Error al obtener rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener rol: {e}")
    
@roles.delete("/roles/{id}")
def delete_rol(id: int):
    try:
        # Preparar la consulta de eliminación
        delete_query = delete(rol).where(rol.c.id_rol == id)

        with engine.connect() as conn:
            result = conn.execute(delete_query)
            conn.commit()  # Hacer commit explícito de la transacción

        # Si no se ha afectado ninguna fila, significa que no se encontró el rol
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        return {"message": f"Rol con id {id} eliminado exitosamente."}
    except Exception as e:
        print(f"Error al eliminar rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar rol: {e}")
    
@roles.put("/roles/{id}")
def update_rol(id: int, roli: Rol):
    if not roli.descripcion:
        raise HTTPException(status_code=400, detail="Descripcion es obligatoria")

    try:
        # Preparar la consulta de actualización
        update_query = update(rol).where(rol.c.id_rol == id).values(descripcion=roli.descripcion)

        with engine.connect() as conn:
            result = conn.execute(update_query)
            conn.commit()  # Hacer commit explícito de la transacción

        # Si no se ha afectado ninguna fila, significa que no se encontró el rol
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        return {"message": f"Rol con id {id} actualizado exitosamente."}
    except Exception as e:
        print(f"Error al actualizar rol: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar rol: {e}")