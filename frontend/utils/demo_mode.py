"""공개 데모에서 운영 인프라 의존 기능을 안전하게 안내한다."""

from __future__ import annotations

import os

import streamlit as st


def backend_configured() -> bool:
    return bool(os.getenv("BACKEND_URL") or os.getenv("BACKEND_API_URL"))


def graph_configured() -> bool:
    return bool(os.getenv("GRAPH_DB_URI"))


def oauth_configured() -> bool:
    return bool(os.getenv("GITHUB_CLIENT_ID") and os.getenv("GITHUB_CLIENT_SECRET"))


def show_unavailable(title: str, description: str, requirements: list[str], icon: str = "🔒") -> None:
    chips = "".join(
        f'<span style="display:inline-block;margin:5px;padding:7px 12px;border-radius:999px;'
        f'background:#eff6ff;color:#1d4ed8;font-size:13px;font-weight:700;">{item}</span>'
        for item in requirements
    )
    st.markdown(
        f"""
        <div style="max-width:760px;margin:100px auto;padding:48px;border:1px solid #e5e7eb;
                    border-radius:24px;background:#fff;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.08);">
          <div style="font-size:42px;margin-bottom:18px;">{icon}</div>
          <h1 style="margin:0 0 16px;font-size:30px;">{title}</h1>
          <p style="margin:0 auto 22px;max-width:620px;color:#64748b;line-height:1.8;">{description}</p>
          <div>{chips}</div>
          <a href="/pokedex" target="_self" style="display:inline-block;margin-top:28px;padding:12px 22px;
             border-radius:999px;background:#2563eb;color:#fff;text-decoration:none;font-weight:700;">도감 둘러보기</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

