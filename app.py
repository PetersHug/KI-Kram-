
import streamlit as st
import requests

# Titel der Website
st.title("Was kann ich für Sie tun? 🚀")

# Passwort-Schutz in der Seitenleiste
password = st.sidebar.text_input("Passwort eingeben", type="password")

if password == "DeinSicheresPasswort123":

    # Auswahlbox für den Modus
    modus = st.radio("Wählen Sie eine Funktion:", ["Chatten (Text)", "Bild generieren"])

    # --- CHATTEN (TEXT MODUS) ---
    if modus == "Chatten (Text)":
        user_input = st.text_input("Stellen Sie mir eine Frage:")
        if st.button("Senden") and user_input:
            with st.spinner("Ich denke nach..."):
                headers = {"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"}
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": user_input}]
                }
                res = requests.post("https://groq.com", json=payload, headers=headers)
                if res.status_code == 200:
                    st.write(res.json()["choices"]["message"]["content"])
                else:
                    st.error("Fehler beim Text-Gehirn. Bitte prüfe deine Secrets.")

    # --- BILDGENERATOR (BILD MODUS) ---
    elif modus == "Bild generieren":
        prompt = st.text_input("Beschreiben Sie das Bild (Englisch klappt am besten):")
        if st.button("Bild generieren") and prompt:
            with st.spinner("Ich zeichne Ihr Bild..."):
                formatted_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai{formatted_prompt}?width=1024&height=1024&nologo=true"
                st.image(image_url, caption=f"Generiertes Bild für: {prompt}")
else:
    st.warning("Bitte geben Sie das richtige Passwort in der Seitenleiste ein, um die KI freizuschalten.")
