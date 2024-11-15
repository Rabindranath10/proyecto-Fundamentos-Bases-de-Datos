from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Vehiculos(BaseModel): # Puede ser opcional si lo genera la base de datos
    created_at: Optional[datetime]
    modelo: str
    marca: str
    placa: str
    rendimiento: str
    galonaje: float
    tipo_combustible: str
