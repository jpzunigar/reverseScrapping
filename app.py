import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from functions import get_info_from_top_position_sync

with st.sidebar:
    st.markdown("<h1 style='color: #14F46F; font-size: 22px;'>Scrapping revert.finance data</h1>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home","Projects","Contact"],
        icons = ["house","book","envelope"],
        menu_icon = "cast",
        default_index = 0,
        styles={

            "icon": {"color": "#14F46F", "font-size": "25px"}, 
            "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#121F23"},
            "nav-link-selected": {"background-color": "#121F23"},
        }

    )
if selected == "Home":
    st.header('Revert.Finance Scrapper App')
    st.subheader("Esta hoja resume la información obtenida de top positions de Revert.Finance")
    num_pages = st.number_input('Inserte el numero de paginas que desea scrapear', min_value=1)
    if st.button('Iniciar Scraping', use_container_width=True):
        df = get_info_from_top_position_sync(num_pages)
        st.write(df)
 

