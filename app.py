import streamlit as st
import requests
import urllib.parse
import random
import base64

# Titel der Website (Vollständig passwortfrei)
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
# BILDGENERATOR (DIREKT-ANZEIGE & DOWNLOAD)
# ==========================================
elif modus == "Bild generieren":
    st.subheader("📸 Fotorealistischer 4K Bild-Designer")
    prompt = st.text_input("Was soll auf dem Bild sein? (Englisch empfohlen):")
    
    if st.button("Bild in 4K zeichnen") and prompt:
        with st.spinner("KI generiert Ihr fotorealistisches Bild..."):
            try:
                # Automatische Erweiterung für 4K-Qualität und echten Fotorealismus
                premium_prompt = f"{prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, photorealistic"
                safe_prompt = urllib.parse.quote(premium_prompt)
                
                # Zufalls-Seed verhindert das Laden alter Bilder aus dem Zwischenspeicher
                zufalls_seed = random.randint(1, 99999999)
                
                # Die freie, unzensierte Bild-Schnittstelle ohne Wasserzeichen-Zwang
                # nologo=true schaltet das Pollinations-Logo in der Ecke vollständig ab!
                image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&private=true&model=flux&seed={zufalls_seed}"
                
                # 1. Server lädt das Bild im Hintergrund als reinen Datenstrom herunter
                img_response = requests.get(image_url, timeout=30)
                
                if img_response.status_code == 200:
                    # 2. Wandelt das Bild in Base64-Text um (macht es immun gegen Browser-Blockaden!)
                    encoded_image = base64.b64encode(img_response.content).decode()
                    
                    # 3. Direktanzeige im Browser via HTML
                    html_code = f"""
                    <div style="text-align: center; margin-top: 20px;">
                        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.2);" />
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    # Platz zwischen Bild und Button schaffen
                    st.write("")
                    
                    # 4. Offizieller Streamlit-Download-Button direkt unter dem Bild
                    st.download_button(
                        label="📥 Bild in voller 4K-Qualität herunterladen",
                        data=img_response.content,
                        file_name=f"ki_bild_{zufalls_seed}.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("Der Bild-Server liefert gerade keine Daten. Bitte klicke noch einmal auf den Button.")
                    
            except Exception as e:
                st.error(f"Fehler bei der Bildübertragung: {e}")
