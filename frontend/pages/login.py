import streamlit as st
import os
import sys

# Ensure frontend is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from login.logic import show_login_page

def main():
    st.set_page_config(
        page_title="트레이너 인증",
        page_icon="https://pokemonkorea.co.kr/img/_con.ico",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    show_login_page()

if __name__ == "__main__":
    main()
