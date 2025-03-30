import streamlit as st
import pandas as pd
from openai import OpenAI

# Cargar datos
clientes_df = pd.read_excel("AsistenteVirtual_DB (1).xlsx", sheet_name="Clientes")
historial_df = pd.read_excel("AsistenteVirtual_DB (1).xlsx", sheet_name="HistorialCompras")
ropa_df = pd.read_excel("AsistenteVirtual_DB (1).xlsx", sheet_name="Ropa")
imagenes_df = pd.read_excel("Imagenes_Drive_Convertidas.xlsx")

# Conectar con OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧥 Asistente Virtual - Tienda de Ropa")

# Paso 1: Solicitar NIF
nif = st.text_input("🔐 Por favor, introduce tu NIF para comenzar:").strip().upper()

if not nif:
    st.info("🕓 Esperando a que introduzcas tu NIF para comenzar la atención personalizada.")
    st.stop()

clientes_df["NIF"] = clientes_df["NIF"].astype(str).str.strip().str.upper()
cliente = clientes_df[clientes_df["NIF"] == nif]

if cliente.empty:
    st.error(f"❌ No encontramos el NIF **{nif}** en nuestra base de datos. ¿Te gustaría registrarte?")
    st.stop()

# Paso 2: Datos del cliente
nombre = cliente.iloc[0]["Nombre"]
estilo = cliente.iloc[0]["Estilo favorito"]
ciudad = cliente.iloc[0]["Ciudad"]

compras = historial_df[historial_df["NIF Cliente"] == nif]
prenda_anterior = None
if not compras.empty:
    id_ultima = compras.iloc[-1]["ID Prenda"]
    prenda_info = ropa_df[ropa_df["ID Prenda"] == id_ultima]
    if not prenda_info.empty:
        prenda_anterior = prenda_info.iloc[0]["Nombre"]

# Saludo personalizado
st.markdown(f"👋 ¡Hola, {nombre}! Encantado de verte por aquí.")
if prenda_anterior:
    st.markdown(f"🧾 Veo que tu última compra fue: **{prenda_anterior}**. ¡Buena elección!")

# Campo de mensaje
mensaje_usuario = st.text_input("📝 ¿Qué estás buscando hoy?")

if mensaje_usuario:
    prompt = f"""
Eres un asesor comercial en una tienda de ropa. El cliente se llama {nombre}, vive en {ciudad} y su estilo favorito es {estilo}.
Su última compra fue: {prenda_anterior if prenda_anterior else "N/A"}.

Tu tarea es recomendarle entre 2 y 3 prendas del inventario, en base a su estilo, el mensaje del cliente: "{mensaje_usuario}" y nuestro catálogo.

Solo puedes sugerir prendas que:
- Estén en la base de datos 'Ropa'
- Tengan imagen en 'Imagenes_Drive_Convertidas.xlsx' (por ID de prenda)

Muestra las imágenes usando Markdown así:
![nombre](URL)

No inventes productos ni uses imágenes externas.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": mensaje_usuario}
        ]
    )

    respuesta = response.choices[0].message.content
    st.markdown("### 💡 Recomendación del asesor:")
    st.markdown(respuesta)