import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ui import inject_common_ui
from utils.demo_mode import backend_configured, show_unavailable

st.set_page_config(
    page_title="포켓몬 비공식 AI 박사",
    page_icon="https://pokemonkorea.co.kr/img/_con.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_common_ui(spacer=True, hide_sidebar=True)

if not backend_configured():
    show_unavailable(
        "AI 박사 챗봇",
        "Hybrid Retrieval과 LangGraph 에이전트를 실행하는 기능입니다. 공개 데모에서는 LLM 키와 운영 데이터베이스를 노출하지 않습니다.",
        ["FastAPI", "PostgreSQL · pgvector", "Neo4j", "LLM API"],
        "🤖",
    )

from chatbot.styles import inject_chatbot_styles
from chatbot.ui import show

inject_chatbot_styles()
show()
