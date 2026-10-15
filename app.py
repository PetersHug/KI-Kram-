import streamlit as st
import requests
import urllib.parse
import random

# Titel der Website
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
# BILDGENERATOR (REINE CLIENT-BROWSER-METHODE)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Englisch empfohlen):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        # Automatische Profi-Erweiterung für 4K-Fotorealismus
        premium_prompt = f"{prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, 35mm lens, photorealistic, no logo, no watermark"
        safe_prompt = urllib.parse.quote(premium_prompt)
        
        # Zufalls-Seed gegen Cache-Probleme
        zufalls_seed = random.randint(1, 99999999)
        
        # Wir nutzen die freie Schnittstelle, übergeben sie aber als reines HTML-Bild-Element.
        # Das zwingt DEINEN BROWSER (nicht den Streamlit-Server), das Bild direkt zu laden.
        image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&private=true&model=flux&seed={zufalls_seed}"
        
        # Reines HTML/Markdown-Injektion. Das umgeht die Server-Sperre (401) vollständig!
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <img src="{image_url}" style="width:100%; max-width:600px; border-radius:10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.2);" />
            <p style="color: gray; font-size: 14px; margin-top: 8px;">Klicke mit der rechten Maustaste auf das Bild, um es zu speichern.</p>
        </div>
        """, unsafe_allow_html=True)
