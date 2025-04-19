from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Configuración de la API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "🤖 Alejandra inteligente está online."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    print(f"📩 Mensaje de {sender}: {incoming_msg}")

    # Preparar la conversación como chat (GPT 3.5)
    messages = [
        {
            "role": "system",
            "content": (
                "Tu nombre es Alejandra. Sos una asistente virtual de UltraEnvíos, "
                "especialista en envíos entre Miami y Nicaragua. "
                "Sos amable, eficiente, empática y respondés como una persona real, no como un robot. "
                "Respondé siempre con claridad, profesionalismo y simpatía. "
                "Si no sabés algo, explicalo con honestidad."
            )
        },
        {
            "role": "user",
            "content": incoming_msg
        }
    ]

    try:
        # Solicitar respuesta al modelo GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        answer = response.choices[0].message["content"].strip()
    except Exception as e:
        print("❌ Error al conectar con OpenAI:", e)
        answer = "Estoy teniendo problemas para responderte ahora mismo 😞. Un asesor te contactará pronto."

    # Enviar respuesta por WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(answer)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
