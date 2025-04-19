from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

# Inicialización de Flask
app = Flask(__name__)

# Claves de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")

# Cliente OpenAI
client = OpenAI(api_key=openai_api_key)

# Ruta principal para recibir mensajes de WhatsApp
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body")
    resp = MessagingResponse()
    msg = resp.message()

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = "Estoy teniendo problemas para responderte ahora mismo 😞. Un asesor te contactará pronto."
        print("Error:", e)

    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)