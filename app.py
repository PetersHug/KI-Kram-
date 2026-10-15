
import streamlit as st
import requests
import urllib.parse

# 1. Neuer Wunsch-Titel der Website
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
    # BILDGENERATOR (BILD MODUS)
    # ==========================================
    elif modus == "Bild generieren":
        st.subheader("🎨 Bild-Designer")
        prompt = st.text_input("Beschreiben Sie Ihr Wunschbild (Englisch empfohlen):")
        
        if st.button("Bild zeichnen") and prompt:
            with st.spinner("Ich zeichne Ihr Bild im Hintergrund..."):
                try:
                    # Macht den Text absolut internet- und URL-sicher
                    safe_prompt = urllib.parse.quote(prompt)
                    
                    # Generiert eine eindeutige URL für das Bild (ohne Anmeldung!)
                    image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true"
                    
                    # Lädt das Bild im Hintergrund als echte Datei herunter, um Browser-Blockaden zu umgehen
                    response = requests.get(image_url, timeout=20)
                    
                    if response.status_code == 200:
                        # Zeigt die heruntergeladene Bilddatei direkt an
                        st.image(response.content, caption=f"Dein generiertes Bild für: '{prompt}'")
                    else:
                        st.error("Der Bild-Server ist gerade überlastet. Bitte versuche es noch einmal.")
                except Exception:
                    st.error("Fehler beim Herunterladen des Bildes. Bitte erneut versuchen.")

# Wenn das Passwort falsch oder leer ist
else:
    st.warning("Bitte geben Sie das richtige Passwort in der linken Seitenleiste ein, um die KI freizuschalten.")
