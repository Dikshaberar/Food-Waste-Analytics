import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FoodWaste Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD DATASET
# ==========================================

DATA_PATH = (
    Path(__file__).parent
    / "archive (3)"
    / "global_food_wastage_dataset.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found! Check your CSV file location.")
    st.stop()

# ==========================================
# DARK THEME CSS
# ==========================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #050d17;
    color: #e5edf5;
}

header[data-testid="stHeader"] {
    background: #050d17;
}

.block-container {
    padding: 1.5rem 2rem;
    max-width: 1600px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #091522;
    border-right: 1px solid #1d3043;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #aab9c8;
}

[data-testid="stSidebar"] h1 {
    color: #4ade80;
}

/* HEADINGS */

h1, h2, h3 {
    color: #f1f5f9;
}

p {
    color: #aab9c8;
}

/* HEADER */

.header-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0 25px 0;
}

.logo {
    font-size: 27px;
    font-weight: 800;
    color: #4ade80;
}

.subtitle {
    font-size: 12px;
    color: #68c995;
}

/* CARDS */

.metric-card {
    background: #0d1b2a;
    border: 1px solid #20354a;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
    transition: 0.3s;
}

.metric-card:hover {
    border-color: #36b879;
    transform: translateY(-3px);
}

.metric-title {
    color: #8fa2b7;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #f1f5f9;
    font-size: 27px;
    font-weight: 800;
    margin-top: 10px;
}

.metric-icon {
    font-size: 22px;
    float: right;
}

/* PANELS */

.panel {
    background: #0d1b2a;
    border: 1px solid #20354a;
    border-radius: 14px;
    padding: 18px;
}

.panel-title {
    font-size: 15px;
    font-weight: 700;
    color: #e5edf5;
    margin-bottom: 12px;
}

/* INSIGHT */

.insight {
    background: linear-gradient(
        135deg,
        #10382c,
        #0d1b2a
    );
    border: 1px solid #21664b;
    border-radius: 14px;
    padding: 20px;
}

.insight-title {
    color: #4ade80;
    font-weight: 700;
    font-size: 13px;
}

.insight-text {
    color: #e5f5eb;
    font-size: 14px;
    line-height: 1.7;
    margin-top: 12px;
}

/* BUTTONS */

.stButton button {
    background: #176b48;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover {
    background: #22965f;
    color: white;
}

/* SELECT BOX */

div[data-baseweb="select"] > div {
    background: #0d1b2a;
    border-color: #294157;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #20354a;
    border-radius: 12px;
}

hr {
    border-color: #20354a;
}

.footer {
    text-align: center;
    color: #63788d;
    padding: 25px;
    font-size: 11px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("""
<div style="padding:15px 5px 25px 5px;">

<div style="font-size:30px;color:#4ade80;">
    🌿
</div>

<h2 style="color:white;margin-bottom:0;">
    FoodWaste
</h2>

<h2 style="color:#4ade80;margin-top:0;">
    Intelligence
</h2>

<p style="font-size:11px;">
TRACK. ANALYZE. REDUCE.
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### MAIN MENU")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Waste Analysis",
        "Food Sources",
        "AI Insights",
        "Prediction",
        "Waste Simulator",
        "Targets",
        "Reports",
        "About"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

st.sidebar.markdown("### FILTERS")

years = sorted(df["Year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

countries = sorted(df["Country"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

categories = sorted(
    df["Food Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Food Categories",
    categories,
    default=categories
)


# ==========================================
# FILTER DATA
# ==========================================

filtered = df[
    (df["Year"].isin(selected_years)) &
    (df["Country"].isin(selected_countries)) &
    (df["Food Category"].isin(selected_categories))
]

if filtered.empty:
    st.warning("No data available. Change your filters.")
    st.stop()


# ==========================================
# COMMON CALCULATIONS
# ==========================================

total_waste = filtered["Total Waste (Tons)"].sum()

total_loss = filtered["Economic Loss (Million $)"].sum()

avg_per_capita = filtered[
    "Avg Waste per Capita (Kg)"
].mean()

household = filtered[
    "Household Waste (%)"
].mean()

top_country = (
    filtered.groupby("Country")["Total Waste (Tons)"]
    .sum()
    .idxmax()
)

top_category = (
    filtered.groupby("Food Category")["Total Waste (Tons)"]
    .sum()
    .idxmax()
)


# ==========================================
# HEADER
# ==========================================

st.markdown(f"""
<div class="header-box">

<div>
    <div class="logo">🌿 FoodWaste Intelligence</div>
    <div class="subtitle">
        Track. Analyze. Reduce. Build a sustainable future.
    </div>
</div>

<div style="color:#4ade80;font-size:12px;">
    ● DATA DASHBOARD
</div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# REUSABLE KPI CARD
# ==========================================

def metric_card(title, value, icon):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# CHART THEME
# ==========================================

def dark_chart(fig, height=350):

    fig.update_layout(
        height=height,
        paper_bgcolor="#0d1b2a",
        plot_bgcolor="#0d1b2a",
        font_color="#b8c6d5",
        margin=dict(l=15, r=15, t=45, b=15),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b8c6d5")
        )
    )

    fig.update_xaxes(
        gridcolor="#20354a",
        zerolinecolor="#20354a"
    )

    fig.update_yaxes(
        gridcolor="#20354a",
        zerolinecolor="#20354a"
    )

    return fig


# ==========================================
# DASHBOARD PAGE
# ==========================================

if page == "Dashboard":

    st.markdown("## Dashboard Overview")

    st.caption(
        "Global food waste monitoring and analytics platform"
    )

    # KPI CARDS

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "TOTAL FOOD WASTE",
            f"{total_waste:,.0f} Tons",
            "🌍"
        )

    with c2:
        metric_card(
            "ECONOMIC LOSS",
            f"${total_loss:,.1f}M",
            "💰"
        )

    with c3:
        metric_card(
            "WASTE PER CAPITA",
            f"{avg_per_capita:,.1f} Kg",
            "👥"
        )

    with c4:
        metric_card(
            "HOUSEHOLD WASTE",
            f"{household:,.1f}%",
            "🏠"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # MAIN THREE COLUMNS

    col1, col2, col3 = st.columns(
        [1, 2.1, 1.1]
    )

    # OVERVIEW

    with col1:

        st.markdown(
            '<div class="panel-title">📊 Overview</div>',
            unsafe_allow_html=True
        )

        st.metric(
            "Countries",
            filtered["Country"].nunique()
        )

        st.metric(
            "Food Categories",
            filtered["Food Category"].nunique()
        )

        st.metric(
            "Years",
            filtered["Year"].nunique()
        )

        st.markdown(
            '<div class="panel-title">Highest Waste Category</div>',
            unsafe_allow_html=True
        )

        st.success(top_category)

    # WORLD MAP

    with col2:

        st.markdown(
            '<div class="panel-title">🌍 Food Waste by Region</div>',
            unsafe_allow_html=True
        )

        map_data = (
            filtered.groupby("Country", as_index=False)
            ["Total Waste (Tons)"].sum()
        )

        fig = px.choropleth(
            map_data,
            locations="Country",
            locationmode="country names",
            color="Total Waste (Tons)",
            hover_name="Country",
            color_continuous_scale=[
                "#123c35",
                "#168b61",
                "#4ade80"
            ],
            title=""
        )

        fig.update_geos(
            bgcolor="#0d1b2a",
            showocean=True,
            oceancolor="#091522",
            showland=True,
            landcolor="#172b3d",
            showcoastlines=False
        )

        fig.update_layout(
            height=330,
            paper_bgcolor="#0d1b2a",
            margin=dict(l=0, r=0, t=0, b=0),
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # AI INSIGHTS

    with col3:
      st.markdown("""
      <div class="insight-card">
        <div class="insight-title">✨ AI INSIGHTS</div>
        <div class="insight-text">
            The highest food waste in your selected data comes from
            <b>Turkey</b>.
        </div>
        <br>
        <div class="insight-title">RECOMMENDATION</div>
        <div class="insight-text">
            Focus on reducing <b>Prepared Food</b> waste through
            improved storage, distribution and food management.
        </div>
        <div style="font-size:40px;text-align:right;">🌱</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CHARTS

    left, right = st.columns([1.7, 1])

    with left:

        st.markdown("### 📈 Food Waste Over Time")

        yearly = (
            filtered.groupby(
                ["Year", "Food Category"],
                as_index=False
            )["Total Waste (Tons)"].sum()
        )

        fig = px.bar(
            yearly,
            x="Year",
            y="Total Waste (Tons)",
            color="Food Category",
            barmode="stack",
            color_discrete_sequence=[
                "#36bd83",
                "#3478d4",
                "#8b63d9",
                "#e8b84f",
                "#e87979",
                "#40b7c5"
            ]
        )

        dark_chart(fig, 320)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.markdown("### 🍩 Food Waste Sources")

        category_data = (
            filtered.groupby("Food Category", as_index=False)
            ["Total Waste (Tons)"].sum()
        )

        fig = px.pie(
            category_data,
            names="Food Category",
            values="Total Waste (Tons)",
            hole=0.65,
            color_discrete_sequence=[
                "#36bd83",
                "#3478d4",
                "#8b63d9",
                "#e8b84f",
                "#e87979"
            ]
        )

        fig.update_traces(
            textinfo="percent",
            textfont_color="white"
        )

        dark_chart(fig, 320)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # BOTTOM SECTION

    st.markdown("### 🏆 Top Food Waste Countries")

    top_countries = (
        filtered.groupby("Country", as_index=False)
        ["Total Waste (Tons)"]
        .sum()
        .nlargest(10, "Total Waste (Tons)")
    )

    fig = px.bar(
        top_countries.sort_values("Total Waste (Tons)"),
        x="Total Waste (Tons)",
        y="Country",
        orientation="h",
        color="Total Waste (Tons)",
        color_continuous_scale=[
            "#123c35",
            "#4ade80"
        ]
    )

    dark_chart(fig, 400)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# WASTE ANALYSIS PAGE
# ==========================================

elif page == "Waste Analysis":

    st.title("📊 Food Waste Analysis")

    country_data = (
        filtered.groupby("Country", as_index=False)
        ["Total Waste (Tons)"].sum()
    )

    fig = px.bar(
        country_data.sort_values("Total Waste (Tons)"),
        x="Total Waste (Tons)",
        y="Country",
        orientation="h",
        color="Total Waste (Tons)",
        color_continuous_scale="Greens"
    )

    dark_chart(fig, 600)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Yearly Food Waste Trend")

    yearly = (
        filtered.groupby("Year", as_index=False)
        ["Total Waste (Tons)"].sum()
    )

    fig = px.line(
        yearly,
        x="Year",
        y="Total Waste (Tons)",
        markers=True
    )

    fig.update_traces(
        line_color="#4ade80",
        line_width=3
    )

    dark_chart(fig)

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# FOOD SOURCES PAGE
# ==========================================

elif page == "Food Sources":

    st.title("🍎 Food Waste Sources")

    category = (
        filtered.groupby("Food Category", as_index=False)
        .agg({
            "Total Waste (Tons)": "sum",
            "Economic Loss (Million $)": "sum"
        })
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            category,
            names="Food Category",
            values="Total Waste (Tons)",
            hole=0.5,
            title="Waste by Food Category"
        )

        dark_chart(fig)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            category,
            x="Food Category",
            y="Economic Loss (Million $)",
            color="Economic Loss (Million $)",
            color_continuous_scale="Oranges",
            title="Economic Loss by Category"
        )

        dark_chart(fig)

        st.plotly_chart(fig, use_container_width=True)


# ==========================================
# AI INSIGHTS PAGE
# ==========================================

elif page == "AI Insights":

    st.title("✨ Food Waste Intelligence")

    st.info(
        "These insights are calculated from your dataset. "
        "They are descriptive analytics, not AI-generated predictions."
    )

    st.markdown("### Important Findings")

    st.success(
        f"Highest waste country: {top_country}"
    )

    st.success(
        f"Highest waste category: {top_category}"
    )

    st.warning(
        f"Average household waste: {household:.2f}%"
    )

    st.info(
        f"Average waste per capita: {avg_per_capita:.2f} Kg"
    )

    st.markdown("### Recommended Actions")

    st.write("""
    1. Improve food storage systems.
    2. Reduce unnecessary food production.
    3. Improve food distribution.
    4. Donate surplus edible food.
    5. Encourage food recycling and composting.
    """)


# ==========================================
# PREDICTION PAGE
# ==========================================

elif page == "Prediction":

    st.title("🤖 Economic Loss Prediction")

    from sklearn.linear_model import LinearRegression

    X = filtered[["Total Waste (Tons)"]]

    y = filtered["Economic Loss (Million $)"]

    if len(filtered) < 2:
        st.warning("At least two records are needed for training.")
    else:

        model = LinearRegression()

        model.fit(X, y)

        waste = st.number_input(
            "Enter food waste in tons",
            min_value=0.0,
            value=10000.0
        )

        if st.button("Predict Economic Loss"):

            prediction = model.predict(
                pd.DataFrame({
                    "Total Waste (Tons)": [waste]
                })
            )[0]

            st.success(
                f"Estimated Economic Loss: ${prediction:,.2f} Million"
            )

            st.caption(
                "This is a simple linear regression estimate "
                "based on the selected dataset."
            )


# ==========================================
# WASTE SIMULATOR PAGE
# ==========================================

elif page == "Waste Simulator":

    st.title("🌍 Food Waste Reduction Simulator")

    country = st.selectbox(
        "Select Country",
        sorted(df["Country"].unique())
    )

    category = st.selectbox(
        "Select Food Category",
        sorted(df["Food Category"].unique())
    )

    reduction = st.slider(
        "Waste Reduction Target",
        0,
        90,
        25
    )

    simulation = df[
        (df["Country"] == country) &
        (df["Food Category"] == category)
    ]

    waste = simulation["Total Waste (Tons)"].sum()

    loss = simulation["Economic Loss (Million $)"].sum()

    saved_waste = waste * reduction / 100

    saved_money = loss * reduction / 100

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Waste Saved",
        f"{saved_waste:,.2f} Tons"
    )

    c2.metric(
        "Money Saved",
        f"${saved_money:,.2f}M"
    )

    c3.metric(
        "Remaining Waste",
        f"{waste-saved_waste:,.2f} Tons"
    )


# ==========================================
# TARGETS PAGE
# ==========================================

elif page == "Targets":

    st.title("🎯 Sustainability Targets")

    target = st.slider(
        "Choose Waste Reduction Target",
        5,
        90,
        30
    )

    saved = total_waste * target / 100

    remaining = total_waste - saved

    st.metric(
        "Potential Waste Reduction",
        f"{saved:,.0f} Tons"
    )

    st.metric(
        "Remaining Waste",
        f"{remaining:,.0f} Tons"
    )

    st.progress(target / 100)

    st.success(
        f"Your target is to reduce food waste by {target}%."
    )


# ==========================================
# REPORTS PAGE
# ==========================================

elif page == "Reports":

    st.title("📥 Download Reports")

    st.write(
        "Download the filtered food waste dataset."
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV Report",
        csv,
        "FoodWaste_Report.csv",
        "text/csv"
    )

    st.dataframe(
        filtered,
        use_container_width=True
    )


# ==========================================
# ABOUT PAGE
# ==========================================

elif page == "About":

    st.title("🌱 About FoodWaste Intelligence")

    st.write("""
    FoodWaste Intelligence is a data analytics project
    designed to study global food wastage.

    The project focuses on:

    - Global food waste analysis
    - Country-wise comparison
    - Economic loss analysis
    - Machine learning prediction
    - Waste reduction simulation
    - Sustainability awareness
    """)

    st.markdown("### Technologies Used")

    st.write("""
    Python | Pandas | NumPy | Plotly |
    Scikit-learn | Streamlit
    """)


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">

FOODWASTE INTELLIGENCE

<br><br>

Track. Analyze. Reduce.

<br>

Building a Sustainable Future 🌱

</div>
""", unsafe_allow_html=True)