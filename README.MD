# Trabalho Back-End Frameworks 4MC

#### Pariticipantes:
- Clailson dos santos silva - 01689159
- Gabriel Antônio de Araújo e Sá - 01672540
- Luiz Eduardo de França Rodrigues - 01680699
- Matheus Pereira do Nascimento - 01693563

-------------------------------------------------------------------

## Descrição:

Trabalho feito para disponibilizar um Sistema de Gerenciamento de uma Bibilioteca de Livros utilizando Cadastramento, Atualização e Remoção de Livros utlizando Flask e Fast API junto com SQLite3 sendo importado via Python.

O Código consiste em 3 arquivos de Python:
- app_flask.py
- api_fast.py
- criar_db.py

E uma DB criada pelo próprio Python ou já incluida no arquivo.

O Código está disponível via GitHub em:
https://github.com/MatheusNascimento87/Biblioteca-Python-Flask-FastAPI

Explicação de Como foi rodado o código via comandos:
- Criação de Ambiente Virtual:
```
python -m venv venv
venv\Scripts\activate
```
- Instalação das Dependências do Projeto:
```
pip install flask fastapi uvicorn pydantic
```
- Execução para utilização do Flask:
```
python app_flask.py
```
- Criação do Local Host no Link:
```
http://localhost:5000/
```
- Execução do Fast API para Utilização no Código:
```
uvicorn api_fast:app --reload --port 8000
```
- Criação de Segundo Local Host para o Fast API no Link:
```
http://localhost:8000/docs
```

-------------------------------------------------------------------

## Código 

### app_flask.py
#### Aplicação Flask para interface web da Biblioteca.
#### Exibe a lista de livros, permitindo cadastrar novos e excluir.
#### Conecta ao banco SQLite conforme solicitado nos requisitos.

Código:
```
from flask import Flask, request, redirect, render_template_string
import sqlite3

DB_FILE = "biblioteca.db"
app = Flask(__name__)


def conectar():
    con = sqlite3.connect(DB_FILE)
    return con


def start_db():
    con = conectar()
    con.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            disponivel INTEGER NOT NULL
        )
    """)
    con.commit()
    con.close()

start_db()


PAGE = PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Biblioteca • Painel de Livros</title>

<style>
    body {
        margin: 0;
        padding: 0;
        background: #0b0f19;
        color: #e0e0e0;
        font-family: "Segoe UI", Arial, sans-serif;
    }

    header {
        background: #111827;
        padding: 20px;
        text-align: center;
        color: #fff;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
        border-bottom: 2px solid #1f2937;
    }

    .wrapper {
        max-width: 900px;
        margin: 40px auto;
        padding: 20px;
        background: #131a2a;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
    }

    h3 {
        margin-top: 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #263041;
        color: #93c5fd;
    }

    /* Formulário */
    form {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 25px;
    }

    form input, form select {
        padding: 10px;
        background: #1f2937;
        border: 1px solid #374151;
        color: #e5e5e5;
        border-radius: 6px;
        font-size: 14px;
    }

    form button {
        grid-column: span 2;
        padding: 12px;
        background: #2563eb;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        cursor: pointer;
        transition: 0.2s;
        font-size: 15px;
    }

    form button:hover {
        background: #1d4ed8;
    }

    /* Tabela */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        border-radius: 10px;
        overflow: hidden;
        background: #0f172a;
    }

    th {
        background: #1e293b;
        padding: 12px;
        font-size: 14px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #93c5fd;
    }

    td {
        padding: 12px;
        text-align: center;
        border-bottom: 1px solid #1e293b;
    }

    tr:hover {
        background: #172033;
    }

    .btn-del {
        padding: 6px 10px;
        background: #dc2626;
        color: white !important;
        text-decoration: none;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.2s;
    }

    .btn-del:hover {
        background: #b91c1c;
    }
</style>

</head>
<body>

<header> Biblioteca Universitária</header>

<div class="wrapper">

<h3>Novo Livro</h3>

<form method="POST">
    <input name="titulo" placeholder="Título do livro" required>
    <input name="autor" placeholder="Autor" required>
    <input name="ano_publicacao" type="number" placeholder="Ano" required>
    <select name="disponivel" required>
        <option value="" disabled selected>Disponibilidade...</option>
        <option value="1">Disponível</option>
        <option value="0">Indisponível</option>
    </select>
    <button type="submit">Cadastrar Livro</button>
</form>

<h3>Acervo Registrado</h3>

<table>
    <tr>
        <th>ID</th>
        <th>Título</th>
        <th>Autor</th>
        <th>Ano</th>
        <th>Status</th>
        <th>Ação</th>
    </tr>

    {% for l in lista %}
    <tr>
        <td>{{ l[0] }}</td>
        <td>{{ l[1] }}</td>
        <td>{{ l[2] }}</td>
        <td>{{ l[3] }}</td>
        <td>{{ "Disponível" if l[4] == 1 else "Indisp." }}</td>
        <td><a class="btn-del" href="/remover/{{ l[0] }}" onclick="return confirm('Confirmar exclusão?')">Excluir</a></td>
    </tr>
    {% endfor %}
</table>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    con = conectar()
    cur = con.cursor()

    if request.method == "POST":
        cur.execute(
            "INSERT INTO livros (titulo, autor, ano_publicacao, disponivel) VALUES (?,?,?,?)",
            (
                request.form["titulo"],
                request.form["autor"],
                int(request.form["ano_publicacao"]),
                int(request.form["disponivel"])
            )
        )
        con.commit()

    lista = cur.execute("SELECT * FROM livros").fetchall()
    con.close()

    return render_template_string(PAGE, lista=lista)


@app.route("/remover/<int:lid>")
def remover(lid):
    con = conectar()
    con.execute("DELETE FROM livros WHERE id = ?", (lid,))
    con.commit()
    con.close()
    return redirect("/")
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

-------------------------------------------------------------------

### api_fast.py
#### API FastAPI para CRUD completo da tabela livros
#### Implementa GET, POST, PUT, DELETE conforme a atividade AV2

Código:
```
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

DB_PATH = "biblioteca.db"

app = FastAPI(title="Sistema de Biblioteca - API")


class LivroSchema(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    disponivel: bool

def get_conn():
    """Abre conexão com o banco SQLite."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def livro_por_id(livro_id: int):
    """Busca um livro pelo ID."""
    con = get_conn()
    res = con.execute("SELECT * FROM livros WHERE id = ?", (livro_id,)).fetchone()
    con.close()
    return res


@app.get("/livros")
def todos():
    """Retorna todos os livros cadastrados."""
    con = get_conn()
    lista = con.execute("SELECT * FROM livros").fetchall()
    con.close()
    return [dict(row) for row in lista]


@app.get("/livros/{lid}")
def buscar(lid: int):
    """Obtém um livro específico."""
    dado = livro_por_id(lid)

    if not dado:
        raise HTTPException(404, "Livro não encontrado")

    return dict(dado)


@app.post("/livros", status_code=201)
def criar(item: LivroSchema):
    """Insere um novo livro no sistema."""
    con = get_conn()
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO livros (titulo, autor, ano_publicacao, disponivel)
        VALUES (?, ?, ?, ?)
        """,
        (item.titulo, item.autor, item.ano_publicacao, int(item.disponivel))
    )

    con.commit()
    novo = cur.lastrowid
    con.close()

    return buscar(novo)


@app.put("/livros/{lid}")
def editar(lid: int, dados: LivroSchema):
    """Atualiza as informações de um livro."""
    con = get_conn()
    cur = con.cursor()

    cur.execute(
        """
        UPDATE livros 
        SET titulo = ?, autor = ?, ano_publicacao = ?, disponivel = ?
        WHERE id = ?
        """,
        (dados.titulo, dados.autor, dados.ano_publicacao, int(dados.disponivel), lid)
    )

    con.commit()
    alteracoes = cur.rowcount
    con.close()

    if alteracoes == 0:
        raise HTTPException(404, "Livro não encontrado")

    return {"status": "ok", "mensagem": "Atualizado com sucesso", "id": lid}


@app.delete("/livros/{lid}")
def remover(lid: int):
    """Remove um livro pelo ID."""
    con = get_conn()
    cur = con.cursor()

    cur.execute("DELETE FROM livros WHERE id = ?", (lid,))
    con.commit()
    deletado = cur.rowcount
    con.close()

    if deletado == 0:
        raise HTTPException(404, "Livro não encontrado")

    return {"status": "ok", "mensagem": "Livro apagado"}
```

-------------------------------------------------------------------

### criar_db.py
#### Importação do SQLite no código para criação do banco de dados;
#### Tabela do SQLite utiliza-se de Integer para o Ano_Publicacao, com o resto da table sendo genérica de uma tabela de banco de dados
#### Print feito para confirmar que o Banco de Dados foi criado.

Código:
```
import sqlite3

def criar():
    con = sqlite3.connect("biblioteca.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            disponivel INTEGER NOT NULL
        )
    """)
    con.commit()
    con.close()
    print("Banco inicializado com sucesso!")

criar()

```
