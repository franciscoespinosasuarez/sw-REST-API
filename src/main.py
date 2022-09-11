"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, PeopleFav, PlanetFav
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# PEOPLE-------------------------------------------------------------------------

@app.route('/people', methods = ['GET'])
def get_people ():

    people = People.query.all()
    all_people = list(map(lambda people:  people.serialize(), people))
  
    return jsonify(all_people)

@app.route('/people/<int:people_id>', methods = ['GET'])
def get_single_person (people_id):

    person = People.query.get(people_id)

    if person is None:
        raise APIException("Persona no encontrada. Llama al 091!", 404)
    
    return jsonify(person.serialize())


#PLANET---------------------------------------------------------------------------

@app.route('/planet', methods = ['GET'])
def get_planet ():

    planet = Planet.query.all()
    all_planet = list(map(lambda planet:  planet.serialize(), planet))

    return jsonify(all_planet)

@app.route('/planet/<int:planet_id>', methods = ['GET'])
def get_single_planet (planet_id):

    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planeta no encontrado. Si lo encuentras avisa a la NASA.", 404)
    
    return jsonify(planet.serialize())

#USERS---------------------------------------------------------------------------

@app.route('/users', methods = ['GET'])
def users ():

    users = User.query.all()
    all_users = list(map(lambda user:  user.serialize(), users))
  
    return jsonify(all_users)



#FAVORITES---------------------------------------------------------------------------

@app.route('/<int:user_id>/planetfav', methods=['GET'])
def favplanet_get(user_id):
        planet_fav= PlanetFav.query.filter_by(user_id=user_id)
        

        all_planets_fav = list(map(lambda planetfav: planetfav.serialize(), planet_fav))
        
        if len(all_planets_fav) == 0:
            return "No hay planetas favoritos."

        return jsonify(all_planets_fav)


@app.route('/<int:user_id>/peoplefav', methods=['GET'])
def favpeople_get(user_id):
        people_fav= PeopleFav.query.filter_by(user_id=user_id)
        

        all_people_fav = list(map(lambda personfav: personfav.serialize(), people_fav))
        
        if len(all_people_fav) == 0:
            return "No hay personas marcadas como favorito."
            
        return jsonify(all_people_fav)

                #Marcar People como favorito#
@app.route('/user/<int:user_id>/peoplefav/<int:people_id>', methods=['POST'])
def post_peoplefav(user_id, people_id):
    favorite = PeopleFav(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize())

                #Marcar Planets como favorito#
@app.route('/user/<int:user_id>/planetfav/<int:planet_id>', methods=['POST'])
def post_planetfav(user_id, planet_id):
    favorite = PlanetFav(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize())

                
                #Eliminar People como favorito#

@app.route('/user/<int:user_id>/peoplefav/<int:people_id>', methods=['DELETE'])
def delete_people_fav(user_id, people_id):
    deleteFav = PeopleFav.query.filter_by(user_id=user_id, people_id=people_id).one()
    db.session.delete(deleteFav)
    db.session.commit()

    return "Persona eliminada de favoritos"

                #Eliminar Planet como favorito#

@app.route('/user/<int:user_id>/planetfav/<int:planet_id>', methods=['DELETE'])
def delete_planet_fav(user_id, planet_id):
    deleteFav = PlanetFav.query.filter_by(user_id=user_id, planet_id=planet_id).one()
    db.session.delete(deleteFav)
    db.session.commit()

    return "Planeta eliminado de favoritos"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
