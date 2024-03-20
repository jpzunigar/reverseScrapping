import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from functions import get_info_from_top_position
from functions import count_values, create_count_plot

#st.set_page_config(layout="wide")
if 'RetrievedData' not in st.session_state:
    st.session_state.RetrievedData = None


with st.sidebar:
    st.markdown("<h1 style='color: #14F46F; font-size: 22px;'>Scrapping revert.finance data</h1>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Top Positions"],
        icons = ["house"],
        menu_icon = "cast",
        default_index = 0,
        styles={

            "icon": {"color": "#14F46F", "font-size": "25px"}, 
            "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#121F23"},
            "nav-link-selected": {"background-color": "#121F23"},
        }

    )
if selected == "Top Positions":
    st.header('Revert.Finance Scrapper App')
    st.markdown("Esta hoja resume la información obtenida de top positions de Revert.Finance.Muestra el top 10 operaciones más realizadas")
    form = st.form(key='my_form')
    num_pages = form.number_input('Inserte el numero de paginas que desea scrapear', min_value=1)
    option_red = form.selectbox(
    'Filtre por red',
    ('All networks', 'Ethereum', 'Polygon','Arbitrum','Optimism','BNB','EVMOS','Base'))
    if form.form_submit_button('Iniciar Scraping', use_container_width=True):
        with st.spinner('Recolectando información...'):
            st.session_state.RetrievedData = get_info_from_top_position(num_pages, red = option_red)

        if st.session_state.RetrievedData is not None:
            with st.expander('Ver datos'):
                st.write(st.session_state.RetrievedData)
            col1, col2 = st.columns(2)
            df_count = count_values(st.session_state.RetrievedData)
            with col1:
                create_count_plot(df_count)
            with col2:
                st.dataframe(df_count,use_container_width=True)
            


 

