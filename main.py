from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)

class Cafe(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    map_url = Column(db.String, nullable=False)
    img_url = Column(db.String, nullable=False)
    location = Column(db.String, nullable=False)
    has_sockets = Column(db.Boolean, nullable=False)
    has_toilet = Column(db.Boolean, nullable=False)
    has_wifi = Column(db.Boolean, nullable=False)
    can_take_calls = Column(db.Boolean, nullable=False)
    seats = Column(Integer, nullable=False)
    coffee_price = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'map_url': self.map_url,
            'img_url': self.img_url,
            'location': self.location,
            'has_sockets': self.has_sockets,
            'has_toilet': self.has_toilet,
            'has_wifi': self.has_wifi,
            'can_take_calls': self.can_take_calls,
            'seats': self.seats,
            'coffee_price': self.coffee_price
        }

with app.app_context():
    db.create_all()

@app.route('/random_cafe')
def random_cafe():
    random_cafe = db.session.execute(db.select(Cafe).order_by(db.sql.func.random()).limit(1)).scalar()

    if random_cafe:
        cafe_data = random_cafe.to_dict()
        return jsonify(cafe_data)
    else:
        return jsonify({'message': 'No cafes found'}), 404


@app.route('/add_cafe', methods=['POST'])
def add_cafe():

    name = request.args.get('name')
    map_url = request.args.get('map_url')
    img_url = request.args.get('img_url')
    location = request.args.get('location')
    has_sockets = request.args.get('has_sockets', type=bool)
    has_toilet = request.args.get('has_toilet', type=bool)
    has_wifi = request.args.get('has_wifi', type=bool)
    can_take_calls = request.args.get('can_take_calls', type=bool)
    seats = request.args.get('seats', type=int)
    coffee_price = request.args.get('coffee_price', type=int)


    new_cafe = Cafe(
        name=name,
        map_url=map_url,
        img_url=img_url,
        location=location,
        has_sockets=has_sockets,
        has_toilet=has_toilet,
        has_wifi=has_wifi,
        can_take_calls=can_take_calls,
        seats=seats,
        coffee_price=coffee_price
    )


    db.session.add(new_cafe)
    db.session.commit()

    return jsonify({'message': 'Cafe added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')