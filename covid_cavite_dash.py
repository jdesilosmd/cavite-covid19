import streamlit as st

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import datetime as dt
from datetime import date
today = dt.date.today()


googleSheetId = '16g_PUxKYMC0XjeEKF6FPUBq2-pFgmTkHoj5lbVrGLhE'
worksheetName = 'DOH_Data_Drop'

URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
    googleSheetId,
    worksheetName
)



covid_cavite = pd.read_csv(URL, encoding='utf-8')
covid_cavite = covid_cavite[covid_cavite['RegionRes'] == 'Cavite']
covid_cavite = covid_cavite.rename(columns={'Latitude': 'lat',
                                            'Longitude': 'lon'})
covid_cavite['RemovalType'] = covid_cavite['RemovalType'].fillna('Active')




# Cavite cases per town/ city

covid_cavite_hometown = covid_cavite['ProvCityRes'].value_counts().to_frame()
covid_cavite_hometown = covid_cavite_hometown.reset_index()
covid_cavite_hometown = covid_cavite_hometown.rename(columns={'index': 'ProvCityRes',
                                                              'ProvCityRes': 'COVID-19 Cases'})

covid_cavite_hometown = pd.merge(covid_cavite_hometown,
                                 covid_cavite.loc[:, ['ProvCityRes', 'lat', 'lon']],
                                 on='ProvCityRes', how='inner')
covid_cavite_hometown = covid_cavite_hometown.drop_duplicates('ProvCityRes')




# Cavite cases by current location
covid_cavite_location = covid_cavite['Location'].value_counts().to_frame()
covid_cavite_location = covid_cavite_location.reset_index()
covid_cavite_location = covid_cavite_location.rename(columns={'index': 'Location',
                                                              'Location': 'COVID-19 Cases'})
covid_cavite_location = pd.merge(covid_cavite_location,
                                 covid_cavite.loc[:, ['Location', 'lat', 'lon']],
                                 on='Location', how='inner')

# SIDEBAR:
st.sidebar.markdown("# Confirmed COVID-19 cases in Cavite:")
st.sidebar.table(covid_cavite_hometown)



# MAP of CASES:
token = "pk.eyJ1IjoiamRlc2lsb3NtZCIsImEiOiJjazhqYXZxOWMwMDhzM2ZxNm83ZnJmOWprIn0.fRYHNglFPDpv7xC2o56Lew"
map_cavite = px.scatter_mapbox(covid_cavite_hometown, lat='lat', lon='lon', zoom=9.4, width=800, height=600,
                               size='COVID-19 Cases',
                               title="Location Map of all COVID-19 Cases in Cavite")
#map_cavite.update_layout(mapbox_style="carto-darkmatter", title_font_size=24)
map_cavite.update_layout(mapbox_style="dark", mapbox_accesstoken=token, title_font_size=24)
map_cavite.update_traces(marker=dict(color='red'))

st.plotly_chart(map_cavite, use_column_width=True)


# Graph
cavite_hist = px.histogram(covid_cavite, x='Age', nbins=20, color='Sex', height=400, width=800)
cavite_hist.update_layout( xaxis_title="Patients with COVID-19", yaxis_title="Age",
                               title= "Histogram: COVID-19 Cases in Cavite as to Age and Sex",
                               title_font_size=20)
st.plotly_chart(cavite_hist, use_container_width=True)


st.markdown('## COVID-19 Cavite Data')
st.markdown('#### Source: [DOH Data Drop](https://www.google.com/url?q=http://bit.ly/dohcovid19data&sa=D&ust=1587041816428000&usg=AFQjCNED0zWXo_krHyneN4hQQaEJaPXUxg)')

st.dataframe(covid_cavite)