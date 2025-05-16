import os
from config import Config
from flask_cors import CORS
from models import db, Instrument, Storage
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file

# Constants
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'userImages')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Flask App Setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)

# CORS Configuration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Database Setup
db.init_app(app)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper Functions
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_instrument_by_id_or_tag(id):
    """Get instrument by dbid or tag_id."""
    return Instrument.query.get(id) or Instrument.query.filter_by(tag_id=id).first()

# Database Initialization
with app.app_context():
    db.create_all()

# Instrument Management Routes
@app.route('/nfc/add_instrument', methods=['POST'])
def add_instrument():
    """Add a new instrument to the database."""
    data = request.json
    required_fields = ["name", "manufacturer", "model", "serial", "manufacture_date"]
    
    if not data or not all(k in data for k in required_fields):
        return jsonify({
            "error": f"Missing fields: {', '.join([k for k in required_fields if k not in data])}"
        }), 400

    try:
        new_instrument = Instrument(
            tag_id=data.get('tag_id'),
            name=data['name'],
            manufacturer=data['manufacturer'],
            model=data['model'],
            serial=data['serial'],
            manufacture_date=int(data['manufacture_date'])
        )
        db.session.add(new_instrument)
        db.session.commit()
        return jsonify({
            "message": "Instrument added successfully!",
            "instrument": new_instrument.to_dict()
        }), 201
    except ValueError:
        return jsonify({"error": "Invalid manufacture_date format"}), 407

@app.route('/nfc/instruments', methods=['GET'])
def get_instruments():
    """Get all instruments."""
    instruments = Instrument.query.all()
    return jsonify([instrument.to_dict() for instrument in instruments])

@app.route('/nfc/instrument/<int:id>', methods=['GET'])
@app.route('/nfc/instrument_by_tag/<int:id>', methods=['GET'])
def get_instrument(id):
    """Get instrument by dbid or tag_id."""
    instrument = get_instrument_by_id_or_tag(id)
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404
    return jsonify(instrument.to_dict()), 200

@app.route('/nfc/delete_instrument/<int:dbid>', methods=['DELETE'])
def delete_instrument(dbid):
    """Delete an instrument by dbid."""
    instrument = Instrument.query.get(dbid)
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404
    db.session.delete(instrument)
    db.session.commit()
    return jsonify({"message": "Instrument deleted successfully!"})

# Image Management Routes
@app.route('/nfc/upload_image/<int:dbid>', methods=['POST'])
def upload_image(dbid):
    """Upload an image for an instrument."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{dbid}.jpg")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Image uploaded successfully!"}), 201
    
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/nfc/check_image/<int:dbid>', methods=['GET'])
def check_image(dbid):
    """Check if an image exists for an instrument."""
    filename = secure_filename(f"{dbid}.jpg")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg')
    return jsonify({"exists": False}), 404

# Tag Management Routes
@app.route('/nfc/instrument_exists/<int:tag_id>', methods=['GET'])
def instrument_exists(tag_id):
    """Check if an instrument exists for a given tag_id."""
    try:
        instrument = Instrument.query.filter_by(tag_id=tag_id).first()
        if instrument:
            return jsonify({
                "exists": True,
                "instrument": instrument.to_dict()
            }), 200
        return jsonify({"exists": False}), 200
    except Exception as e:
        print(f"Error in instrument_exists: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/nfc/pair_instrument', methods=['POST', 'OPTIONS'])
def pair_instrument():
    """Pair a tag with an instrument."""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        if not data or 'tag_id' not in data or 'serial' not in data:
            return jsonify({
                "error": "Missing required fields: tag_id and serial"
            }), 400
        
        tag_id = data['tag_id']
        serial = data['serial']
        
        # Check if tag is already paired
        existing_tag = Instrument.query.filter_by(tag_id=tag_id).first()
        if existing_tag:
            return jsonify({
                "error": f"Tag ID {tag_id} is already paired with instrument: {existing_tag.name}"
            }), 409
        
        # Find instrument by serial
        instrument = Instrument.query.filter_by(serial=serial).first()
        if not instrument:
            return jsonify({
                "error": f"No instrument found with serial number: {serial}"
            }), 404
        
        # Check if instrument is already paired
        if instrument.tag_id is not None:
            return jsonify({
                "error": f"This instrument is already paired with tag ID: {instrument.tag_id}"
            }), 409
        
        # Perform pairing
        instrument.tag_id = tag_id
        db.session.commit()
        return jsonify({
            "message": f"Successfully paired tag ID {tag_id} with {instrument.name}",
            "instrument": instrument.to_dict()
        }), 200
    except Exception as e:
        print(f"Error in pair_instrument: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/nfc/unpair_tag/<int:tag_id>', methods=['DELETE'])
def unpair_tag(tag_id):
    """Unpair a tag from its instrument."""
    instrument = Instrument.query.filter_by(tag_id=tag_id).first()
    if not instrument:
        return jsonify({
            "error": f"No instrument found paired with tag ID: {tag_id}"
        }), 404
    
    instrument_name = instrument.name
    instrument.tag_id = None
    db.session.commit()
    return jsonify({
        "message": f"Successfully unpaired tag ID {tag_id} from {instrument_name}"
    }), 200

# Storage Management Routes
@app.route('/nfc/update_storage/<int:dbid>', methods=['PUT'])
def update_instrument_storage(dbid):
    """Update the storage location of an instrument."""
    data = request.json
    if not data or 'storage_id' not in data:
        return jsonify({
            "error": "Missing 'storage_id' in request body"
        }), 400

    instrument = Instrument.query.get(dbid)
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404

    storage = Storage.query.get(data['storage_id'])
    if not storage and data['storage_id'] is not None:
        return jsonify({"error": "Storage not found"}), 404

    instrument.storage = storage
    db.session.commit()
    return jsonify({
        "message": "Instrument storage updated successfully!",
        "instrument": instrument.to_dict()
    }), 200

if __name__ == '__main__':
    app.run(port=7100, host="0.0.0.0", debug=True)