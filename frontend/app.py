import streamlit as st
import requests

st.set_page_config(page_title="Prédiction de maladie cardiaque", layout="centered")
st.title("Prédiction de maladie cardiaque")
st.write("Remplissez les informations ci-dessous pour estimer le risque de maladie cardiaque.")

def predict_heart_disease(data):
    url = "http://127.0.0.1:8000/predict"
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API: {e}")
        return None

with st.form("formulaire_patient"):
    age = st.number_input("Quel est votre âge ?", min_value=1, max_value=120, value=50)

    sex_label = st.radio("Quel est votre sexe ?", ["Homme", "Femme"])
    sex = 1 if sex_label == "Homme" else 0

    cp_label = st.selectbox(
        "Quel type de douleur thoracique ressentez-vous ?",
        [
            "0 - Douleur typique liée au cœur (effort)",
            "1 - Douleur atypique",
            "2 - Douleur non liée au cœur",
            "3 - Pas de douleur"
        ]
    )
    cp = int(cp_label.split(" - ")[0])

    trestbps = st.number_input("Votre tension artérielle au repos (en mm Hg)", min_value=80, max_value=250, value=120)

    chol = st.number_input("Votre taux de cholestérol total (en mg/dl)", min_value=100, max_value=600, value=200)

    fbs_label = st.radio("Avez-vous une glycémie à jeun supérieure à 120 mg/dl ?", ["Oui", "Non"])
    fbs = 1 if fbs_label == "Oui" else 0

    restecg_label = st.selectbox(
        "Résultat de votre électrocardiogramme au repos :",
        [
            "0 - Normal",
            "1 - Anomalie légère (ST-T)",
            "2 - Épaississement du cœur (hypertrophie)"
        ]
    )
    restecg = int(restecg_label.split(" - ")[0])

    thalach = st.number_input("Fréquence cardiaque maximale atteinte lors d’un effort (en bpm)", min_value=60, max_value=220, value=150)

    exang_label = st.radio("Avez-vous ressenti une douleur thoracique lors d’un effort physique ?", ["Oui", "Non"])
    exang = 1 if exang_label == "Oui" else 0

    oldpeak = st.number_input("Baisse observée du segment ST à l’effort (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    slope_label = st.selectbox(
        "Pente du segment ST pendant l'effort :",
        [
            "0 - Descendante (peu rassurante)",
            "1 - Plate",
            "2 - Montante (meilleure situation)"
        ]
    )
    slope = int(slope_label.split(" - ")[0])

    ca = st.selectbox("Nombre de vaisseaux majeurs visibles à l'examen (de 0 à 4)", [0, 1, 2, 3, 4])

    thal_label = st.selectbox(
        "Résultat de l'examen cardiaque (test au thallium) :",
        [
            "1 - Normal",
            "2 - Anomalie permanente",
            "3 - Anomalie temporaire"
        ]
    )
    thal = int(thal_label.split(" - ")[0])

    submitted = st.form_submit_button("Lancer la prédiction")

if submitted:
    input_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
    }

    result = predict_heart_disease(input_data)

    if result:
        pred = result.get("prediction", None)
        if pred == 1:
            st.error(" Le modèle prédit un **risque élevé de maladie cardiaque**. Il est recommandé de consulter un professionnel de santé.")
        elif pred == 0:
            st.success("Le modèle ne détecte **pas de signe de maladie cardiaque**.")
        else:
            st.warning("Résultat inattendu. Veuillez réessayer.")
