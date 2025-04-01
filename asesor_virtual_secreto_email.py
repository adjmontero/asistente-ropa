
import streamlit as st
import pandas as pd
from openai import OpenAI

# Cargar datos
clientes_df = pd.read_excel("AsistenteVirtual_DB_email.xlsx", sheet_name="Clientes")
historial_df = pd.read_excel("AsistenteVirtual_DB_email.xlsx", sheet_name="HistorialCompras")
ropa_df = pd.read_excel("AsistenteVirtual_DB_email.xlsx", sheet_name="Ropa")
imagenes_df = pd.read_excel("Imagenes_Drive_Convertidas.xlsx")

# Conectar con OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧥 Asistente Virtual - Tu tienda de moda personalizada")
st.warning("Versión cargada correctamente ✅")

# Paso 1: Solicitar email
email = st.text_input("📧 Introduce tu correo electrónico para empezar:").strip().lower()

if not email:
    st.info("⏳ Esperando que introduzcas tu email para comenzar tu experiencia personalizada.")
    st.stop()

clientes_df["Email"] = clientes_df["Email"].astype(str).str.strip().str.lower()
cliente = clientes_df[clientes_df["Email"] == email]

if cliente.empty:
    st.error(f"❌ No encontramos el email **{email}** en nuestra base de datos. ¿Te gustaría registrarte?")
    st.stop()

# Paso 2: Datos del cliente
nombre = cliente.iloc[0]["Nombre"]
estilo = cliente.iloc[0]["Estilo favorito"]
ciudad = cliente.iloc[0]["Ciudad"]

compras = historial_df[historial_df["NIF Cliente"] == cliente.iloc[0]["NIF"]]
prenda_anterior = None
if not compras.empty:
    id_ultima = compras.iloc[-1]["ID Prenda"]
    prenda_info = ropa_df[ropa_df["ID Prenda"] == id_ultima]
    if not prenda_info.empty:
        prenda_anterior = prenda_info.iloc[0]["Nombre"]

# Saludo cálido
st.markdown(f"👋 ¡Qué alegría verte por aquí otra vez, {nombre}!")
if prenda_anterior:
    st.markdown(f"🧾 Veo que tu última compra fue: **{prenda_anterior}**. ¡Buena elección!")

# Campo de mensaje
mensaje_usuario = st.text_input("📝 ¿Qué estás buscando hoy?")

if mensaje_usuario:
    prompt = f'''
Eres un asesor comercial virtual en una tienda de ropa. El cliente se llama {nombre}, vive en {ciudad} y su estilo favorito es {estilo}.
Su última compra fue: {prenda_anterior if prenda_anterior else "N/A"}.
Tu tarea es recomendarle entre 2 y 3 prendas del inventario que coincidan con su estilo y el mensaje proporcionado.

⚠️ Solo puedes mostrar prendas:
- Que estén en la base 'Ropa'
- Que tengan una imagen en Imagenes_Drive_Convertidas.xlsx (por ID de prenda)
- No inventes productos ni uses imágenes externas.

Muestra las imágenes así:
Nombre de la prenda
👉 [Ver imagen](URL)

Mensaje del cliente: "{mensaje_usuario}"
'''

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
