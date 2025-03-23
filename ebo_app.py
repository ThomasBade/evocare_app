import streamlit as st
import openai

st.set_page_config(page_title="EBoMo GPT-Assessment", layout="centered")

st.title("EBoMo Assessment – GPT-gestützte Auswertung")
st.markdown("**Projekt: MobilBleiben@home** – Digital unterstützte Mobilitätsförderung")

# Eingabeformular
with st.form("assessment_form"):
    mobilität = st.selectbox("Wie schätzt du die Mobilität ein?", ["gut", "mäßig", "eingeschränkt"])
    hilfe_bettstuhl = st.selectbox("Hilfe beim Aufstehen aus Bett/Stuhl?", ["keine", "mit Hilfe", "nicht möglich"])
    gehstrecke = st.text_input("Gehstrecke (z. B. mit Rollator, selbstständig, unsicher ...)")
    sturzangst = st.selectbox("Hat die Person Angst vor Stürzen?", ["nein", "manchmal", "ja"])
    ziel = st.text_input("Was möchte die Person wieder besser können?")
    submitted = st.form_submit_button("GPT-Auswertung generieren")

# GPT-API-Schlüssel (manuell einfügen)
openai.api_key = "DEIN_API_KEY"

if submitted:
    with st.spinner("GPT denkt nach ..."):
        assessment_daten = {
            "mobilität": mobilität,
            "hilfe_bettstuhl": hilfe_bettstuhl,
            "gehstrecke": gehstrecke,
            "sturzangst": sturzangst,
            "ziel": ziel
        }

        prompt = f"""Erstelle eine pflegefachliche Mobilitätsauswertung auf Basis dieser Daten:
{assessment_daten}
Formuliere ein Pflegeziel und 2 Maßnahmen gemäß DNQP-Expertenstandard 'Mobilität'.
Sprich in klarer, sachlicher Sprache für Pflegekräfte."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du bist eine erfahrene Pflegefachkraft."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            st.success("Auswertung:")
            st.markdown(result)
        except Exception as e:
            st.error(f"Fehler beim Abrufen der GPT-Auswertung: {e}")
