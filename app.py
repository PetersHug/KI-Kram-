import streamlit as st
import requests
import random

# App-Konfiguration für maximale Ladegeschwindigkeit
st.set_page_config(page_title="KI-Zentrale", layout="centered")

# Der saubere Wunsch-Titel
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
                    st.error("Fehler bei der Text-Anfrage. Bitte prüfe deine GROQ_API_KEY in den Secrets.")
            except Exception as e:
                st.error(f"Verbindung zum Text-Server fehlgeschlagen: {e}")

# ==========================================
# BILDGENERATOR (BLITZSCHNELL, UNBLOCKIERBAR & REIN)
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

                # Qualitäts-Booster für gestochen scharfen Fotorealismus ohne Logos und Signaturen
                premium_prompt = f"{english_prompt}, professional photography, 4k resolution, hyperrealistic, highly detailed, sharp focus, clean frame, no watermark, no text, no logo"
                
                # Mathematisch sichere Codierung (Keine String-Verkettungsfehler möglich!)
                safe_prompt = requests.utils.quote(premium_prompt)
                zufalls_seed = random.randint(1, 99999999)
                
                # Der stabile, unzensierte High-End Flux Bild-Pfad
                # nologo=true und private=true schalten alle Wasserzeichen vollständig ab!
                image_url = f"https://pollinations.ai{safe_prompt}?width=1024&height=1024&nologo=true&private=true&model=flux&seed={zufalls_seed}"
                
                # 2. DER ULTIMATIVE TRICK: Einbettung über eine HTML5/JavaScript-Komponente.
                # Dein BROWSER lädt das Bild direkt von der Quelle. Der Streamlit-Server wird komplett umgangen!
                # Das integrierte Skript erlaubt das sofortige Abspeichern ohne blockierte Downloads.
                html_code = f"""
                <div style="text-align: center; margin-top: 20px;">
                    <img id="ki_image" src="{image_url}" style="width: 100%; max-width: 600px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);" />
                    <br><br>
                    <button onclick="downloadImage()" style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0px 2px 5px rgba(0,0,0,0.2);">
                        📥 Bild in voller Qualität herunterladen
                    </button>
                </div>

                <script>
                async function downloadImage() {{
                    try {{
                        const image = document.getElementById('ki_image');
                        const response = await fetch(image.src);
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = 'ki_studio_{zufalls_seed}.jpg';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }} catch (err) {{
                        // Fallback, falls der Browser den direkten JavaScript-Download sperrt
                        window.open('{image_url}', '_blank');
                    }}
                }}
                </script>
                """
                # Betten das HTML-Element absolut unblockierbar in Streamlit ein
                st.components.v1.html(html_code, height=650)
                    
            except Exception as e:
                st.error(f"Systemfehler: {e}")
