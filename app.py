from flask import Flask, jsonify, make_response
from controller.functions import  post, index, get_all, delete, update, minimo_comun_multiplo, suma
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow
from utils.db import db

# Inicializamos la app
app = Flask(__name__)

# db configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Chistes API'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

# Inicializamos el objeto db
SQLAlchemy(app)

# Inicializamos marshmallow
Marshmallow(app)

# Agregamos rutas con sus funciones
app.add_url_rule("/Chistes/<tipo>", methods=['GET'], view_func=index)
app.add_url_rule("/Chistes/<tipo>", methods=['POST'], view_func=post)
app.add_url_rule("/Chistes/<id>", methods=['DELETE'], view_func=delete)
app.add_url_rule("/Chistes/all", methods=['GET'], view_func=get_all)
app.add_url_rule("/Chistes/<id>/<text>", methods=['PUT'], view_func=update)
app.add_url_rule("/Mates/MCM/", methods=['GET'], view_func=minimo_comun_multiplo)
app.add_url_rule("/Mates/suma/<numero>", methods=['GET'], view_func=suma)


# Error control
@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
