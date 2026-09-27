import os
import json
import sqlite3

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    make_response,
    send_from_directory,
    g,
    abort,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nimbus.db")
FLAGS_PATH = os.path.join(BASE_DIR, "flags.json")

app = Flask(__name__)


def load_flags():
    try:
        with open(FLAGS_PATH, "r") as fh:
            return json.load(fh)
    except (FileNotFoundError, ValueError):
        return {
            "recon": "FLAG{not_configured}",
            "backup": "FLAG{not_configured}",
            "auth": "FLAG{not_configured}",
            "idor": "FLAG{not_configured}",
            "privesc": "FLAG{not_configured}",
            "devnotes": "FLAG{not_configured}",
        }


FLAGS = load_flags()

MASTER_PASSWORD = "nimbus-ops-2019"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html", recon_flag=FLAGS["recon"])


@app.route("/robots.txt")
def robots():
    body = (
        "User-agent: *\n"
        "Disallow: /internal-notes\n"
        "Disallow: /static/old_backups/\n"
        "Disallow: /admin\n"
    )
    resp = make_response(body)
    resp.headers["Content-Type"] = "text/plain"
    return resp


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()

        if password == MASTER_PASSWORD:
            row = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
            if row is None:
                row = db.execute(
                    "SELECT * FROM users WHERE role = 'admin' LIMIT 1"
                ).fetchone()
            return _do_login(row)

        query = (
            "SELECT * FROM users WHERE username = '%s' AND password = '%s'"
            % (username, password)
        )
        try:
            row = db.execute(query).fetchone()
        except sqlite3.Error:
            row = None

        if row is not None:
            return _do_login(row)
        error = "Usuario ou senha invalidos."

    return render_template("login.html", error=error)


def _do_login(row):
    resp = make_response(redirect(url_for("dashboard")))
    resp.set_cookie("username", row["username"])
    resp.set_cookie("uid", str(row["id"]))
    resp.set_cookie("role", row["role"])
    return resp


@app.route("/dashboard")
def dashboard():
    username = request.cookies.get("username")
    if not username:
        return redirect(url_for("login"))
    uid = request.cookies.get("uid", "0")
    db = get_db()
    row = db.execute(
        "SELECT role FROM users WHERE username = ?", (username,)
    ).fetchone()
    auth_flag = None
    if row is not None and row["role"] == "admin":
        auth_flag = FLAGS["auth"]
    return render_template(
        "dashboard.html", username=username, uid=uid, auth_flag=auth_flag
    )


@app.route("/profile")
def profile():
    username = request.cookies.get("username")
    if not username:
        return redirect(url_for("login"))
    uid = request.args.get("id", request.cookies.get("uid", "1"))
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    if row is None:
        abort(404)
    return render_template("profile.html", user=row)


@app.route("/admin")
def admin():
    role = request.cookies.get("role", "")
    if role != "admin":
        return render_template("forbidden.html"), 403
    db = get_db()
    rows = db.execute("SELECT id, username, role, email FROM users").fetchall()
    return render_template("admin.html", users=rows, flag=FLAGS["privesc"])


@app.route("/internal-notes")
def internal_notes():
    return render_template("notes.html", flag=FLAGS["devnotes"])


@app.route("/static/old_backups/<path:filename>")
def old_backups(filename):
    directory = os.path.join(BASE_DIR, "static", "old_backups")
    return send_from_directory(directory, filename)


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("index")))
    for c in ("username", "uid", "role"):
        resp.delete_cookie(c)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
