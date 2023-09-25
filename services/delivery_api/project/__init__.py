from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.swagger import api, api_v1

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

# Ligando o API ao app Flask
api.init_app(app)

# Ligando o namespace ao API
api.add_namespace(api_v1, path='/api/v1')

from project import routes