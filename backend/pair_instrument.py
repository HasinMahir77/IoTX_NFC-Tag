import os
import sys
from flask import Flask, request, jsonify
from models import db, Instrument, Storage

# Path manipulation to ensure we can import from the current directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import config
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/nfc/pair_instrument', methods=['POST'])
def pair_instrument():
    """
    Pair an NFC tag with an instrument using the serial number
    
    Request body:
    {
        "tag_id": 123,          # The NFC tag ID to pair
        "serial": "123456789"   # The serial number of the instrument to pair with
    }
    
    Response:
    {
        "success": true/false,
        "message": "Success/error message",
        "instrument": {instrument_data} # If successful
    }
    """
    data = request.json
    
    if not data or 'tag_id' not in data or 'serial' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: tag_id and serial"
        }), 400
    
    tag_id = data['tag_id']
    serial = data['serial']
    
    # Check if the tag is already paired
    existing_tag = Instrument.query.filter_by(tag_id=tag_id).first()
    if existing_tag:
        return jsonify({
            "success": False,
            "message": f"Tag ID {tag_id} is already paired with instrument: {existing_tag.name}"
        }), 409
    
    # Find the instrument by serial number
    instrument = Instrument.query.filter_by(serial=serial).first()
    if not instrument:
        return jsonify({
            "success": False,
            "message": f"No instrument found with serial number: {serial}"
        }), 404
    
    # Check if the instrument is already paired with a different tag
    if instrument.tag_id is not None:
        return jsonify({
            "success": False,
            "message": f"This instrument is already paired with tag ID: {instrument.tag_id}"
        }), 409
    
    # Pair the instrument with the tag
    instrument.tag_id = tag_id
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": f"Successfully paired tag ID {tag_id} with {instrument.name}",
        "instrument": instrument.to_dict()
    }), 200

@app.route('/nfc/check_tag/<int:tag_id>', methods=['GET'])
def check_tag(tag_id):
    """
    Check if a tag ID is already paired with an instrument
    
    Response:
    {
        "is_paired": true/false,
        "instrument": {instrument_data} # If paired
    }
    """
    instrument = Instrument.query.filter_by(tag_id=tag_id).first()
    
    if instrument:
        return jsonify({
            "is_paired": True,
            "instrument": instrument.to_dict()
        }), 200
    else:
        return jsonify({
            "is_paired": False
        }), 200

@app.route('/nfc/search_serial/<string:serial>', methods=['GET'])
def search_instrument_by_serial(serial):
    """
    Search for an instrument by serial number (for pairing process)
    
    Response:
    {
        "found": true/false,
        "instrument": {instrument_data} # If found
    }
    """
    instrument = Instrument.query.filter_by(serial=serial).first()
    
    if instrument:
        return jsonify({
            "found": True,
            "instrument": instrument.to_dict(),
            "is_paired": instrument.tag_id is not None
        }), 200
    else:
        return jsonify({
            "found": False
        }), 200

@app.route('/nfc/unpair_tag/<int:tag_id>', methods=['DELETE'])
def unpair_tag(tag_id):
    """
    Remove pairing between a tag and an instrument
    
    Response:
    {
        "success": true/false,
        "message": "Success/error message"
    }
    """
    instrument = Instrument.query.filter_by(tag_id=tag_id).first()
    
    if not instrument:
        return jsonify({
            "success": False,
            "message": f"No instrument found paired with tag ID: {tag_id}"
        }), 404
    
    # Store instrument info for the response message
    instrument_name = instrument.name
    
    # Remove the pairing
    instrument.tag_id = None
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": f"Successfully unpaired tag ID {tag_id} from {instrument_name}"
    }), 200

if __name__ == "__main__":
    with app.app_context():
        # Make sure we have data to work with
        if Instrument.query.count() == 0:
            print("No instruments found in the database. Please run seed_database.py first.")
        else:
            # Show some example instruments for testing
            untagged = Instrument.query.filter(Instrument.tag_id.is_(None)).limit(5).all()
            print("Example instruments for pairing tests:")
            for i, instr in enumerate(untagged, 1):
                print(f"{i}. {instr.name} - Serial: {instr.serial}")
    
    # Start the API service on a different port to avoid conflict with main.py
    app.run(port=5002, debug=True) 