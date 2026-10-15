import streamlit as st
import requests
import urllib.parse

# 1. Titel der Website
st.title("Was kann ich für Sie tun? 🚀")

# 2. Passwort-Schutz in der Seitenleiste
password = st.sidebar.text_input("Passwort eingeben", type="password")

# Prüft, ob das Passwort richtig ist
if password == "DeinSicheresPasswort123":

    # Auswahlmenü für die Funktionen
    modus = st.sidebar.radio("Funktion auswählen:", ["Chatten (Text)", "Bild generieren"])

    # ==========================================
    # CHATTEN (TEXT MODUS)
    # ==========================================
    if modus == "Chatten (Text)":
        st.subheader("🤖 Text-Assistent")
        user_input = st.text_input("Stellen Sie mir eine Frage:")
        
        if st.button("Antwort generieren") and user_input:
            with st.spinner("Ich denke nach..."):
                try:
                    headers = {"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"}
                    payload = {
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://groq.com", json=payload, headers=headers)
                    
                    if res.status_code == 200:
                        st.write(res.json()["choices"]["message"]["content"])
                    else:
                        st.error("Fehler beim Text-Gehirn. Bitte prüfe deine Streamlit Secrets (GROQ_API_KEY).")
                except Exception:
                    st.error("Verbindung zum Text-Server fehlgeschlagen.")

    # ==========================================
    # BILDGENERATOR (BILD MODUS - DIREKTLINK-METHODE)
    # ==========================================
    elif modus == "Bild generieren":
        st.subheader("🎨 Bild-Designer")
        prompt = st.text_input("Beschreiben Sie Ihr Wunschbild (Englisch empfohlen):")
        
        if st.button("Bild zeichnen") and prompt:
            # Erstellt die URL vollkommen sicher
            safe_prompt = urllib.parse.quote(prompt)
            # Nutzt die stabile, offizielle URL von Pollinations
            image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true"
            
            # Der Trick: Streamlit reicht die URL direkt an das Browserfenster weiter.
            # Kein fehleranfälliges Herunterladen im Hintergrund mehr nötig!
            st.image(image_url, caption=f"Dein generiertes Bild für: '{prompt}'")

# Wenn das Passwort falsch oder leer ist
else:
    st.warning("Bitte geben Sie das richtige Passwort in der linken Seitenleiste ein, um die KI freizuschalten.")
