from fastapi import FastAPI, APIRouter, Query

from typing import Optional

from app.schemas import RecipeSearchResults, Recipe, RecipeCreate
from app.recipe_data import RECIPES


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


# Actualizado para usar un modelo de respuesta
# https://fastapi.tiangolo.com/tutorial/response-model/
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Obtener una receta individual por ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


# Actualizado utilizando la validación de parámetros de FastAPI con la clase `Query`
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/
@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(
        None,
        min_length=3,
        openapi_examples={
            "chickenExample": {
                "summary": "Un ejemplo de búsqueda de pollo",
                "value": "chicken",
            }
        },
    ),
    max_results: Optional[int] = 10
) -> dict:
    """
    Buscar recetas basadas en la palabra clave de la etiqueta
    """
    if not keyword:
        # Usamos el corte de listas de Python para limitar los resultados
        # basándonos en el parámetro de consulta max_results
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}


# Nueva adición, usando el modelo Pydantic `RecipeCreate` para definir
# el cuerpo de la solicitud POST
@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    """
    Crear una nueva receta (solo en memoria)
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())

    return recipe_entry


app.include_router(api_router)


if __name__ == "__main__":
    # Usar esto solo para fines de depuración
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

