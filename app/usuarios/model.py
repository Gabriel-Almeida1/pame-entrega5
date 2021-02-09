from ..extensions import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), nullable=False)
    data_nasc = db.Column(db.String(10), nullable=False) # Formato padrão: xx/xx/xxxx
    cpf = db.Column(db.String(14), nullable=False, unique=True) # Formato com os pontos em hífen: 576.576.576-57

    # Considerando que o cliente pode querer cadastrar múltiplas formas de pagamento
    pagamentos = db.relationship('Pagamentos', backref='owner') # One (Usuario) to many (pagamentos)