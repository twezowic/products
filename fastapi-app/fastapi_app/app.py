# from flask import Flask, render_template, request, url_for, flash, redirect

from fastapi import FastAPI, Request, Form
from celery import Celery
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from .service import ProductService
from .model import Schema
from pydantic import BaseModel
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
import typing

Schema()


# https://medium.com/@arunksoman5678/fastapi-flash-message-like-flask-f0970605031a
def flash(request: Request, message: typing.Any, category: str = "primary") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
        request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []


middleware = [
    Middleware(
        SessionMiddleware, secret_key="ea8247aa00526c39376b4a34598cac655030ecfae35d5904"
    )
]
app = FastAPI(middleware=middleware)
app.mount("/static/", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages

# app.config['SECRET_KEY'] = 'ea8247aa00526c39376b4a34598cac655030ecfae35d5904'
# app.config['CELERY_BROKER_URL']     = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery("fastapi_app", broker="redis://localhost:6379/0")
# celery.conf.update(app.config)


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
    if not name:
        flash(request, "Name is required!")
    elif not quantity:
        flash(request, "quantity is required!")
    elif not price:
        flash(request, "Price is required!")
    else:
        ProductService().create(
            {
                "name": name,
                "description": description,
                "quantity": quantity,
                "price": price,
            }
        )
        return RedirectResponse(url=app.url_path_for("index"), status_code=302)
    return templates.TemplateResponse("create.html", {"request": request})


# @app.route('/create_async/', methods=('GET', 'POST'))
# def create_async():
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         quantity = request.form['quantity']
#         price = request.form['price']

#         if not name:
#             flash('Name is required!')
#         elif not quantity:
#             flash('quantity is required!')
#         elif not price:
#             flash('Price is required!')
#         else:
#             add_product_to_db.delay({'name': name, 'description': description,
#                                      'quantity': quantity, 'price': price})
#             return redirect(url_for('index'))

#     return render_template('create.html')


# # CRUD
# # CREATE READ UPDATE DELETE
# fastapi run
