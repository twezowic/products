from flask import Flask, render_template, request, url_for, flash, redirect
from celery import Celery
from flask_app.service import ProductService
from flask_app.model import Schema

Schema()

app = Flask(__name__)
app.config["SECRET_KEY"] = "ea8247aa00526c39376b4a34598cac655030ecfae35d5904"
app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

celery = Celery(f"flask_app.{app.name}", broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@app.route("/")
def index():
    return render_template("index.html", products=ProductService().read())


@celery.task
def add_product_to_db(data):
    ProductService().create(data)


@app.route("/create_sync/", methods=("GET", "POST"))
def create_sync():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        if not name:
            flash("Name is required!")
        elif not quantity:
            flash("quantity is required!")
        elif not price:
            flash("Price is required!")
        else:
            ProductService().create(
                {
                    "name": name,
                    "description": description,
                    "quantity": quantity,
                    "price": price,
                }
            )
            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/create_async/", methods=("GET", "POST"))
def create_async():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        if not name:
            flash("Name is required!")
        elif not quantity:
            flash("quantity is required!")
        elif not price:
            flash("Price is required!")
        else:
            add_product_to_db.delay(
                {
                    "name": name,
                    "description": description,
                    "quantity": quantity,
                    "price": price,
                }
            )
            return redirect(url_for("index"))

    return render_template("create.html")


# CRUD
# CREATE READ UPDATE DELETE
