from flask import Blueprint, Flask
from .views.home import home
from .config import DevelopmentConfig
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(home)

db = SQLAlchemy(app)
def run():
    app.run()

