import streamlit as st
import requests
import base64
import random
import urllib.parse
import re

# 1. Titel der Website
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
# BILDGENERATOR (PERFEKT, FOTOREALISTISCH & REIN)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe komplett auf Deutsch erlaubt):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI übersetzt und zeichnet Ihr sauberes Bild..."):
            try:
                # 1. Deutsche Eingabe per Groq ins Englische übersetzen
                headers = {
                    "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                    "Content-Type": "application/json"
                }
                translation_payload = {
                    "model": "llama-3-8b-8192", 
                    "messages": [{"role": "user", "content": f"Translate this text to english for an AI image prompt. Output ONLY the plain translation text, no quotes, no explanation: {prompt}"}]
                }
                translation_res = requests.post("https://groq.com", json=translation_payload, headers=headers)
                
                if translation_res.status_code == 200:
                    english_prompt = translation_res.json()["choices"]["message"]["content"].strip()
                else:
                    english_prompt = prompt

                # 2. Text radikal von allen Zeichen säubern, die den Server abstürzen lassen könnten
                english_prompt = re.sub(r'[^a-zA-Z0-9\s,.-]', '', english_prompt)
                
                # Premium Fotorealismus-Zusätze anhängen
                premium_prompt = f"{english_prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, award winning photo, clean frame, no watermark, no text, no logo"
                
                # Absolut sichere Web-Codierung
                safe_prompt = urllib.parse.quote(premium_prompt)
                zufalls_seed = random.randint(1, 99999999)
                
                # Die saubere Schnittstelle über das Flux-Modell
                optimized_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={zufalls_seed}&model=flux&nologo=true&private=true"
                
                # 3. Das Bild stabil über den Server herunterladen
                img_response = requests.get(optimized_url, timeout=30)
                
                if img_response.status_code == 200:
                    # Direktanzeige im Browser mittels Streamlit-Standardkomponente (unblockierbar)
                    st.image(img_response.content, use_container_width=True)
                    
                    # 4. Offizieller Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_response.content,
                        file_name=f"ki_studio_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error(f"Der Server meldet einen Fehler (Code {img_response.status_code}). Bitte versuche es noch einmal.")
                    
            except Exception as e:
                st.error(f"Fehler bei der Bildübertragung: {e}")
