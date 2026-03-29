import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8001/chat"

st.set_page_config(page_title="Chatbot KB", page_icon="💬", layout="centered")

st.title("💬 Chatbot da Base de Conhecimento")
st.caption("Responde somente com base no conteúdo disponível na base local.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Digite sua pergunta...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Consultando base..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"pergunta": user_input},
                    timeout=40
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("resposta", "Erro ao obter resposta.")
                score = data.get("score")
                item = data.get("item_encontrado")
                fonte = data.get("fonte")

                st.markdown(answer)

                with st.expander("Detalhes da busca"):
                    st.write(f"**Score:** {score}")
                    st.write(f"**Item encontrado:** {item}")
                    st.write(f"**Fonte da resposta:** {fonte}")

            except Exception as e:
                answer = f"Erro ao consultar o backend: {e}"
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})