from flask import Blueprint, Flask
from .views.home import home
# clients = Blueprint('index', __name__, template_folder='templates', static_folder='static')
from .config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(home)

def run():
    app.run()

