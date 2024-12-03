
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Geospatial Dashboard" ,
    page_icon="🌐" ,
    layout="wide"
)
df = pd.read_csv('world_population.csv')
with st.sidebar:
    st.title('🌐 Geospatial Dashboard ')
    # A.CONTINENT
    continent_lst = list(df['Continent'].unique())
    select_continent = st.multiselect('Select Continent', continent_lst)
    if select_continent:
        df = df[df['Continent'].isin(select_continent)]
    else:
        df = df.copy()
    
    # B.COUNTRY
    country_lst = list(df['Country/Territory'].unique())
    select_country = st.multiselect('Select a Country', country_lst)
    if select_country:
        df = df[df['Country/Territory'].isin(select_country)]
    else:
        df = df.copy()
st.subheader('Chloropeth Map : Population')
fig1 = px.choropleth(df.dropna(),
                     locations = 'Country/Territory',
                     locationmode = 'country names',
                     color = 'World Population Percentage',
                     hover_name = 'Country/Territory',
                     hover_data = ['World Population Percentage', 'Area (km²)'],
                     color_continuous_scale='Inferno'
                     )
fig1.update_geos(
    showcoastlines=True,
    coastlinecolor='white',
    showland=True,
    landcolor='gray',
    showocean=True,
    oceancolor='Black',
    showlakes = True,
    lakecolor='Black',
    bgcolor='Black',
)
st.plotly_chart(fig1, use_container_width=True)
block1, block2 = st.columns(2)
#css for metric card
st.markdown(
    """
    <style>
    .card{
      border-radius: 5px;
      padding: 5px;
      margin:100ox 0px 0px -50px;
      color: white;
      font-size:30px;
      text-align: center;
    }
    .value{
      font-size:48x;
      font-weight: bold;
    }
    .change-positive {
        color: green;
        font-size: 20px;
        font-weight: bold;
    }
    .change-negative {
        color: red;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

with block1:
  st.subheader('Growth Rate :📈')
  if not select_country:
    country_data = df.iloc[0]
  else:
    country_data = df[df['Country/Territory'] == select_country[0]].iloc[0]
  
  #function to compute growth percentage
  def calculate_growth(previous, current):
    return ((current - previous) / previous) * 100
  
  #calculate growth
  country_growth = calculate_growth(country_data['2000 Population'], country_data['2022 Population'])

  #define card creation function
  def create_metric_card(country_name, current_population, growth):
    if growth > 0:
      growth_class = 'change-positive'
      growth_symbol = '↑'
    else:
      growth_class = 'change-negative'
      growth_symbol = '↓'
  
    return f"""
    <div class="card">
    <div class="value">{country_name}</div>
    <div class="value">{current_population:.1f} M</div>
    <div class="value {growth_class}">{growth_symbol}{abs(growth):.2f}%</div?]>
    """
  st.markdown(create_metric_card(country_data['Country/Territory'], country_data['2022 Population'], country_growth), 
            unsafe_allow_html=True)
with block2:
  st.subheader('Donut Chart : Population by Continent')
  df_continent_pop = df.groupby('Continent')['2022 Population'].sum().reset_index()
  fig2 = px.pie(df_continent_pop,
                names = 'Continent',
                values = '2022 Population',
                hole = 0.4,
                title = 'Population distribution by continent (2022)')
  st.plotly_chart(fig2, use_container_width = True)
     
st.subheader('Heatmap : Population Growth Over Years')
population_cols = ['1970 Population', '1980 Population', '1990 Population', '2000 Population', '2010 Population']
df_heatmap = df[population_cols]

fig3 = go.Figure(data = go.Heatmap(
                                    z = df_heatmap.T,
                                    x = df['Country/Territory'],
                                    y = population_cols,
                                    colorscale = 'Plasma'
))
st.plotly_chart(fig3, use_container_width = True)
     
