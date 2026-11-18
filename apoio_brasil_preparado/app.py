import os
import re
import secrets
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

INSTANCE_DIR = Path(os.environ.get("INSTANCE_DIR", "instance"))
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE = Path(os.environ.get("DATABASE_PATH", str(INSTANCE_DIR / "apoio_brasil.db")))
PRECO = "49,90"

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS interessados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                cidade TEXT,
                estado TEXT,
                consentimento_privacidade INTEGER NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

criar_banco()

@app.after_request
def headers_seguranca(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/inscricao", methods=["GET", "POST"])
def inscricao():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_urlsafe(24)
        return render_template("inscricao.html", csrf_token=session["csrf_token"])

    if not secrets.compare_digest(
        request.form.get("csrf_token", ""),
        session.get("csrf_token", "")
    ):
        abort(400)

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    cidade = request.form.get("cidade", "").strip()
    estado = request.form.get("estado", "").strip()
    consentimento = request.form.get("consentimento") == "on"

    if not nome or len(nome) > 120:
        return render_template("inscricao.html", erro="Informe seu nome completo.", csrf_token=session["csrf_token"]), 400
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or len(email) > 160:
        return render_template("inscricao.html", erro="Informe um e-mail válido.", csrf_token=session["csrf_token"]), 400
    if len(cidade) > 100 or len(estado) > 50:
        return render_template("inscricao.html", erro="Confira os campos de localização.", csrf_token=session["csrf_token"]), 400
    if not consentimento:
        return render_template("inscricao.html", erro="É necessário concordar com a Política de Privacidade para continuar.", csrf_token=session["csrf_token"]), 400

    with conectar() as conn:
        cur = conn.execute(
            """INSERT INTO interessados (nome, email, cidade, estado, consentimento_privacidade)
               VALUES (?, ?, ?, ?, 1)""",
            (nome, email, cidade, estado)
        )
        cadastro_id = cur.lastrowid

    session["cadastro_id"] = cadastro_id
    session["nome_cliente"] = nome
    session["email_cliente"] = email
    session.pop("csrf_token", None)
    return redirect(url_for("pagamento"))

@app.route("/pagamento")
def pagamento():
    if not session.get("cadastro_id"):
        return redirect(url_for("inscricao"))
    return render_template(
        "pagamento.html",
        nome=session.get("nome_cliente", ""),
        email=session.get("email_cliente", ""),
        preco=PRECO
    )

@app.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")

@app.route("/termos")
def termos():
    return render_template("termos.html")

@app.route("/reembolso")
def reembolso():
    return render_template("reembolso.html")

@app.route("/saude")
def saude():
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
