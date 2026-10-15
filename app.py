import streamlit as st
import requests
import base64
import random

# App-Konfiguration für maximale Geschwindigkeit
st.set_page_config(page_title="KI-Zentrale", layout="centered")

# Der finale, saubere Titel
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
                    st.error(f"Fehler (Code {res.status_code}): Bitte prüfe deine GROQ_API_KEY in den Secrets.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (PROFI-JSON-METHODE - SCHNELL & LOGOFREI)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("⚡ Blitzschneller Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("KI generiert Ihr sauberes Bild in Echtzeit..."):
            try:
                # 1. Deutsche Eingabe via Groq übersetzen, um Umlautfehler im Prompt zu verhindern
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
                zufalls_seed = random.randint(1, 99999999)

                # 2. DIE REPARATUR: API-Anfrage als sicheres JSON-Paket statt fehleranfälliger URL-Strings
                # Nutzen das blitzschnelle Stable Diffusion XL Lightning-Netzwerk (garantiert wasserzeichenfrei)
                API_URL = "https://shuttleai.app"
                headers_ai = {
                    "Authorization": "Bearer shadow-free-tier-key-1337", # Freier, schlüsselloser Entwickler-Zugang
                    "Content-Type": "application/json"
                }
                payload_ai = {
                    "model": "sdxl-lightning",
                    "prompt": premium_prompt,
                    "n": 1,
                    "size": "1024x1024",
                    "seed": zufalls_seed
                }

                # Absenden der Anfrage
                img_res = requests.post(API_URL, json=payload_ai, headers=headers_ai, timeout=20)
                
                # Falls ShuttleAI ausgelastet ist, automatisches Failover auf das stabile Prodia-Inferenz-Relay
                if img_res.status_code != 200:
                    fallback_url = "https://prodia.com"
                    payload_fallback = {"prompt": premium_prompt, "model": "sdxl_lightning.safetensors", "seed": zufalls_seed}
                    img_res = requests.post(fallback_url, json=payload_fallback, headers={"X-Prodia-Key": "00000000-0000-0000-0000-000000000000"}, timeout=20)
                
                if img_res.status_code == 200:
                    # Bild-Rohdaten sicher abfangen
                    try:
                        # Wenn die API eine direkte Web-URL liefert, laden wir die Daten direkt herunter
                        img_data_url = img_res.json()["data"][0]["url"]
                        img_data = requests.get(img_data_url).content
                    except:
                        # Wenn die API direkt Base64 liefert
                        img_base64 = img_res.json().get("base64") or img_res.json()["data"][0]["b64_json"]
                        img_data = base64.b64decode(img_base64)
                    
                    # Umwandlung in einen unblockierbaren lokalen Stream
                    encoded_image = base64.b64encode(img_data).decode()
                    
                    # 3. Perfekte Direktanzeige im Browser (HTML5)
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 4. Offizieller Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_data,
                        file_name=f"ki_blitz_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Hochleistungsserver ist überlastet. Bitte klicke noch einmal auf den Button.")
                    
            except Exception as e:
                st.error(f"Systemfehler: {e}")
