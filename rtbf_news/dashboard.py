import streamlit as st


class RTBF_Dashboard:
    def create_dashboard(self):
        st.set_page_config(page_title="Scoring Bancaire", layout="wide")
        st.header("Application de détection de faillite bancaire")
