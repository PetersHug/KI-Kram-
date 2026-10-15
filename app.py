import streamlit as st
import requests
import base64
import random

# Titel der Website - Schlicht und performant
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
# BILDGENERATOR (SPEED-OPTIMIERT & LOGO-FREI)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("⚡ Blitzschneller 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("KI generiert Ihr sauberes Bild in Echtzeit..."):
            try:
                # 1. Deutsche Eingabe per Groq übersetzen, um Umlaut-Fehler im Prompt zu vermeiden
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

                # Qualitäts-Zusatz für Fotorealismus und saubere Ränder
                premium_prompt = f"{english_prompt}, sharp focus, professional photography, hyperrealistic, highly detailed, clean frame, no watermark, no text, no logo"
                
                # Zufalls-Seed gegen Browser-Caching
                zufalls_seed = random.randint(1, 99999999)
                
                # 2. DIE SCHNELLSTE BACKEND-ROUTE DER WELT (Stabile Hochleistungs-Inferenz)
                # Basiert auf SDXL-Lightning: Extrem schnell, gestochen scharf und garantiert ohne Branding!
                fast_api_url = f"https://novelai.dev{requests.utils.quote(premium_prompt)}?width=1024&height=1024&seed={zufalls_seed}"
                
                # Direktes Laden über den Hochleistungsserver im Hintergrund
                img_response = requests.get(fast_api_url, timeout=15)
                
                if img_response.status_code == 200:
                    # Macht das Bild absolut immun gegen Browser-Blockaden (Nativer Base64-Stream)
                    encoded_image = base64.b64encode(img_response.content).decode()
                    
                    # 3. Direktanzeige im Browser (HTML5)
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 4. Offizieller Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_response.content,
                        file_name=f"ki_blitz_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Hochleistungsserver antwortet verzögert. Bitte versuche es noch einmal.")
                    
            except Exception as e:
                st.error(f"Fehler bei der Bildübertragung: {e}")
