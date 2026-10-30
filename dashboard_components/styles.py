import streamlit as st


def apply_dashboard_styles():
    """Apply the shared black, violet, purple, and white dashboard theme."""
    st.markdown(
        """
        <style>
        
        .stApp {
            background: #09070F;
            color: #F5F3FF;
            font-family: Times New Roman;
        }
        [data-testid="stHeader"] { background: #09070F; }
        [data-testid="stMainBlockContainer"] {
            max-width: 1450px;
            padding-top: 1.8rem;
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            background: #100B19;
            border-right: 1px solid #302342;
        }
        [data-testid="stSidebar"] * { color: #E9DFFF; }
        h1, h2, h3 {
            color: #FFFFFF !important;
            letter-spacing: -0.4px;
        }
        h1 { font-size: 2.1rem !important; font-weight: 750 !important; }
        h2 { font-size: 1.45rem !important; font-weight: 650 !important; }
        h3 { font-size: 1.05rem !important; font-weight: 600 !important; }
        p, label { color: #D6CDE7; }
        .dashboard-header {
            background: linear-gradient(125deg, #1B102B, #120C1D 70%);
            border: 1px solid #493267;
            border-radius: 16px;
            padding: 26px 30px;
            margin-bottom: 24px;
        }
        .dashboard-header h1 {
            margin: 0 0 8px 0;
            color: #FFFFFF !important;
        }
        .dashboard-header p {
            color: #C4B5FD;
            margin: 0;
            font-size: 14px;
        }
        .eyebrow {
            color: #A78BFA !important;
            font-size: 11px !important;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        [data-testid="stMetric"] {
            background: #171023;
            border: 1px solid #38264F;
            border-radius: 14px;
            padding: 18px 20px;
            min-height: 112px;
        }
        [data-testid="stMetricLabel"] {
            color: #C4B5FD !important;
            font-size: 13px !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 27px !important;
            font-weight: 750 !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid #38264F;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px 8px 0 0;
            padding: 12px 16px;
            color: #C4B5FD;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
            border-bottom: 2px solid #A78BFA !important;
        }
        .stTabs [data-baseweb="tab-panel"] { padding-top: 22px; }
        [data-testid="stForm"] {
            background: #130D1D;
            border: 1px solid #38264F;
            border-radius: 14px;
            padding: 22px;
        }
        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input {
            background: #100B19;
            color: #FFFFFF;
            border: 1px solid #493267;
            border-radius: 8px;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            background: #100B19;
            border-color: #493267;
            border-radius: 8px;
        }
        .stButton > button, .stFormSubmitButton > button {
            background: #6D28D9;
            color: #FFFFFF;
            border: 1px solid #8B5CF6;
            border-radius: 9px;
            padding: 9px 18px;
            font-weight: 650;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            background: #7C3AED;
            color: #FFFFFF;
            border-color: #C4B5FD;
        }
        [data-testid="stPlotlyChart"],
        [data-testid="stImage"],
        [data-testid="stDataFrame"] {
            border: 1px solid #302342;
            border-radius: 12px;
        }
        [data-testid="stAlert"] { border-radius: 10px; }
        hr { border-color: #302342; }
        .dashboard-footer {
            border-top: 1px solid #302342;
            margin-top: 35px;
            padding-top: 16px;
            color: #A99ABD;
            font-size: 12px;
            text-align: center;
        }
        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] { padding: 1rem; }
            h1 { font-size: 1.65rem !important; }
            [data-testid="stMetricValue"] { font-size: 22px !important; }
        }
        
        
        /* ===== PROFESSIONAL SIDEBAR ===== */
        overflow-y: hidden;
        [data-testid="stSidebar"] {
            background: linear-gradient(
               180deg,
               #10091D 0%,
               #190D2B 55%,
               #0C0714 100%
            );
            border-right: 1px solid #493267;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.4rem;
            padding-bottom: 0.2rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #C4B5FD;
        }

        /* Brand */
        .sidebar-brand {
            padding: 10px 12px;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #291447, #171023);
            border: 1px solid #56377C;
            border-radius: 11px;
        }

        .sidebar-brand h2 {
            color: #FFFFFF !important;
            font-size: 17px !important;
            margin: 0;
        }

        .sidebar-brand p {
            color: #A78BFA !important;
            font-size: 9px;
            letter-spacing: 1.2px;
            margin: 4px 0 0;
        }

        /* Section headings */
        .sidebar-section {
            color: #8B79A8;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin: 10px 0 6px;
        }

        /* Navigation */
        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 5px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: #1A1028;
            border: 1px solid #34234A;
            border-radius: 8px;
            padding: 6px 10px;
            min-height: 0;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: #302047;
            border-color: #8B5CF6;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(110deg, #54269A, #30164F);
            border: 1px solid #A78BFA;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p {
            color: #F5F3FF !important;
            font-size: 12px;
            font-weight: 600;
            margin: 0;
        }

        /* System status */
        .sidebar-status {
            background: #171023;
            border: 1px solid #493267;
            border-radius: 10px;
            padding: 9px 11px;
            margin-top: 10px;
        }

        .sidebar-status-title {
            color: #A78BFA;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        .sidebar-status-value {
            color: #FFFFFF;
            font-size: 11px;
            font-weight: 600;
            margin-top: 3px;
        }

        .sidebar-status hr {
            margin: 6px 0;
        }

        .sidebar-footer {
            color: #847493;
            font-size: 9px;
            text-align: center;
            margin-top: 10px;
        }

        /* ===== PROFESSIONAL MAIN AREA ===== */

        [data-testid="stMainBlockContainer"] {
           max-width: 1550px;
           padding-left: 2rem;
           padding-right: 2rem;
        }

        [data-testid="stMetric"] {
           background: linear-gradient(145deg, #1D1230, #110B1C);
           border: 1px solid #493267;
           border-left: 3px solid #8B5CF6;
           border-radius: 13px;
           padding: 18px;
           box-shadow: 0 5px 18px rgba(109, 40, 217, 0.10);
           transition: transform 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
           transform: translateY(-3px);
           border-color: #A78BFA;
        }

        .main-card {
           background: linear-gradient(135deg, #211333, #110B1C);
           border: 1px solid #493267;
           border-radius: 15px;
           padding: 22px;
        }

        .hero-side-card {
           background: linear-gradient(145deg, #291642, #140C20);
           border: 1px solid #7651A5;
           border-radius: 15px;
           padding: 22px;
           min-height: 220px;
           box-shadow: 0 8px 25px rgba(109, 40, 217, 0.15);
        }

        .hero-side-label {
           color: #A78BFA;
           font-size: 10px;
           font-weight: 700;
           letter-spacing: 2px;
        }

        .hero-side-title {
           color: #FFFFFF;
           font-size: 21px;
           font-weight: 750;
           margin-top: 17px;
        }

        .hero-side-text {
           color: #C4B5FD;
           font-size: 12px;
           line-height: 1.8;
           margin-top: 10px;
        }

        .status-indicator {
           color: #86EFAC;
           font-size: 12px;
           font-weight: 600;
           margin-top: 18px;
        }
        
        /* Sidebar: fit content within screen height */
        section[data-testid="stSidebar"] > div {
            height: 100vh;
            overflow-y: auto;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        /* Reduce sidebar vertical spacing */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        /* Compact sidebar headings */
           section[data-testid="stSidebar"] h1,
           section[data-testid="stSidebar"] h2,
           section[data-testid="stSidebar"] h3 {
           margin-top: 0.3rem;
           margin-bottom: 0.3rem;
        }

        /* Compact sidebar radio menu */
           section[data-testid="stSidebar"] div[role="radiogroup"] {
           gap: 4px;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
           padding: 5px 8px;
           margin-bottom: 2px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def style_plotly_figure(fig, height=380):
    """Apply a consistent dark-purple style to a Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#171023",
        plot_bgcolor="#171023",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#E9DFFF", size=12),
        title_font=dict(size=16, color="#FFFFFF"),
        height=height,
        margin=dict(l=20, r=20, t=60, b=35),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#E9DFFF")),
    )
    fig.update_xaxes(gridcolor="#38264F", zerolinecolor="#493267")
    fig.update_yaxes(gridcolor="#38264F", zerolinecolor="#493267")
    return fig

def render_sidebar(total, fraud_rate):
    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-brand">
                <h2>◈ FRAUD AI</h2>
                <p>INTELLIGENCE PLATFORM</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section">WORKSPACE</div>', unsafe_allow_html=True
        )

        selected = st.radio(
            "Navigation",
            [
                "📊 Analytics",
                "🧪 Model Evaluation",
                "🔎 Predict Transaction",
                "📁 Batch Fraud Detection",
                "🗂️ Explore Data",
            ],
            label_visibility="collapsed",
            key="dashboard_navigation",
        )

        st.markdown(
            '<div class="sidebar-section">SYSTEM STATUS</div>', unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="sidebar-status">
                <div class="sidebar-status-title">
                    MODEL STATUS
                </div>
                <div class="sidebar-status-value">
                    ● Loaded Successfully
                </div>
                <hr style="border-color:#493267">
                <div class="sidebar-status-title">
                    DATASET RECORDS
                </div>
                <div class="sidebar-status-value">
                    {total:,} Transactions
                </div>
                <hr style="border-color:#493267">
                <div class="sidebar-status-title">
                    LABELLED FRAUD RATE
                </div>
                <div class="sidebar-status-value">
                    {fraud_rate:.2f}%
                </div>
            </div>

            <div class="sidebar-footer">
                FINANCIAL FRAUD INTELLIGENCE<br>
                Version 1.0.0 · ML Dashboard
            </div>
        """,
            unsafe_allow_html=True,
        )

    return selected
