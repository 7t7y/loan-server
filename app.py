import os
import mercadopago
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

@app.route("/pagar", methods=["POST"])
def pagar():
    email = request.form["email"]

    payment_data = {
        "transaction_amount": 10.0,
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

    result = sdk.payment().create(payment_data)
    payment = result["response"]

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
    app.run(debug=true)
