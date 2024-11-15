from fastapi import FastAPI

from routes.user import user
from routes.gasolinera import gasolinera
from routes.proyecto import proyecto
from routes.rol import roles
from routes.log import log
from routes.vehiculo import vehiculo
from routes.bitacora import bitacoras
from fastapi.responses import RedirectResponse




app = FastAPI(
    title="Proyecto Fundamentos de Bases de datos",
    description="API para gestionar CRUD de usuarios, gasolineras, proyectos, roles, vehículos y bitacoras"
)



app.include_router(user, prefix="/users", tags=["Usuarios"])
app.include_router(vehiculo, prefix="/vehiculos", tags=["Vehículos"])
app.include_router(proyecto, prefix="/proyectos", tags=["Proyectos"])
app.include_router(roles, prefix="/roles", tags=["Roles"])
app.include_router(gasolinera, prefix="/gasolinera", tags=["Gasolineras"])
app.include_router(bitacoras, prefix="/bitacora", tags=["Bitacoras"])

