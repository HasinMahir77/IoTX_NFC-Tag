from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Guitar  # Import Guitar instead of User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS
db.init_app(app)

# Create database tables (only needed for first-time setup)
with app.app_context():
    db.create_all()

# Route to add a new guitar
@app.route('/add_guitar', methods=['POST'])
def add_guitar():
    data = request.json
    if not data or not all(k in data for k in ["tag_id", "name", "model", "manufacture_year"]):
        return jsonify({"error": "Invalid input"}), 400

    try:
        new_guitar = Guitar(
            tag_id=data['tag_id'],
            name=data['name'],
            model=data['model'],
            manufacture_year=int(data['manufacture_year'])
        )
        db.session.add(new_guitar)
        db.session.commit()
        return jsonify({"message": "Guitar added successfully!", "guitar": new_guitar.to_dict()}), 201
    except ValueError:
        return jsonify({"error": "Invalid manufacture_year format"}), 400

# Route to get all guitars
@app.route('/guitars', methods=['GET'])
def get_guitars():
    guitars = Guitar.query.all()
    return jsonify([guitar.to_dict() for guitar in guitars])

# Route to get a guitar by tag_id
@app.route('/guitar/<string:tag_id>', methods=['GET'])
def get_guitar(tag_id):
    guitar = Guitar.query.get(tag_id)
    if not guitar:
        return jsonify({"error": "Guitar not found"}), 404
    return jsonify(guitar.to_dict())

# Route to delete a guitar by tag_id
@app.route('/delete_guitar/<string:tag_id>', methods=['DELETE'])
def delete_guitar(tag_id):
    guitar = Guitar.query.get(tag_id)
    if not guitar:
        return jsonify({"error": "Guitar not found"}), 404

    db.session.delete(guitar)
    db.session.commit()
    return jsonify({"message": "Guitar deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True, port=2000, host="0.0.0.0")