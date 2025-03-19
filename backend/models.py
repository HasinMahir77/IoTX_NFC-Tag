from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Guitar(db.Model):
    tag_id = db.Column(db.String(8), primary_key=True)  # Update tag_id to be a string with a fixed length
    name = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    manufacture_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "tag_id": self.tag_id,
            "name": self.name,
            "model": self.model,
            "manufacture_year": self.manufacture_year
        }