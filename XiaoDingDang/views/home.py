from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from . import BluePrints
index_page = Blueprint('home', __name__)

@index_page.route("/")
def index():
    try:
        return render_template("home/index.html")
    except TemplateNotFound:
        abort(404)