import streamlit as st
import requests
import urllib.parse
import random
import base64

# Titel der Website
st.title("Was kann ich für Sie tun? 🚀")

# Passwort-Schutz in der Seitenleiste
password = st.sidebar.text_input("Passwort eingeben", type="password")

# Prüft, ob das Passwort richtig ist
if password == "DeinSicheresPasswort123":

    # Auswahlmenü für die Funktionen
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
    # BILDGENERATOR (AUSFALLSICHERE BASE64-METHODE)
    # ==========================================
    elif modus == "Bild generieren":
        st.subheader("🎨 Bild-Designer")
        prompt = st.text_input("Beschreiben Sie Ihr Wunschbild (Englisch empfohlen):")
        
        if st.button("Bild zeichnen") and prompt:
            with st.spinner("Künstliche Intelligenz zeichnet Ihr Bild..."):
                try:
                    # Macht den Text internettauglich
                    safe_prompt = urllib.parse.quote(prompt)
                    zufalls_seed = random.randint(1, 999999)
                    
                    # Offizielle API-URL ohne Logos/Wasserzeichen
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&no-watermark=true&seed={zufalls_seed}"
                    
                    # 1. Bild sicher im Hintergrund vom Streamlit-Server anfordern
                    img_response = requests.get(image_url, timeout=30)
                    
                    if img_response.status_code == 200:
                        # 2. Das Bild in Base64-Text umwandeln (macht es immun gegen Browser-Blockaden)
                        encoded_image = base64.b64encode(img_response.content).decode()
                        
                        # 3. Das Bild als Daten-Stream direkt in das HTML einbetten
                        html_code = f"""
                        <div style="text-align: center; margin-top: 20px;">
                            <img src="data:image/jpeg;base64,{encoded_image}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);" />
                            <p style="color: gray; font-size: 14px; margin-top: 5px;">Generiert für: "{prompt}"</p>
                        </div>
                        """
                        st.markdown(html_code, unsafe_allow_html=True)
                    else:
                        st.error("Der Bild-Server liefert gerade keine Daten. Bitte versuche es gleich noch einmal.")
                        
                except Exception as e:
                    st.error(f"Fehler beim Laden des Bildes: {e}")

else:
    st.warning("Bitte geben Sie das richtige Passwort in der linken Seitenleiste ein, um die KI freizuschalten.")
