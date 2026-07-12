"""AMPLIFY Analytics Dashboard (Streamlit)."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

LOG_PATH = Path(os.getenv("AMPLIFY_LOG_PATH", "data/amplify_chat_history.csv"))
DASHBOARD_PASSWORD = os.getenv("AMPLIFY_DASHBOARD_PASSWORD", "changeme")

st.set_page_config(page_title="AMPLIFY Analytics", page_icon="📊", layout="wide")


def _auth_gate() -> bool:
    if st.session_state.get("authed"):
        return True
    with st.sidebar:
        st.subheader("🔒 Restricted")
        pwd = st.text_input("Dashboard password", type="password")
        if st.button("Unlock", use_container_width=True):
            if pwd == DASHBOARD_PASSWORD:
                st.session_state["authed"] = True
                st.rerun()
            else:
                st.error("Incorrect password")
    return False


def _load() -> pd.DataFrame:
    if not LOG_PATH.exists():
        return pd.DataFrame(columns=["timestamp", "backend", "prompt", "response", "latency_ms"])
    df = pd.read_csv(LOG_PATH)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


def main() -> None:
    st.title("📊 AMPLIFY — Analytics")
    st.caption("Private, local, self-hosted telemetry.")

    if not _auth_gate():
        st.stop()

    df = _load()
    if df.empty:
        st.info("No chats logged yet. Start a conversation to populate the dashboard.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Total chats", f"{len(df):,}")
    c2.metric("Avg latency (ms)", f"{df['latency_ms'].mean():.0f}")
    c3.metric("Backends used", df["backend"].nunique())

    st.subheader("Latency over time")
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y="latency_ms",
                  color="backend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent chats")
    st.dataframe(
        df.sort_values("timestamp", ascending=False)
          .head(25)[["timestamp", "backend", "prompt", "response", "latency_ms"]],
        use_container_width=True, hide_index=True,
    )


if __name__ == "__main__":
    main()
