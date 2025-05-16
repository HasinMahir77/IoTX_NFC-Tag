from models import db, Instrument
from main import app
import random

def generate_serial():
    manufacturers = ['F', 'G', 'M', 'I', 'Y', 'T', 'S', 'R', 'P', 'C']
    return f"{random.choice(manufacturers)}{random.randint(100000, 999999)}"

def generate_instrument():
    manufacturers = ['Fender', 'Gibson', 'Martin', 'Ibanez', 'Yamaha', 'Taylor', 'Seagull', 'Rickenbacker', 'PRS', 'Cort']
    models = {
        'Fender': ['Stratocaster', 'Telecaster', 'Jazzmaster', 'Mustang', 'Precision Bass'],
        'Gibson': ['Les Paul', 'SG', 'ES-335', 'Flying V', 'Explorer'],
        'Martin': ['D-28', 'D-18', 'OM-28', '000-28', 'HD-28'],
        'Ibanez': ['RG', 'S', 'AZ', 'Artcore', 'SR'],
        'Yamaha': ['FG', 'LL', 'A', 'Pacifica', 'Revstar'],
        'Taylor': ['214ce', '314ce', '414ce', '514ce', '614ce'],
        'Seagull': ['S6', 'Entourage', 'Artist', 'Performer', 'Coastline'],
        'Rickenbacker': ['330', '360', '4003', '620', '480'],
        'PRS': ['Custom 24', 'McCarty', 'SE', 'S2', 'Mira'],
        'Cort': ['G', 'CR', 'L', 'X', 'Earth']
    }
    
    manufacturer = random.choice(manufacturers)
    model = random.choice(models[manufacturer])
    name = f"{manufacturer} {model}"
    
    return Instrument(
        name=name,
        manufacturer=manufacturer,
        model=model,
        serial=generate_serial(),
        manufacture_date=random.randint(2010, 2024),
        storage=None,
        tag_id=None
    )

def seed_database():
    with app.app_context():
        # Clear existing data
        Instrument.query.delete()
        
        # Generate 350 instruments
        instruments = [generate_instrument() for _ in range(350)]
        
        # Add all instruments to the database
        db.session.add_all(instruments)
        db.session.commit()
        print("Database seeded successfully with 350 instruments!")

if __name__ == "__main__":
    seed_database() 