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
    st.write("First of all, let's take a look at the aspect of the data:")
    st.dataframe(df)

    # First figure: AQI vs RespiratoryCases
    st.write("""Regarding the graphs, in the Respiratory Cases vs Air Quality Index graph, we can see that respiratory cases are 
             mostly around 10 for all air quality index intervals. However, as the air quality index increases, the number of 
             instances with around 10 respiratory cases also increases. This observation makes sense, as the degree of air pollution 
             could have a significant impact on the number of respiratory problems the population might experience. Nonetheless, 
             making definitive statements can be risky, so this relationship is not certain. The effect of other indices and 
             pollutants needs to be studied, as will be done later on.""")
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
        yaxis_title='Air Quality Index (AQI)',
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
        yaxis_title='Air Quality Index (AQI)',
        hovermode='closest',
        template='plotly_white')

    st.plotly_chart(fig)


    # Third plot: contaminants vs HealthImpactClass
    st.write("""Next, with the following bar chart, we aim to see if different pollutants might have any effect on the health impact 
             class. We can observe that with lower impact (i.e., when reaching 4), there is a lower average concentration of the 
             following pollutants: PM2_5, NO2, SO2, and O3. This is an interesting observation; however, the difference is too small 
             to be significant. On the other hand, regarding PM10, we see that it is the only pollutant that increases as the impact 
             decreases. Since they are larger particles, they do not penetrate the respiratory system as easily and they are not as 
             harmful as the smaller and more irritating ones (i.e., the PM2_5), so it could be that they do not have a significant 
             impact on the health.""")

    colors = {
        'PM10': 'blue',
        'PM2_5': 'green',
        'NO2': 'red',
        'SO2': 'purple',
        'O3': 'orange'}

    def update_plot(class_selected):
        data_filtered = df[df['HealthImpactClass'] == class_selected]
        
        if data_filtered.empty:
            print(f"No data found for HealthImpactClass '{class_selected}'")
            return
        
        pollutants = ['PM10', 'PM2_5', 'NO2', 'SO2', 'O3']
        values = data_filtered[pollutants].mean()
        
        bar_colors = [colors[pollutant] for pollutant in pollutants]
        
        trace = go.Bar(
            x=pollutants,
            y=values,
            marker=dict(color=bar_colors),)
        
        layout = go.Layout(
            title=f'Average of the Concentration of the Contaminants for HealthImpactClass {class_selected}',
            xaxis=dict(title='Contaminants'),
            yaxis=dict(title='Concentration'),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',)
        
        fig = go.Figure(data=[trace], layout=layout)
        st.plotly_chart(fig)

    class_selected = st.selectbox(
            'Health Impact Class:',
            sorted(df['HealthImpactClass'].unique()))

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
