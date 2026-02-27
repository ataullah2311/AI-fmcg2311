import streamlit as st
import plotly.graph_objects as go
from groq import Groq
from dotenv import load_dotenv
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch



# Initialize the Groq client
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="AI FMCG Strategy Simulator",
    page_icon="📊",
    layout="wide"
)

# ==============================
# DARK CORPORATE THEME
# ==============================

st.markdown("""
<style>

/* Clean Executive Dark Background */
.stApp {
    background-color: #111827;   /* Deep neutral dark */
    color: #F3F4F6;              /* Soft white text */
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background-color: #1F2937;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #374151;
}

/* Buttons */
.stButton>button {
    background-color: #3B82F6;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #2563EB;
    color: white;
}

/* Download Button */
.stDownloadButton>button {
    background-color: #10B981;
    color: white;
}

.stDownloadButton>button:hover {
    background-color: #059669;
}

/* Success (AI Report) Box Fix */
div[data-testid="stAlert"] {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border-radius: 10px;
}

/* Inputs */
.stNumberInput input {
    background-color: #1F2937;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SIMPLE LOGIN SYSTEM
# ==============================

def login():
    st.title("🔐 AI Strategy Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ==============================
# LOAD GROQ
# ==============================

#load_dotenv()
#client = Groq(api_key=os.getenv("GROQ_API_KEY"))
groq_api_key = st.secrets["GROQ_API_KEY"]

# ==============================
# TITLE
# ==============================

st.title("📊 AI FMCG Strategic War Simulator")
st.markdown("### Enterprise Decision Intelligence Dashboard")

# ==============================
# INPUT SECTION
# ==============================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏭 Company Inputs")
    current_price = st.number_input("Current Price", value=100)
    cost_per_unit = st.number_input("Cost Per Unit", value=60)
    current_quantity = st.number_input("Monthly Sales Quantity", value=10000)

with col2:
    st.subheader("⚔ Strategy Controls")
    price_change = st.slider("Change Price (%)", -50, 50, 0)
    marketing_increase = st.slider("Increase Marketing Budget (%)", 0, 100, 0)

st.markdown("---")

# ==============================
# RUN SIMULATION
# ==============================

if st.button("🚀 Run Strategic Simulation"):

    elasticity = -1.5

    demand_price = elasticity * (price_change / 100)
    demand_marketing = (marketing_increase / 10) * 0.03
    total_demand = demand_price + demand_marketing

    new_quantity = current_quantity * (1 + total_demand)
    new_price = current_price * (1 + price_change / 100)

    revenue = new_price * new_quantity
    profit = (new_price - cost_per_unit) * new_quantity

    current_revenue = current_price * current_quantity
    current_profit = (current_price - cost_per_unit) * current_quantity

    # ==============================
    # KPI CARDS
    # ==============================

    st.markdown("""
<div style="
    background: linear-gradient(90deg, #2563EB, #1E3A8A);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
">
    <h2 style="color:white; margin:0;">
        📈 Performance Overview
    </h2>
</div>
""", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("New Price", round(new_price,2))
    k2.metric("New Quantity", round(new_quantity,2))
    k3.metric("Projected Revenue", round(revenue,2),
              delta=round(revenue-current_revenue,2))
    k4.metric("Projected Profit", round(profit,2),
              delta=round(profit-current_profit,2))

    # ==============================
    # REVENUE GRAPH
    # ==============================

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Current Revenue", "Projected Revenue"],
        y=[current_revenue, revenue],
        text=[round(current_revenue,2), round(revenue,2)],
        textposition="auto"
    ))
    fig.update_layout(title="Revenue Impact Analysis", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # PROFIT GRAPH
    # ==============================

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=["Current Profit", "Projected Profit"],
        y=[current_profit, profit],
        text=[round(current_profit,2), round(profit,2)],
        textposition="auto"
    ))
    fig2.update_layout(title="Profit Impact Analysis", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    # ==============================
    # AI STRATEGIC INSIGHT
    # ==============================

    st.markdown("## 🤖 AI Executive Strategic Insight")

    prompt = f"""
    Company changed price by {price_change}% 
    and marketing by {marketing_increase}%.
    Projected revenue: {round(revenue,2)}
    Projected profit: {round(profit,2)}.

    Provide:
    - Strategic analysis
    - Risk factors
    - Competitive advice
    - Final recommendation
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_text = response.choices[0].message.content
    st.success(ai_text)

    st.session_state.revenue = revenue
    st.session_state.profit = profit
    st.session_state.price_change = price_change
    st.session_state.marketing_increase = marketing_increase
    st.session_state.ai_text = ai_text

    # ==============================
# PDF DOWNLOAD OUTSIDE BUTTON
# ==============================

if "ai_text" in st.session_state:

    if st.button("📄 Generate CEO PDF Report"):

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch

        file_path = "CEO_Strategy_Report.pdf"
        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("AI FMCG Strategy Report", styles['Title']))
        elements.append(Spacer(1, 0.5 * inch))

        elements.append(Paragraph(f"Price Change: {st.session_state.price_change}%", styles['Normal']))
        elements.append(Paragraph(f"Marketing Increase: {st.session_state.marketing_increase}%", styles['Normal']))
        elements.append(Paragraph(f"Projected Revenue: {round(st.session_state.revenue,2)}", styles['Normal']))
        elements.append(Paragraph(f"Projected Profit: {round(st.session_state.profit,2)}", styles['Normal']))

        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("AI Strategic Recommendation:", styles['Heading2']))
        elements.append(Paragraph(st.session_state.ai_text, styles['Normal']))

        doc.build(elements)

        with open(file_path, "rb") as f:
            st.download_button(
                "⬇ Download CEO Report",
                f,
                file_name="CEO_Strategy_Report.pdf"
            )

# ==============================
# AI STRATEGY OPTIMIZER
# ==============================

st.markdown("---")
st.subheader("🤖 AI Strategy Optimizer")

if st.button("🔍 Find Most Profitable Strategy"):

    best_profit = 0
    best_price = 0
    best_marketing = 0

    for p in range(-20, 21, 5):
        for m in range(0, 51, 10):

            elasticity = -1.5
            demand_price = elasticity * (p / 100)
            demand_marketing = (m / 10) * 0.03
            total_demand = demand_price + demand_marketing

            test_quantity = current_quantity * (1 + total_demand)
            test_price = current_price * (1 + p / 100)

            test_profit = (test_price - cost_per_unit) * test_quantity

            if test_profit > best_profit:
                best_profit = test_profit
                best_price = p
                best_marketing = m

    st.success("🏆 Optimal Strategy Identified")
    st.write("Recommended Price Change:", best_price, "%")
    st.write("Recommended Marketing Increase:", best_marketing, "%")

    st.write("Expected Maximum Profit:", round(best_profit,2))

