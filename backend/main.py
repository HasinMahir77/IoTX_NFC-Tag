import os
from config import Config
from flask_cors import CORS
from models import db, Intrument
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file

# Define the upload folder relative to the current file's directory
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'userImages')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)
CORS(app)  # Enable CORS
db.init_app(app)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create database tables (only needed for first-time setup)
with app.app_context():
    db.create_all()

# Route to add a new instrument
@app.route('/add_instrument', methods=['POST'])
def add_instrument():
    data = request.json
    print(data)
    required_fields = ["tag_id", "name", "manufacturer", "model", "serial", "manufacture_date"]
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": f"Missing fields: {', '.join([k for k in required_fields if k not in data])}"}), 400

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
        return jsonify({"error": "Invalid manufacture_date format"}), 407

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
    return jsonify(instrument.to_dict()), 200

# Route to delete an instrument by tag_id
@app.route('/delete_instrument/<int:tag_id>', methods=['DELETE'])
def delete_instrument(tag_id):
    instrument = Intrument.query.get(tag_id)
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404

    db.session.delete(instrument)
    db.session.commit()
    return jsonify({"message": "Instrument deleted successfully!"})

# Route to upload an image for an instrument
@app.route('/upload_image/<int:tag_id>', methods=['POST'])
def upload_image(tag_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{tag_id}.jpg")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Image uploaded successfully!"}), 201
    else:
        return jsonify({"error": "File type not allowed"}), 400
    
# Route to check if an image exists and return it
@app.route('/check_image/<int:tag_id>', methods=['GET'])
def check_image(tag_id):
    filename = secure_filename(f"{tag_id}.jpg")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg')
    else:
        return jsonify({"exists": False}), 404
    
# Route to check if an instrument exists by tag_id
@app.route('/instrument_exists/<int:tag_id>', methods=['GET'])
def instrument_exists(tag_id):
    instrument = Intrument.query.get(tag_id)
    if instrument:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 404


if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0", debug=True)