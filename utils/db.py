from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicializamos SQLAlchemy
db = SQLAlchemy()

# Inizializamos marshmallow
ma = Marshmallow()

# Modelo db 
class Chistes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chiste = db.Column(db.String(300))
    tipo_chiste = db.Column(db.String(8))

    def __init__(self, chiste, tipo_chiste):
        self.chiste = chiste
        self.tipo_chiste = tipo_chiste

# Schema db
class ChistesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'chiste', 'tipo_chiste')
        
