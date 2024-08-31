import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page


st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stColumn {
            flex-direction: column;
        }
    }
    @media (min-width: 769px) {
        .stApp {
            max-width: 100%;
            padding: 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Create two columns for desktop view
col1, col2 = st.columns(2)

with col1:
    show_predict_page()

with col2:
    show_explore_page()