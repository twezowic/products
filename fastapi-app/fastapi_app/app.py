from fastapi import FastAPI, Request, Form
from celery import Celery
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from service import ProductService
from model import Schema

Schema()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

celery = Celery("fastapi_app", broker="redis://redis:6379/0")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "products": ProductService().read()}
    )


@celery.task
def add_product_to_db(data):
    ProductService().create(data)


@app.get("/create_sync/", response_class=HTMLResponse)
def create_sync(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create_sync/")
def create_sync(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
):
    ProductService().create(
        {
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
        }
    )
    return RedirectResponse(url=app.url_path_for("index"), status_code=302)


@app.get("/create_async/", response_class=HTMLResponse)
def create_async(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create_async/")
def create_async(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
):
    add_product_to_db.delay(
        {
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
        }
    )
    return RedirectResponse(url=app.url_path_for("index"), status_code=302)
