import os
from flask import Flask, render_template, request, redirect, url_for
import mercadopago

app = Flask(__name__)

# Debug: ver se a variável de ambiente está chegando
token = os.getenv("MP_ACCESS_TOKEN")
if not token:
    raise RuntimeError("Variável de ambiente MP_ACCESS_TOKEN não encontrada!")

# Inicializa SDK com token de ambiente
sdk = mercadopago.SDK(token)

@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

@app.route("/pagar", methods=["POST"])
def pagar():
    email = request.form["email"]

    # Dados de pagamento Pix
    payment_data = {
        "transaction_amount": 10.0,  # valor de teste
        "description": "Acesso ao serviço",
        "payment_method_id": "pix",
        "payer": {"email": email},
        "back_urls": {
            "success": url_for("sucesso", _external=True),
            "failure": url_for("erro", _external=True),
            "pending": url_for("pendente", _external=True),
        },
        "auto_return": "approved"
    }

    # Cria pagamento
    result = sdk.payment().create(payment_data)
    payment = result["response"]

    # Redireciona para QR Code Pix
    return redirect(payment["point_of_interaction"]["transaction_data"]["ticket_url"])

@app.route("/sucesso")
def sucesso():
    return "Pagamento aprovado. Acesso liberado."

@app.route("/erro")
def erro():
    return "Pagamento falhou."

@app.route("/pendente")
def pendente():
    return "Pagamento pendente."

if __name__ == "__main__":
    # Só para debug local
    app.run(debug=True)
