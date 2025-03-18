from fastapi import APIRouter
from models import Product

router = APIRouter()

@router.post("/products/")
async def create_product(product: Product):
    return {"message": f"Producto {product.name} creado correctamente"}

@router.get("/products/{product_id}")
async def get_product(product_id: int):
    return {"product_id": product_id, "name": "producto_ejemplo"}

#similar a users.py se crean las rutas para gestionar productos 
