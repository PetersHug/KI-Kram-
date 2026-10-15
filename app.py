
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
                    headers = {
                        "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        # Nutzen das stabilste und aktuellste Standardmodell
                        "model": "llama-3-8b-8192", 
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://groq.com", json=payload, headers=headers)
                    
                    if res.status_code == 200:
                        st.write(res.json()["choices"]["message"]["content"])
                    else:
                        # Zeigt dir jetzt die ECHTE Fehlermeldung von Groq an!
                        st.error(f"Fehler von Groq (Code {res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

    # ==========================================
    # BILDGENERATOR (PERFEKTE HTML-METHODE OHNE WASSERZEICHEN)
    # ==========================================
    elif modus == "Bild generieren":
        st.subheader("🎨 Bild-Designer")
        prompt = st.text_input("Beschreiben Sie Ihr Wunschbild (Englisch empfohlen):")
        
        if st.button("Bild zeichnen") and prompt:
            with st.spinner("Künstliche Intelligenz zeichnet Ihr Bild..."):
                safe_prompt = urllib.parse.quote(prompt)
                zufalls_seed = random.randint(1, 999999)
                image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&no-watermark=true&seed={zufalls_seed}"
                
                html_code = f"""
                <div style="text-align: center; margin-top: 20px;">
                    <img src="{image_url}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);" />
                    <p style="color: gray; font-size: 14px; margin-top: 5px;">Generiert für: "{prompt}"</p>
                </div>
                """
                st.markdown(html_code, unsafe_allow_html=True)

else:
    st.warning("Bitte geben Sie das richtige Passwort in der linken Seitenleiste ein, um die KI freizuschalten.")
