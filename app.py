import streamlit as st
import requests
import base64
import random
import time

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
# BILDGENERATOR (AI HORDE INFRASTRUKTUR - NEU)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Wasserzeichen-freier 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI-Netzwerk zeichnet Ihr sauberes Bild..."):
            try:
                # 1. Deutsche Eingabe automatisch übersetzen
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

                # Qualitäts-Zusatz für gestochen scharfen Fotorealismus
                premium_prompt = f"{english_prompt}, masterpiece, 4k photography, hyperrealistic, sharp focus, clean composition, no text, no logo, no watermark"

                # 2. Anfrage an das dezentrale AI Horde Netzwerk senden
                HORDE_URL = "https://aihorde.net"
                horde_headers = {
                    "Content-Type": "application/json",
                    "apikey": "0000000000"  # Der offizielle, freie Open-Source Schlüssel
                }
                
                horde_payload = {
                    "prompt": premium_prompt,
                    "params": {
                        "n": 1,
                        "width": 1024,
                        "height": 1024,
                        "steps": 25,
                        "sampler_name": "k_euler_a"
                    },
                    "models": ["stable_diffusion"]
                }
                
                init_res = requests.post(HORDE_URL, json=horde_payload, headers=horde_headers)
                
                if init_res.status_code == 202:
                    req_id = init_res.json()["id"]
                    check_url = f"https://aihorde.net{req_id}"
                    
                    # Warten, bis ein Server im Netzwerk das Bild fertig gezeichnet hat
                    status = "processing"
                    for _ in range(30):
                        time.sleep(2)
                        check_res = requests.get(check_url)
                        if check_res.status_code == 200 and check_res.json().get("done"):
                            status = "done"
                            break
                    
                    if status == "done":
                        # Bild-Daten abholen
                        status_url = f"https://aihorde.net{req_id}"
                        status_res = requests.get(status_url)
                        img_web_url = status_res.json()["generations"][0]["img"]
                        
                        # Bild über Server streamen, um Browserfilter zu umgehen
                        img_data = requests.get(img_web_url).content
                        encoded_image = base64.b64encode(img_data).decode()
                        
                        # 3. Direktanzeige im Browser (HTML5)
                        html_code = f"""
                        <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                            <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                        </div>
                        """
                        st.markdown(html_code, unsafe_allow_html=True)
                        
                        # 4. Offizieller Download-Button darunter
                        st.download_button(
                            label="📥 Bild in voller Qualität herunterladen",
                            data=img_data,
                            file_name=f"ki_horde_{random.randint(1,99999)}.jpg",
                            mime="image/jpeg"
                        )
                    else:
                        st.error("Das Netzwerk benötigt gerade zu lange. Bitte versuche es noch einmal.")
                else:
                    st.error("Fehler beim Starten des Bild-Netzwerks.")
                    
            except Exception as e:
                st.error(f"Fehler bei der Bildübertragung: {e}")
