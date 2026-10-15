import streamlit as st
import requests
import random
import base64

# Titel der Website (Sofort offen ohne Passwort)
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
                    st.error("Fehler bei der Text-Anfrage. Bitte prüfe deine GROQ_API_KEY in den Secrets.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (HUGGING FACE SDXL - STABIL & REIN)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("Offizieller Stabilitäts-Server zeichnet Ihr Bild..."):
            try:
                # 1. Deutsche Eingabe automatisch via Groq übersetzen (Umlaut-Schutz)
                headers_groq = {
                    "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                    "Content-Type": "application/json"
                }
                translation_payload = {
                    "model": "llama-3-8b-8192", 
                    "messages": [{"role": "user", "content": f"Translate to english for an AI image prompt. ONLY plain text, no quotes, no explanations: {prompt}"}]
                }
                translation_res = requests.post("https://groq.com", json=translation_payload, headers=headers_groq)
                english_prompt = translation_res.json()["choices"]["message"]["content"].strip() if translation_res.status_code == 200 else prompt

                # Qualitäts-Booster für gestochen scharfen Fotorealismus ohne Logos
                premium_prompt = f"{english_prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, clean frame, no watermark, no text, no logo"
                
                # 2. Direkter Zugriff auf die stabile, freie Standard-Inferenz von Hugging Face
                # Stable Diffusion XL erzeugt standardmäßig KEINE Logos!
                API_URL = "https://huggingface.co"
                
                # Senden der Anfrage. Wir erwarten direkt die binären Bilddaten zurück
                img_res = requests.post(API_URL, json={"inputs": premium_prompt}, timeout=30)
                
                if img_res.status_code == 200 and len(img_res.content) > 1000:
                    # Wandelt das Bild in einen unblockierbaren Base64-Datenstream um
                    encoded_image = base64.b64encode(img_res.content).decode()
                    
                    # 3. Direktanzeige im Browser (HTML5)
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 4. Offizieller Streamlit Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_res.content,
                        file_name=f"ki_studio_{random.randint(1, 99999)}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Bild-Server bereitet die Infrastruktur vor oder ist ausgelastet. Bitte klicke in 5 Sekunden noch einmal.")
            except Exception as e:
                st.error(f"Systemfehler: {e}")
