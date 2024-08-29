"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abcde"

app.app_context().push()
app.app_context()

connect_db(app)


@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!."""

    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************
@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes."""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake in particular."""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake."""

    new_cupcake = Cupcake(
                flavor=request.json["flavor"], 
                size=request.json["size"], 
                rating=request.json["rating"], 
                image=request.json["image"] or None
                )

    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake."""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
  
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
