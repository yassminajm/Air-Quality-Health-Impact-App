import streamlit as st
from joblib import load
import pandas as pd
import pickle
from xgboost import XGBClassifier


st.set_page_config(page_title="Classifier",
                   page_icon="🩺")


def surveyMod():

    st.title("How will the air quality of your city impact your health?")
    st.write(" ")
    descp = f"""
            The trained classification model will allow you to classify the health impact based on the data you provide in 
            the survey below. Specifically, the model used was XGBoost, which has a lot of advantages, such as: it can manage 
            large databases with multiple variables, its results are truly precise, it has excellent execution speed, and more.
            Also, it must be added that we did not use the RecordID field, as it does not provide any relevant information to the 
            classification task, and neither the HealthImpactScore field, as it gives the same information as the target variable.
            """
    st.markdown(descp, unsafe_allow_html=True)

    if 'submissions' not in st.session_state:
        st.session_state.submissions = []


    model = load('data/xgboost_model.joblib')


    with st.form("my_form"):
        st.write("Answer this survey to classify (if there is any field you do not know, you can look it up on the internet, for example, through [this link](https://www.accuweather.com/es/es/valencia/310683/air-quality-index/310683)):")
    
        # Air Quality Data
        st.header("Air Quality Metrics")
        aqi = st.number_input("AQI: Air Quality Index", min_value=0.0, format="%.1f")
        pm10 = st.number_input("PM10: Particulate Matter <10μm (μg/m³)", min_value=0.0, format="%.1f")
        pm2_5 = st.number_input("PM2.5: Particulate Matter <2.5μm (μg/m³)", min_value=0.0, format="%.1f")
        no2 = st.number_input("NO2: Nitrogen Dioxide (ppb)", min_value=0.0, format="%.1f")
        so2 = st.number_input("SO2: Sulfur Dioxide (ppb)", min_value=0.0, format="%.1f")
        o3 = st.number_input("O3: Ozone (ppb)", min_value=0.0, format="%.1f")

        # Weather Conditions
        st.header("Weather Conditions")
        temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=50.0, format="%.1f")
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, format="%.1f")
        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, format="%.1f")

        # Health Impact Metrics
        st.header("Health Impact Metrics")
        respiratory_cases = st.number_input("Number of Respiratory Cases (your cases)", min_value=0, step=1)
        cardiovascular_cases = st.number_input("Number of Cardiovascular Cases (your cases)", min_value=0, step=1)
        hospital_admissions = st.number_input("Number of Hospital Admissions (your cases)", min_value=0, step=1)

        submitted = st.form_submit_button("Submit")
    
        # Survey sent
        if submitted:
            input_data = {
                'AQI': [float(aqi)],
                'PM10': [float(pm10)],
                'PM2_5': [float(pm2_5)],
                'NO2': [float(no2)],
                'SO2': [float(so2)],
                'O3': [float(o3)],
                'Temperature': [float(temperature)],
                'Humidity': [float(humidity)],
                'WindSpeed': [float(wind_speed)],
                'RespiratoryCases': [int(respiratory_cases)],
                'CardiovascularCases': [int(cardiovascular_cases)],
                'HospitalAdmissions': [int(hospital_admissions)]
        }
        
            input_df = pd.DataFrame(input_data)

            st.session_state.submissions.append(input_df)

            st.success("Data submitted:")
            st.write(input_df)

            res = model.predict(input_df)

            res = int(res[0])

            if res == 0:
                res2 = "Very High😡" 
            elif res == 1:
                res2 = "High😞" 
            elif res == 2:
                res2 = "Moderate😐" 
            elif res == 3:
                res2 = "Low😊"
            else:
                res2 = "Very Low😄"  
            
            
            st.markdown("""
                <style>
                .big-font {
                font-size:40px !important; 
                }
                .small-font {
                font-size:20px !important;  
                }
                </style>""", unsafe_allow_html=True)
            st.markdown(f'<p class="small-font">The impact on your health will be of class {res}:  </p><p class="big-font">{res2} </p>', unsafe_allow_html=True)

        
surveyMod()