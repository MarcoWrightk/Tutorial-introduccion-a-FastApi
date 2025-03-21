
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.api.api_v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="Recipe API")


@root_router.get("/", status_code=200)
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


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__"
    #Utilice esto solo para fines de depuración
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
