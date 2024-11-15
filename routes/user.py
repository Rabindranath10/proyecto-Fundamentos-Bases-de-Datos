from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select, delete, update
from config.db import engine, meta
from schemas.user import Usuarios
from models.user import usuarios
from cryptography.fernet import Fernet
from models.logs import log

# Función para cargar la clave de cifrado
def load_key():
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Clave de cifrado no encontrada. Asegúrate de haber generado 'secret.key'.")

# Cargar la clave y crear el objeto Fernet
key = load_key()
f = Fernet(key)

# Router para usuarios
user = APIRouter()

@user.post("/users")
def create_users(user_data: Usuarios):
    if not user_data.nombre or not user_data.apellido or not user_data.username or not user_data.password:
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    # Cifrar la contraseña antes de guardarla
    encrypted_password = f.encrypt(user_data.password.encode())
    
    # Asignar valores por defecto si no se proporcionan
    created_at = user_data.created_at if user_data.created_at else datetime.now()
    last_login = user_data.last_login if user_data.last_login else datetime.now()

    # Preparar la consulta de inserción
    insert_query = insert(usuarios).values(
        created_at=created_at,
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        password=encrypted_password,  # Guardar la contraseña cifrada
        id_rol=user_data.id_rol,
        activo=user_data.activo,
        username=user_data.username,
        last_login=last_login
    )
    
    try:
        # Ejecutar la inserción usando SQLAlchemy Core
        with engine.connect() as conn:
            result = conn.execute(insert_query)
            conn.commit()  # Hacer commit explícito de la transacción
            return {"id": result.inserted_primary_key[0], "message": "Usuario creado exitosamente"}
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al insertar usuario: {e}")
    
@user.get("/users/{id}")
def get_user(id: int):
    try:
        # Ejecuta la consulta usando `.mappings()` para obtener un diccionario
        with engine.connect() as conn:
            result = conn.execute(select(usuarios).where(usuarios.c.id_usuario == id)).mappings().first()
        
        if result:
            return dict(result)  # Si `result` ya es un diccionario, esta línea lo convierte correctamente
        else:
            return {"error": "Usuario no encontrado"}
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {e}")
    
@user.delete("/users/{id}")
def delete_user(id: int):
    try:
        with engine.connect() as conn:
            # Iniciar una transacción
            with conn.begin():
                # Verificar si el usuario tiene registros en la tabla 'logs'
                logs_result = conn.execute(
                    log.select().where(log.c.id_usuario == id)
                ).fetchall()

                # Si tiene registros en la tabla logs, eliminarlos
                if logs_result:
                    conn.execute(delete(log).where(log.c.id_usuario == id))

                # Eliminar el usuario de la tabla 'usuarios'
                result = conn.execute(delete(usuarios).where(usuarios.c.id_usuario == id))

                # Verificar si alguna fila fue afectada
                if result.rowcount > 0:
                    return {"message": "Usuario y registros relacionados eliminados exitosamente"}
                else:
                    return {"error": "Usuario no encontrado"}

    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {e}")

@user.put("/users/{id}")
def update_user(id: int, user_data: Usuarios):
    try:
        with engine.connect() as conn:
            # Verificar si el usuario existe
            result = conn.execute(
                usuarios.select().where(usuarios.c.id_usuario == id)
            ).mappings().first()  # Usamos `.mappings()` para obtener un diccionario

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Si se proporciona una nueva contraseña, cifrarla antes de actualizar
            if user_data.password:
                encrypted_password = f.encrypt(user_data.password.encode())
            else:
                encrypted_password = result['password']  # Mantener la contraseña existente si no se proporciona

            # Asignar valores por defecto si no se proporcionan
            updated_at = datetime.now()

            # Preparar la consulta de actualización
            update_query = (
                update(usuarios)
                .where(usuarios.c.id_usuario == id)
                .values(
                    nombre=user_data.nombre if user_data.nombre else result['nombre'],
                    apellido=user_data.apellido if user_data.apellido else result['apellido'],
                    password=encrypted_password,  # Si la contraseña fue proporcionada, se actualiza
                    id_rol=user_data.id_rol if user_data.id_rol else result['id_rol'],
                    activo=user_data.activo if user_data.activo is not None else result['activo'],
                    username=user_data.username if user_data.username else result['username'],
                    last_login=user_data.last_login if user_data.last_login else result['last_login'],
                    created_at=result['created_at'],  # Mantener la fecha de creación original
                )
            )

            # Ejecutar la actualización
            conn.execute(update_query)
            conn.commit()

            return {"message": "Usuario actualizado exitosamente"}

    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {e}")