from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Gasolinera(BaseModel): # Puede ser opcional si lo genera la base de datos
    created_at: Optional[datetime]
    nombre: str
    direccion: str