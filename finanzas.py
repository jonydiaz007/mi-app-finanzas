import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mi Asesor Financiero AI", page_icon="💰")

st.title("💰 Asesor Financiero Personal")
st.caption("Potenciado por Gemini")

# --- BARRA LATERAL PARA API KEY ---
# Esto es para que no tengas que pegar tu llave en el código público
api_key = st.sidebar.text_input("Pega tu Google API Key aquí:", type="password")

# --- EL CEREBRO (TU LÓGICA DE AI STUDIO) ---
# Aquí es donde pegas lo que hiciste en AI Studio.
# Copia tus "System Instructions" y pégalas dentro de las comillas triples abajo.
INSTRUCCIONES_SISTEMA = """
Eres un experto asesor financiero personal llamado 'Gemini Finanzas'.
Tu objetivo es ayudar al usuario a organizar sus gastos, ahorrar e invertir.
Responde de manera clara, empática y usando listas cuando sea necesario.
Si el usuario ingresa un gasto, clasifícalo y dale un consejo breve.
"""

# --- LÓGICA DE LA APP ---
if api_key:
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        
        # Usamos el modelo flash por ser rápido y eficiente para finanzas
        # Si tienes acceso a otro modelo, cambia el nombre aquí.
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=INSTRUCCIONES_SISTEMA
        )

        # Inicializar historial de chat
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])

        # Mostrar mensajes anteriores
        for message in st.session_state.chat.history:
            role = "user" if message.role == "user" else "assistant"
            with st.chat_message(role):
                st.markdown(message.parts[0].text)

        # Capturar entrada del usuario
        if prompt := st.chat_input("Ej: Gasté $50 en café, ¿es mucho?"):
            # Mostrar mensaje del usuario
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Obtener respuesta de Gemini
            response = st.session_state.chat.send_message(prompt)
            
            # Mostrar respuesta del Asesor
            with st.chat_message("assistant"):
                st.markdown(response.text)

    except Exception as e:
        st.error(f"Ocurrió un error con la API Key: {e}")
else:
    st.warning("⚠️ Por favor, ingresa tu API Key en la barra lateral para comenzar.")