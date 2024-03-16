import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from bs4 import BeautifulSoup as bs
import requests as rq
from requests_html import HTMLSession, AsyncHTMLSession
import asyncio

from selenium import webdriver
import time


def get_info_from_top_position(pages):
    with st.echo():
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.os_manager import ChromeType

        list_df_all = []

        @st.cache_resource
        def get_driver():
            return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        ) 

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")

        driver = get_driver()
        for i in range(pages):
            driver.get(f"https://revert.finance/#/top-positions?page={i+1}")
            time.sleep(4.5)  # Let the page render

            soup = bs(driver.page_source, 'html.parser')
            lines = soup.find('div', class_=['border', 'hover:bg-gray-90', 'ease-linear'])
            link_elements = lines.findAll('a', class_='text-green-30')
            text_elements = lines.findAll('div', class_='text-ellipsis')
            age = lines.findAll('div', class_='text-sm h-[80px] flex items-center md:h-[60px] md:border-b-transparent justify-end w-28 text-gray-20')
            link_elements = [element.text for element in link_elements]
            text_elements = [element.text for element in text_elements]
            age_elements = [element.text.split(' ')[0] for element in age]
            # Reshape the flat list into a list of lists
            nested_link = [link_elements[i:i + 3] for i in range(0, len(link_elements), 3)]
            nested_text = [text_elements[i:i + 4] for i in range(0, len(text_elements), 4)]
            df = pd.DataFrame(nested_link, columns=['pool_fees', 'NFT_id', 'owner'])
            df2 = pd.DataFrame(nested_text, columns=['PnL', 'APR', 'fee_APR', 'value'])
            df3 = pd.DataFrame(age_elements, columns=['age'])
            df_final_page = pd.concat([df, df2, df3], axis=1)
            # Convert numeric columns to numeric types
            numeric_columns = ['NFT_id', 'PnL', 'APR', 'fee_APR', 'value','age']

            for col in numeric_columns:
                # Remove commas and dollar signs, then convert to numeric
                df_final_page[col] = pd.to_numeric(df_final_page[col].replace('[\$,%]', '', regex=True), errors='coerce')
            list_df_all.append(df_final_page)

            driver.quit()
            return pd.concat(list_df_all).reset_index()