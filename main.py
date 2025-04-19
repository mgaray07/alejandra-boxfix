from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Cargar la API KEY desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(user_input):
    try:
        print("🔄 Llamando a OpenAI con el prompt:", user_input)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos una asistente llamada Alejandra. Ayudá con respuestas claras, amables y útiles."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        reply = response.choices[0].message["content"].strip()
        print("✅ Respuesta de OpenAI:", reply)
        return reply
    except Exception as e:
        print("❌ Error al llamar a OpenAI:", e)
        return "En este momento no puedo responderte, pero pronto un asesor lo hará."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body")
    print("📩 Mensaje recibido:", incoming_msg)
    
    reply = get_openai_response(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

@app.route("/")
def home():
    return "Servidor Alejandra activo 🚀"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
