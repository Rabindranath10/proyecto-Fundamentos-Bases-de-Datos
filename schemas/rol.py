from pydantic import BaseModel
from typing import Optional


class Rol(BaseModel): # Puede ser opcional si lo genera la base de datos
    descripcion: str