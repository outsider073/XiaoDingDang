from flask import Blueprint, Flask
from .views import home
from .config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(home.index_page)

db = SQLAlchemy(app)
def run():
    app.run()

