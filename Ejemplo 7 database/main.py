from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path
from sqlalchemy.orm import Session

from app.schemas.recipe import RecipeSearchResults, Recipe, RecipeCreate
from app import deps
from app import crud


# Directorios del proyecto
ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes},
    )


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Obtener una receta individual por ID
    """
    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        # Se lanza la excepción, no se retorna - de lo contrario se obtendría
        # un error de validación.
        raise HTTPException(
            status_code=404, detail=f"Receta con ID {recipe_id} no encontrada"
        )

    return result


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Buscar recetas basadas en la palabra clave de la etiqueta
    """
    recipes = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": recipes}

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(
    *, recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Crear una nueva receta en la base de datos.
    """
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe


app.include_router(api_router)


if __name__ == "__main__":
    # Usar esto solo para fines de depuración
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
