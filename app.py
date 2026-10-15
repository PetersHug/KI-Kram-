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
                        "model": "llama-3-8b-8192", 
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://groq.com", json=payload, headers=headers)
                    
                    if res.status_code == 200:
                        st.write(res.json()["choices"]["message"]["content"])
                    else:
                        st.error(f"Fehler von Groq (Code {res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

    # ==========================================
    # BILDGENERATOR (PREMIUM FLUX - WASSERZEICHEN-FREI)
    # ==========================================
    elif modus == "Bild generieren":
        st.subheader("🎨 Premium Bild-Designer")
        prompt = st.text_input("Beschreiben Sie Ihr Wunschbild (Englisch empfohlen):")
        
        if st.button("Bild zeichnen") and prompt:
            with st.spinner("Künstliche Intelligenz generiert Ihr Bild..."):
                # Macht den Text internettauglich
                safe_prompt = urllib.parse.quote(prompt)
                
                # Erzeugt einen zufälligen Code für ein frisches Bild
                zufalls_seed = random.randint(1, 99999999)
                
                # DER FIX: Wir nutzen das extrem starke 'flux' Modell.
                # 'nologo=true' und 'private=true' garantieren ein sauberes Bild ohne Wasserzeichen!
                image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&private=true&model=flux&seed={zufalls_seed}"
                
                # Übermittlung direkt an das Browserfenster des Nutzers (Keine Serverblockaden möglich!)
                st.image(image_url, caption=f"Generiert für: '{prompt}'")

# Wenn das Passwort falsch oder leer ist
else:
    st.warning("Bitte geben Sie das richtige Passwort in der linken Seitenleiste ein, um die KI freizuschalten.")
