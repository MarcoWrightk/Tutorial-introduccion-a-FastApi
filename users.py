from fastapi import APIRouter
from models import User

router = APIRouter()

@router.post("/users/")
async def create_user(user: User):
    return {"message": f"Usuario {user.username} creado correctamente"}

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "username": "usuario_ejemplo"}

#Explicación:

Se importa APIRouter de FastAPI para crear un enrutador modular para las rutas de los usuarios.

El decorador @router.post define una ruta para crear usuarios, mientras que @router.get se usa para obtener información de un usuario específico.

