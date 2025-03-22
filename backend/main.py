from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Intrument  # Import Intrument instead of Guitar
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS
db.init_app(app)

# Create database tables (only needed for first-time setup)
with app.app_context():
    db.create_all()

# Route to add a new instrument
@app.route('/add_instrument', methods=['POST'])
def add_instrument():
    data = request.json
    if not data or not all(k in data for k in ["tag_id", "name", "manufacturer", "model", "serial", "manufacture_date"]):
        return jsonify({"error": "Invalid input"}), 400

    try:
        new_instrument = Intrument(
            tag_id=int(data['tag_id']),
            name=data['name'],
            manufacturer=data['manufacturer'],
            model=data['model'],
            serial=data['serial'],
            manufacture_date=int(data['manufacture_date'])
        )
        db.session.add(new_instrument)
        db.session.commit()
        return jsonify({"message": "Instrument added successfully!", "instrument": new_instrument.to_dict()}), 201
    except ValueError:
        return jsonify({"error": "Invalid manufacture_date format"}), 400

# Route to get all instruments
@app.route('/instruments', methods=['GET'])
def get_instruments():
    instruments = Intrument.query.all()
    return jsonify([instrument.to_dict() for instrument in instruments])

# Route to get an instrument by tag_id
@app.route('/instrument/<int:tag_id>', methods=['GET'])
def get_instrument(tag_id):
    instrument = Intrument.query.get(tag_id)
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404
    return jsonify(instrument.to_dict())

# Route to delete an instrument by tag_id
@app.route('/delete_instrument/<int:tag_id>', methods=['DELETE'])
def delete_instrument(tag_id):
    instrument = Intrument.query.get(tag_id)
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404

    db.session.delete(instrument)
    db.session.commit()
    return jsonify({"message": "Instrument deleted successfully!"})

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0", debug=True)