import random
import string
import os
import sys
from datetime import datetime
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

# Guitar manufacturers and their common models
manufacturers = {
    "Taylor": [
        "110e", "114e", "150e", "214ce", "224ce-K DLX", "254ce", 
        "314ce", "322e", "414ce", "456ce", "514ce", "562ce", 
        "614ce", "714ce", "812ce", "814ce", "K24ce", "GS Mini",
        "Baby Taylor", "T5z", "T3", "Academy 12", "Academy 10"
    ],
    "Martin": [
        "D-18", "D-28", "D-35", "D-41", "D-45", "HD-28", 
        "000-15M", "000-18", "000-28", "OM-21", "OM-28", "OM-42",
        "SC-13E", "DC-16E", "LX1", "00L-17", "D-16E", "D Jr",
        "Backpacker", "Little Martin", "Road Series", "X Series"
    ],
    "Gibson": [
        "J-45", "Hummingbird", "SJ-200", "L-00", "J-15", "J-200",
        "ES-335", "ES-175", "Les Paul Standard", "SG Standard", 
        "Flying V", "Explorer", "Firebird", "Nighthawk", "ES-339"
    ],
    "Fender": [
        "Stratocaster", "Telecaster", "Jazzmaster", "Jaguar", "Mustang",
        "American Professional", "Player Series", "Vintera", "Ultra", 
        "Custom Shop", "American Original", "Acoustasonic", "Newporter", "Malibu"
    ],
    "PRS": [
        "Custom 24", "Custom 22", "McCarty 594", "CE 24", "S2 Standard",
        "SE Custom 24", "SE Standard", "SE Hollowbody", "SE Custom 22"
    ],
    "Ibanez": [
        "RG550", "S Series", "AZ Series", "AR Series", "Artcore", 
        "Prestige", "Premium", "PIA", "JEM", "RGD", "RGA", "AE Series"
    ],
    "Gretsch": [
        "White Falcon", "Duo Jet", "Country Gentleman", "Nashville", 
        "Electromatic", "Streamliner", "G5420T", "G6120", "G2622"
    ],
    "Epiphone": [
        "Casino", "Dot", "Les Paul Standard", "SG Standard", "Sheraton",
        "Texan", "DR-100", "Hummingbird", "Inspired by Gibson"
    ]
}

# Generate random serial numbers based on manufacturer
def generate_serial(manufacturer, year):
    if manufacturer == "Taylor":
        # 10-digit format (2009-present)
        if year >= 2009:
            factory = random.choice(["1", "2"])  # 1 for El Cajon, 2 for Mexico
            y1 = str(year)[2]  # Third digit of year
            y2 = str(year)[3]  # Fourth digit of year
            month = f"{random.randint(1, 12):02d}"
            day = f"{random.randint(1, 28):02d}"
            sequence = f"{random.randint(0, 999):03d}"
            return f"{factory}{y1}{month}{day}{y2}{sequence}"
        # 9-digit format (1993-1999)
        elif 1993 <= year <= 1999:
            yy = str(year)[2:]  # Last two digits
            month = f"{random.randint(1, 12):02d}"
            day = f"{random.randint(1, 28):02d}"
            series = random.choice(["0", "1", "2", "3", "7", "8"])
            sequence = f"{random.randint(0, 99):02d}"
            return f"{yy}{month}{day}{series}{sequence}"
        # 5-digit format (classic)
        else:
            return f"{random.randint(5000, 17000)}"
    
    elif manufacturer == "Martin":
        # Standard Martin format
        if year >= 2000:
            base = {
                2000: 724078, 2001: 780501, 2002: 845645, 2003: 916760,
                2004: 978707, 2005: 1042559, 2006: 1115863, 2007: 1197800,
                2008: 1268092, 2009: 1337043, 2010: 1406716, 2011: 1473462,
                2012: 1555768, 2013: 1656743, 2014: 1755537, 2015: 1857400,
                2016: 1972130, 2017: 2076796, 2018: 2161733, 2019: 2258890,
                2020: 2366881, 2021: 2440000, 2022: 2576416, 2023: 2711441
            }.get(year, 2800000)
            
            offset = random.randint(0, 50000)
            return f"{base + offset}"
        else:
            return f"{random.randint(300000, 700000)}"
    
    elif manufacturer == "Gibson":
        if year >= 2000:
            # Modern Gibson YDDDYRRRRR format (Y=last digit of year, DDD=day of year, RRRRR=ranking number)
            y = str(year)[-1]
            ddd = f"{random.randint(1, 365):03d}"
            rrrrr = f"{random.randint(1, 999):03d}"
            return f"{y}{ddd}{y}{rrrrr}"
        else:
            # Historical format
            return ''.join(random.choices(string.digits, k=8))
    
    else:
        # Generic serial number with year prefix
        year_prefix = str(year)[-2:]
        return f"{year_prefix}{random.randint(100000, 999999)}"

# Generate a random name for an instrument
def generate_name(manufacturer, model):
    adjectives = ["Vintage", "Classic", "Custom", "Special", "Signature", "Elite", "Premium", "Standard", "Professional", "Deluxe"]
    if random.random() < 0.7:  # 70% chance to get a name
        return f"{random.choice(adjectives)} {manufacturer} {model}"
    else:
        # Just use manufacturer and model
        return f"{manufacturer} {model}"

# Main function to seed the database
def seed_database():
    with app.app_context():
        print("Clearing existing data...")
        # Clear existing data
        db.session.query(Instrument).delete()
        db.session.commit()
        
        # Make sure we have our storage locations
        if not Storage.query.filter_by(name="Storage 1").first():
            storage1 = Storage(name="Storage 1", address="123 Main St, Suite A, Anytown, CA 12345")
            db.session.add(storage1)
        
        if not Storage.query.filter_by(name="Storage 2").first():
            storage2 = Storage(name="Storage 2", address="456 Oak Ave, Building B, Somewhere, CA 67890")
            db.session.add(storage2)
            
        if not Storage.query.filter_by(name="Storage 3").first():
            storage3 = Storage(name="Storage 3", address="789 Pine Dr, Warehouse C, Otherplace, CA 54321")
            db.session.add(storage3)
        
        db.session.commit()
        
        print("Creating 350 fake instruments...")
        # Create 350 instruments
        instruments = []
        
        for i in range(350):
            manufacturer = random.choice(list(manufacturers.keys()))
            model = random.choice(manufacturers[manufacturer])
            year = random.randint(1980, 2023)
            serial = generate_serial(manufacturer, year)
            
            # No storage or tag_id assigned initially
            instrument = Instrument(
                tag_id=None,  # No tag_id assigned
                name=generate_name(manufacturer, model),
                manufacturer=manufacturer,
                model=model,
                serial=serial,
                manufacture_date=year,
                storage_id=None  # No storage assigned
            )
            
            instruments.append(instrument)
        
        # Add all instruments to the database
        db.session.add_all(instruments)
        db.session.commit()
        
        print(f"Successfully added 350 instruments to the database.")
        
        # Display some stats
        tagged_count = db.session.query(Instrument).filter(Instrument.tag_id.isnot(None)).count()
        untagged_count = db.session.query(Instrument).filter(Instrument.tag_id.is_(None)).count()
        print(f"Tagged instruments: {tagged_count}")
        print(f"Untagged instruments: {untagged_count}")
        
        # Manufacturers count
        for manufacturer in manufacturers.keys():
            count = db.session.query(Instrument).filter_by(manufacturer=manufacturer).count()
            print(f"{manufacturer}: {count} instruments")

if __name__ == "__main__":
    seed_database() 