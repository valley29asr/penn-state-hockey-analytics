# dashboard/styles.py

import streamlit as st


def apply_styles():
    st.markdown(
        """
<style>
.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(49, 130, 206, 0.14),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #07111f 0%,
            #0b1728 55%,
            #0d1b2e 100%
        );

    color: #f8fafc;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1,
h2,
h3 {
    color: #f8fafc !important;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    letter-spacing: -0.02em;
}

h1 {
    font-weight: 800 !important;
}

h2,
h3 {
    font-weight: 700 !important;
}

p,
label,
.stMarkdown {
    color: #dbeafe;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #06101d 0%,
        #0a192b 100%
    );

    border-right: 1px solid rgba(147, 197, 253, 0.18);
}

section[data-testid="stSidebar"] * {
    color: #eaf4ff;
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(18, 42, 70, 0.96),
        rgba(10, 27, 47, 0.96)
    );

    border: 1px solid rgba(125, 211, 252, 0.22);
    border-radius: 16px;

    padding: 1.1rem 1.2rem;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

div[data-testid="stMetric"]:hover {
    border-color: rgba(125, 211, 252, 0.55);
    transform: translateY(-2px);
    transition: 0.2s ease;
}

div[data-testid="stMetricLabel"] {
    color: #9ec5e8;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 800;
}

hr {
    border-color: rgba(148, 163, 184, 0.18);
}

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(125, 211, 252, 0.18);
    border-radius: 14px;
    overflow: hidden;
}

div[data-baseweb="select"] > div {
    background-color: #10233b;
    border-color: rgba(125, 211, 252, 0.25);
    color: white;
    border-radius: 10px;
}

div[role="radiogroup"] label {
    background-color: rgba(255, 255, 255, 0.025);
    border-radius: 10px;
    padding: 0.45rem 0.6rem;
    margin-bottom: 0.25rem;
}

div[role="radiogroup"] label:hover {
    background-color: rgba(56, 189, 248, 0.10);
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #0ea5e9,
        #2563eb
    );

    color: white;
    border: none;
    border-radius: 10px;

    padding: 0.6rem 1.2rem;
    font-weight: 700;
}

.stButton > button:hover {
    box-shadow: 0 8px 22px rgba(14, 165, 233, 0.25);
    transform: translateY(-1px);
}

.hockey-accent {
    width: 72px;
    height: 5px;
    border-radius: 999px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #7dd3fc,
        #2563eb
    );

    margin-bottom: 1.25rem;
}

.hero-card {
    background: linear-gradient(
        135deg,
        rgba(20, 47, 78, 0.96),
        rgba(8, 24, 43, 0.96)
    );

    border: 1px solid rgba(125, 211, 252, 0.22);
    border-radius: 22px;

    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;

    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
}

.hero-subtitle {
    color: #b9d8f2;
    font-size: 1.05rem;
    line-height: 1.65;
    max-width: 950px;
}

.section-card {
    background: rgba(11, 31, 52, 0.72);
    border: 1px solid rgba(125, 211, 252, 0.16);
    border-radius: 18px;

    padding: 1.3rem 1.4rem;
    margin-bottom: 1rem;
}

.page-label {
    color: #7dd3fc;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}
</style>
""",
        unsafe_allow_html=True
    )