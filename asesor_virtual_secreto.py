import streamlit as st
from openai import OpenAI
import pandas as pd

# Leer API key desde los secretos de Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Cargar la base de datos de imágenes
@st.cache_data
def cargar_imagenes():
    return pd.read_excel("Imagenes_Drive_Convertidas.xlsx")

imagenes_df = cargar_imagenes()

# Interfaz
st.title("🧥 Asistente Virtual - Tienda de Ropa")
st.write("Hola 👋 Soy tu asesor virtual. ¿En qué puedo ayudarte hoy?")

user_input = st.text_input("Escribe tu mensaje:")

if user_input:
    prompt = f"""Actúas como un asesor comercial en una tienda de ropa.
Solo puedes mostrar productos reales. A continuación, una base de datos con imágenes por ID de prenda:

{imagenes_df.to_dict(orient='records')}

Mensaje del cliente: {user_input}"""

    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asesor virtual profesional en una tienda de ropa. Solo ofreces prendas reales del inventario con imágenes desde Google Drive."},
            {"role": "user", "content": prompt}
        ]
    )

    st.markdown("### 🧠 Recomendación del asesor:")
    st.markdown(respuesta.choices[0].message.content, unsafe_allow_html=True)
