import streamlit as st
import os
import sys

# Ensure frontend is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui import inject_common_ui
from utils.demo_mode import backend_configured, oauth_configured, show_unavailable

def main():
    st.set_page_config(
        page_title="트레이너 인증",
        page_icon="https://pokemonkorea.co.kr/img/_con.ico",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    if not (backend_configured() and oauth_configured()):
        inject_common_ui(spacer=True)
        show_unavailable(
            "GitHub 로그인",
            "GitHub OAuth와 사용자 데이터 저장이 필요한 기능입니다. 공개 데모에는 Client Secret과 사용자 데이터베이스를 포함하지 않았습니다.",
            ["GitHub OAuth", "FastAPI", "PostgreSQL"],
            "👤",
        )

    from login.logic import show_login_page
    show_login_page()

if __name__ == "__main__":
    main()
