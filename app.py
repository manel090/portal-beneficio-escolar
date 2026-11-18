
from flask import Flask, render_template, request, redirect, url_for
import secrets
import re

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/inscricao", methods=["GET", "POST"])
def inscricao():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        cpf = request.form.get("cpf", "").strip()
        cpf_numeros = re.sub(r"\D", "", cpf)

        if not nome or not email or len(cpf_numeros) != 11:
            return "Preencha os campos obrigatórios e informe um CPF fictício com 11 dígitos.", 400

        protocolo = "DEMO-" + secrets.token_hex(4).upper()

        return render_template(
            "confirmacao.html",
            nome=nome,
            protocolo=protocolo
        )

    return render_template("inscricao.html")


if __name__ == "__main__":
    app.run(host="192.168.1.2", port=5000, debug=True)
