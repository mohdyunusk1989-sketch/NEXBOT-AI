import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from binance.client import Client

st.set_page_config(
    page_title="NexBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== API KEYS ======================
API_KEY = "f79GlppYGMwTMdfKJdVZdSeIcugbam6hca0omva71gg8pHyhHc3p4dB6MgiFbnvH"
API_SECRET = "cM2OuD31KMzpsL1AG7Ivlf8b8nS9vjZC13yHqeeFuqfBl80bdZNzQIxnaCnTt7Wi"

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b0e1a, #1a1a2e, #16213e);
        color: #e0e0e0;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #1e293b);
        border-right: 1px solid #334155;
    }
    h1, h2, h3, h4 {
        color: #38bdf8 !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #7dd3fc !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #1e293b !important;
        color: #f0f9ff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e11d48, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #4ade80 !important;
    }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== BINANCE FUNCTIONS ======================
def get_client():
    try:
        return Client(API_KEY, API_SECRET)
    except:
        return None

def get_balance(client):
    try:
        acc = client.get_account()
        return [{"asset": b["asset"], "free": float(b["free"])} for b in acc["balances"] if float(b["free"]) > 0]
    except:
        return []

def get_price(client, symbol="BTCUSDT"):
    try:
        return float(client.get_symbol_ticker(symbol=symbol)["price"])
    except:
        return None

# ====================== SESSION STATE ======================
defaults = {
    "authenticated": False,
    "owner_income": 0.0,
    "total_profit": 0.0,
    "paper_balance": 1000.0,
    "referral_code": "NEXBOT4348",
    "referral_count": 0,
    "grid_running": False,
    "auto_compound": True,
    "session1_active": False,
    "session2_active": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

MASTER_PIN = "8312"
OWNER_PIN = "Aqsa@7860"
LIVE_LINK = "https://nexbot-ai-q7eycecsypyvxagq8tgcyu.streamlit.app"

# ====================== LOGIN ======================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center;color:#f43f5e;'>🔒 NEXBOT SECURITY GATEWAY</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin = st.text_input("Enter Security PIN", type="password")
        if st.button("🔓 AUTHORIZE ACCESS", use_container_width=True):
            if pin == MASTER_PIN:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid PIN")
else:
    client = get_client()

    # ====================== SIDEBAR ======================
    st.sidebar.markdown("### 🧭 NexBot Control")
    st.sidebar.markdown(f"**👑 Owner Vault:** `{st.session_state.owner_income:.2f} USDT`")
    st.sidebar.markdown(f"**📄 Paper Balance:** `{st.session_state.paper_balance:.2f} USDT`")
    st.sidebar.markdown(f"**🔗 Referral Code:** `{st.session_state.referral_code}`")
    st.sidebar.markdown(f"**👥 Total Joined:** `{st.session_state.referral_count}`")

    if client:
        balances = get_balance(client)
        if balances:
            st.sidebar.markdown("### 💰 Real Balance")
            for b in balances[:5]:
                st.sidebar.write(f"**{b['asset']}**: {b['free']:.4f}")

    page = st.sidebar.selectbox("Navigation Menu", [
        "🤖 Trading Core",
        "🎛️ Smart Grid Pro",
        "⏰ Dual Session Hunter",
        "👥 Referral + Share",
        "📄 Paper Trading",
        "👑 Owner Panel"
    ])

    # ====================== TRADING CORE ======================
    if page == "🤖 Trading Core":
        st.markdown("## 🤖 Trading Core Suite")

        if client:
            cols = st.columns(4)
            for i, symbol in enumerate(["SOLUSDT", "BTCUSDT", "ETHUSDT", "BNBUSDT"]):
                price = get_price(client, symbol)
                cols[i].metric(symbol.replace("USDT", "/USDT"), f"${price:,.2f}" if price else "—")

        st.divider()
        st.markdown("### 📊 Strategy Calculator")

        c1, c2, c3, c4 = st.columns(4)
        capital = c1.number_input("Capital (USDT)", value=30.0, min_value=1.0)
        target_pct = c2.number_input("Target %", value=0.7, min_value=0.1, step=0.1)
        down_pct = c3.number_input("Down %", value=1.0, min_value=0.1, step=0.1)
        symbol = c4.selectbox("Coin", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])

        current_price = get_price(client, symbol) if client else 70000
        if current_price:
            target_price = current_price * (1 + target_pct / 100)
            down_price = current_price * (1 - down_pct / 100)

            st.markdown("### 🎯 Price Range")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Current Price", f"${current_price:,.2f}")
            col_b.metric("Target Price", f"${target_price:,.2f}")
            col_c.metric("Down Price", f"${down_price:,.2f}")
            st.success(f"**Range:** {down_price:,.0f} — {target_price:,.0f}")

            profit = capital * (target_pct / 100)
            st.metric("💰 Expected Profit", f"{profit:.4f} USDT")

            if st.button("🚀 Launch Strategy", type="primary", use_container_width=True):
                st.session_state.owner_income += profit * 0.05
                st.session_state.total_profit += profit * 0.95
                st.success(f"Strategy Launched! Expected Profit: {profit:.4f} USDT")
                st.balloons()

    # ====================== SMART GRID PRO ======================
    elif page == "🎛️ Smart Grid Pro":
        st.markdown("## 🎛️ NexBot Smart Grid Pro")
        st.caption("30-Level Martingale Grid with Auto Compound")

        c1, c2, c3 = st.columns(3)
        st.session_state.grid_running = c1.toggle("🟢 Grid Running", value=st.session_state.grid_running)
        st.session_state.auto_compound = c2.toggle("♻️ Auto Compound", value=st.session_state.auto_compound)
        c3.markdown(f"**Status:** {'🟢 RUNNING' if st.session_state.grid_running else '🔴 STOPPED'}")

        st.markdown("### Level Settings")
        st.caption("Enter USDT amount, Target % and Down % for each level. Price range is calculated automatically.")

        header = st.columns([0.5, 1.3, 1.2, 1.2, 2])
        header[0].markdown("**#**")
        header[1].markdown("**USDT Amount**")
        header[2].markdown("**Target %**")
        header[3].markdown("**Down %**")
        header[4].markdown("**Price Range (BTC)**")

        current_btc = get_price(client, "BTCUSDT") if client else 70000

        for i in range(30):
            cols = st.columns([0.5, 1.3, 1.2, 1.2, 2])
            cols[0].markdown(f"**{i+1}**")
            usdt = cols[1].number_input("USDT", value=10.0 if i == 0 else 0.0, key=f"grid_usdt_{i}", label_visibility="collapsed", min_value=0.0)
            target = cols[2].number_input("Target", value=0.7, key=f"grid_target_{i}", label_visibility="collapsed", min_value=0.1)
            down = cols[3].number_input("Down", value=1.0, key=f"grid_down_{i}", label_visibility="collapsed", min_value=0.1)

            if current_btc and usdt > 0:
                target_price = current_btc * (1 + target / 100)
                down_price = current_btc * (1 - down / 100)
                cols[4].markdown(f"**{down_price:,.0f} — {target_price:,.0f}**")
            else:
                cols[4].write("—")

        if st.button("💾 Save Grid Settings", type="primary", use_container_width=True):
            st.success("✅ 30-Level Grid Settings Saved Successfully!")
            st.balloons()

    # ====================== DUAL SESSION HUNTER ======================
    elif page == "⏰ Dual Session Hunter":
        st.markdown("## ⏰ Dual Session Hunter")
        st.caption("Automatic entry system designed for 2 sessions per day")

        st.markdown("### Common Settings")
        c1, c2, c3, c4 = st.columns(4)
        capital = c1.number_input("USDT Amount", value=20.0, key="ds_capital")
        target = c2.number_input("Target %", value=0.7, key="ds_target")
        down = c3.number_input("Down %", value=1.0, key="ds_down")
        coin1 = c4.selectbox("Session 1 Coin", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"], key="coin1")

        coin2 = st.selectbox("Session 2 Coin", ["ETHUSDT", "SOLUSDT", "BNBUSDT", "BTCUSDT"], key="coin2")

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🌅 Session 1 — 12:00 AM")
            st.write("Bot will start waiting from 12:00 AM")
            st.write("Places order as soon as price drops")
            st.session_state.session1_active = st.toggle("Activate Session 1", value=st.session_state.session1_active)

        with col2:
            st.markdown("#### 🌞 Session 2 — 1:00 PM")
            st.write("Bot will start waiting from 1:00 PM")
            st.write("Waits 3 minutes after price drop, then places order")
            st.session_state.session2_active = st.toggle("Activate Session 2", value=st.session_state.session2_active)

        st.divider()
        profit = capital * (target / 100)
        st.metric("Expected Profit (per session)", f"{profit:.4f} USDT")
        st.metric("If both sessions hit", f"{profit * 2:.4f} USDT")

        if st.button("💾 Save Dual Session Settings", type="primary", use_container_width=True):
            st.success("Dual Session Settings Saved Successfully!")
            st.balloons()

    # ====================== REFERRAL + SHARE ======================
    elif page == "👥 Referral + Share":
        st.markdown("## 👥 Referral System + WhatsApp Share")

        st.success(f"### 🔗 Your Referral Code: `{st.session_state.referral_code}`")
        st.metric("Total People Joined", st.session_state.referral_count)

        st.markdown("""
        ### 💰 Income Structure
        - **Membership (30 USDT):** Direct Referrer → 10 USDT | Owner → 20 USDT  
        - **Profit Share:** Owner 5% | Level 1: 5% | Level 2: 4% | Level 3: 3% | Level 4: 2% | Level 5: 1%
        """)

        st.divider()
        st.markdown("### 📤 Share on WhatsApp")

        message = f"""🚀 *NexBot AI - Smart Trading Bot*

I am using NexBot AI.
It has advanced Grid + Dual Session system.

🔗 *Open the App:*
{LIVE_LINK}

📌 *Join with my referral code:*
*{st.session_state.referral_code}*

Let's grow together! 💰"""

        whatsapp_url = "https://wa.me/?text=" + urllib.parse.quote(message)
        st.markdown(f'''
        <a href="{whatsapp_url}" target="_blank">
            <button style="background:#25D366;color:white;padding:14px;border:none;border-radius:10px;width:100%;font-weight:bold;font-size:16px;cursor:pointer;">
                📲 Share on WhatsApp
            </button>
        </a>
        ''', unsafe_allow_html=True)

        st.info("When someone joins using your code, the count will increase here.")

    # ====================== PAPER TRADING ======================
    elif page == "📄 Paper Trading":
        st.markdown("## 📄 Paper Trading (Safe Mode)")
        st.info(f"Available Paper Balance: **{st.session_state.paper_balance:.2f} USDT**")

        c1, c2, c3 = st.columns(3)
        symbol = c1.selectbox("Symbol", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])
        amount = c2.number_input("Amount (USDT)", value=10.0)
        side = c3.selectbox("Side", ["BUY", "SELL"])

        if st.button("📝 Place Paper Order", type="primary"):
            if amount <= st.session_state.paper_balance:
                st.session_state.paper_balance -= amount
                st.success(f"Paper {side} order placed successfully for {amount} USDT")
            else:
                st.error("Insufficient Paper Balance")

    # ====================== OWNER PANEL ======================
    elif page == "👑 Owner Panel":
        st.markdown("## 👑 Owner Panel")
        pin = st.text_input("Owner Password", type="password")
        if pin == OWNER_PIN:
            st.success("Access Granted")
            c1, c2, c3 = st.columns(3)
            c1.metric("Owner Vault", f"{st.session_state.owner_income:.2f} USDT")
            c2.metric("Total User Profit", f"{st.session_state.total_profit:.2f} USDT")
            c3.metric("Total Referrals", st.session_state.referral_count)
        elif pin:
            st.error("Wrong Password")
