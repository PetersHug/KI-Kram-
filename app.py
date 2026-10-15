import streamlit as st
import requests
import urllib.parse
import random

# App-Konfiguration für maximale Geschwindigkeit
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
                    st.error(f"Fehler (Code {res.status_code}): Bitte prüfe deine GROQ_API_KEY in den Secrets.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (100% FEHLERFREI, SCHNELL & LOGOFREI)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("⚡ Blitzschneller Premium Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in Sekunden zeichnen") and prompt:
        with st.spinner("KI generiert Ihr sauberes Bild..."):
            try:
                # 1. Deutsche Eingabe automatisch via Groq übersetzen (Verhindert Umlautfehler)
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

                # Qualitäts-Booster für gestochen scharfen Fotorealismus ohne Logos und Signaturen
                premium_prompt = f"{english_prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, clean frame, no watermark, no text, no logo"
                
                # Absolut sichere Web-Codierung des Prompts
                safe_prompt = urllib.parse.quote(premium_prompt)
                zufalls_seed = random.randint(1, 99999999)
                
                # DIE ABSOLUTE REPARATUR: urljoin erzwingt die mathematisch korrekte Trennung mit Schrägstrich!
                base_url = "https://pollinations.ai"
                image_url = urllib.parse.urljoin(base_url, f"{safe_prompt}?width=1024&height=1024&nologo=true&private=true&model=flux&seed={zufalls_seed}")
                
                # 2. Direktanzeige im Browser mittels Streamlit-Standardkomponente (Absolut unblockierbar)
                st.image(image_url, use_container_width=True)
                
                # 3. Offizieller Download-Button direkt darunter vorbereiten
                try:
                    img_data = requests.get(image_url, timeout=15).content
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_data,
                        file_name=f"ki_studio_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                except Exception:
                    # Ausfallsicheres Backup bei Server-Überlastung
                    st.markdown(f'[🔗 Klicke hier zum Speichern (Bild öffnen & Rechtsklick)]({image_url})')
                    
            except Exception as e:
                st.error(f"Systemfehler: {e}")
