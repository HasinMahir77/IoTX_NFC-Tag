import os
import sys
from flask import Flask
from models import db, Instrument, Storage

# Path manipulation to ensure we can import from the current directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import config
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def test_queries():
    with app.app_context():
        # Test 1: Count total instruments
        total_instruments = Instrument.query.count()
        print(f"Total instruments in database: {total_instruments}")
        
        # Test 2: Check if a specific tag_id exists (simulating NFC tag scan)
        tag_id = 42  # Example tag
        instrument = Instrument.query.filter_by(tag_id=tag_id).first()
        if instrument:
            print(f"\nTag ID {tag_id} is associated with:")
            print(f"  Name: {instrument.name}")
            print(f"  Manufacturer: {instrument.manufacturer}")
            print(f"  Model: {instrument.model}")
            print(f"  Serial: {instrument.serial}")
            print(f"  Year: {instrument.manufacture_date}")
            if instrument.storage:
                storage = Storage.query.get(instrument.storage_id)
                print(f"  Storage: {storage.name} ({storage.address})")
            else:
                print("  Storage: Unassigned")
        else:
            print(f"\nTag ID {tag_id} is not associated with any instrument")
            
        # Test 3: Find available tag IDs (not yet assigned)
        assigned_tags = [instr.tag_id for instr in Instrument.query.filter(Instrument.tag_id.isnot(None)).all()]
        print(f"\nTotal number of assigned tags: {len(assigned_tags)}")
        
        # Find some available tags (first 5 unassigned tags)
        available_tags = []
        for i in range(1, 500):
            if i not in assigned_tags:
                available_tags.append(i)
                if len(available_tags) >= 5:
                    break
        
        print(f"Sample available tag IDs: {available_tags}")
        
        # Test 4: Find instruments without tag IDs
        untagged = Instrument.query.filter(Instrument.tag_id.is_(None)).limit(5).all()
        print(f"\nSample of instruments without assigned tags:")
        for instr in untagged:
            print(f"  {instr.name} (SN: {instr.serial})")
        
        # Test 5: Find instruments by serial number (for pairing)
        serial_example = Instrument.query.limit(1).first().serial
        print(f"\nSearching for instrument with serial: {serial_example}")
        
        instrument = Instrument.query.filter_by(serial=serial_example).first()
        if instrument:
            print(f"  Found: {instrument.name} (Tag ID: {instrument.tag_id or 'None'})")
            
            # Test 6: Simulate assigning a tag to this instrument if not already assigned
            if instrument.tag_id is None:
                instrument.tag_id = available_tags[0] if available_tags else 999
                db.session.commit()
                print(f"  Tagged instrument with ID: {instrument.tag_id}")
        
        # Test 7: Get instruments by storage
        storage1 = Storage.query.filter_by(name="Storage 1").first()
        if storage1:
            count = Instrument.query.filter_by(storage_id=storage1.id).count()
            print(f"\nInstruments in {storage1.name}: {count}")
            
            # Get 3 sample instruments from Storage 1
            instruments = Instrument.query.filter_by(storage_id=storage1.id).limit(3).all()
            for instr in instruments:
                print(f"  {instr.name} (SN: {instr.serial})")

if __name__ == "__main__":
    test_queries() 