import streamlit as st
import openai
import pandas as pd

# Configura tu API key aquí
openai.api_key = "TU_API_KEY_AQUI"  # <-- Reemplázala con tu clave real de OpenAI

# Cargar la base de datos de imágenes
@st.cache_data
def cargar_imagenes():
    return pd.read_excel("Imagenes_Drive_Convertidas.xlsx")

imagenes_df = cargar_imagenes()

# Interfaz de usuario
st.title("🧥 Asistente Virtual - Tienda de Ropa")
st.write("Hola 👋 Soy tu asesor virtual. ¿En qué puedo ayudarte hoy?")

user_input = st.text_input("Escribe tu mensaje:")

if user_input:
    # Crear el mensaje para el modelo
    prompt = f"""Actúas como un asesor comercial en una tienda de ropa.
Muestra solo prendas reales del inventario. Usa Markdown o texto plano para recomendar productos.
A continuación, una base de datos con imágenes reales asociadas a ID de prendas:

{imagenes_df.to_dict(orient='records')}

Mensaje del cliente: {user_input}"""

    # Solicitud a la API de OpenAI
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asesor virtual profesional en una tienda de ropa. Solo usas prendas disponibles y las muestras usando sus imágenes desde Google Drive."},
            {"role": "user", "content": prompt}
        ]
    )

    # Mostrar la respuesta
    st.markdown("### 🧠 Recomendación del asesor:")
    st.markdown(respuesta.choices[0].message['content'], unsafe_allow_html=True)
