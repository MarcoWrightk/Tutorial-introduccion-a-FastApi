from pydantic import BaseModel

# Modelo de usuario
class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    disabled: bool = None

# Modelo de producto
class Product(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = 0.0




//Explicación:

Los modelos User y Product se utilizan para definir cómo se estructuran los datos en la API.

Pydantic se encarga de validar y asegurar que los datos enviados en las solicitudes cumplan con la estructura definida.

Estos modelos son utilizados en las rutas para validar los datos de entrada y salida.
