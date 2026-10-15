
import streamlit as st
import requests

st.title("Was kann ich für Sie tun")

# 1. Passwort-Schutz (Nur du hast Zugriff)
password = st.sidebar.text_input("Admin-Passwort", type="password")
if password == "c434c$$§c$§$§Vc$%V&bv$V%54":

    # Modus auswählen: Text oder Bild
    modus = st.radio("Was möchtest du tun?", ["Chatten (Text)", "Bild generieren"])

    # --- TEXT MODUS ---
    if modus == "Chatten (Text)":
        user_input = st.text_input("Deine Frage:")
        if st.button("Senden") and user_input:
            with st.spinner("KI denkt nach..."):
                headers = {"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"}
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": user_input}]
                }
                res = requests.post("https://groq.com", json=payload, headers=headers)
                if res.status_code == 200:
                    st.write(res.json()["choices"]["message"]["content"])
                else:
                    st.error("Fehler beim Text-Gehirn. Bitte prüfe deinen GROQ_API_KEY.")

    # --- BILD MODUS (Ohne Anmeldung!) ---
    elif modus == "Bild generieren":
        prompt = st.text_input("Was soll auf dem Bild sein? (Englisch klappt am besten):")
        if st.button("Generieren") and prompt:
            with st.spinner("Bild wird ohne Anmeldung generiert..."):
                # Macht den Text internettauglich (ersetzt Leerzeichen durch %20)
                formatted_prompt = prompt.replace(" ", "%20")
                
                # Nutzt die kostenlose, freie Bild-URL von Pollinations
                image_url = f"https://pollinations.ai{formatted_prompt}?width=1024&height=1024&nologo=true"
                
                # Zeigt das Bild direkt auf deiner Streamlit-Seite an
                st.image(image_url, caption=f"Generiertes Bild für: {prompt}")
else:
    st.warning("Bitte gib das richtige Admin-Passwort in der Seitenleiste ein.")
