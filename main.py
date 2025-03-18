from fastapi import FastAPI
from routes import users, products

app = FastAPI()

# Incluyendo las rutas
app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de FastAPI!"}
