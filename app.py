from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EMAIL = "sentinela7proton@gmail.com"
SENHA = "pcal rhcd pgpk nwgu"

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        valor = request.form["valor"]

        corpo = f"""
Nova solicitação de empréstimo:

Nome: {nome}
Email: {email}
Telefone: {telefone}
Valor solicitado: R$ {valor}
"""

        msg = MIMEText(corpo)
        msg["Subject"] = "Nova Solicitação de Empréstimo"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Reply-To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, SENHA)
            server.send_message(msg)

        return "Solicitação enviada com sucesso."

    return render_template("form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
