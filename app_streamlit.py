import streamlit as st
import requests
import datetime

st.set_page_config(page_title="F1 Chatbot", page_icon="🏎️", layout="wide")

st.markdown(
    """
    <style>
    /* Fondo de toda la página */
    .stApp {
        background-color: #000000;
    }
    /* Color del texto */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)



tabs = ["Inicio", "Chat F1", "Consultar Historial", "Obtener ID", "Eliminar Historial"]
selected_tab = st.sidebar.radio("Navegación", tabs)

API_URL = "http://localhost:8000"

if selected_tab == "Inicio":
    st.markdown("""
            <div style="position: relative; width: 100%; height: 0; padding-top: 25.0000%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https://www.canva.com/design/DAGgq50rf6s/ENJAUZ3cv-gXrcPCrLef2A/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>
""", unsafe_allow_html=True)
    
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