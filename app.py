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
# BILDGENERATOR (UNBLOCKIERBARE MARKDOWN METHODE)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Englisch empfohlen):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI generiert Ihr fotorealistisches Bild..."):
            
            # Profi-Prompt-Erweiterung für 4K-Fotorealismus
            premium_prompt = f"{prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, photorealistic, no text, no logo, clean background"
            safe_prompt = urllib.parse.quote(premium_prompt)
            
            # Zufalls-Seed gegen Browser-Caching
            zufalls_seed = random.randint(1, 99999999)
            
            # Die neue offizielle, wasserzeichenfreie Standard-Domain
            image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&private=true&enhance=true&model=flux&seed={zufalls_seed}"
            
            # DER ULTIMATIVE TRICK: Wir nutzen einfaches Markdown zur Anzeige.
            # Das lädt das Bild direkt als Text-Referenz im Web und umgeht jede Serverblockade von Streamlit!
            st.markdown(f"![Generiertes Bild]({image_url})")
            st.write(f"*Fertig! Bild generiert für: '{prompt}'*")
