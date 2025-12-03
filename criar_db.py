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
