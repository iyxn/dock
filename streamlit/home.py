import streamlit as st
import requests

url = "http://api:8001/generate" # API server

# fungsi untuk call ke API server
def generate_text(messages, generation_config):
    data = {
        "messages": messages,
        "generationConfig": generation_config
    }

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text
        else:
            return f"Error: {response.status_code}, Detail: {response.text}"
    except Exception as e:
        return f"Error: {e}"

# tampilan chatting
def main():
    st.title("Chatbot sederhana")

    # Menu konfigurasi parameter
    st.sidebar.title("Konfigurasi parameter")
    temperature = st.sidebar.slider("Temperature", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    max_output_tokens = st.sidebar.number_input("Max Output Tokens", min_value=10, max_value=500, value=200, step=10)

    # Pesan pertama bot dan inisialisasi session
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Ada yang bisa saya bantu?"}]

    # menampilkan isi pesan berdasarkan role, assistant = bot, user = user
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Prompt user
    if prompt := st.chat_input("Ketik pesan:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # membalas pesan user
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Mencari Jawaban..."): #animasi spinner
                    generation_config = { #inisialisasi konfigurasi parameter
                        "temperature": temperature,
                        "maxOutputTokens": max_output_tokens
                    }
                    response = generate_text(prompt, generation_config) # call ke API server yang telah dibuat
                    st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # menambahkan pesan balasan ke dalam session state

if __name__ == "__main__":
    main()


# REFERENSI UI
# https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/