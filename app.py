import streamlit as st
import requests
import base64
import random

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
                    st.error("Fehler bei der Text-Anfrage. Bitte prüfe deine GROQ_API_KEY.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (HUGGING FACE FLUX - UNZERSTÖRBAR & REIN)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer FLUX Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("Premium FLUX-Modell generiert dein Bild..."):
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

                # Qualitäts-Booster für perfekten Fotorealismus ohne Wasserzeichen
                premium_prompt = f"{english_prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, photorealistic, clean background, no text, no logo"
                
                # 2. Direktzugriff auf den offiziellen, freien Hugging-Face-Server
                API_URL = "https://huggingface.co"
                
                # Wir senden eine schlüssellose, anonyme Anfrage direkt an das Modell
                res = requests.post(API_URL, json={"inputs": premium_prompt}, timeout=30)
                
                if res.status_code == 200 and len(res.content) > 1000:
                    # Das Bild wird als unblockierbarer Datenstrom verarbeitet
                    encoded_image = base64.b64encode(res.content).decode()
                    
                    # Direktanzeige im Browser (HTML5)
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # Zufallszahl für den Dateinamen
                    zufalls_seed = random.randint(1, 99999)
                    
                    # 3. Funktionierender Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=res.content,
                        file_name=f"ki_flux_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Bild-Server ist im Moment ausgelastet. Bitte klicke noch einmal auf den Button.")
            except Exception as e:
                st.error(f"Fehler bei der Bildgenerierung: {e}")
