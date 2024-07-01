from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/index")
def get_base(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
