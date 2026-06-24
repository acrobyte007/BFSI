import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="BFSI Intelligence Dashboard", layout="wide")

df = pd.read_csv("E:/BFSI/BFSI/data/final_output.csv")

df["driver"] = df["driver"].fillna("Unknown")
df["sub_driver"] = df["sub_driver"].fillna("Unknown")

# =========================
# HEADER
# =========================
st.title("📊 BFSI Reputation Intelligence Dashboard")
st.markdown("AI-powered reputation tracking across digital BFSI mentions")

# =========================
# KPI SECTION (EXECUTIVE VIEW)
# =========================
st.header("📌 Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Mentions", len(df))
col2.metric("Drivers", df["driver"].nunique())
col3.metric("Sub-drivers", df["sub_driver"].nunique())

if "sentiment" in df.columns:
    neg_pct = round((df["sentiment"] == "Negative").mean() * 100, 2)
    col4.metric("Negative Mentions %", f"{neg_pct}%")

st.divider()

# =========================
# OVERVIEW CHARTS
# =========================
st.header("📊 Reputation Overview")

col1, col2 = st.columns(2)

# Driver Distribution
driver_counts = df["driver"].value_counts().reset_index()
driver_counts.columns = ["driver", "count"]

fig1 = px.bar(
    driver_counts.sort_values("count"),
    x="count",
    y="driver",
    orientation="h",
    text="count",
    title="Driver Distribution"
)
fig1.update_traces(textposition="outside")
col1.plotly_chart(fig1, use_container_width=True)

# Sub-driver Distribution
sub_counts = df["sub_driver"].value_counts().reset_index()
sub_counts.columns = ["sub_driver", "count"]

fig2 = px.bar(
    sub_counts.sort_values("count"),
    x="count",
    y="sub_driver",
    orientation="h",
    text="count",
    title="Sub-driver Distribution"
)
fig2.update_traces(textposition="outside")
col2.plotly_chart(fig2, use_container_width=True)

st.divider()

# =========================
# SENTIMENT OVERVIEW
# =========================
st.header("😊 Sentiment Analysis")

if "sentiment" in df.columns:
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]

    fig3 = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        title="Sentiment Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# =========================
# RISK INTELLIGENCE LAYER
# =========================
st.header("⚠️ Risk & Reputation Insights")

df_ins = df.copy()

if "sentiment" in df_ins.columns:
    sentiment_map = {"Positive": 1, "Neutral": 0, "Negative": -1}
    df_ins["sentiment_score"] = df_ins["sentiment"].map(sentiment_map)

# Risk Drivers
if "driver" in df_ins.columns:
    risk = df_ins.groupby("driver")["sentiment"].value_counts(normalize=True).unstack().fillna(0)

    if "Negative" in risk.columns:
        risk = risk.sort_values("Negative", ascending=False)

        fig4 = px.bar(
            risk.reset_index(),
            x="Negative",
            y="driver",
            orientation="h",
            title="Reputation Risk Drivers (Negative Share)"
        )

        st.plotly_chart(fig4, use_container_width=True)

# Heatmap
heatmap = df_ins.groupby(["driver", "sentiment"]).size().unstack().fillna(0)

fig5 = go.Figure(
    data=go.Heatmap(
        z=heatmap.values,
        x=heatmap.columns,
        y=heatmap.index,
        colorscale="RdYlGn_r"
    )
)

fig5.update_layout(title="Driver vs Sentiment Heatmap")
st.plotly_chart(fig5, use_container_width=True)

# Executive Summary
st.subheader("🧠 Auto Insights")

if "sentiment" in df_ins.columns:
    top_neg = df_ins[df_ins["sentiment"] == "Negative"]["driver"].value_counts().idxmax()
    top_pos = df_ins[df_ins["sentiment"] == "Positive"]["driver"].value_counts().idxmax()

    col1, col2 = st.columns(2)
    col1.write(f"🔴 Highest Risk Driver: **{top_neg}**")
    col2.write(f"🟢 Best Performing Driver: **{top_pos}**")

st.divider()

# =========================
# DEEP DIVE EXPLORER
# =========================
st.header("🔍 Content Explorer")

col1, col2, col3 = st.columns(3)

drivers = st.multiselect("Filter Drivers", df["driver"].unique())
subs = st.multiselect("Filter Sub-drivers", df["sub_driver"].unique())
sent = st.multiselect("Filter Sentiment", df["sentiment"].unique() if "sentiment" in df.columns else [])

filtered = df.copy()

if drivers:
    filtered = filtered[filtered["driver"].isin(drivers)]

if subs:
    filtered = filtered[filtered["sub_driver"].isin(subs)]

if sent:
    filtered = filtered[filtered["sentiment"].isin(sent)]

st.dataframe(filtered, use_container_width=True)

st.divider()

# =========================
# TOP THEMES
# =========================
st.header("🔥 Top Discussion Themes")

if "title" in df.columns:
    top = df["title"].value_counts().head(10).reset_index()
    top.columns = ["topic", "count"]

    fig6 = px.bar(
        top.sort_values("count"),
        x="count",
        y="topic",
        orientation="h",
        title="Top Themes"
    )

    st.plotly_chart(fig6, use_container_width=True)