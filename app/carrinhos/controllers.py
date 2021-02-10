from flask import request, Blueprint, jsonify
from ..extensions import db
from .model import Carrinhos
from ..produtos.model import Produtos
from ..usuarios.model import Usuarios

carrinhos_api = Blueprint('carrinhos_api', __name__)


@carrinhos_api.route('/carrinho/<int:id>', methods=['POST','GET','DELETE'])
def index(id):
    if request.method == 'POST': # recebe "produto"
        # Vai receber o produto a ser adicionado e o usuario 
        dados = request.json
        nome_produto = dados.get('produto')
        #cpf_user = dados.get('cpf')

        #if cpf_user == '' or cpf_user == None:
         #   return{"Erro":"CPF obrigatório (formato: xxx.xxx.xxx-xx)"}, 400
        
        if nome_produto == '' or nome_produto == None:
            return{"Erro":"Nome do produto é obrigatório"}, 400
        
        user = Usuarios.query.get_or_404(id)
        #user = Usuarios.query.filter_by(cpf=cpf_user).first()
        #if not user:
         #   return{"Erro": "Usuário não cadastrado"}, 400
        
        produto = Produtos.query.filter_by(nome=nome_produto).first()
        if not produto:
            return{"Erro": "Produto não cadastrado"}, 400

        if user.carrinho:
            carrinho = user.carrinho
            carrinho.produtos.append(produto)
            db.session.commit()
        else:
            carrinho = Carrinhos(usuario=user)
            carrinho.produtos.append(produto)
            db.session.add(carrinho)
            db.session.commit()

        return carrinho.json(), 200

    if request.method == 'GET':
        # Vai receber o cpf da pessoa alvo
        dados = request.json
        cpf = dados.get('cpf')

        if cpf == '' or cpf == None:
            return{"Erro":"CPF obrigatório (formato: xxx.xxx.xxx-xx)"}, 400
        
        user = Usuarios.query.filter_by(cpf=cpf).first()
        if not user:
            return{"Erro": "Usuário não cadastrado"}, 400
        
        if not user.carrinho:
            return{"Erro":"Carrinho Vazio"}, 400

        return jsonify([produto.json() for produto in user.carrinho.produtos])

    if request.method == 'DELETE':
        # Vai esvaziar o carrinho. Recebe o cpf da pessoa
        dados = request.json
        cpf = dados.get('cpf')

        if cpf == '' or cpf == None:
            return{"Erro":"CPF obrigatório (formato: xxx.xxx.xxx-xx)"}, 400
        
        user = Usuarios.query.filter_by(cpf=cpf).first()
        if not user:
            return{"Erro": "Usuário não cadastrado"}, 400

        if not user.carrinho:
            return{"Erro":"Carrinho já está Vazio"}, 400
        
        for produto in user.carrinho.produtos:
            print(produto)
            db.session.delete(produto)
            db.session.commit()

        return user.json(), 200