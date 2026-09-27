import os
import json
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nimbus.db")
FLAGS_PATH = os.path.join(BASE_DIR, "flags.json")

with open(FLAGS_PATH, "r") as fh:
    flags = json.load(fh)

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT,
        notes TEXT
    )
    """
)

users = [
    (1, "carlos.mendes", "verao2021", "employee", "carlos.mendes@nimbus.local",
     "Bem-vindo a Nimbus! Lembre de trocar sua senha no primeiro acesso."),
    (2, "ana.souza", "ana123456", "employee", "ana.souza@nimbus.local",
     "Rota de entregas da regiao sul atualizada."),
    (3, "bruno.lima", "futebol10", "employee", "bruno.lima@nimbus.local",
     "Reuniao de logistica toda segunda as 9h."),
    (4, "patricia.rocha", "P@tricia2020", "manager", "patricia.rocha@nimbus.local",
     "Aprovacoes de rota pendentes na fila."),
    (5, "admin", "Nimbu5-M@ster-K3y-9x2", "admin", "admin@nimbus.local",
     "Painel administrativo em /admin. Nota interna: " + flags["idor"]),
]

cur.executemany(
    "INSERT INTO users (id, username, password, role, email, notes) VALUES (?, ?, ?, ?, ?, ?)",
    users,
)

conn.commit()
conn.close()
print("Banco populado com %d usuarios." % len(users))
