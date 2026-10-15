import streamlit as st
import requests
import base64
import random

# Titel der Website
st.title("Was wünschen Sie? 🚀")

# Auswahlmenü in der Seitenleiste
modus = st.sidebar.radio("Funktion auswählen:", ["Chatten (Text)", "Bild generieren"])

# ==========================================
# CHATTEN (TEXT MODUS VIA GROQ)
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
                    st.error("Fehler bei der Text-Anfrage. Bitte prüfe deine GROQ_API_KEY.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (GOOGLE IMAGEN 3 - SCHNELL & REIN)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer Google Imagen 3 Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("Google-KI zeichnet Ihr Bild in Höchstgeschwindigkeit..."):
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

                # Qualitäts-Booster für perfekten Google Fotorealismus
                premium_prompt = f"{english_prompt}, professional studio photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, clean frame, no watermark, no text, no logo"
                
                # 2. Schnittstelle zu Google AI Studio (Imagen 3)
                # Die URL enthält deinen kostenlosen Google-Key aus den Secrets
                API_URL = f"https://googleapis.com{st.secrets['GEMINI_API_KEY']}"
                
                headers_google = {"Content-Type": "application/json"}
                payload_google = {
                    "instances": [{"prompt": premium_prompt}],
                    "parameters": {
                        "sampleCount": 1,
                        "outputMimeType": "image/jpeg",
                        "aspectRatio": "1:1"
                    }
                }
                
                res = requests.post(API_URL, json=payload_google, headers=headers_google, timeout=30)
                
                if res.status_code == 200:
                    # Google liefert das Bild direkt als Base64-Text zurück
                    img_base64 = res.json()["predictions"][0]["bytesBase64Encoded"]
                    img_data = base64.b64decode(img_base64)
                    
                    # 3. Direktanzeige im Browser (HTML5)
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 4. Funktionierender Download-Button
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_data,
                        file_name=f"google_imagen_{random.randint(1, 99999)}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error(f"Google-Server meldet einen Fehler (Code {res.status_code}). Bitte prüfe deinen GEMINI_API_KEY.")
            except Exception as e:
                st.error(f"Systemfehler: {e}")
                
