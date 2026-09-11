import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from binance.client import Client
import random
import string

st.set_page_config(page_title="NexBot AI", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# ====================== API KEYS ======================
API_KEY = "f79GlppYGMwTMdfKJdVZdSeIcugbam6hca0omva71gg8pHyhHc3p4dB6MgiFbnvH"
API_SECRET = "cM2OuD31KMzpsL1AG7Ivlf8b8nS9vjZC13yHqeeFuqfBl80bdZNzQIxnaCnTt7Wi"

# ====================== YOUR TRC20 WALLET (Change this later) ======================
TRC20_WALLET = "TYourWalletAddressHere"   # <-- Yahan apna TRC20 address daalna

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0b0e1a, #1a1a2e, #16213e); color: #e0e0e0; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a, #1e293b); border-right: 1px solid #334155; }
    h1, h2, h3, h4 { color: #38bdf8 !important; }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #7dd3fc !important; font-weight: 600 !important; font-size: 14px !important;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #1e293b !important; color: #f0f9ff !important;
        border: 1px solid #38bdf8 !important; border-radius: 8px !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #e11d48, #7c3aed) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] { color: #4ade80 !important; }
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== BINANCE ======================
def get_client():
    try: return Client(API_KEY, API_SECRET)
    except: return None

def get_balance(client):
    try:
        acc = client.get_account()
        return [{"asset": b["asset"], "free": float(b["free"])} for b in acc["balances"] if float(b["free"]) > 0]
    except: return []

def get_price(client, symbol="BTCUSDT"):
    try: return float(client.get_symbol_ticker(symbol=symbol)["price"])
    except: return None

def generate_referral_code():
    return "NEXBOT" + ''.join(random.choices(string.digits, k=4))

# ====================== SESSION STATE ======================
if "users" not in st.session_state:
    st.session_state.users = {}

if "pending_memberships" not in st.session_state:
    st.session_state.pending_memberships = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

defaults = {
    "owner_income": 0.0,
    "total_profit": 0.0,
    "paper_balance": 1000.0,
    "grid_running": False,
    "auto_compound": True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

OWNER_PIN = "Aqsa@7860"
LIVE_LINK = "https://nexbot-ai-q7eycecsypyvxagq8tgcyu.streamlit.app"
MEMBERSHIP_FEE = 30

# ====================== LOGIN / REGISTER ======================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;color:#38bdf8;'>🤖 NexBot AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#94a3b8;'>Smart Trading System</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        mobile = st.text_input("Mobile Number", key="login_mobile")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            if mobile in st.session_state.users and st.session_state.users[mobile]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = st.session_state.users[mobile]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid Mobile or Password")

    with tab2:
        st.subheader("Create New Account")
        name = st.text_input("Full Name")
        mobile_reg = st.text_input("Mobile Number", key="reg_mobile")
        ref_code = st.text_input("Referral Code (Optional)")
        password_reg = st.text_input("Create Password", type="password", key="reg_pass")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Register", use_container_width=True):
            if not name or not mobile_reg or not password_reg:
                st.error("Please fill all required fields")
            elif password_reg != confirm:
                st.error("Passwords do not match")
            elif mobile_reg in st.session_state.users:
                st.error("Mobile already registered")
            else:
                new_code = generate_referral_code()
                st.session_state.users[mobile_reg] = {
                    "name": name,
                    "mobile": mobile_reg,
                    "password": password_reg,
                    "referral_code": new_code,
                    "used_referral": ref_code,
                    "membership": False,
                    "joined": datetime.now().strftime("%d-%m-%Y %H:%M")
                }
                st.success(f"Registration successful! Your Referral Code is: **{new_code}**")
                st.balloons()

else:
    user = st.session_state.current_user
    client = get_client()

    # ====================== SIDEBAR ======================
    st.sidebar.markdown(f"### 👋 {user['name']}")
    st.sidebar.markdown(f"**Mobile:** {user['mobile']}")
    st.sidebar.markdown(f"**Referral Code:** `{user['referral_code']}`")
    st.sidebar.markdown(f"**Membership:** {'✅ Active' if user.get('membership') else '❌ Inactive'}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    page = st.sidebar.selectbox("Menu", [
        "🏠 Dashboard",
        "💎 Membership",
        "🤖 Trading Core",
        "🎛️ Smart Grid Pro",
        "⏰ Dual Session",
        "👥 Referral + Share",
        "👑 Owner Panel"
    ])

    # ====================== DASHBOARD ======================
    if page == "🏠 Dashboard":
        st.markdown("## 🏠 Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Membership", "Active ✅" if user.get("membership") else "Inactive ❌")
        c2.metric("Your Referral Code", user["referral_code"])
        c3.metric("Paper Balance", f"{st.session_state.paper_balance:.2f} USDT")

        if not user.get("membership"):
            st.warning("⚠️ Your membership is not active. Please go to **Membership** page and complete payment.")

    # ====================== MEMBERSHIP ======================
    elif page == "💎 Membership":
        st.markdown("## 💎 Membership")
        st.info(f"**Membership Fee: {MEMBERSHIP_FEE} USDT (TRC20)**")

        if user.get("membership"):
            st.success("✅ Your membership is already Active!")
        else:
            st.markdown("### Payment Instructions")
            st.markdown(f"""
            1. Send **{MEMBERSHIP_FEE} USDT (TRC20)** to this address:
