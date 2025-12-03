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
