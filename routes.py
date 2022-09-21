from flask import Flask, make_response, request, render_template, redirect, Response,  flash

from database import *
from services import *

app = Flask(__name__, static_folder='static')

@app.route("/")
@app.route("/realizarLogin")
def menu():
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro = "")

    return render_template("/index.html", logado = logado, mensagem = "")

@app.route("/realizarLogin", methods = ["POST"])
def realizar_login():
    f = request.form
    if "login" not in f or "senha" not in f:
        return ":(", 422
    login = f["login"]
    senha = f["senha"]

    logado = db_fazer_login(login, senha)

    if logado is None:
        return render_template("login.html", erro = "E-mail ou senha incorretos")
    resposta = make_response(redirect("/"))

    resposta.set_cookie("login", login, samesite = "Strict")
    resposta.set_cookie("senha", senha, samesite = "Strict")
    return resposta

@app.route("/logout", methods = ["POST"])
def logout():
    resposta = make_response(render_template("login.html"))

    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta

@app.route("/adega/cadastro", methods = ["GET"])
def form_criar_adega_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    adega = {
        'id_adega': 'cadastro', 
        'nomeAdega': '', 
        'cnpj': '', 
        'cep': '', 
        'cidade': '',
        'rua': '',
        'bairro': '',
        'nEstabelecimento': '',
        'complemento': '',
        'telefone': ''
        
        }

    return render_template("cadastro-adega.html", logado = logado, adega = adega)

@app.route("/adega/cadastro", methods = ["POST"])
def criar_adega_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    nomeAdega = request.form["nomeAdega"]
    cnpj = request.form["cnpj"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nEstabelecimento = request.form["nEstabelecimento"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    ja_existia, adega = criar_adega(nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone)

    mensagem = f"A adega {cnpj} já existe com o id {adega['id_adega']}." if ja_existia else f"A adega {cnpj} foi criada com id {adega['id_adega']}"
    return render_template("index.html", logado = logado, mensagem = mensagem)
    

# Tela de listagem de adegas.
@app.route("/adegas")
def listar_adegas_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    lista = db_listar_adegas()

    return render_template("lista-adegas.html", logado = logado, adegas = lista)

@app.route("/adega/<int:id_adega>", methods = ["GET"])
def form_alterar_adega_api(id_adega):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    adega = db_consultar_adega(id_adega)

    return render_template("cadastro-adega.html", logado = logado, adega = adega)

@app.route("/adega/<int:id_adega>", methods = ["POST"])
def editar_adega_api(id_adega):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    nomeAdega = request.form["nomeAdega"]
    cnpj = request.form["cnpj"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nEstabelecimento = request.form["nEstabelecimento"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    editar_adega(id_adega, nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone)

    return redirect("/adegas")

@app.route("/adega/<int:id_adega>", methods = ["DELETE"])
def excluir_adega_api(id_adega):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    apagar_adega(id_adega)
    return Response(status=204)

@app.route("/cliente/cadastro", methods = ["GET"])
def form_criar_cliente_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    cliente = {
        'id_cliente': 'cadastro', 
        'nomeCliente': '', 
        'cpf': '', 
        'cep': '', 
        'cidade': '',
        'rua': '',
        'bairro': '',
        'nResidencia': '',
        'complemento': '',
        'telefone': ''
        
        }

    return render_template("cadastro-cliente.html", logado = logado, cliente = cliente)

@app.route("/cliente/cadastro", methods = ["POST"])
def criar_cliente_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    nomeCliente = request.form["nomeCliente"]
    cpf = request.form["cpf"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nResidencia = request.form["nResidencia"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    ja_existia, cliente = criar_cliente(nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone)

    mensagem = f"O cliente {cpf} já existe com o id {cliente['id_cliente']}." if ja_existia else f"O cliente {cpf} foi criada com id {cliente['id_cliente']}."
    return render_template("index.html", logado = logado, mensagem = mensagem)

@app.route("/clientes")
def listar_clientes_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    lista = db_listar_clientes()

    return render_template("lista-clientes.html", logado = logado, clientes = lista)

@app.route("/cliente/<int:id_cliente>", methods = ["GET"])
def form_alterar_cliente_api(id_cliente):

    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    cliente = db_consultar_cliente(id_cliente)

    return render_template("cadastro-cliente.html", logado = logado, cliente = cliente)

@app.route("/cliente/<int:id_cliente>", methods = ["POST"])
def editar_cliente_api(id_cliente):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    nomeCliente = request.form["nomeCliente"]
    cpf = request.form["cpf"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nResidencia = request.form["nResidencia"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    editar_cliente(id_cliente, nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone)

    return redirect("/clientes")

@app.route("/produto/cadastro", methods = ["GET"])
def form_criar_produto_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    produto = {
        'id_produto': 'cadastro', 
        'nomeProduto': '', 
        'preco': '', 
        'quantidade': ''        
        }

    return render_template("cadastro-produto.html", logado = logado, produto = produto)

@app.route("/cliente/<int:id_cliente>", methods = ["DELETE"])
def excluir_cliente_api(id_cliente):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    apagar_cliente(id_cliente)
    return Response(status=204)

@app.route("/produto/cadastro", methods = ["POST"])
def criar_produto_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    nomeProduto = request.form["nomeProduto"]
    preco = request.form["preco"]
    quantidade = request.form["quantidade"]

    criar_produto(nomeProduto, preco, quantidade)

    return render_template("index.html", logado = logado)
    

@app.route("/produtos")
def listar_produtos_api():
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    lista = db_listar_produtos()

    return render_template("lista-produtos.html", logado = logado, produtos = lista)

@app.route("/produto/<int:id_produto>", methods = ["GET"])
def form_alterar_produto_api(id_produto):

    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    produto = db_consultar_produto(id_produto)

    return render_template("cadastro-produto.html", logado = logado, produto = produto)

@app.route("/produto/<int:id_produto>", methods = ["POST"])
def editar_produto_api(id_produto):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    nomeProduto = request.form["nomeProduto"]
    preco = request.form["preco"]
    quantidade = request.form["quantidade"]

    editar_produto(id_produto, nomeProduto, preco, quantidade)

    return redirect("/produtos")

@app.route("/produto/<int:id_produto>", methods = ["DELETE"])
def excluir_produto_api(id_produto):
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    apagar_produto(id_produto)
    return Response(status=204)

def autenticar_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return db_fazer_login(login, senha)


if __name__ == "__main__":
    db_inicializar()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()