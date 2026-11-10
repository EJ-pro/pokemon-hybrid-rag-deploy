import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ui import inject_common_ui
from utils.demo_mode import backend_configured, show_unavailable

st.set_page_config(
    page_title="팀빌딩",
    page_icon="https://pokemonkorea.co.kr/img/_con.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_common_ui(spacer=True)

if not backend_configured():
    show_unavailable(
        "AI 팀 빌더",
        "선택한 포켓몬의 타입 관계를 분석하고 Hybrid RAG로 팀원을 추천하는 기능입니다. 운영 데이터베이스가 필요한 기능이라 공개 데모에서는 실행을 제한했습니다.",
        ["Graph-guided Retrieval", "pgvector", "Neo4j", "LangGraph"],
        "🧩",
    )

from teambuilding.ui import show_v2

show_v2()
