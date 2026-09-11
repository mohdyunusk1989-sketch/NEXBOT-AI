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

# ====================== YOUR TRC20 WALLET ======================
TRC20_WALLET = "TYourWalletAddressHere"

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

def generate_referral_code():
    return "NEXBOT" + "".join(random.choices(string.digits, k=4))

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
            st.warning("Your membership is not active. Please go to Membership page and complete payment.")

    # ====================== MEMBERSHIP ======================
    elif page == "💎 Membership":
        st.markdown("## 💎 Membership")
        st.info(f"Membership Fee: **{MEMBERSHIP_FEE} USDT (TRC20)**")

        if user.get("membership"):
            st.success("Your membership is already Active!")
        else:
            st.markdown("### Payment Instructions")
            st.write(f"1. Send **{MEMBERSHIP_FEE} USDT (TRC20)** to this address:")
            st.code(TRC20_WALLET)
            st.write("2. Copy the Transaction ID")
            st.write("3. Submit the form below")
            st.write("4. Wait for Owner to verify and activate")

            st.divider()
            st.markdown("### Submit Payment Details")
            tx_id = st.text_input("Transaction ID / Hash")
            note = st.text_input("Any Note (Optional)")

            if st.button("Submit Membership Request", type="primary", use_container_width=True):
                if not tx_id:
                    st.error("Please enter Transaction ID")
                else:
                    st.session_state.pending_memberships.append({
                        "name": user["name"],
                        "mobile": user["mobile"],
                        "tx_id": tx_id,
                        "note": note,
                        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "status": "Pending"
                    })
                    st.success("Request submitted successfully! Please wait for activation.")
                    st.balloons()

    # ====================== TRADING CORE ======================
    elif page == "🤖 Trading Core":
        if not user.get("membership"):
            st.warning("Please activate Membership first.")
        else:
            st.markdown("## 🤖 Trading Core")
            if client:
                cols = st.columns(4)
                for i, sym in enumerate(["SOLUSDT", "BTCUSDT", "ETHUSDT", "BNBUSDT"]):
                    price = get_price(client, sym)
                    cols[i].metric(sym.replace("USDT", "/USDT"), f"${price:,.2f}" if price else "—")

            c1, c2, c3 = st.columns(3)
            capital = c1.number_input("Capital (USDT)", value=30.0)
            target = c2.number_input("Target %", value=0.7)
            down = c3.number_input("Down %", value=1.0)

            profit = capital * (target / 100)
            st.metric("Expected Profit", f"{profit:.4f} USDT")

            if st.button("Launch Strategy", type="primary"):
                st.session_state.owner_income += profit * 0.05
                st.session_state.total_profit += profit * 0.95
                st.success(f"Strategy Launched! Profit: {profit:.4f} USDT")

    # ====================== SMART GRID ======================
    elif page == "🎛️ Smart Grid Pro":
        if not user.get("membership"):
            st.warning("Please activate Membership first.")
        else:
            st.markdown("## 🎛️ Smart Grid Pro")
            st.session_state.grid_running = st.toggle("Grid Running", value=st.session_state.grid_running)
            st.session_state.auto_compound = st.toggle("Auto Compound", value=st.session_state.auto_compound)

            for i in range(10):
                c1, c2, c3 = st.columns(3)
                c1.number_input(f"Level {i+1} USDT", value=10.0, key=f"u{i}")
                c2.number_input(f"Target %", value=0.7, key=f"t{i}")
                c3.number_input(f"Down %", value=1.0, key=f"d{i}")

            if st.button("Save Grid"):
                st.success("Grid Saved!")

    # ====================== DUAL SESSION ======================
    elif page == "⏰ Dual Session":
        if not user.get("membership"):
            st.warning("Please activate Membership first.")
        else:
            st.markdown("## ⏰ Dual Session Hunter")
            st.write("Session 1: 12:00 AM | Session 2: 1:00 PM")
            st.toggle("Activate Session 1")
            st.toggle("Activate Session 2")
            if st.button("Save Sessions"):
                st.success("Saved!")

    # ====================== REFERRAL ======================
    elif page == "👥 Referral + Share":
        st.markdown("## 👥 Referral + Share")
        st.success(f"Your Referral Code: `{user['referral_code']}`")

        msg = f"""🚀 NexBot AI

I am using NexBot AI.

Open App: {LIVE_LINK}

My Referral Code: {user['referral_code']}

Join now!"""
        url = "https://wa.me/?text=" + urllib.parse.quote(msg)
        st.markdown(f'<a href="{url}" target="_blank"><button style="background:#25D366;color:white;padding:14px;border:none;border-radius:10px;width:100%;font-weight:bold;">Share on WhatsApp</button></a>', unsafe_allow_html=True)

    # ====================== OWNER PANEL ======================
    elif page == "👑 Owner Panel":
        st.markdown("## 👑 Owner Panel")
        pin = st.text_input("Owner Password", type="password")
        if pin == OWNER_PIN:
            st.success("Access Granted")

            c1, c2, c3 = st.columns(3)
            c1.metric("Owner Vault", f"{st.session_state.owner_income:.2f} USDT")
            c2.metric("Total Users", len(st.session_state.users))
            pending_count = len([x for x in st.session_state.pending_memberships if x["status"] == "Pending"])
            c3.metric("Pending Requests", pending_count)

            st.divider()
            st.markdown("### Pending Membership Requests")

            if st.session_state.pending_memberships:
                for i, req in enumerate(st.session_state.pending_memberships):
                    if req["status"] == "Pending":
                        with st.expander(f"{req['name']} | {req['mobile']} | {req['time']}"):
                            st.write(f"Transaction ID: `{req['tx_id']}`")
                            st.write(f"Note: {req['note']}")
                            if st.button(f"Activate {req['name']}", key=f"act_{i}"):
                                if req["mobile"] in st.session_state.users:
                                    st.session_state.users[req["mobile"]]["membership"] = True
                                req["status"] = "Activated"
                                st.session_state.owner_income += 20
                                st.success(f"{req['name']} Activated Successfully!")
                                st.rerun()
            else:
                st.info("No pending requests")

            st.divider()
            st.markdown("### All Registered Users")
            for mobile, data in st.session_state.users.items():
                status = "Active" if data.get("membership") else "Inactive"
                st.write(f"{data['name']} | {mobile} | {status} | Code: {data['referral_code']}")
        elif pin:
            st.error("Wrong Password")
