from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Bitacora(BaseModel): # Puede ser opcional si lo genera la base de datos
    created_at: Optional[datetime]
    comentario: str
    km_inicial: int
    km_final: int
    num_galones: float
    costo: float
    tipo_gasolina: str
    id_usuario: int
    id_vehiculo: int
    id_gasolinera: int
    id_proyecto: int
