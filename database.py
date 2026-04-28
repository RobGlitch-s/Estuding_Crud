import sqlite3

class Database:
    def __init__(self, db_name="alunos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            ra INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            nome TEXT NOT NULL,
            data_nascimento TEXT
        )
        """)
        self.conn.commit()

    def insert_aluno(self, nome, data_nascimento):
        self.cursor.execute(
            "INSERT INTO alunos (nome, data_nascimento) VALUES (?, ?)",
            (nome, data_nascimento)
        )
        self.conn.commit()

    def fetch_alunos(self):
        self.cursor.execute("SELECT * FROM alunos")
        return self.cursor.fetchall()

    def update_aluno(self, ra, nome, data_nascimento):
        self.cursor.execute(
            "UPDATE alunos SET nome=?, data_nascimento=? WHERE ra=?",
            (nome, data_nascimento, ra)
        )
        self.conn.commit()

    def delete_aluno(self, ra):
        self.cursor.execute("DELETE FROM alunos WHERE ra=?", (ra,))
        self.conn.commit()