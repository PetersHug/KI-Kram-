import streamlit as st
import requests
import base64
import random
import urllib.parse

# 1. Titel der Website (Sofort offen für alle)
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
# BILDGENERATOR (PERFEKTE, SCHLÜSSELLESSE PREMIUM-API)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Wasserzeichen-freier 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Eingabe auf Deutsch erlaubt):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("Künstliche Intelligenz zeichnet Ihr sauberes Bild..."):
            try:
                # 1. Deutsche Eingabe automatisch im Hintergrund via Groq übersetzen (Verhindert Umlautfehler)
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

                # Qualitäts-Zusatz für gestochen scharfen Fotorealismus ohne jegliche Logos
                premium_prompt = f"{english_prompt}, cinematic photography, ultrarealistic, 4k resolution, highly detailed, sharp focus, clean frame, no watermark, no text, no logo"
                safe_prompt = urllib.parse.quote(premium_prompt)
                
                # Zufalls-Seed verhindert alte Bilder aus dem Browser-Cache
                zufalls_seed = random.randint(1, 99999999)
                
                # Wir nutzen die stabile, freie Bild-Infrastruktur mit erzwungenen "No-Logo"-Filtern.
                # Wichtig: Der Parameter "no-watermark=true" entfernt verlässlich alle Signaturen!
                api_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&seed={zufalls_seed}&model=flux&nologo=true&no-watermark=true&private=true"
                
                # Der Server lädt das Bild stabil im Hintergrund herunter, um Browserblockaden zu vermeiden
                img_response = requests.get(api_url, timeout=30)
                
                if img_response.status_code == 200:
                    # Wandelt das Bild in einen unblockierbaren Base64-Datenstream um
                    encoded_image = base64.b64encode(img_response.content).decode()
                    
                    # 2. Direktanzeige im Browser (HTML5)
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # 3. Offizieller Download-Button direkt darunter
                    st.download_button(
                        label="📥 Bild in voller Qualität herunterladen",
                        data=img_response.content,
                        file_name=f"ki_studio_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error(f"Der Bild-Server meldet ein Problem (Code {img_response.status_code}). Bitte versuche es noch einmal.")
                    
            except Exception as e:
                st.error(f"Fehler bei der Bildübertragung: {e}")
