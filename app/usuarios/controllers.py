from flask import request, Blueprint
from ..extensions import db
from .model import Usuarios
from ..pagamentos.model import Pagamentos

usuario_api = Blueprint('usuario_api', __name__)

@usuario_api.route('/registrar', methods=['POST'])
def registrarUsuario():
    if request.method == 'POST':
        dados = request.json

        nome = dados.get('nome')
        data_nasc = dados.get('data_nasc')
        cpf = dados.get('cpf')
        senha = dados.get('senha')

        if nome == '' or nome == None:
            return{"Erro":"Nome é obrigatório"}, 400

        if senha == '' or senha == None:
            return{"Erro":"Senha obrigatório"}, 400

        if data_nasc == '' or data_nasc == None:
            return{"Erro":"Problema na Data de Nascimento"}, 400

        if cpf == '' or cpf == None:
            return{"Erro":"CPF obrigatório"}, 400
        if Usuarios.query.filter_by(cpf=cpf).first():
            return{"Erro": "CPF já cadastrado"},400

        usuario = Usuarios(nome=nome, data_nasc=data_nasc, cpf=cpf, senha=senha)
        db.session.add(usuario)
        db.session.commit()

        return usuario.json(), 200


@usuario_api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        dados = request.json

        nome = dados.get('nome')
        senha = dados.get('senha')

        if nome == '' or nome == None:
            return{"Erro":"Nome é obrigatório"}, 400

        if senha == '' or senha == None:
            return{"Erro":"Senha obrigatória"}, 400

        usuario = Usuarios.query.filter_by(nome=nome, senha=senha).first() # .first_or_404()
        if not usuario:
            return{"Erro": "Usuário não cadastrado"},400

        return usuario.json(), 200


@usuario_api.route('/cartao', methods=['POST'])
def registrarCartao():
    if request.method == 'POST':
        dados = request.json

        nome = dados.get('nome')
        senha = dados.get('senha')
        numero_cartao = dados.get('numero_cartao')
        cvv = dados.get('cvv')

        if nome == '' or nome == None:
            return{"Erro":"Nome é obrigatório"}, 400

        if senha == '' or senha == None:
            return{"Erro":"Senha obrigatória"}, 400

        if numero_cartao == '' or numero_cartao == None:
            return{"Erro":"Cartão é obrigatório"}, 400

        if cvv == '' or cvv == None:
            return{"Erro":"Cvv obrigatório"}, 400

        usuario = Usuarios.query.filter_by(nome=nome,senha=senha).first()
        if not usuario:
            return{"Erro": "Usuário não cadastrado ou usuário/senha incorreto(a)"},400
        
        if Pagamentos.query.filter_by(numero_cartao=numero_cartao, owner_id=usuario.id).first():
            return{"Erro":"Cartão já cadastrado"},400

        cartao = Pagamentos(numero_cartao=numero_cartao, cvv=cvv, owner=usuario)
        db.session.add(cartao)
        db.session.commit()

        return usuario.json(), 200

# Fazer funções para atualizar os dados.