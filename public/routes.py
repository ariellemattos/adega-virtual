from flask import Flask, make_response, request, render_template, redirect, Response

from createDatabase import *
from functionsDatabase import *

# Cria o objeto principal do Flask.
app = Flask(__name__, static_folder='assets')

@app.route("/")
@app.route("/realizarLogin")
def menu():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro = "")

    # Monta a resposta.
    return render_template("/index.html", logado = logado, mensagem = "")

@app.route("/realizarLogin", methods = ["POST"])
def realizar_login():
    # Extrai os dados do formulário.
    f = request.form
    if "login" not in f or "senha" not in f:
        return ":(", 422
    login = f["login"]
    senha = f["senha"]

    # Faz o processamento.
    logado = db_fazer_login(login, senha)

    # Monta a resposta.
    if logado is None:
        return render_template("login.html", erro = "Ops. A senha estava errada.")
    resposta = make_response(redirect("/"))

    # Armazena o login realizado com sucesso em cookies (autenticação).
    resposta.set_cookie("login", login, samesite = "Strict")
    resposta.set_cookie("senha", senha, samesite = "Strict")
    return resposta

@app.route("/logout", methods = ["POST"])
def logout():
    # Monta a resposta.
    resposta = make_response(render_template("login.html", mensagem = "Tchau."))

    # Limpa os cookies com os dados de login (autenticação).
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta

# Tela com o formulário de criação de uma nova adega.
@app.route("/adega/cadastro", methods = ["GET"])
def form_criar_adega_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
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

    # Monta a resposta.
    return render_template("cadastro-adega.html", logado = logado, adega = adega)

# Processa o formulário de criação de adega.
@app.route("/adega/cadastro", methods = ["POST"])
def criar_adega_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nomeAdega = request.form["nomeAdega"]
    cnpj = request.form["cnpj"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nEstabelecimento = request.form["nEstabelecimento"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    # Faz o processamento.
    ja_existia, adega = criar_adega(nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone)

    # Monta a resposta.
    mensagem = f"A adega {cnpj} já existe com o id {adega['id_adega']}." if ja_existia else f"A adega {cnpj} foi criada com id {adega['id_adega']}."
    return render_template("index.html", logado = logado, mensagem = mensagem)

# Tela de listagem de adegas.
@app.route("/adegas")
def listar_adegas_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = db_listar_adegas()

    # Monta a resposta.
    return render_template("lista-adegas.html", logado = logado, adegas = lista)

# Tela com o formulário de alteração de um aluno existente.
@app.route("/adega/<int:id_adega>", methods = ["GET"])
def form_alterar_adega_api(id_adega):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    adega = db_consultar_adega(id_adega)

    # Monta a resposta.
    return render_template("cadastro-adega.html", logado = logado, adega = adega)


# Processa o formulário de alteração de alunos. Inclui upload de fotos.
@app.route("/adega/<int:id_adega>", methods = ["POST"])
def editar_adega_api(id_adega):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nomeAdega = request.form["nomeAdega"]
    cnpj = request.form["cnpj"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nEstabelecimento = request.form["nEstabelecimento"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    # Faz o processamento.
    editar_adega(id_adega, nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone)

    # Monta a resposta.
    return redirect("/adegas")

# Processa o botão de excluir um aluno.
@app.route("/adega/<int:id_adega>", methods = ["DELETE"])
def excluir_adega_api(id_adega):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    apagar_adega(id_adega)
    return Response(status=204)

# Tela com o formulário de criação de um cliente.
@app.route("/cliente/cadastro", methods = ["GET"])
def form_criar_cliente_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
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

    # Monta a resposta.
    return render_template("cadastro-cliente.html", logado = logado, cliente = cliente)


# Processa o formulário de criação de clientes.
@app.route("/cliente/cadastro", methods = ["POST"])
def criar_cliente_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nomeCliente = request.form["nomeCliente"]
    cpf = request.form["cpf"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nResidencia = request.form["nResidencia"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    # Faz o processamento.
    ja_existia, cliente = criar_cliente(nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone)

    # Monta a resposta.
    mensagem = f"O cliente {cpf} já existe com o id {cliente['id_cliente']}." if ja_existia else f"A adega {cpf} foi criada com id {cliente['id_cliente']}."
    return render_template("index.html", logado = logado, mensagem = mensagem)

# Tela de listagem de clientes.
@app.route("/clientes")
def listar_clientes_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = db_listar_clientes()

    # Monta a resposta.
    return render_template("lista-clientes.html", logado = logado, clientes = lista)

@app.route("/cliente/<int:id_cliente>", methods = ["GET"])
def form_alterar_cliente_api(id_cliente):

    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    cliente = db_consultar_cliente(id_cliente)

    return render_template("cadastro-cliente.html", logado = logado, cliente = cliente)

# Processa o formulário de alteração de alunos. Inclui upload de fotos.
@app.route("/cliente/<int:id_cliente>", methods = ["POST"])
def editar_cliente_api(id_cliente):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nomeCliente = request.form["nomeCliente"]
    cpf = request.form["cpf"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    rua = request.form["rua"]
    bairro = request.form["bairro"]
    nResidencia = request.form["nResidencia"]
    complemento = request.form["complemento"]
    telefone = request.form["telefone"]

    # Faz o processamento.
    editar_cliente(id_cliente, nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone)

    # Monta a resposta.
    return redirect("/clientes")


# Tela com o formulário de criação de um novo produto.
@app.route("/produto/cadastro", methods = ["GET"])
def form_criar_produto_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    produto = {
        'id_produto': 'cadastro', 
        'nomeProduto': '', 
        'preco': '', 
        'quantidade': ''        
        }

    # Monta a resposta.
    return render_template("cadastro-produto.html", logado = logado, produto = produto)

# Processa o botão de excluir um aluno.
@app.route("/cliente/<int:id_cliente>", methods = ["DELETE"])
def excluir_cliente_api(id_cliente):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    apagar_cliente(id_cliente)
    return Response(status=204)

# Processa o formulário de criação de clientes.
@app.route("/produto/cadastro", methods = ["POST"])
def criar_produto_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nomeProduto = request.form["nomeProduto"]
    preco = request.form["preco"]
    quantidade = request.form["quantidade"]

    # Faz o processamento.
    criar_produto(nomeProduto, preco, quantidade)

    # Monta a resposta.
    return render_template("index.html", logado = logado)

# Tela de listagem de produtos.
@app.route("/produtos")
def listar_produtos_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = db_listar_produtos()

    # Monta a resposta.
    return render_template("lista-produtos.html", logado = logado, produtos = lista)

@app.route("/produto/<int:id_produto>", methods = ["GET"])
def form_alterar_produto_api(id_produto):

    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    produto = db_consultar_produto(id_produto)

    return render_template("cadastro-produto.html", logado = logado, produto = produto)

# Processa o formulário de alteração de alunos. Inclui upload de fotos.
@app.route("/produto/<int:id_produto>", methods = ["POST"])
def editar_produto_api(id_produto):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nomeProduto = request.form["nomeProduto"]
    preco = request.form["preco"]
    quantidade = request.form["quantidade"]

    # Faz o processamento.
    editar_produto(id_produto, nomeProduto, preco, quantidade)

    # Monta a resposta.
    return redirect("/produtos")

# Processa o botão de excluir um aluno.
@app.route("/produto/<int:id_produto>", methods = ["DELETE"])
def excluir_produto_api(id_produto):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
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