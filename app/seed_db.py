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
    (1, "carol.dev", "summer2021", "employee", "carol.dev@nimbus.local",
     "Welcome to Nimbus! Remember to change your password on first login."),
    (2, "alex.stone", "alex123456", "employee", "alex.stone@nimbus.local",
     "Southern region delivery routes updated."),
    (3, "sam.rivera", "soccer10", "employee", "sam.rivera@nimbus.local",
     "Logistics meeting every Monday at 9am."),
    (4, "morgan.lee", "M0rgan2020!", "manager", "morgan.lee@nimbus.local",
     "Route approvals pending in the queue."),
    (5, "admin", "Nimbu5-M@ster-K3y-9x2", "admin", "admin@nimbus.local",
     "Admin dashboard at /admin. Internal note: " + flags["idor"]),
]

cur.executemany(
    "INSERT INTO users (id, username, password, role, email, notes) VALUES (?, ?, ?, ?, ?, ?)",
    users,
)

conn.commit()
conn.close()
print("Database seeded with %d users." % len(users))
