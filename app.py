python
import streamlit as st
import requests

st.title("Meine All-in-One KI 🚀")

# 1. Passwort-Schutz (Nur du hast Zugriff)
password = st.sidebar.text_input("Admin-Passwort", type="password")
if password == "DeinSicheresPasswort123":

    # Modus auswählen: Text oder Bild
    modus = st.radio("Was möchtest du tun?", ["Chatten (Text)", "Bild generieren"])

    # --- TEXT MODUS ---
    if modus == "Chatten (Text)":
        user_input = st.text_input("Deine Frage:")
        if st.button("Senden") and user_input:
            with st.spinner("KI denkt nach..."):
                headers = {"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"}
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": user_input}]
                }
                res = requests.post("https://groq.com", json=payload, headers=headers)
                st.write(res.json()["choices"]["message"]["content"])

    # --- BILD MODUS ---
    elif modus == "Bild generieren":
        prompt = st.text_input("Was soll auf dem Bild sein? (Englisch empfohlen):")
        if st.button("Generieren") and prompt:
            with st.spinner("Bild wird gemalt..."):
                headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
                res = requests.post("https://huggingface.co", headers=headers, json={"inputs": prompt})
                if res.status_code == 200:
                    st.image(res.content)
                else:
                    st.error("Fehler bei der Bildgenerierung.")
else:
    st.warning("Bitte gib das richtige Admin-Passwort in der Seitenleiste ein.")
