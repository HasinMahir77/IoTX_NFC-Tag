from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Intrument(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(30), nullable=False)
    manufacturer = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    serial = db.Column(db.String(30), nullable=False)
    manufacture_date = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "tag_id": self.tag_id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial": self.serial,
            "manufacture_date": self.manufacture_date
        }