from flask import request, Blueprint
from ..extensions import db
from .model import Usuarios

usuario_api = Blueprint('usuario_api', __name__)

@usuario_api.route('/registrar', methods=['POST'])
def registrar():
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

        usuario = Usuarios.query.filter_by(nome=nome, senha=senha).first_or_404()

        return usuario.json(), 200