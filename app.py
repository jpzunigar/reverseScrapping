import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from functions import get_info_from_top_position
from functions import count_values, create_count_plot



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
    option_red = st.selectbox(
    'Filtre por red',
    ('All networks', 'Ethereum', 'Polygon','Arbitrum','Optimism','BNB','EVMOS','Base'))
if selected == "Top Positions":
    st.header('Revert.Finance Scrapper App')
    st.subheader("Esta hoja resume la información obtenida de top positions de Revert.Finance")
    num_pages = st.number_input('Inserte el numero de paginas que desea scrapear', min_value=1)
    if st.button('Iniciar Scraping', use_container_width=True):
        with st.spinner('Recolectando información...'):
            df = get_info_from_top_position(num_pages, red = option_red)
            with st.expander('Ver datos'):
                st.write(df)
            col1, col2 = st.columns(2)
            df_count = count_values(df)
            with col1:
                create_count_plot(df_count)
            with col2:
                st.dataframe(df_count)
            


 

