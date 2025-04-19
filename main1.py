from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

twilio_number = 'whatsapp:+14155238886'  # Este es el número del sandbox
admin_number = 'whatsapp:+50577769586'   # Tu número personal para recibir alertas

@app.route("/")
def home():
    return "🤖 Alejandra está activa."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From", "")

    response = MessagingResponse()
    reply = get_response(incoming_msg)

    if reply:
        response.message(reply)
    else:
        mensaje = f"❗Alejandra no entendió esto: '{incoming_msg}'\nCliente: {from_number}"
        client.messages.create(body=mensaje, from_=twilio_number, to=admin_number)
        response.message("Gracias por escribirnos. En este momento un asesor te responderá directamente 😊")

    return str(response)

def get_response(msg):
    msg = msg.lower()
    if "aéreo" in msg or "aereo" in msg:
        return "El envío aéreo cuesta $7 por libra. Sale cada viernes desde Miami."
    elif "marítimo" in msg or "maritimo" in msg:
        return "El envío marítimo cuesta $2.50 por libra o $27 por pie cúbico."
    elif "barril" in msg:
        return "El envío de un barril cuesta $340 hasta Managua. El barril vacío cuesta $45."
    else:
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
