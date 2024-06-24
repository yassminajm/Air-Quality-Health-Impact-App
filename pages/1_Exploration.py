import streamlit as st
import markdown
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
import plotly.graph_objects as go


st.set_page_config(page_title="Exploration",
                   page_icon="📊")


def dashboard():
    df = pd.read_csv("data/air_quality_health_impact_data.csv")
    df['HealthImpactClass'] = df['HealthImpactClass'].astype(int)
    st.title('Exploratory Data Analysis')
    st.write(" ")
    st.write("Here we have a review of the data aspect.")
    st.dataframe(df)

    # First figure: AQI vs RespiratoryCases
    aqi_bins = [0, 50, 100, 150, 200, 300, 500]
    aqi_labels = ['0-50', '51-100', '101-150', '151-200', '201-300', '301-500']
    df['AQI_interval'] = pd.cut(df['AQI'], bins=aqi_bins, labels=aqi_labels, include_lowest=True)

    count_data = df.groupby(['AQI_interval', 'RespiratoryCases']).size().reset_index(name='count')

    fig = px.scatter(count_data, x='RespiratoryCases', y='AQI_interval', size='count',
                    color='count', hover_name='count',
                    color_continuous_scale='viridis',
                    title='Interactive Scatter Plot of AQI vs RespiratoryCases',
                    labels={'count': 'Number of Instances', 'RespiratoryCases': 'Respiratory Cases', 'AQI_interval': 'Air Quality Index (AQI)'})

    fig.update_layout(
        xaxis_title='Respiratory Cases',
        yaxis_title='Air Quality Indeex (AQI)',
        hovermode='closest',
        template='plotly_white')

    st.plotly_chart(fig)


    # Second figure: AQI vs CardiovascularCases
    count_data_C = df.groupby(['AQI_interval', 'CardiovascularCases']).size().reset_index(name='count_C')

    fig = px.scatter(count_data_C, x='CardiovascularCases', y='AQI_interval', size='count_C',
                    color='count_C', hover_name='count_C',
                    color_continuous_scale='viridis',
                    title='Interactive Scatter Plot of AQI vs CardiovascularCases',
                    labels={'count_C': 'Number of Instances', 'CardiovascularCases': 'Cardiovascular Cases', 'AQI_interval': 'Air Quality Index (AQI)'})

    fig.update_layout(
        xaxis_title='Cardiovascular Cases',
        yaxis_title='Air Quality Indeex (AQI)',
        hovermode='closest',
        template='plotly_white')

    st.plotly_chart(fig)


    # Third plot: contaminants vs HealthImpactClass
    def update_plot(class_selected):
        plt.figure(figsize=(10, 6))
        
        data_filtered = df[df['HealthImpactClass'] == class_selected]
        
        pollutants = ['PM10', 'PM2_5', 'NO2', 'SO2', 'O3']
        values = data_filtered[pollutants].values[0]
        
        plt.bar(pollutants, values, color=['blue', 'green', 'red', 'purple', 'orange'])
        
        plt.xlabel('Contaminants')
        plt.ylabel('Concentration')
        plt.title(f'Concentration of the Contaminants for HealthImpactClass {class_selected}')
        plt.ylim(0, max(df[pollutants].max()) * 1.2)  
        
        st.pyplot(plt.gcf())

    class_selected = st.selectbox(
        'Health Impact Class:',
        df['HealthImpactClass'].unique())

    update_plot(class_selected)


    # Fourth plot: HealthImpactClass by HospitalAdmissions and AQI
    aqi = df['AQI'].dropna()
    admissions = df['HospitalAdmissions'].dropna()
    classes = df['HealthImpactClass'].dropna()

    data_H = pd.DataFrame({
        'AQI': aqi,
        'HospitalAdmissions': admissions,
        'HealthImpactClass': classes})

    data_H.dropna(inplace=True)

    colors = {
        0: 'blue',
        1: 'green',
        2: 'yellow',
        3: 'orange',
        4: 'red'}

    fig = go.Figure()

    for class_value, color in colors.items():
        class_data = data_H[data_H['HealthImpactClass'] == class_value]
        fig.add_trace(go.Scatter(
            x=class_data['HospitalAdmissions'],
            y=class_data['AQI'],
            mode='markers',
            name=f'Health Impact Class {class_value}',
            marker=dict(color=color)))

    fig.update_layout(
        title='Interactive Distribution of HealthImpactClass by HospitalAdmissions and AQI',
        xaxis_title='HospitalAdmissions',
        yaxis_title='Air Quality Index (AQI)',
        template='plotly_white')

    st.plotly_chart(fig) 

dashboard()
