import os
import streamlit as st
from utils.ui import inject_common_ui

st.set_page_config(
    page_title="Battle - Pokemon World",
    page_icon="https://pokemonkorea.co.kr/img/_con.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_common_ui(spacer=True)

# 배틀은 Neo4j 기술·상성 데이터에 직접 연결되는 운영 기능입니다.
# 공개 데모에서는 DB 접속 정보를 배포하지 않고 안내 화면만 제공합니다.
if not os.environ.get("GRAPH_DB_URI"):
    st.markdown(
        """
        <div style="max-width:760px;margin:100px auto;padding:48px;border:1px solid #e5e7eb;
                    border-radius:24px;background:#fff;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.08);">
          <div style="font-size:42px;margin-bottom:18px;">⚔️</div>
          <h1 style="margin:0 0 16px;font-size:30px;">배틀 시뮬레이터</h1>
          <p style="margin:0;color:#64748b;line-height:1.8;">
            이 기능은 Neo4j의 포켓몬·기술·타입 관계 데이터와 배틀 API를 사용합니다.<br>
            공개 데모에서는 데이터베이스 접속 정보를 보호하기 위해 실행을 제한했습니다.
          </p>
          <a href="/pokedex" target="_self" style="display:inline-block;margin-top:28px;padding:12px 22px;
             border-radius:999px;background:#2563eb;color:#fff;text-decoration:none;font-weight:700;">도감 둘러보기</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

from battle.battle import display_battle
from battle.build_team import display_builder
from battle.menu import display_menu
from battle.ui import inject_battle_styles, get_gym_bg_base64

# 선택된 관장에 맞는 체육관 배경 적용
# base64를 session_state에 캐싱 → 매 rerun에 동일 문자열 유지 → React style 태그 재렌더링 방지 → 깜빡임 제거
_leader = st.session_state.get("leader_name") or st.session_state.get("selected_leader", "웅이")
_bg_cache_key = f"_gym_bg_b64_{_leader}"
if _bg_cache_key not in st.session_state:
    st.session_state[_bg_cache_key] = get_gym_bg_base64(_leader)
inject_battle_styles(bg_url=st.session_state[_bg_cache_key])


def show():
    if "player_team" not in st.session_state:
        st.session_state.player_team = []
    if "battle_stage" not in st.session_state:
        st.session_state.battle_stage = "menu"

    if st.session_state.battle_stage == "menu":
        display_menu()
    elif st.session_state.battle_stage == "teambuilding":
        display_builder()
    elif st.session_state.battle_stage == "battle":
        display_battle()


if __name__ == "__main__":
    show()
