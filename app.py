import streamlit as st
import requests

# Dein neuer Wunsch-Titel
st.title("Was kann ich für Sie tun? 🚀")

# 1. Passwort-Schutz (Nur du/deine Kunden haben Zugriff)
password = st.sidebar.text_input("Passwort eingeben", type="password")

if password == "DeinSicheresPasswort123": # Das Passwort kannst du hier ändern

    # Auswahlmenü für den Nutzer: Text oder Bild
    modus = st.radio("Wählen Sie eine Funktion:", ["Chatten (Text)", "Bild generieren"])

    # --- CHATTEN (TEXT MODUS) ---
    if modus == "Chatten (Text)":
        user_input = st.text_input("Stellen Sie mir eine Frage:")
        if st.button("Senden") and user_input:
            with st.spinner("Ich denke nach..."):
                headers = {"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"}
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": user_input}]
                }
                res = requests.post("https://groq.com", json=payload, headers=headers)
                if res.status_code == 200:
                    st.write(res.json()["choices"]["message"]["content"])
                else:
                    st.error("Fehler beim Text-Gehirn. Bitte prüfe deine Secrets.")

    # --- BILDGENERATOR (BILD MODUS) ---
    elif modus == "Bild generieren":
        prompt = st.text_input("Beschreiben Sie das Bild (Englisch klappt am besten):")
        if st.button("Bild generieren") and prompt:
            with st.spinner("Ich zeichne Ihr Bild..."):
                # Macht den eingegebenen Text internettauglich (ersetzt Leerzeichen durch %20)
                formatted_prompt = prompt.replace(" ", "%20")
                
                # Ruft den kostenlosen Bildgenerator ohne Anmeldung ab
                image_url = f"https://pollinations.ai{formatted_prompt}?width=1024&height=1024&nologo=true"
                
                # Zeigt das fertige Bild direkt auf deiner Streamlit-Seite an
                st.image(image_url, caption=f"Generiertes Bild für: {prompt}")
else:
    st.warning("Bitte geben Sie das richtige Passwort in der Seitenleiste ein, um die KI freizuschalten.")
Verwende Code mit Vorsicht.
5. Klicke oben rechts auf den grünen Button "Commit changes..." (Änderungen speichern) und bestätige es noch einmal.

Was jetzt auf deiner Webseite passiert:

Streamlit übernimmt die Änderung in wenigen Sekunden vollautomatisch. Wenn du dich jetzt auf deiner Seite einloggst, siehst du unter der Überschrift zwei auswählbare Punkte (Radio-Buttons):
1. "Chatten (Text)"
2. "Bild generieren"
Sobald du auf Bild generieren klickst, wechselt die Maske. Du kannst dort zum Beispiel cyberpunk astronaut neon style eingeben, auf den Button klicken, und deine App zaubert das Bild direkt auf den Bildschirm.
Hat das Aktualisieren geklappt und siehst du den Bildgenerator jetzt einsatzbereit auf deiner Seite?
KI-Antworten können Fehler enthalten. Weitere Informationen
