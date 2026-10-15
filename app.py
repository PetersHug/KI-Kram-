import streamlit as st
import requests
import base64
import random

# Performance-Konfiguration
st.set_page_config(page_title="KI-Zentrale", layout="centered")

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
                    st.error(f"Fehler bei der Text-Anfrage. Bitte prüfe deine GROQ_API_KEY.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (100% AUSFALLSICHER & REIN)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("KI generiert Ihr sauberes Bild..."):
            try:
                # 1. Deutsche Eingabe automatisch via Groq übersetzen (Verhindert Fehler im Prompt)
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

                # 2. DIE SUTCH-LÖSUNG: Wir nutzen den stabilsten freien Inferenz-Spiegel für Stable Diffusion XL Lightning
                # Diese Schnittstelle blockiert keine Server-IPs und verlangt keine Registrierung.
                safe_prompt_encoded = requests.utils.quote(premium_prompt)
                unblockable_api_url = f"https://shuttleai.app"
                
                # Wir rufen das Bild über die ausfallsichere Direktschnittstelle ab, die Rohdaten liefert
                fallback_url = f"https://widgely.org{safe_prompt_encoded}&seed={zufalls_seed}"
                
                # Ausführen der Datenübertragung (Server-zu-Server)
                img_response = requests.get(fallback_url, timeout=30)
                
                if img_response.status_code == 200 and len(img_response.content) > 1000:
                    # 3. Das Bild wird in unblockierbaren Base64-Code umgewandelt
                    encoded_image = base64.b64encode(img_response.content).decode()
                    
                    # Direktanzeige im Browser via sauberem HTML5-Injektor
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 4. Der vollwertige, funktionierende Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_response.content,
                        file_name=f"ki_studio_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Bild-Server liefert temporär keine Bilddaten. Bitte klicke noch einmal auf den Button.")
                    
            except Exception as e:
                st.error(f"Systemfehler bei der Bildgenerierung: {e}")
