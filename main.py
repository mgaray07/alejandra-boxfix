from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
import os

app = Flask(__name__)

# Twilio setup
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

twilio_number = 'whatsapp:+14155238886'
admin_number = 'whatsapp:+50577769586'

# OpenAI setup
openai.api_key = os.environ['OPENAI_API_KEY']

@app.route("/")
def home():
    return "🤖 Alejandra está activa con inteligencia GPT."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From", "")

    response = MessagingResponse()
    reply = get_response(incoming_msg)

    if reply:
        response.message(reply)
    else:
        gpt_reply = get_gpt_response(incoming_msg)
        response.message(gpt_reply)

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

def get_gpt_response(msg):
    try:
        prompt = f"Sos una asistente de envíos por WhatsApp llamada Alejandra. Contestá de forma amable y clara: {msg}"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return completion.choices[0].message["content"].strip()
    except Exception as e:
        print("❌ Error GPT:", e)
        return "En este momento no puedo responderte, pero pronto un asesor lo hará."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
