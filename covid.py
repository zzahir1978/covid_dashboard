from curses import def_prog_mode
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd                                 # pip install pandas openpyxl
import plotly.express as px                         # pip install plotly-express
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from email.mime import image
import requests

st.set_page_config(page_title="KKM Open Data Dashboard", page_icon=":warning:", layout="wide")       # https://www.webfx.com/tools/emoji-cheat-sheet/
st.title(":bar_chart:"+" KKM Open Data Dashboard")

#@st.experimental_memo
#def read_csv(path) -> pd.DataFrame:
    #return pd.read_csv(path)

# IMPORTING ALL DATA
# Covid Dataframe
df_mas_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
df_mas_deaths = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv')
df_mas_vaksin = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv')
df_mas_pop = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/static/population.csv')
df_bloodDonor = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv')
df_hospital = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/data-resources-public/main/bedutil_state.csv')
# Creating new columns
df_mas_cases['cum_cases'] = df_mas_cases['cases_new'].cumsum()
df_mas_cases['cum_recover'] = df_mas_cases['cases_recovered'].cumsum()
df_mas_deaths['cum_deaths'] = df_mas_deaths['deaths_new'].cumsum()
df_mas_vaksin['cum_vax'] = df_mas_vaksin['daily'].cumsum()
df_mas_cases_graph = pd.merge(df_mas_cases,df_mas_vaksin,on='date')
df_mas_cases_graph['vax_perc'] = (df_mas_cases_graph["daily_full"].cumsum()/df_mas_pop.at[df_mas_pop.index[0],'pop'])*100
df_mas_deaths_graph = pd.merge(df_mas_deaths, df_mas_vaksin,on='date')
df_mas_deaths_graph['vax_perc'] = (df_mas_deaths_graph["daily_full"].cumsum()/df_mas_pop.at[df_mas_pop.index[0],'pop'])*100
#st.dataframe(df_mas_cases)
# Creating New Date + Information
df_date_end = df_mas_cases.tail(1)
new_cases = df_mas_cases.tail(1)
new_recover = df_mas_cases.tail(1)
new_deaths = df_mas_deaths.tail(1)
new_vaksin = df_mas_vaksin.tail(1)
# Creating Yearly Data Tables
df1 = pd.merge(df_mas_cases,df_mas_deaths,on='date')
df1['frate'] = (df1['deaths_new']/df1['cases_new'])*100
new_frate = df1.tail(1)
#df_covid = df_mas_cases.append(df_mas_deaths)
df_covid = pd.concat([df_mas_cases, df_mas_deaths])
df_covid = df_covid.append(df_mas_vaksin)

def getYear(s):
  return s.split("-")[0]

def getMonth(s):
  return s.split("-")[1]

df_covid['Year']= df_covid['date'].apply(lambda x: getYear(x))
df_covid['Month']= df_covid['date'].apply(lambda x: getMonth(x))
df_covid = df_covid.groupby('Year').sum().reset_index()
# ---- READ DATA 2----
dfworld1 = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
dfworld_top = dfworld1[dfworld1['continent'].notna()]
dfworld_top_cases = dfworld_top.sort_values('total_cases',ascending=False)
dfworld_top_cases = dfworld_top_cases.head(10)
dfworld_top_deaths = dfworld_top.sort_values('total_deaths',ascending=False)
dfworld_top_deaths = dfworld_top_deaths.head(10)
dfworld_top_vax = dfworld_top.sort_values('people_fully_vaccinated',ascending=False)
dfworld_top_vax = dfworld_top_vax.head(10)

df_asean = dfworld1[dfworld1['continent'].notna()]
df_asean = df_asean.loc[df_asean['location'].isin(['Malaysia','Singapore','Thailand','Indonesia','Philippines','Cambodia',
                                                  'Laos','Vietnam','Myanmar','Brunei'])]
df_asean_cases = df_asean.sort_values('total_cases',ascending=False)
df_asean_cases = df_asean_cases.head(10)
df_asean_deaths = df_asean.sort_values('total_deaths',ascending=False)
df_asean_deaths = df_asean_deaths.head(10)
df_asean_vax = df_asean.sort_values('people_fully_vaccinated',ascending=False)
df_asean_vax = df_asean_vax.head(10)
df_asean_pop = df_asean.sort_values('population',ascending=False)
df_asean_popdensity = df_asean.sort_values('population_density',ascending=False)
df_asean_gdp = df_asean.sort_values('gdp_per_capita',ascending=False)
df_asean_poverty = df_asean.sort_values('extreme_poverty',ascending=False)
df_asean_hdi = df_asean.sort_values('human_development_index',ascending=False)
df_asean_life = df_asean.sort_values('life_expectancy',ascending=False)
df_asean_hosp_bed = df_asean.sort_values('hospital_beds_per_thousand',ascending=False)
df_asean_cardiovasc = df_asean.sort_values('cardiovasc_death_rate',ascending=False)

# ---- READ DATA 3----
dfworld2 = dfworld1.groupby('continent').sum().reset_index()
dfworld2['vaccination_percentage'] = (dfworld2['people_fully_vaccinated']/dfworld2['population'])*100
dfworld2 = dfworld2.sort_values('total_cases',ascending=False)

total_cases = int(df_covid["cases_new"].sum())
new_cases = int(new_cases.at[new_cases.index[0],'cases_new'])
total_recover = int(df_covid["cases_recovered"].sum())
new_recover = int(new_recover.at[new_recover.index[0],'cases_recovered'])
total_death = int(df_covid["deaths_new"].sum())
new_deaths = int(new_deaths.at[new_deaths.index[0],'deaths_new'])
total_full = int(df_covid["daily_full"].sum())
vax_perc = int((df_covid["daily_full"].sum()/df_mas_pop.at[df_mas_pop.index[0],'pop'])*100)
fatal_rate = new_frate.at[new_frate.index[0],'frate']

# ---- READ STATES DATA ----
df_states_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv')
df_states_deaths = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_state.csv')
df_states_vaksin = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv')
df_cases = df_states_cases.groupby('state').sum()
df_deaths = df_states_deaths.groupby('state').sum()
df_vaksin = df_states_vaksin.groupby('state').sum()
df_states = pd.merge(df_cases,df_deaths,on='state')
df_states = pd.merge(df_states,df_vaksin,on='state')
df_states = df_states.reset_index()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Overview','Covid19','Blood Donation','Hospital Capacity','Population','Disclaimer'])

with tab1:
    st.subheader("[KKMNOW](https://data.moh.gov.my/) is an open data source in collaboration between the Ministry of Health Malaysia and the Department of Statistics Malaysia to institutionalise transparency and make data accessible for all.")
    st.subheader("All the information shown in this webpages are extracted from the relevant KKM open data sources.")
    st.subheader("The open data can be downloaded at [KKM Github Page](https://github.com/MoH-Malaysia/).")
    # Footer
    st.write("---")
    components.html(
        """
        <script src="https://code.iconify.design/2/2.2.1/iconify.min.js"></script>
        <div style="text-align:center">
        <p style="font-family:verdana">Powered By:</p>
        <span class="iconify" data-icon="logos:python"></span> <span class="iconify" data-icon="simple-icons:pandas"></span> <span class="iconify" data-icon="simple-icons:plotly"></span> <span class="iconify" data-icon="icon-park:github"></span> <span class="iconify" data-icon="logos:github"></span> <span class="iconify" data-icon="simple-icons:streamlit"></span>
        <p style="font-family:verdana">zahiruddin.zahidanishah<span class="iconify" data-icon="icon-park:at-sign"></span>2022</p>
        </div>
        """
    )


with tab2:    
    st.header("Malaysia Covid19 Overview")
    st.subheader(f"Updated On: {df_date_end.at[df_date_end.index[0],'date']}")
    st.markdown("##")
    first_column, second_column, third_column, fourth_column = st.columns(4)
    with first_column:
        st.subheader(":red_circle: Total Cases:")
        st.subheader(f"{total_cases:,}")
    with second_column:
        st.subheader(":large_blue_circle: Total Recover:")
        st.subheader(f"{total_recover:,}")
    with third_column:
        st.subheader(":black_circle: Total Deaths:")
        st.subheader(f"{total_death:,}")
    with fourth_column:
        st.subheader(":syringe: Full Vax.:")
        st.subheader(f"{vax_perc:,}%")

    first_column, second_column, third_column, fourth_column = st.columns(4)
    with first_column:
        st.subheader(":red_circle: New Cases:")
        st.subheader(f"{new_cases:,}")
    with second_column:
        st.subheader(":large_blue_circle: New Recover:")
        st.subheader(f"{new_recover:,}")
    with third_column:
        st.subheader(":black_circle: New Deaths:")
        st.subheader(f"{new_deaths:,}")
    with fourth_column:
        st.subheader("Fatality Rate:")
        #st.subheader(f"{fatal_rate:,.2f}%")
        st.subheader(f"{(new_cases/new_cases):,.0f} : "f"{(new_deaths/new_cases):,.3f}")

    with st.expander('Malaysia Covid19 Cases'):
        #st.subheader('Malaysia Covid19 Cases') 
        df_selection = df_covid
        # Malaysia Charts 
        # New Cases Bar Chart
        fig_cases = px.bar(df_selection,x="Year",y=["cases_new","cases_fvax"],barmode="group",title="Total Cases by Year",template="plotly_white")
        fig_cases.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_cases.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_cases.add_hline(y=df_selection['cases_new'].mean(), line_dash="dot",line_color="red",annotation_text="Average Cases", annotation_position="bottom left")

        # Deaths Cases Bar Chart
        fig_deaths = px.bar(df_selection,x="Year",y=["deaths_new",'deaths_fvax'],barmode='group',title="Total Deaths by Year",template="plotly_white")
        fig_deaths.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_deaths.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_deaths.add_hline(y=df_selection['deaths_new'].mean(), line_dash="dot",line_color="red",annotation_text="Average Deaths", annotation_position="bottom left")

        # Vaccination Bar Chart
        fig_vax = px.bar(df_selection,x="Year",y=["daily_full",'daily_booster'],barmode='group',title="Total Vaccination by Year",template="plotly_white")
        fig_vax.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_vax.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph Layout
        # First Row Graph
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig_cases, use_container_width=True)
        col2.plotly_chart(fig_deaths, use_container_width=True)
        col3.plotly_chart(fig_vax, use_container_width=True)

        # Daily Cases Chart
        fig_cases_daily = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_cases_daily.add_trace(go.Scatter(x = df_mas_cases_graph['date'], y = df_mas_cases_graph['cases_new'],name='New Cases',fill='tozeroy',
            mode='lines', line = dict(color='blue', width=1)), secondary_y=True)
        fig_cases_daily.add_trace(go.Scatter(x = df_mas_cases_graph['date'], y = df_mas_cases_graph['vax_perc'],name='Vax %',fill='tozeroy',
            mode='lines',line = dict(color='red', width=1)), secondary_y=False)
        fig_cases_daily.update_layout(height=350,title_text='Daily New Cases VS Vax %',title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_cases_daily.update_annotations(font=dict(family="Helvetica", size=10))
        fig_cases_daily.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_cases_daily.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Daily Deaths Chart
        fig_deaths_daily = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_deaths_daily.add_trace(go.Scatter(x = df_mas_deaths_graph['date'], y = df_mas_deaths_graph['deaths_new'],name='Deaths Cases',fill='tozeroy',
            mode='lines', line = dict(color='blue', width=1)), secondary_y=True)
        fig_deaths_daily.add_trace(go.Scatter(x = df_mas_deaths_graph['date'], y = df_mas_deaths_graph['vax_perc'],name='Vax %',fill='tozeroy',
            mode='lines',line = dict(color='red', width=1)), secondary_y=False)
        fig_deaths_daily.update_layout(height=350,title_text='Daily Deaths Cases VS Vax %',title_x=0.5,font=dict(family="Helvetica", size=10),
            xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_deaths_daily.update_annotations(font=dict(family="Helvetica", size=10))
        fig_deaths_daily.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_deaths_daily.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Daily Vaksin Chart
        fig_vax_daily = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_vax_daily.add_trace(go.Scatter(x = df_mas_vaksin['date'], y = df_mas_vaksin['daily'],name='Daily Vax',fill='tozeroy',mode='lines', 
            line = dict(color='blue', width=1)), secondary_y=True)
        fig_vax_daily.add_trace(go.Scatter(x = df_mas_vaksin['date'], y = df_mas_vaksin['cum_vax'],name='Cum. Vax',fill='tozeroy',mode='lines',
            line = dict(color='red', width=1)), secondary_y=False)
        fig_vax_daily.update_layout(height=350,title_text='Daily Vaccination',title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_vax_daily.update_annotations(font=dict(family="Helvetica", size=10))
        fig_vax_daily.update_xaxes(title_text='Malaysia', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_vax_daily.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Second Row Graph
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig_cases_daily, use_container_width=True)
        col2.plotly_chart(fig_deaths_daily, use_container_width=True)
        col3.plotly_chart(fig_vax_daily, use_container_width=True)

    with st.expander('Malaysia States Covid19 Cases'):
        #st.subheader('')
        # States Graphs
        # Total Cases
        df_states_cases_fig = df_states.sort_values('cases_new',ascending=False)
        fig_bar_states_cases = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_bar_states_cases.add_trace(go.Bar(x = df_states_cases_fig['state'], y = df_states_cases_fig['cases_new'],name='Total Cases'))
        fig_bar_states_cases.update_layout(title_text='Total Cases',title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_bar_states_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_bar_states_cases.update_xaxes(title_text='', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_bar_states_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Graph layout
        st.plotly_chart(fig_bar_states_cases, use_container_width=True)

        # Total Deaths
        df_states_deaths_fig = df_states.sort_values('deaths_new',ascending=False)
        fig_bar_states_deaths = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_bar_states_deaths.add_trace(go.Bar(x = df_states_deaths_fig['state'], y = df_states_deaths_fig['deaths_new'],name='Total Deaths'))
        fig_bar_states_deaths.update_layout(title_text='Total Deaths',title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_bar_states_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_bar_states_deaths.update_xaxes(title_text='', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_bar_states_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Graph layout
        st.plotly_chart(fig_bar_states_deaths, use_container_width=True)

        # Total Vaccination
        df_states_vacc_fig = df_states.sort_values('daily',ascending=False)
        fig_bar_states_vacc = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
        fig_bar_states_vacc.add_trace(go.Bar(x = df_states_vacc_fig['state'], y = df_states_vacc_fig['daily'],name='Total Vaccination'))
        fig_bar_states_vacc.update_layout(title_text='Total Vaccination',title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
        fig_bar_states_vacc.update_annotations(font=dict(family="Helvetica", size=10))
        fig_bar_states_vacc.update_xaxes(title_text='', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_bar_states_vacc.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        # Graph layout
        st.plotly_chart(fig_bar_states_vacc, use_container_width=True)

        # States Cases [PIE CHART]
        fig_states_cases = make_subplots(specs=[[{"type": "domain"}]])
        fig_states_cases.add_trace(go.Pie(values=df_states['cases_new'],labels=df_states['state'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_states_cases.update_layout(height=350, showlegend=False,title_text='States Positive Cases',title_x=0.5)
        fig_states_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_states_cases.update_layout(font=dict(family="Helvetica", size=10))

        # States Deaths [PIE CHART]
        fig_states_deaths = make_subplots(specs=[[{"type": "domain"}]])
        fig_states_deaths.add_trace(go.Pie(values=df_states['deaths_new'],labels=df_states['state'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_states_deaths.update_layout(height=350, showlegend=False,title_text='States Deaths Cases',title_x=0.5)
        fig_states_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_states_deaths.update_layout(font=dict(family="Helvetica", size=10))

        # States Vaccination [PIE CHART]
        fig_states_vax = make_subplots(specs=[[{"type": "domain"}]])
        fig_states_vax.add_trace(go.Pie(values=df_states['daily'],labels=df_states['state'],textposition='inside',textinfo='label+percent'),row=1, col=1)
        fig_states_vax.update_layout(height=350, showlegend=False,title_text='States Vaccination',title_x=0.5)
        fig_states_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_states_vax.update_layout(font=dict(family="Helvetica", size=10))

        # Graph layout
        # Second Row Graph
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_states_cases, use_container_width=True)
        col2.plotly_chart(fig_states_deaths, use_container_width=True)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_states_vax, use_container_width=True)

    with st.expander('ASEAN Covid19 Cases'):
        #st.subheader('')
        # ASEAN Bar Chart
        # ASEAN Total Cases
        fig_asean_cases = px.bar(df_asean_cases,x="location",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_asean_cases.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_asean_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_cases.update_xaxes(title_text='ASEAN Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # ASEAN Deaths Cases
        fig_asean_deaths = px.bar(df_asean_deaths,x="location",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_asean_deaths.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_asean_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_deaths.update_xaxes(title_text='ASEAN Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # ASEAN Vaccination
        fig_asean_vax = px.bar(df_asean_vax,x="location",y="people_fully_vaccinated",title="Total Vaccination",template="plotly_white")
        fig_asean_vax.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_asean_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_asean_vax.update_xaxes(title_text='ASEAN Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_asean_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Third Row Graph
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig_asean_cases, use_container_width=True)
        col2.plotly_chart(fig_asean_deaths, use_container_width=True)
        col3.plotly_chart(fig_asean_vax, use_container_width=True)

    with st.expander('World Countries Covid19 Cases'):
        #st.subheader('')
        # World Top Bar Chart
        # World Top Total Cases
        fig_world_top_cases = px.bar(dfworld_top_cases,x="location",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_world_top_cases.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_world_top_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_world_top_cases.update_xaxes(title_text='World Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_world_top_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # World Top Deaths Cases
        fig_world_top_deaths = px.bar(dfworld_top_deaths,x="location",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_world_top_deaths.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_world_top_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_world_top_deaths.update_xaxes(title_text='World Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_world_top_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # World Top Vaccination
        fig_world_top_vax = px.bar(dfworld_top_vax,x="location",y="people_fully_vaccinated",title="Total Vaccination",template="plotly_white")
        fig_world_top_vax.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_world_top_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_world_top_vax.update_xaxes(title_text='World Top 10',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_world_top_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Fourth Row Graph
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig_world_top_cases, use_container_width=True)
        col2.plotly_chart(fig_world_top_deaths, use_container_width=True)
        col3.plotly_chart(fig_world_top_vax, use_container_width=True)

        st.subheader('World Continent Covid19 Cases')
        # Continent Bar Chart
        # Continent Positive Cases Bar Chart
        df_selection_continent = dfworld2
        fig_con_cases = px.bar(df_selection_continent,x="continent",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_con_cases.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_con_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_con_cases.update_xaxes(title_text='World Continent',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_con_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Continent Deaths Cases Bar Chart
        fig_con_deaths = px.bar(df_selection_continent,x="continent",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_con_deaths.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_con_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_con_deaths.update_xaxes(title_text='World Continent',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_con_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Continent Vaccination Bar Chart
        fig_con_vax = px.bar(df_selection_continent,x="continent",y="people_fully_vaccinated",title="Total Vaccinations",template="plotly_white")
        fig_con_vax.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_con_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_con_vax.update_xaxes(title_text='World Continent',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_con_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Fifth Row Graph
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig_con_cases, use_container_width=True)
        col2.plotly_chart(fig_con_deaths, use_container_width=True)
        col3.plotly_chart(fig_con_vax, use_container_width=True)

    with st.expander('Covid19 Cases By Selected Country/Continent:'):
        #st.subheader('')
        # Selection Options
        Location = st.multiselect("Select the Country:",options=dfworld1["location"].unique(),default=None)
        df_selection_country = dfworld1.query("location == @Location")

        # Country Selection Bar Chart
        # Country Positive Cases Bar Chart
        fig_country_cases = px.bar(df_selection_country,x="location",y="total_cases",title="Total Positive Cases",template="plotly_white")
        fig_country_cases.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_country_cases.update_annotations(font=dict(family="Helvetica", size=10))
        fig_country_cases.update_xaxes(title_text='Country',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_country_cases.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Country Deaths Cases Bar Chart
        fig_country_deaths = px.bar(df_selection_country,x="location",y="total_deaths",title="Total Deaths Cases",template="plotly_white")
        fig_country_deaths.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,xaxis_title=None)
        fig_country_deaths.update_annotations(font=dict(family="Helvetica", size=10))
        fig_country_deaths.update_xaxes(title_text='Country',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_country_deaths.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Country Vaccination Bar Chart
        fig_country_vax = px.bar(df_selection_country,x="location",y="people_fully_vaccinated",title="Total Vaccinations",template="plotly_white")
        fig_country_vax.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
            plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
        fig_country_vax.update_annotations(font=dict(family="Helvetica", size=10))
        fig_country_vax.update_xaxes(title_text='Country',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
        fig_country_vax.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

        # Graph layout
        # Sixth Row Graph
        col1, col2, col3 = st.columns(3)
        col1.plotly_chart(fig_country_cases, use_container_width=True)
        col2.plotly_chart(fig_country_deaths, use_container_width=True)
        col3.plotly_chart(fig_country_vax, use_container_width=True)

with tab3:
    st.subheader('Blood Donation')
    df_bloodDonor['Year']= df_bloodDonor['date'].apply(lambda x: getYear(x))
    df_bloodDonor['Month']= df_bloodDonor['date'].apply(lambda x: getMonth(x))
    df_bloodDonor = df_bloodDonor.groupby('Year').sum().reset_index()
    
    # Blood Donation Annual Bar Chart
    fig_blood_annual = px.bar(df_bloodDonor,x="Year",y="daily",title="Annual Blood Donation (Person)",template="plotly_white")
    fig_blood_annual.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_blood_annual.update_annotations(font=dict(family="Helvetica", size=10))
    fig_blood_annual.update_xaxes(title_text='Year',showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_blood_annual.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    # Graph layout
    #st.plotly_chart(fig_blood_annual, use_container_width=True)

    # Blood Donation By Types Bar Chart
    fig_blood_types_annual = px.bar(df_bloodDonor,x="Year",y=["blood_a","blood_b","blood_o","blood_ab"],barmode="group",title="Annual Blood Donation By Types (Person)",
        template="plotly_white")
    fig_blood_types_annual.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_blood_types_annual.update_annotations(font=dict(family="Helvetica", size=10))
    fig_blood_types_annual.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_blood_types_annual.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    # Graph layout
    #st.plotly_chart(fig_blood_types_annual, use_container_width=True)

    # Blood Donation Location Chart
    fig_blood_location_annual = px.bar(df_bloodDonor,x="Year",y=["location_centre","location_mobile"],barmode="group",title="Blood Donation Location",
        template="plotly_white")
    fig_blood_location_annual.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_blood_location_annual.update_annotations(font=dict(family="Helvetica", size=10))
    fig_blood_location_annual.update_xaxes(title_text='Year', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_blood_location_annual.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    # Graph layout
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_blood_types_annual, use_container_width=True)
    col2.plotly_chart(fig_blood_annual, use_container_width=True)
    #st.write(df_bloodDonor)

with tab4:
    st.subheader('Hospital Capacity')
    df_hospital = df_hospital.drop(0)
    df_mas_pop = df_mas_pop.drop([0,1])
    df_hospital = pd.merge(df_hospital,df_mas_pop, on='state')
    df_hospital['total_beds'] = df_hospital['beds_icu'] + df_hospital['beds_nonicu']
    df_hospital['percentage'] = (df_hospital['total_beds']/df_hospital['pop'])*100
    # Hospital Nos. Of Beds Chart ICU
    df_hospital = df_hospital.sort_values('beds_icu', ascending=False)
    fig_hospital_beds_icu = px.bar(df_hospital,x="state",y=["beds_icu"],barmode="group",title="Nos. Of Beds",
        template="plotly_white")
    fig_hospital_beds_icu.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_hospital_beds_icu.update_annotations(font=dict(family="Helvetica", size=10))
    fig_hospital_beds_icu.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_hospital_beds_icu.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_hospital_beds_icu.add_hline(y=df_hospital['beds_icu'].mean(), line_dash="dot",line_color="red",annotation_text="Average Nos.", annotation_position="bottom right")
    # Hospital Nos. Of Beds Chart Non ICU
    df_hospital = df_hospital.sort_values('beds_nonicu', ascending=False)
    fig_hospital_beds_nonIcu = px.bar(df_hospital,x="state",y=["beds_nonicu"],barmode="group",title="Nos. Of Beds",
        template="plotly_white")
    fig_hospital_beds_nonIcu.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_hospital_beds_nonIcu.update_annotations(font=dict(family="Helvetica", size=10))
    fig_hospital_beds_nonIcu.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_hospital_beds_nonIcu.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_hospital_beds_nonIcu.add_hline(y=df_hospital['beds_nonicu'].mean(), line_dash="dot",line_color="red",annotation_text="Average Nos.", annotation_position="bottom right")
    # Hospital Nos. Of Beds Percentage
    df_hospital = df_hospital.sort_values('percentage', ascending=False)
    fig_hospital_percentage = px.bar(df_hospital,x="state",y=["percentage"],barmode="group",title="(%)",
        template="plotly_white")
    fig_hospital_percentage.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_hospital_percentage.update_annotations(font=dict(family="Helvetica", size=10))
    fig_hospital_percentage.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_hospital_percentage.update_yaxes(title_text='%', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_hospital_percentage.add_hline(y=df_hospital['percentage'].mean(), line_dash="dot",line_color="red",annotation_text="Average Nos.", annotation_position="bottom right")
    
    # Graph layout
    col1, col2 = st.columns(2)
    col1.subheader('ICU')
    col1.plotly_chart(fig_hospital_beds_icu, use_container_width=True)
    col2.subheader('Non ICU')
    col2.plotly_chart(fig_hospital_beds_nonIcu, use_container_width=True)
    st.subheader('Percentage Of Beds By Population')
    st.plotly_chart(fig_hospital_percentage, use_container_width=True)
    #st.write(df_hospital)

with tab5:
    st.subheader('Population')
    df_mas_pop['18-59'] = df_mas_pop['pop_18']+df_mas_pop['pop_60']
    df_mas_pop['0-4'] = df_mas_pop['pop'] - (df_mas_pop['pop_18']+df_mas_pop['pop_12']+df_mas_pop['pop_5'])
    df_mas_pop.rename(columns={'pop_12':'12-17','pop_60':'>60','pop_5':'5-11'},inplace=True)
    #st.write(df_mas_pop)

    # Deaths Cases Bar Chart
    #fig_pop = px.bar(df_mas_pop,x="state",y=['>60','18-59','12-17','5-11','0-4'],barmode='group',title="Total Deaths by Year",template="plotly_white")
    df_mas_pop = df_mas_pop.sort_values('pop',ascending=False)
    fig_pop = px.bar(df_mas_pop,x="state",y='pop',barmode='group',title="Total Population",template="plotly_white")
    fig_pop.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_pop.update_annotations(font=dict(family="Helvetica", size=10))
    fig_pop.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_pop.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    st.plotly_chart(fig_pop, use_container_width=True)

    fig_pop_60 = px.bar(df_mas_pop,x="state",y='>60',barmode='group',title="Population",template="plotly_white")
    fig_pop_60.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_pop_60.update_annotations(font=dict(family="Helvetica", size=10))
    fig_pop_60.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_pop_60.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

    fig_pop_18 = px.bar(df_mas_pop,x="state",y='18-59',barmode='group',title="Population",template="plotly_white")
    fig_pop_18.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_pop_18.update_annotations(font=dict(family="Helvetica", size=10))
    fig_pop_18.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_pop_18.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

    fig_pop_12 = px.bar(df_mas_pop,x="state",y='12-17',barmode='group',title="Population",template="plotly_white")
    fig_pop_12.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_pop_12.update_annotations(font=dict(family="Helvetica", size=10))
    fig_pop_12.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_pop_12.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

    col1, col2, col3 = st.columns(3)
    col1.subheader('Above 60')
    col1.plotly_chart(fig_pop_60, use_container_width=True)
    col2.subheader('18 to 59')
    col2.plotly_chart(fig_pop_18, use_container_width=True)
    col3.subheader('12 to 17')
    col3.plotly_chart(fig_pop_12, use_container_width=True)

    fig_pop_5 = px.bar(df_mas_pop,x="state",y='5-11',barmode='group',title="Population",template="plotly_white")
    fig_pop_5.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_pop_5.update_annotations(font=dict(family="Helvetica", size=10))
    fig_pop_5.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_pop_5.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

    fig_pop_4 = px.bar(df_mas_pop,x="state",y='0-4',barmode='group',title="Population",template="plotly_white")
    fig_pop_4.update_layout(height=350,title_x=0.5,font=dict(family="Helvetica", size=10),xaxis=dict(tickmode="array"),
        plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),showlegend=False,yaxis_title=None,xaxis_title=None)
    fig_pop_4.update_annotations(font=dict(family="Helvetica", size=10))
    fig_pop_4.update_xaxes(title_text='States', showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')
    fig_pop_4.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=2, linecolor='black')

    col1, col2, col3 = st.columns(3)
    col1.subheader('5 to 11')
    col1.plotly_chart(fig_pop_5, use_container_width=True)
    col2.subheader('Below 4')
    col2.plotly_chart(fig_pop_4, use_container_width=True)


with tab6:
    st.subheader('Disclaimer')
    st.write(
        '''
        Covid19 Dashboard shows the current cases and trends focusing on Malaysia and also selected countries around the world. 
        Data for these dashboards are retrieved from [KKM Github pages](https://github.com/MoH-Malaysia/covid19-public) and 
        from [Johns Hopkins University CSSE Github pages](https://github.com/CSSEGISandData/COVID-19). 
        More details on the Covid19 reports can be view at [Covid19 Full Report](https://zzahir1978.github.io/projects/Covid19MalaysiaNow.html).
    ''')
    st.write(
        '''
        All data visualisation shown on this website is based on the author's experience and knowledge in presenting data in at its best forms.
        '''
    )

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
