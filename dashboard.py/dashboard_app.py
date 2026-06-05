import sys
from pathlib import Path
import plotly.express as px

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
from www.services.etl.pipeline import openalex_pipeline
import pandas as pd

st.set_page_config(
    page_title="Bibliometrix Dashboard",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #0A0A0A;
}

h1 {
    color: #D4AF37 !important;
}

h2, h3 {
    color: #00A86B !important;
}

div[data-testid="metric-container"] {
    background-color: #1A1A1A;
    border: 1px solid #D4AF37;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

st.title("📚 Bibliometrix Dashboard")
st.write("OpenAlex ETL + Bibliometric Analysis")

colA, colB = st.columns([3, 1])

with colA:
    query = st.text_input(
        "",
        placeholder="🔍 Search topics like AI, Machine Learning, Data Science..."
    )

with colB:
    max_results = st.selectbox(
        "Documents",
        [50, 100, 200, 500],
        index=1
    )

if not query:
    query = "machine learning"

df = openalex_pipeline(
    query=query,
    max_results=max_results
)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Documents", len(df))

with col2:
    st.metric(
        "Authors",
        df["AU"].explode().dropna().nunique()
    )

with col3:
    st.metric(
        "Keywords",
        df["DE"].explode().dropna().nunique()
    )

with col4:
    st.metric(
        "Total Citations",
        int(df["TC"].fillna(0).sum())
    )
# ==================================================
# DATASET PREVIEW
# ==================================================

st.markdown("""
<h2 style='color:#D4AF37;
font-size:42px;
font-weight:700;'>
📄 STANDARDIZED DATASET PREVIEW
</h2>
""", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)

# ==================================================
# PUBLICATIONS BY YEAR
# ==================================================

st.divider()

st.markdown("""
<h2 style='color:#D4AF37;
font-size:42px;
font-weight:700;'>
📊 PUBLICATIONS BY YEAR
</h2>
""", unsafe_allow_html=True)

year_counts = df["PY"].value_counts().sort_index()

fig = px.bar(
    x=year_counts.index,
    y=year_counts.values
)

fig.update_traces(
    marker_color="#D4AF37"
)

fig.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#0A0A0A",
    font_color="white",
    xaxis_title="Year",
    yaxis_title="Publications",
    yaxis=dict(dtick=1),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TOP CITED PAPERS
# ==================================================

st.divider()

st.markdown("""
<h2 style='color:#D4AF37;
font-size:42px;
font-weight:700;'>
🏆 TOP 10 MOST CITED PAPERS
</h2>
""", unsafe_allow_html=True)

if "TC" in df.columns:

    top_papers = (
        df.sort_values("TC", ascending=False)
        [["TI", "TC"]]
        .head(10)
    )

    st.dataframe(top_papers, use_container_width=True)

# ==================================================
# TOP AUTHORS
# ==================================================

st.divider()

st.markdown("""
<h2 style='color:#00C78C;
font-size:42px;
font-weight:700;'>
👥 TOP AUTHORS
</h2>
""", unsafe_allow_html=True)

top_authors = (
    df["AU"]
    .explode()
    .dropna()
    .value_counts()
    .head(10)
    .reset_index()
)

top_authors.columns = ["Author", "Publications"]

# Ranking Column
top_authors.insert(
    0,
    "Rank",
    ["🥇", "🥈", "🥉", "4", "5", "6", "7", "8", "9", "10"]
)

col1, col2 = st.columns([3, 1])

with col1:
    st.dataframe(
        top_authors,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.metric(
        "TOP AUTHOR",
        top_authors.iloc[0]["Author"]
    )

    st.metric(
        "PUBLICATIONS",
        int(top_authors.iloc[0]["Publications"])
    )
# ==================================================
# TOP KEYWORDS
# ==================================================

st.divider()

st.markdown("""
<h2 style='color:#D4AF37;
font-size:42px;
font-weight:700;'>
🔑 TOP KEYWORDS
</h2>
""", unsafe_allow_html=True)

top_keywords = (
    df["DE"]
    .explode()
    .dropna()
    .value_counts()
    .head(10)
    .reset_index()
)

top_keywords.columns = ["Keyword", "Frequency"]

fig = px.bar(
    top_keywords.sort_values("Frequency"),
    x="Frequency",
    y="Keyword",
    orientation="h",
    text="Frequency"
)

fig.update_traces(
    marker_color="#D4AF37",
    textposition="outside"
)

fig.update_layout(
    paper_bgcolor="#0A0A0A",
    plot_bgcolor="#0A0A0A",
    font_color="white",
    xaxis_title="Frequency",
    yaxis_title="",
    showlegend=False,
    height=600,
    margin=dict(l=20, r=20, t=20, b=20)
)

fig.update_xaxes(
    nticks=8
)


st.plotly_chart(fig, use_container_width=True)
st.divider()

st.markdown("""
<h2 style='color:#D4AF37;font-size:42px;font-weight:700;'>
⬇ EXPORT RESULTS
</h2>
""", unsafe_allow_html=True)

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset (CSV)",
    data=csv,
    file_name=f"{query}_bibliometric_data.csv",
    mime="text/csv"
)

st.divider()

st.markdown("""
<div style="
text-align:center;
padding:30px;
font-size:15px;
line-height:1.8;
color:#CCCCCC;
">

<h3 style="color:#D4AF37;">
📚 Bibliometrix Dashboard 
</h3>

<b style="color:#00C78C;">Developed by</b><br>
Madhumithra Balasubramanian<br>
Aya Soundous Hechaichi<br>
Alina Siddiqui

<br>

<b style="color:#00C78C;">Technologies Used</b><br>
Python • Streamlit • OpenAlex API • Bibliometrix Framework

<br>

<b style="color:#00C78C;">Hardware and Software for Big Data – Mod B</b><br>
University of Naples Federico II

<br>

<b style="color:#00C78C;">Professor:</b> Vincenzo Moscato<br>Data Science Course – Academic Year 2025/2026
</div>
""", unsafe_allow_html=True)