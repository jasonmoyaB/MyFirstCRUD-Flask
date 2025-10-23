# models.py
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    instructor = db.Column(db.String(100), unique=True, nullable=False)
    topico = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Curso {self.nombre}>"
