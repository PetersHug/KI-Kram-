import streamlit as st
import requests
import urllib.parse
import random

# Titel der Website
st.title("Was kann ich für Sie tun? 🚀")

# Passwort-Schutz in der Seitenleiste
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
    # BILDGENERATOR (WASSERZEICHEN-FREI & REAKTIV)
    # ==========================================
    elif modus == "Bild generieren":
        st.subheader("🎨 Bild-Designer (Wasserzeichen-frei)")
        prompt = st.text_input("Beschreiben Sie Ihr Wunschbild (Englisch empfohlen):")
        
        if st.button("Bild zeichnen") and prompt:
            with st.spinner("Künstliche Intelligenz zeichnet..."):
                # Macht den Text internettauglich
                safe_prompt = urllib.parse.quote(prompt)
                
                # Generiert eine Zufallszahl (Seed), damit Streamlit das Bild zwingend neu lädt
                zufalls_seed = random.randint(1, 999999)
                
                # WICHTIG: Die Parameter "nologo=true" und "no-watermark" schalten alle Logos ab!
                image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&no-watermark=true&seed={zufalls_seed}"
                
                # Zeigt das saubere Bild direkt auf der Seite an
                st.image(image_url, caption=f"Dein fertiges Bild für: '{prompt}'")

# Wenn das Passwort falsch oder leer ist
else:
    st.warning("Bitte geben Sie das richtige Passwort in der linken Seitenleiste ein, um die KI freizuschalten.")
