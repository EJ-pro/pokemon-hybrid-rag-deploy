import streamlit as st
import os
import sys

# Ensure frontend is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui import inject_common_ui
from utils.demo_mode import backend_configured, show_unavailable

st.set_page_config(
    page_title="마이페이지",
    page_icon="https://pokemonkorea.co.kr/img/_con.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def main():
    # 1. 공통 UI 주입
    inject_common_ui()

    if not backend_configured():
        show_unavailable(
            "트레이너 마이페이지",
            "GitHub 활동과 게임 기록, 추천 이력을 통합해 보여주는 기능입니다. 사용자 데이터가 없는 공개 데모에서는 실행을 제한했습니다.",
            ["GitHub API", "사용자 활동 로그", "PostgreSQL"],
            "🏅",
        )

    from mypage.styles import inject_mypage_styles
    from mypage.ui import show
    
    # 2. 스타일 주입
    inject_mypage_styles()
    
    # 3. 메인 UI 렌더링
    show()

if __name__ == "__main__":
    main()
