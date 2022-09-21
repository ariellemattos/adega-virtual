from contextlib import closing
import sqlite3

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

sql_create = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeCliente VARCHAR(50) NOT NULL,
    cpf VARCHAR(50) NOT NULL,
    cep VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    rua VARCHAR(50) NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    nResidencia VARCHAR(50) NOT NULL,
    complemento VARCHAR(50) NULL,
    telefone VARCHAR(50) NOT NULL,
    UNIQUE(cpf)
);

CREATE TABLE IF NOT EXISTS adegas (
    id_adega INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeAdega VARCHAR(50) NOT NULL,
    cnpj VARCHAR(50) NOT NULL,
    cep VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    rua VARCHAR(50) NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    nEstabelecimento VARCHAR(50) NOT NULL,
    complemento VARCHAR(50) NULL,
    telefone VARCHAR(50) NOT NULL,
    UNIQUE(cnpj)
);

CREATE TABLE IF NOT EXISTS produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nomeProduto INTEGER(50) NOT NULL,
    preco DOUBLE(50) NOT NULL,
    quantidade VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    login VARCHAR(50) PRIMARY KEY NOT NULL,
    senha VARCHAR(50) NOT NULL,
    nome VARCHAR(50) NOT NULL
);

REPLACE INTO usuario (login, senha, nome) VALUES ('admin@admin.com', 'admin', 'Admin');
"""

def conectar():
    return sqlite3.connect('adega.db')

def db_inicializar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()

def db_fazer_login(login, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT u.login, u.senha, u.nome FROM usuario u WHERE u.login = ? AND u.senha = ?", [login, senha])
        return row_to_dict(cur.description, cur.fetchone())

def db_verificar_adega(cnpj):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_adega, cnpj FROM adegas WHERE cnpj = ?", [cnpj])
        return row_to_dict(cur.description, cur.fetchone())

def db_criar_adega(nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO adegas (nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone])
        id_adega = cur.lastrowid
        con.commit()
        return {'id_adega': id_adega, 'nomeAdega': nomeAdega, 'cnpj': cnpj}

def db_verificar_cliente(cpf):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, cpf FROM clientes WHERE cpf = ?", [cpf])
        return row_to_dict(cur.description, cur.fetchone())

def db_criar_cliente(nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO clientes (nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone])
        id_cliente = cur.lastrowid
        con.commit()
        return {'id_cliente': id_cliente, 'nomeCliente': nomeCliente, 'cpf': cpf}

def db_criar_produto(nomeProduto, preco, quantidade):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO produtos (nomeProduto, preco, quantidade) VALUES (?, ?, ?)", [nomeProduto, preco, quantidade])
        id_produto = cur.lastrowid
        con.commit()
        return {'id_produto': id_produto, 'nomeProduto': nomeProduto}

def db_listar_clientes():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nomeCliente, cpf, telefone FROM clientes")
        return rows_to_dict(cur.description, cur.fetchall())

def db_listar_produtos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, nomeProduto, preco, quantidade FROM produtos")
        return rows_to_dict(cur.description, cur.fetchall())

def db_listar_adegas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_adega, nomeAdega, cnpj, telefone FROM adegas")
        return rows_to_dict(cur.description, cur.fetchall())

def db_consultar_adega(id_adega):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_adega, nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone FROM adegas WHERE id_adega = ?", [id_adega])
        return row_to_dict(cur.description, cur.fetchone())

def db_consultar_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_cliente, nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone FROM clientes WHERE id_cliente = ?", [id_cliente])
        return row_to_dict(cur.description, cur.fetchone())

def db_consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT id_produto, nomeProduto, preco, quantidade FROM produtos WHERE id_produto = ?", [id_produto])
        return row_to_dict(cur.description, cur.fetchone())

def db_editar_adega(id_adega, nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE adegas SET nomeAdega = ?, cnpj = ?, cep = ?, cidade = ?, rua = ?, bairro = ?, nEstabelecimento = ?, complemento = ?, telefone = ? WHERE id_adega = ?", [nomeAdega, cnpj, cep, cidade, rua, bairro, nEstabelecimento, complemento, telefone, id_adega])
        con.commit()
        return {'id_adega': id_adega, 'nomeAdega': nomeAdega, 'cnpj': cnpj, 'cep': cep, 'cidade': cidade, 'rua': rua, 'bairro': bairro, 'nEstabelecimento': nEstabelecimento, 'complemento': complemento, 'telefone': telefone}

def db_editar_cliente(id_cliente, nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(
            "UPDATE clientes SET nomeCliente = ?, cpf = ?, cep = ?, cidade = ?, rua = ?, bairro = ?, nResidencia = ?, complemento = ?, telefone = ? WHERE id_cliente = ?",
            [nomeCliente, cpf, cep, cidade, rua, bairro, nResidencia, complemento, telefone, id_cliente]
        )

        con.commit()
        return {'id_cliente': id_cliente, 'nomeCliente': nomeCliente, 'cpf': cpf, 'cep': cep, 'cidade': cidade, 'rua': rua, 'bairro': bairro, 'nResidencia': nResidencia, 'complemento': complemento, 'telefone': telefone}

def db_editar_produto(id_produto, nomeProduto, preco, quantidade):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(
            "UPDATE produtos SET nomeProduto = ?, preco = ?, quantidade = ? WHERE id_produto = ?", [nomeProduto, preco, quantidade, id_produto]
        )

        con.commit()
        return {'id_produto': id_produto, 'nomeProduto': nomeProduto, 'preco': preco, 'quantidade': quantidade}

def db_deletar_adega(id_adega):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM adegas WHERE id_adega = ?", [id_adega])
        con.commit()

def db_deletar_cliente(id_cliente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM clientes WHERE id_cliente = ?", [id_cliente])
        con.commit()

def db_deletar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM produtos WHERE id_produto = ?", [id_produto])
        con.commit()

