import streamlit as st
import requests
import base64
import random
import urllib.parse

# 1. Optimierter Titel der Website
st.title("Was wünschen Sie? 🚀")

# Auswahlmenü in der Seitenleiste
modus = st.sidebar.radio("Funktion auswählen:", ["Chatten (Text)", "Bild generieren"])

# ==========================================
# CHATTEN (TEXT MODUS OPTIMIERT)
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
# BILDGENERATOR (100% LOGO-FREI & OPTIMIERT)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Englisch klappt am besten):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI generiert Ihr sauberes Bild ohne Wasserzeichen..."):
            try:
                # Qualitäts-Booster für perfekten Fotorealismus ohne Text-Überreste
                premium_prompt = f"{prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, award winning photo, clean frame, no watermark, no text, no logo"
                safe_prompt = urllib.parse.quote(premium_prompt)
                
                # Zufälliger Seed verhindert das Laden alter Bilder aus dem Browser-Cache
                zufalls_seed = random.randint(1, 99999999)
                
                # DIE PERFEKTE ROUTE: Der flux-realism Pfad erzeugt standardmäßig KEINE Logos!
                optimized_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&seed={zufalls_seed}&model=flux-realism&nologo=true&private=true"
                
                # Server lädt das Bild stabil im Hintergrund herunter
                img_response = requests.get(optimized_url, timeout=30)
                
                if img_response.status_code == 200:
                    # Macht das Bild immun gegen alle Browser-Sicherheitsblockaden (Base64 Stream)
                    encoded_image = base64.b64encode(img_response.content).decode()
                    
                    # 1. Direktanzeige im Browser ohne störende Elemente
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 2. Direkter Download-Button unter dem Bild
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_response.content,
                        file_name=f"ki_studio_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Bild-Server ist im Moment überlastet. Bitte versuche es noch einmal.")
                    
            except Exception as e:
                st.error(f"Fehler bei der Bildübertragung: {e}")
