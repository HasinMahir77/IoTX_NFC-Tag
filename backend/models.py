from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Instrument(db.Model):  # Corrected typo in class name
    dbid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_id = db.Column(db.Integer, nullable=True)  
    name = db.Column(db.String(30), nullable=False)
    manufacturer = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    serial = db.Column(db.String(30), nullable=False)
    manufacture_date = db.Column(db.Integer, nullable=False)
    storage_id = db.Column(db.Integer, db.ForeignKey('storage.id'), nullable=True)  # Nullable foreign key

    def to_dict(self):
        return {
            "dbid": self.dbid,
            "tag_id": self.tag_id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial": self.serial,
            "manufacture_date": self.manufacture_date,
            "storage": self.storage.name if self.storage else "Unassigned"  # Include storage name or None
        }

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-assigned integer ID
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    instruments = db.relationship('Instrument', backref='storage', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "instruments": [instrument.to_dict() for instrument in self.instruments]
        }