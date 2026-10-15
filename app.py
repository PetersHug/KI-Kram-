import streamlit as st
import requests
import urllib.parse
import random

# Der saubere Wunsch-Titel (Sofort offen für alle)
st.title("Was wünschen Sie? 🚀")

# Auswahlmenü in der Seitenleiste
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
# BILDGENERATOR (FOTOREALISTISCH & LOGO-FREI)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Englisch empfohlen):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI generiert Ihr fotorealistisches Bild..."):
            
            # Automatische Erweiterung für echten Fotorealismus
            premium_prompt = f"{prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, 35mm lens, photorealistic"
            safe_prompt = urllib.parse.quote(premium_prompt)
            
            # Zufalls-Seed für ein frisches Bild bei jedem Klick
            zufalls_seed = random.randint(1, 99999999)
            
            # Die perfekte Parameter-Kombination um Logos und Wasserzeichen abzustellen
            image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&private=true&enhance=true&model=flux&seed={zufalls_seed}"
            
            # Direkte Ausgabe auf deiner Webseite
            st.image(image_url, caption=f"Generiert für: '{prompt}'")
