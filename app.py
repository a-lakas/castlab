import streamlit as st
import requests

API_ENDPOINT = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
HEADERS = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

def get_response(input_text):
    data = {
        "inputs": input_text
    }
    response = requests.post(API_ENDPOINT, json=data, headers=HEADERS)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return "Error: Unable to fetch response from the model."

def main():
    st.title("Chat with Gemma (Google Gemma-7B-IT)")

    input_text = st.text_input("You:", "")
    if st.button("Send"):
        response = get_response(input_text)
        st.text_area("Gemma:", response, height=200, max_chars=None)

if __name__ == "__main__":
    main()
