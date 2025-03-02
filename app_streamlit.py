import streamlit as st
import requests
import datetime

st.set_page_config(page_title="F1 Chatbot", page_icon="🏎️", layout="wide")

tabs = ["Inicio", "Chat F1", "Consultar Historial", "Obtener ID", "Eliminar Historial"]
selected_tab = st.sidebar.radio("Navegación", tabs)

API_URL = "http://localhost:8000"

if selected_tab == "Inicio":
    st.title("🏁 Bienvenido al Chatbot de Fórmula 1 🏎️")
    st.write("Esta aplicación te permite interactuar con un chatbot experto en Fórmula 1. Aquí tienes un resumen de cómo funciona:")
    
    response = requests.get(f"{API_URL}/getid/")
    if response.status_code == 200:
        session_id = response.json()
        st.success(f"Tu ID de sesión único lo podrás encontrar en la pestaña Obtener ID, utilizalo para consultar o eliminar tu historial de búsqueda siempre que lo necesites")
    else:
        st.error("No se pudo obtener el ID de sesión.")
    
    st.write("### ¿Qué puedes hacer?")
    st.write("- **Chat F1**: Pregunta cualquier cosa sobre F1 y recibe respuestas en tiempo real.")
    st.write("- **Consultar Historial**: Revisa todas tus consultas anteriores usando tu ID de sesión.")
    st.write("- **Obtener ID**: Para consultar tu ID de sesión.")
    st.write("- **Eliminar Historial**: Borra tu historial de consultas cuando lo desees.")
    st.write("¡Disfruta de la experiencia y descubre todo sobre la Fórmula 1! 🏎️💨")

elif selected_tab == "Chat F1":
    st.title("🏁 Chat sobre Fórmula 1 🏎️")
    st.write("Pregunta cualquier cosa sobre F1 y nuestro chatbot responderá de forma sencilla.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("Escribe tu pregunta aquí:")
    if st.button("Enviar") and user_input:
        response = requests.post(f"{API_URL}/question/", json={"prompt": user_input})
        if response.status_code == 200:
            answer = response.json()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.session_state.chat_history.append((timestamp, user_input, answer))
        else:
            st.error("Error al obtener respuesta del chatbot.")
    
    for chat in st.session_state.chat_history[::-1]:
        st.write(f"🕒 {chat[0]}")
        st.write(f"👤 **Tú:** {chat[1]}")
        st.write(f"🤖 **Chatbot:** {chat[2]}")
        st.write("---")

elif selected_tab == "Consultar Historial":
    st.title("📜 Historial de Consultas")
    session_id = st.text_input("Introduce tu ID de sesión:")
    if st.button("Consultar") and session_id:
        response = requests.post(f"{API_URL}/consult/", json={"id": session_id})
        if response.status_code == 200:
            historial = response.json()
            for entry in historial:
                timestamp = entry['timestamp'].replace("T", " ")
                st.write(f"🕒 {timestamp}")
                st.write(f"👤 **Tú:** {entry['question']}")
                st.write(f"🤖 **Chatbot:** {entry['response']}")
                st.write("---")
        else:
            st.error("No se pudo recuperar el historial.")

elif selected_tab == "Obtener ID":
    st.title("🔑 Obtener ID de Sesión")
    if st.button("Generar ID"):
        response = requests.get(f"{API_URL}/getid/")
        if response.status_code == 200:
            st.success(f"Tu ID de sesión es: {response.json()}")
        else:
            st.error("Error al obtener el ID de sesión.")

elif selected_tab == "Eliminar Historial":
    st.title("🗑️ Eliminar Historial")
    session_id = st.text_input("Introduce tu ID de sesión para borrar el historial:")
    if st.button("Eliminar") and session_id:
        response = requests.delete(f"{API_URL}/delete_history/", json={"id": session_id})
        if response.status_code == 200:
            st.success("Historial eliminado correctamente.")
        else:
            st.error("No se pudo eliminar el historial.")
