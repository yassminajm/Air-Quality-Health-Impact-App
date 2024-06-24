import markdown
import streamlit as st


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout = "wide"
)

col1, col2 = st.columns(2)

with col1:
    st.title("Air Quality and Health Impact")
    st.text("")
    st.write("Welcome to this web application, which performs an exploratory analysis of the air quality and health impact data and classifies the impact of this on health.")
    st.write("You can explore the data, visualize different graphs, and understand how air quality can affect your health. Moreover, you are able to predict how high will be the impact on your health according to the air quality data of the place where you live.")
with col2:
    st.image("data/imagen ciudad.jpg", width=500)
st.write("_____")

c1, c2 = st.columns(2)

with c1:
    st.title("About the data")
    st.write("This dataset contains comprehensive information on the air quality and its impact on public health for 5,811 records. It includes variables such as air quality index (AQI), concentrations of various pollutants, weather conditions, and health impact metrics. The target variable is the health impact class, which categorizes the health impact based on the air quality and other related factors.")
    st.write("The data source is a Kaggle repository which can be accessed through this link: https://www.kaggle.com/datasets/rabieelkharoua/air-quality-and-health-impact-dataset.")
    st.markdown("""
                ### Record Information
                #### Record ID
                **RecordID:** A unique identifier assigned to each record (1 to 2392).

                #### Air Quality Metrics
                **AQI:** Air Quality Index, a measure of how polluted the air currently is or how polluted it is forecast to become.  
                **PM10:** Concentration of particulate matter less than 10 micrometers in diameter (μg/m³).  
                **PM2_5:** Concentration of particulate matter less than 2.5 micrometers in diameter (μg/m³).  
                **NO2:** Concentration of nitrogen dioxide (ppb).  
                **SO2:** Concentration of sulfur dioxide (ppb).  
                **O3:** Concentration of ozone (ppb).

                ### Weather Conditions
                **Temperature:** Temperature in degrees Celsius (°C).  
                **Humidity:** Humidity percentage (%).  
                **WindSpeed:** Wind speed in meters per second (m/s).

                ### Health Impact Metrics
                **RespiratoryCases:** Number of respiratory cases reported.  
                **CardiovascularCases:** Number of cardiovascular cases reported.  
                **HospitalAdmissions:** Number of hospital admissions reported.

                ### Target Variable: Health Impact Class
                **HealthImpactScore:** A score indicating the overall health impact based on air quality and other related factors, ranging from 0 to 100.  
                **HealthImpactClass:** Classification of the health impact based on the health impact score:
                - 0: 'Very High' (HealthImpactScore >= 80)
                - 1: 'High' (60 <= HealthImpactScore < 80)
                - 2: 'Moderate' (40 <= HealthImpactScore < 60)
                - 3: 'Low' (20 <= HealthImpactScore < 40)
                - 4: 'Very Low' (HealthImpactScore < 20)
                """)


with c2:
    st.title("About us")
    st.markdown("""
                This web application  was developed by a team of two students of the Polytchnic University of Valencia (UPV) as a project of the Evaluation, Deployment and Monitoring of Models subject of the Data Science Degree (GCD). 
                The team consists of Qilu Diana Wu and Yassmina Jebbour Maamri.
                """)