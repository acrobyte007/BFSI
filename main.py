
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BFSI Reputation Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("E:/BFSI/BFSI/data/final_output.csv")
    return df


df = load_data()

df["driver"] = df["driver"].fillna("Unknown")
df["sub_driver"] = df["sub_driver"].fillna("Unknown")

st.title("BFSI Reputation Intelligence Dashboard")

# =========================
# OVERVIEW
# =========================
st.header("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Mentions", len(df))
col2.metric("Unique Drivers", df["driver"].nunique())
col3.metric("Unique Sub-drivers", df["sub_driver"].nunique())

# -------------------------
# DRIVER DISTRIBUTION
# -------------------------
driver_counts = (
    df["driver"]
    .value_counts()
    .rename_axis("driver")
    .reset_index(name="count")
    .sort_values(by="count", ascending=True)
)

color_map = {
    "Brand Perception": "#1f77b4",
    "User Experience": "#2ca02c",
    "Responsible Business Practices": "#ff7f0e"
}

fig1 = px.bar(
    driver_counts,
    x="count",
    y="driver",
    orientation="h",
    text="count",
    color="driver",
    color_discrete_map=color_map,
    title="Driver Distribution"
)

fig1.update_layout(
    xaxis_title="Number of Mentions",
    yaxis_title="Reputation Driver",
    title_x=0.3
)

fig1.update_traces(textposition="outside")

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# SUB-DRIVER DISTRIBUTION
# -------------------------
sub_counts = (
    df["sub_driver"]
    .value_counts()
    .rename_axis("sub_driver")
    .reset_index(name="count")
    .sort_values(by="count", ascending=True)
)

fig2 = px.bar(
    sub_counts,
    x="count",
    y="sub_driver",
    orientation="h",
    text="count",
    title="Sub-driver Distribution"
)

fig2.update_layout(
    xaxis_title="Number of Mentions",
    yaxis_title="Sub-driver",
    title_x=0.3
)

fig2.update_traces(textposition="outside")

st.plotly_chart(fig2, use_container_width=True)

# =========================
# CONTENT EXPLORER
# =========================
st.header("Content Explorer")

driver_filter = st.multiselect("Filter by Driver", df["driver"].unique())
sub_filter = st.multiselect("Filter by Sub Driver", df["sub_driver"].unique())

filtered_df = df.copy()

if driver_filter:
    filtered_df = filtered_df[filtered_df["driver"].isin(driver_filter)]

if sub_filter:
    filtered_df = filtered_df[filtered_df["sub_driver"].isin(sub_filter)]

st.dataframe(filtered_df, use_container_width=True)

# =========================
# INSIGHTS
# =========================
st.header("Insights")

top_driver = df["driver"].value_counts().idxmax()
top_sub = df["sub_driver"].value_counts().idxmax()

st.subheader("Key Findings")
st.write(f"Most discussed driver: **{top_driver}**")
st.write(f"Most discussed sub-driver: **{top_sub}**")

# -------------------------
# SENTIMENT DISTRIBUTION
# -------------------------
if "sentiment" in df.columns:
    sentiment_counts = (
        df["sentiment"]
        .value_counts()
        .rename_axis("sentiment")
        .reset_index(name="count")
    )

    fig3 = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        title="Sentiment Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# TOP DISCUSSION THEMES
# -------------------------
if "title" in df.columns:
    top_titles = (
        df["title"]
        .value_counts()
        .head(10)
        .rename_axis("topic")
        .reset_index(name="count")
        .sort_values(by="count", ascending=True)
    )

    fig4 = px.bar(
        top_titles,
        x="count",
        y="topic",
        orientation="h",
        title="Top Discussion Themes"
    )

    st.plotly_chart(fig4, use_container_width=True)