import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

st.set_option('deprecation.showPyplotGlobalUse', False)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Dashboard", "Trend Line", "Comorbidities and COVID-19", "Lockdown Prediction", ])


@st.cache_data
def fetch_data():
    df = pd.read_json('https://api.covidtracking.com/v1/us/daily.json')
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df


df = fetch_data()

options = {"Cumulative Positive Results": 'positive',
           "Daily Positive Tests": 'positiveIncrease',
           "Cumulative Deaths": 'death',
           "Daily Deaths": 'deathIncrease',
           "Current Hospitalizations": 'hospitalizedCurrently',
           "Daily Hospitalizations": 'hospitalizedIncrease',
           "Cumulative Hospitalizations": 'hospitalizedCumulative',
           "Current ICU Patients": 'inIcuCurrently',
           "Cumulative ICU Patients": 'inIcuCumulative',
           "Current Ventilator Patients": 'onVentilatorCurrently',
           "Cumulative Ventilator Patients": 'onVentilatorCumulative',
           "Recovered Patients": 'recovered',
           "Daily Tests Performed": 'totalTestResultsIncrease',
           "Cumulative Tests Performed": 'totalTestResults'}

with tab1:
    # Build page
    st.title('COVID-19 Dashboard: US Data')

    st.sidebar.title('Umass Dartmouth Hackathon')
    start_date = st.sidebar.date_input(
        "Start Date", value=datetime(2020, 3, 1))
    end_date = st.sidebar.date_input("End Date", value=df.index.max())

    charts = st.sidebar.multiselect("Select individual charts to display:",
                                    options=list(options.keys()),
                                    default=list(options.keys())[:1])

    for chart in charts:
        df[options[chart]].loc[start_date: end_date +
                               timedelta(days=1)].plot(label=chart, figsize=(8, 6))
        plt.xlabel('Date')
        plt.legend(loc="upper left")
    st.pyplot()

with tab2:
    st.title('Question')
    st.markdown("How did the number of COVID-19 cases and deaths trend over time in the top 25 counties, and what patterns emerge from a year-on-year comparison from 2020 to 2023?")
    st.image('trendline.png', caption='Trendline')
    st.markdown("Results - The line graph exhibits cyclical patterns in both cases and deaths among the top 25 counties over the course of three years, highlighting the impact of successive waves of the COVID-19 pandemic. The simultaneous rise and fall in the number of cases and deaths across these counties suggest a regional similarity in the pandemic's behavior and potentially the effects of shared public health responses or seasonal factors.")


with tab3:
    st.title('Question')
    st.markdown("Does a higher prevalence of smoking among adults correlate with an increased number of COVID-19 cases at the county level, and how might other factors like obesity rates influence this relationship?")
    st.image('smokers.png')
    st.markdown('Results -  The scatter plot suggests that there is a diverse range of smoking rates among the adult population across different counties, which does not show a clear or consistent correlation with the number of COVID-19 cases reported in those counties. Further statistical analysis may be required to determine if there is a significant relationship between these variables as this data is only for top 15 counties')

    st.write("---")

    st.title('Question')
    st.markdown(" Is there a significant correlation between the percentage of the population with diabetes and the total number of COVID-19 cases in U.S. counties, and how might additional factors contribute to this relationship?")
    st.image('diabetes.png')
    st.markdown('Results - The plot shows a distribution of counties across a range of diabetes prevalence, plotted against the total number of COVID-19 cases reported in those counties. There does not seem to be a clear linear relationship, suggesting that diabetes prevalence alone may not be a straightforward predictor of COVID-19 case numbers. The data requires further statistical analysis to understand the nature of the relationship?"')

with tab4:
    st.subheader(
        'Prediciting regional lockdown based on death per population and cases per population with random forest')
    st.image('severity1.jpg')
