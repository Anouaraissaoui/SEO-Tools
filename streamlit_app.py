import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import datetime
from datetime import date
import base64
from parseCountries import parse

# Initialize pytrends request
pytrend = TrendReq()

def removeRestrictedCharactersAndWhiteSpaces(keywords):
    restricted_characters = ['-', ',', '\'', ')', '(', '[', ']', '{', '}', '.', '*', '?', '_', '@', '!', '$']
    preprocessed_list = []
    
    for keyword in keywords:
        clean_keyword = "".join([char for char in keyword if char not in restricted_characters]).strip()
        preprocessed_list.append(clean_keyword)
    
    return preprocessed_list
    
st.set_page_config(layout="wide")

st.title("The G-Trendalyser :snake::fire:")
st.markdown('**Your 5 Top & Rising Google Trends Dashboard⚡**') 

text2 = st.markdown("Get your Top & Rising trends for 5 keywords, directly from Google Trends, no coding needed :sunglasses:.")
text3 = st.markdown("To get started: Paste 1 keyword per line, pick your country (geo) & timeframe from the dropdowns & hit 'Get Trends🤘' ")

text = st.text_area("by Orit Mutznik (@oritsimu)", height=150, key=1)
text2 = st.markdown('*Value column does not represent search volume, it is more of a value assigned by Google to signal how trending a kw is')
lines = text.split("\n")  # A list of lines
linesList = list(dict.fromkeys(filter(None, lines)))  # Remove duplicates and empty lines

MAX_LINES = 5
if len(linesList) > MAX_LINES:
    st.warning(f"⚠️ Only the first {MAX_LINES} keywords will be reviewed.")
    linesList = linesList[:MAX_LINES]

# Parse countries
country_names, country_codes = parse()
country_names, country_codes = country_names[:243], country_codes[:243]

country = st.selectbox("Your Country", country_names)
st.write(f"You selected {country}")
idx = country_names.index(country)
country_code = country_codes[idx]

# Timeframe selections
period_list = ["Past 12 months", "Past hour", "Past 4 hours", "Past day", "Past 7 days", "Past 30 days", "Past 90 days", "Past 5 years", "2004 - present", "Custom time range"]
tf = ["today 12-m", "now 1-H", "now 4-H", "now 1-d", "now 7-d", "today 1-m", "today 3-m", "today 5-y", "all", "custom"]

timeframe_selectbox = st.selectbox("Choose Period", period_list)
idx = period_list.index(timeframe_selectbox)
selected_timeframe = tf[idx]

todays_date = date.today()
current_year = todays_date.year

years = list(range(2005, current_year + 1))
months = list(range(1, 13))
days = list(range(1, 32))

if selected_timeframe == "custom":
    st.write("From")
    col11, col12, col13 = st.columns(3)
    year_from = col11.selectbox("Year", years, key="0")
    month_from = col12.selectbox("Month", months, key="1")
    day_from = col13.selectbox("Day", days, key="2")
    
    st.write("To")
    col21, col22, col23 = st.columns(3)
    year_to = col21.selectbox("Year", years, key="3")
    month_to = col22.selectbox("Month", months, key="4")
    day_to = col23.selectbox("Day", days, key="5")
    
    selected_timeframe = f"{year_from}-{month_from:02d}-{day_from:02d} {year_to}-{month_to:02d}-{day_to:02d}"

# Button to start execution
start_execution = st.button("Get Trends! 🤘")

if start_execution:
    if len(linesList) == 0:
        st.warning("Please enter at least 1 keyword.")
    else:
        linesList = removeRestrictedCharactersAndWhiteSpaces(linesList)
        pytrend.build_payload(linesList, timeframe=selected_timeframe, geo=country_code)
        related_queries = pytrend.related_queries()
        
        for i, keyword in enumerate(linesList, start=1):
            st.header(f"GTrends data for keyword #{i}: {keyword}")
            c29, c30, c31 = st.columns([6, 2, 6])

            with c29:
                st.subheader("Top Trends🏆")
                st.write(related_queries[keyword].get("top"))

            with c31:
                st.subheader("Rising Trends⚡")
                st.write(related_queries[keyword].get("rising"))