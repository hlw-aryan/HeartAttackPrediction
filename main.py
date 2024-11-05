import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File to store patient data
DATA_FILE = "patient_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["ID", "Name", "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", 
                                 "FastingBS", "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", 
                                 "ST_Slope", "HeartDisease"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def register_patient(df):
    st.subheader("🏥 Register New Patient")
    
    with st.form("patient_form"):
        # Personal Information
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input("Patient ID")
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0)
            sex = st.selectbox("Sex", options=["M", "F"])
        
        with col2:
            chest_pain_type = st.selectbox("Chest Pain Type", options=["ATA", "NAP", "ASY", "TA"])
            fasting_bs = st.number_input("Fasting Blood Sugar", min_value=0.0,format="%.6f")
            exercise_angina = st.selectbox("Exercise Induced Angina", options=["Y", "N"])
            st_slope = st.selectbox("ST Slope", options=["Up", "Flat", "Down"])
        
        # Health Metrics
        st.markdown("### Health Metrics")
        col3, col4 = st.columns(2)
        
        with col3:
            resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0.0,format="%.6f")
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=0.0,format="%.6f")
            max_hr = st.number_input("Max Heart Rate Achieved", min_value=0.0,format="%.6f")
        
        with col4:
            resting_ecg = st.selectbox("Resting ECG", options=["Normal", "ST", "LVH"])
            oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, format="%.6f")
            heart_disease = st.selectbox("Heart Disease", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        
        # Submit Button
        submitted = st.form_submit_button("Register Patient")
    
    if submitted:
        if patient_id and name:
            new_patient = pd.DataFrame({
                "ID": [patient_id],
                "Name": [name],
                "Age": [age],
                "Sex": [sex],
                "ChestPainType": [chest_pain_type],
                "RestingBP": [resting_bp],
                "Cholesterol": [cholesterol],
                "FastingBS": [fasting_bs],
                "RestingECG": [resting_ecg],
                "MaxHR": [max_hr],
                "ExerciseAngina": [exercise_angina],
                "Oldpeak": [oldpeak],
                "ST_Slope": [st_slope],
                "HeartDisease": [heart_disease]
            })
            df = pd.concat([df, new_patient], ignore_index=True)
            save_data(df)
            st.success("Patient registered successfully!")
        else:
            st.error("Please provide both Patient ID and Name.")
    
    return df

def view_patients(df):
    st.subheader("📋 All Patients")
    
    if df.empty:
        st.info("No patients registered yet.")
    else:
        patients_list = df[["ID", "Name"]]
        for _, patient in patients_list.iterrows():
            if st.button(f"{patient['ID']} - {patient['Name']}", key=patient['ID']):
                st.session_state['selected_patient'] = patient['ID']
                st.session_state['view_mode'] = 'details'

def display_patient_details(df, patient_id):
    patient = df[df["ID"] == patient_id].iloc[0]
    
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Patient Profile</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Personal Information Section
    st.markdown("### Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**ID:** {patient['ID']}")
        st.markdown(f"**Name:** {patient['Name']}")
        st.markdown(f"**Age:** {patient['Age']}")
        st.markdown(f"**Sex:** {patient['Sex']}")
    
    with col2:
        st.markdown(f"**Chest Pain Type:** {patient['ChestPainType']}")
        st.markdown(f"**Fasting Blood Sugar:** {patient['FastingBS']} (1 if > 120 mg/dL)")
        st.markdown(f"**Exercise Angina:** {patient['ExerciseAngina']}")
        st.markdown(f"**ST Slope:** {patient['ST_Slope']}")
    
    st.markdown("---")
    
    # Health Metrics Section
    st.markdown("### Health Metrics")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(f"**Resting BP:** {patient['RestingBP']} mmHg")
        st.markdown(f"**Cholesterol:** {patient['Cholesterol']} mg/dL")
        st.markdown(f"**Max Heart Rate Achieved:** {patient['MaxHR']}")
    
    with col4:
        st.markdown(f"**Resting ECG:** {patient['RestingECG']}")
        st.markdown(f"**Oldpeak (ST Depression):** {patient['Oldpeak']:.1f}")
        st.markdown(f"**Heart Disease:** {'Yes' if patient['HeartDisease'] == 1 else 'No'}")
    
    # Visualization (Optional)
    with st.expander("📊 View Health Metrics Chart"):
        metrics = {
            "Resting BP": patient['RestingBP'],
            "Cholesterol": patient['Cholesterol'],
            "Max HR": patient['MaxHR']
        }
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(metrics.keys(), metrics.values(), color=['#FF9999', '#66B3FF', '#99FF99'])
        ax.set_ylabel('Values')
        ax.set_title('Patient Health Metrics')
        st.pyplot(fig)
    
    # Back Button
    st.button("Back to Patient List", on_click=lambda: reset_view_mode())

def reset_view_mode():
    st.session_state['selected_patient'] = None
    st.session_state['view_mode'] = 'list'

def main():
    st.set_page_config(page_title="Patient Management System", layout="wide")
    st.title("🏥 Patient Management System")
    
    # Load existing data
    df = load_data()
    
    # Initialize session state variables
    if 'selected_patient' not in st.session_state:
        st.session_state['selected_patient'] = None
    if 'view_mode' not in st.session_state:
        st.session_state['view_mode'] = 'list'  # Default view mode is list

    menu = ["Register Patient", "View Patients"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Register Patient":
        df = register_patient(df)
    elif choice == "View Patients":
        if st.session_state['view_mode'] == 'details' and st.session_state['selected_patient']:
            display_patient_details(df, st.session_state['selected_patient'])
        else:
            view_patients(df)

if __name__ == "__main__":
    main()
