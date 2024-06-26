# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from models import Earthquake, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Existing view for getting an earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    session = Session(db.engine)
    earthquake = session.get(Earthquake, id)
    if earthquake:
        response = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404

# New view for getting earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    session = Session(db.engine)
    earthquakes = session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()
    quakes = [{
        'id': eq.id,
        'location': eq.location,
        'magnitude': eq.magnitude,
        'year': eq.year
    } for eq in earthquakes]

    response = {
        'count': len(quakes),
        'quakes': quakes
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
