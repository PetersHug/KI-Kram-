
import streamlit as st
import requests
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
                    st.error("Fehler bei der Text-Anfrage. Bitte prüfe deine GROQ_API_KEY.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (PRODIAS SDXL - BLITZSCHNELL & REIN)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("KI generiert Ihr sauberes Bild..."):
            try:
                # 1. Deutsche Eingabe automatisch via Groq übersetzen
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
                
                # Absolut sichere Trennung: Wir nutzen ein Dictionary für die Parameter!
                # Python übergibt dies isoliert an die API. Ein Verschmelzen von Worten ist unmöglich.
                zufalls_seed = random.randint(1, 99999999)
                api_base_url = "https://prodia.com"
                
                headers_api = {
                    "X-Prodia-Key": "00000000-0000-0000-0000-000000000000",
                    "Content-Type": "application/json"
                }
                
                payload_api = {
                    "prompt": premium_prompt,
                    "model": "sdxl_lightning.safetensors",
                    "seed": zufalls_seed
                }
                
                # Wir stoßen die Generierung über ein sicheres JSON-Paket an
                response = requests.post(api_base_url, json=payload_api, headers=headers_api, timeout=20)
                
                if response.status_code == 200:
                    # Prodia liefert eine direkte, saubere Bild-URL zurück
                    job_id = response.json()["job"]
                    status_url = f"https://prodia.com{job_id}"
                    
                    # Kurz warten, bis das Bild fertig berechnet ist
                    import time
                    for _ in range(10):
                        time.sleep(1)
                        status_res = requests.get(status_url, headers=headers_api)
                        if status_res.json()["status"] == "succeeded":
                            image_url = status_res.json()["imageUrl"]
                            break
                    
                    # Bild-Rohdaten für Anzeige und unblockierbaren Download herunterladen
                    img_data = requests.get(image_url).content
                    
                    # 2. Direktanzeige über Streamlits eigene, sichere Komponente
                    st.image(img_data, use_container_width=True)
                    
                    # 3. Funktionierender Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_data,
                        file_name=f"ki_studio_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Bild-Server meldet eine Verzögerung. Bitte versuche es noch einmal.")
                    
            except Exception as e:
                st.error(f"Systemfehler: {e}")
