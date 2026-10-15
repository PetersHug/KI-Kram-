import streamlit as st
import requests
import urllib.parse
import random

# Titel der Website (Sofort offen ohne Passwort!)
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
# BILDGENERATOR (UNBLOCKIERBARE WEB-METHODE)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Englisch empfohlen):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI generiert Ihr fotorealistisches Bild..."):
            
            # Profi-Kamera-Erweiterungen für echten Fotorealismus
            premium_prompt = f"{prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, 35mm lens, photorealistic"
            safe_prompt = urllib.parse.quote(premium_prompt)
            
            # Zufalls-Seed verhindert das Laden alter Bilder aus dem Cache
            zufalls_seed = random.randint(1, 99999999)
            
            # Der offizielle, neue 2026-Endpunkt von Pollinations
            image_url = f"https://gen.pollinations.ai/image/{safe_prompt}?width=1024&height=1024&model=flux&seed={zufalls_seed}&nologo=true"
            
            # DER ULTIMATIVE TRICK: Einbettung über eine HTML-Iframe-Komponente.
            # Das hebelt jede Streamlit-Sicherheitsblockade im Browser aus!
            html_iframe = f"""
            <div style="text-align: center; margin-top: 20px;">
                <iframe src="{image_url}" width="100%" height="550" style="border:none; border-radius:10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.15);" scrolling="no"></iframe>
                <p style="color: gray; font-size: 14px; margin-top: 8px;">Motive: "{prompt}" (Rechtsklick auf das Bild zum Speichern)</p>
            </div>
            """
            st.components.v1.html(html_iframe, height=600)
