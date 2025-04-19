import os
import openai

# Intenta obtener la clave desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ ERROR: No se encontró la clave OPENAI_API_KEY en el entorno.")
else:
    print("✅ La clave se está leyendo correctamente.")
    openai.api_key = api_key

    # Hacemos una prueba con una pregunta simple
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos Alejandra, una asistente muy amigable."},
                {"role": "user", "content": "Hola, ¿cómo estás?"}
            ]
        )
        print("💬 Respuesta de OpenAI:")
        print(response["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"❌ Error al llamar a la API de OpenAI: {e}")
