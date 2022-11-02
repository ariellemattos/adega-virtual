import os
from database import *
from flask import request
from uuid import uuid4

# Cliente


def criar_cliente(nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone):
    cliente_ja_existe = db_verificar_cliente(cpf)
    if cliente_ja_existe is not None:
        return True, cliente_ja_existe
    cliente_novo = db_criar_cliente(
        nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone)
    return False, cliente_novo


def editar_cliente(id_cliente, nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone):
    cliente = db_consultar_cliente(id_cliente)

    db_editar_cliente(id_cliente, nomeCliente, cpf, cep, cidade,
                      rua, bairro, nResidencia, complemento, telefone)
    return 'alterado', cliente


def apagar_cliente(id_cliente):
    cliente = db_consultar_cliente(id_cliente)
    if cliente is not None:
        db_deletar_cliente(id_cliente)
    return cliente

# Adega


def criar_adega(nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone):
    adega_ja_existe = db_verificar_adega(cnpj)
    if adega_ja_existe is not None:
        return True, adega_ja_existe
    adega_nova = db_criar_adega(
        nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone)
    return False, adega_nova


def editar_adega(id_adega, nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone):
    adega = db_consultar_adega(id_adega)

    db_editar_adega(id_adega, nomeAdega, cnpj, cep, cidade, rua,
                    bairro, nEstabelecimento, complemento, telefone)
    return 'alterado', adega


def apagar_adega(id_adega):
    adega = db_consultar_adega(id_adega)
    if adega is not None:
        db_deletar_adega(id_adega)
    return adega


# Subir imagem
def pegar_extensao(filename):
    if not ('.' in filename):
        return ''
    return filename.rsplit('.', 1)[1].lower()


def subir_imagem_produto():
    if ("imagem" in request.files):
        image = request.files["imagem"]
        ext = pegar_extensao(image.filename)
        if (ext in ['jpg', 'jpeg', 'png', 'svg', 'webp']):
            filename = f"{uuid4()}.{ext}"
            image.save(os.path.join("static/uploads", filename))

            return f"/static/uploads/{filename}"

    return "/static/images/inserir-icone-de-imagem.png"



# Produto
def criar_produto(nomeProduto, preco, quantidade, img):
    produto_novo = db_criar_produto(nomeProduto, preco, quantidade, img)
    return False, produto_novo


def editar_produto(id_produto, nomeProduto, preco, quantidade, img):
    produto = db_consultar_produto(id_produto)
    
    if (img is None):
        img = produto['img']
    else:
        filepath = os.path.abspath(produto['img'].split('/', 1)[1])
        if os.path.exists(filepath):
            os.remove(filepath)

    db_editar_produto(id_produto, nomeProduto, preco, quantidade, img)
    return 'alterado', produto


def apagar_produto(id_produto):
    produto = db_consultar_produto(id_produto)
    if produto is not None:
        db_deletar_produto(id_produto)
    return produto
