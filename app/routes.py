from flask import Flask, make_response, request, jsonify, g
from models.hero import Hero, db
from models.power import Power
from models.heropower import HeroPower
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os

def create_app():
    app = Flask(__name__)
    # Allow CORS for all routes
    CORS(app)
    app.config.from_object('config.Config')
    db.init_app(app)

    # Sample request hook
    @app.before_request
    def app_path():
        g.path = os.path.abspath(os.getcwd())
    @app.route('/', methods=['GET'])
    def index():
        response_body = 'Welcome to the Superheroes API'
        status_code = 200
        return make_response(response_body, status_code)

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        hero_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
        return jsonify(hero_data), 200

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)

        if not hero:
            response_data = {"error": "Hero not found"}
            status_code = 404
            return make_response(jsonify(response_data), status_code)

        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "created_at": hero.created_at,
            "updated_at": hero.updated_at
        }

        return jsonify(hero_data), 200

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        power_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
        return jsonify(power_data), 200

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)

        if not power:
            response_data = {"error": "Power not found"}
            status_code = 404
            return make_response(jsonify(response_data), status_code)

        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
            "created_at": power.created_at,
            "updated_at": power.updated_at
        }

        return jsonify(power_data), 200

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def patch_power(id):
        power = Power.query.get(id)

        if not power:
            response_data = {"error": "Power not found"}
            status_code = 404
            return make_response(jsonify(response_data), status_code)

        data = request.get_json()
        description = data.get('description')

        if not description:
            response_data = {"error": "Description is required"}
            status_code = 400
            return make_response(jsonify(response_data), status_code)

        power.description = description

        try:
            db.session.commit()
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at,
                "updated_at": power.updated_at
            }), 200
        except IntegrityError:
            db.session.rollback()
            response_data = {"errors": ["Validation errors"]}
            status_code = 400
            return make_response(jsonify(response_data), status_code)

    @app.route('/hero_powers', methods=['POST'])
    def post_hero_power():
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        if not strength or not power_id or not hero_id:
            response_data = {"error": "Strength, power_id, and hero_id are required"}
            status_code = 400
            return make_response(jsonify(response_data), status_code)

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            response_data = {"error": "Hero or Power not found"}
            status_code = 404
            return make_response(jsonify(response_data), status_code)

        hero_power = HeroPower(strength=strength, hero=hero, power=power)

        try:
            db.session.add(hero_power)
            db.session.commit()

            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name, 
                "powers": [
                    {
                        "id": power.id,
                        "name": power.name,
                        "description": power.description
                    }
                ]
            }

            return jsonify(hero_data), 200
        except IntegrityError:
            db.session.rollback()
            response_data = {"errors": ["Validation errors"]}
            status_code = 400
            return make_response(jsonify(response_data), status_code)

    return app