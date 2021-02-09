from ..extensions import db

class Pagamentos(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    numero_cartao = db.Column(db.String(16), unique=True)
    cvv = db.Column(db.String(3))