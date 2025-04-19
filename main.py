from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Claves de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Prompt base para la personalidad de Alejandra
base_prompt = """Tu nombre es Alejandra, una asistente virtual amable, directa y profesional que ayuda a clientes de UltraEnvíos con todo lo relacionado a envíos de paquetería a Nicaragua. Tu estilo es conversacional, cálido pero siempre útil. Si el usuario te dice "hola", respondés como si fueras una persona real. Si no sabés algo, lo decís con sinceridad."""

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    phone_number = request.values.get('From', '')
    
    # Construcción del prompt
    full_prompt = f"{base_prompt}\nUsuario ({phone_number}): {incoming_msg}\nAlejandra:"
    
    try:
        # Llamada a la API de OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",  # o "gpt-3.5-turbo" si usás chat completions
            prompt=full_prompt,
            max_tokens=200,
            temperature=0.8
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        answer = "En este momento no puedo responderte, pero pronto un asesor lo hará."

    # Enviar respuesta por Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(answer)
    return str(twilio_response)

if __name__ == "__main__":
    app.run()
