from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Usuarios(BaseModel): # Puede ser opcional si lo genera la base de datos
    created_at: Optional[datetime]
    nombre: str
    apellido: str
    password: str
    id_rol: int
    activo: int
    username: str
    last_login: Optional[datetime]
