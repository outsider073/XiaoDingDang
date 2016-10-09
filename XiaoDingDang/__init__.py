from flask import Blueprint, Flask
from .views.home import home
# clients = Blueprint('index', __name__, template_folder='templates', static_folder='static')

app = Flask(__name__)

app.register_blueprint(home)

def run():
    app.run(debug=True)