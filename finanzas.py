import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asesor Financiero", page_icon="💰")

st.title("💰 Mi Asesor Financiero")
st.write("Ingresa tu API Key para comenzar.")

# Entrada de la API Key
api_key = st.text_input("Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Instrucciones simples para evitar errores de formato
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction="Eres un experto en finanzas. Responde breve y útil."
        )

        # Chat simple
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Pregunta sobre tus finanzas..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {e}")
