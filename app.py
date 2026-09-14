import streamlit as st
import urllib.parse
from datetime import datetime
from binance.client import Client
import random
import string
from supabase import create_client, Client as SupabaseClient

st.set_page_config(page_title="NexBot AI", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# ====================== SUPABASE ======================
SUPABASE_URL = "https://uktmbjwcsqgdciwuprhp.supabase.co"
SUPABASE_KEY = "sb_publishable_SWlh8SwyNlRZBCtGDUkyeg_pfGlyJr1"
supabase: SupabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)

# ====================== BINANCE ======================
API_KEY = "f79GlppYGMwTMdfKJdVZdSeIcugbam6hca0omva71gg8pHyhHc3p4dB6MgiFbnvH"
API_SECRET = "cM2OuD31KMzpsL1AG7Ivlf8b8nS9vjZC13yHqeeFuqfBl80bdZNzQIxnaCnTt7Wi"

# ====================== TRC20 ======================
TRC20_WALLET = "TYourWalletAddressHere"

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0a0e17, #111827, #0f172a); color: #f1f5f9; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a, #1e293b); border-right: 1px solid #334155; }
    h1, h2, h3, h4 { color: #38bdf8 !important; }
    p, span, label, .stMarkdown { color: #e2e8f0 !important; }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #7dd3fc !important; font-weight: 600 !important; font-size: 14px !important;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #1e293b !important; color: #f8fafc !important;
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

# ====================== HELPERS ======================
def get_client():
    try: return Client(API_KEY, API_SECRET)
    except: return None

def get_price(client, symbol="BTCUSDT"):
    try: return float(client.get_symbol_ticker(symbol=symbol)["price"])
    except: return None

def generate_referral_code():
    return "NEXBOT" + "".join(random.choices(string.digits, k=4))

def get_user_by_mobile(mobile):
    try:
        res = supabase.table("users").select("*").eq("mobile", mobile).execute()
        return res.data[0] if res.data else None
    except: return None

def create_user(name, mobile, password, referral_code, used_referral):
    try:
        data = {
            "name": name, "mobile": mobile, "password": password,
            "referral_code": referral_code, "used_referral": used_referral,
            "membership": False, "joined": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        supabase.table("users").insert(data).execute()
        return True
    except: return False

def update_membership(mobile, status=True):
    try:
        supabase.table("users").update({"membership": status}).eq("mobile", mobile).execute()
        return True
    except: return False

def get_all_users():
    try:
        res = supabase.table("users").select("*").execute()
        return res.data
    except: return []

# ====================== SESSION ======================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "current_user" not in st.session_state: st.session_state.current_user = None
if "paper_balance" not in st.session_state: st.session_state.paper_balance = 1000.0
if "paper_trades" not in st.session_state: st.session_state.paper_trades = []
if "owner_income" not in st.session_state: st.session_state.owner_income = 0.0
if "grid_settings" not in st.session_state: st.session_state.grid_settings = {}
if "session_settings" not in st.session_state: st.session_state.session_settings = {}

OWNER_PIN = "Aqsa@7860"
LIVE_LINK = "https://nexbot-ai-q7eycecsypyvxagq8tgcyu.streamlit.app"
MEMBERSHIP_FEE = 30
OWNER_PROFIT_SHARE = 0.10

# ====================== LOGIN ======================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;color:#38bdf8;'>🤖 NexBot AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#94a3b8;'>Smart Trading System</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        st.subheader("Login")
        mobile = st.text_input("Mobile Number", key="login_mobile")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            user = get_user_by_mobile(mobile)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = user
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
            elif get_user_by_mobile(mobile_reg):
                st.error("Mobile already registered")
            else:
                new_code = generate_referral_code()
                if create_user(name, mobile_reg, password_reg, new_code, ref_code):
                    st.success(f"Registration successful! Your Referral Code: **{new_code}**")
                    st.balloons()

else:
    user = st.session_state.current_user
    fresh = get_user_by_mobile(user["mobile"])
    if fresh:
        user = fresh
        st.session_state.current_user = fresh
    client = get_client()

    # SIDEBAR
    st.sidebar.markdown(f"### 👋 {user['name']}")
    st.sidebar.markdown(f"**Mobile:** {user['mobile']}")
    st.sidebar.markdown(f"**Referral:** `{user['referral_code']}`")
    st.sidebar.markdown(f"**Membership:** {'✅ Active' if user.get('membership') else '❌ Inactive'}")
    st.sidebar.markdown(f"**Paper Balance:** `{st.session_state.paper_balance:.2f} USDT`")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    page = st.sidebar.selectbox("Menu", [
        "🏠 Dashboard", "💎 Membership", "🤖 Trading Core", "📄 Paper Trading",
        "🎛️ Smart Grid Pro", "⏰ Dual Session", "👥 Referral + Share", "👑 Owner Panel"
    ])

    # DASHBOARD
    if page == "🏠 Dashboard":
        st.markdown("## 🏠 Dashboard")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Membership", "Active ✅" if user.get("membership") else "Inactive ❌")
        c2.metric("Referral Code", user["referral_code"])
        c3.metric("Paper Balance", f"{st.session_state.paper_balance:.2f} USDT")
        c4.metric("Owner Share", "10%")
        if not user.get("membership"):
            st.warning("Membership inactive. Please activate from Membership page.")

    # MEMBERSHIP
    elif page == "💎 Membership":
        st.markdown("## 💎 Membership")
        st.info(f"Membership Fee: **{MEMBERSHIP_FEE} USDT (TRC20)**")
        if user.get("membership"):
            st.success("Your membership is Active!")
        else:
            st.write(f"Send **{MEMBERSHIP_FEE} USDT (TRC20)** to:")
            st.code(TRC20_WALLET)
            tx_id = st.text_input("Transaction ID")
            if st.button("Submit Request", type="primary"):
                if tx_id:
                    st.success("Request submitted! Wait for Owner activation.")
                else:
                    st.error("Enter Transaction ID")

    # TRADING CORE
    elif page == "🤖 Trading Core":
        if not user.get("membership"):
            st.warning("Activate Membership first.")
        else:
            st.markdown("## 🤖 Trading Core")
            if client:
                cols = st.columns(4)
                for i, sym in enumerate(["SOLUSDT", "BTCUSDT", "ETHUSDT", "BNBUSDT"]):
                    price = get_price(client, sym)
                    cols[i].metric(sym.replace("USDT","/USDT"), f"${price:,.2f}" if price else "—")
            c1, c2, c3 = st.columns(3)
            capital = c1.number_input("Capital (USDT)", value=30.0)
            target = c2.number_input("Target %", value=0.7)
            down = c3.number_input("Down %", value=1.0)
            profit = capital * (target/100)
            owner_share = profit * OWNER_PROFIT_SHARE
            st.metric("Gross Profit", f"{profit:.4f} USDT")
            st.metric("Owner Share (10%)", f"{owner_share:.4f} USDT")
            st.metric("Your Net Profit", f"{profit-owner_share:.4f} USDT")
            if st.button("Launch Strategy", type="primary"):
                st.session_state.owner_income += owner_share
                st.success("Strategy Launched!")
                st.balloons()

    # PAPER TRADING
    elif page == "📄 Paper Trading":
        st.markdown("## 📄 Paper Trading")
        st.info(f"Paper Balance: **{st.session_state.paper_balance:.2f} USDT**")
        c1, c2, c3, c4 = st.columns(4)
        symbol = c1.selectbox("Symbol", ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT"])
        amount = c2.number_input("Amount (USDT)", value=20.0, min_value=1.0)
        side = c3.selectbox("Side", ["BUY","SELL"])
        leverage = c4.number_input("Leverage (x)", value=1.0, min_value=0.5, max_value=20.0, step=0.5)
        if st.button("Place Paper Order", type="primary"):
            if amount > st.session_state.paper_balance:
                st.error("Insufficient balance")
            else:
                st.session_state.paper_balance -= amount
                st.session_state.paper_trades.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "symbol": symbol, "side": side, "amount": amount, "leverage": leverage
                })
                st.success(f"{side} {amount} USDT | {leverage}x")
        if st.session_state.paper_trades:
            st.divider()
            for t in reversed(st.session_state.paper_trades[-8:]):
                st.write(f"{t['time']} | {t['side']} | {t['symbol']} | {t['amount']} | {t['leverage']}x")

    # ====================== SMART GRID PRO (IMPROVED) ======================
    elif page == "🎛️ Smart Grid Pro":
        if not user.get("membership"):
            st.warning("Activate Membership first.")
        else:
            st.markdown("## 🎛️ Smart Grid Pro")
            st.caption("Strict Mode: Bot waits for Down % + Confirmation Bounce before entry")

            c1, c2, c3 = st.columns(3)
            grid_on = c1.toggle("Grid Running", value=False)
            auto_compound = c2.toggle("Auto Compound", value=True)
            mode = c3.selectbox("Mode", ["Strict", "Normal", "Aggressive"])

            st.divider()
            st.markdown("### Grid Levels (Max 8)")
            st.caption("Down % = Kitna girne pe wait | Confirmation = Upar bounce ke baad entry")

            levels = []
            for i in range(8):
                cols = st.columns(4)
                usdt = cols[0].number_input(f"L{i+1} USDT", value=10.0, key=f"gu{i}")
                target = cols[1].number_input(f"Target %", value=0.7, key=f"gt{i}")
                down = cols[2].number_input(f"Down %", value=0.5, key=f"gd{i}", help="User setting")
                conf = cols[3].number_input(f"Confirm %", value=0.2, key=f"gc{i}", help="Strict bounce")
                levels.append({"usdt": usdt, "target": target, "down": down, "confirm": conf})

            st.divider()
            st.markdown("### How Strict Mode Works")
            st.info("""
            1. Price girna start kare → Bot **intezaar** karega  
            2. User ka **Down %** hit ho → Bot still wait karega  
            3. Price thoda **uper bounce** kare (Confirm %) → Tab entry  
            4. Chhoti upar-neeche ignore hogi  
            """)

            if st.button("Save Grid Settings", type="primary", use_container_width=True):
                st.session_state.grid_settings = {
                    "running": grid_on,
                    "auto_compound": auto_compound,
                    "mode": mode,
                    "levels": levels
                }
                st.success(f"Grid Saved! Mode: {mode} | Levels: {len(levels)}")
                st.balloons()

    # ====================== DUAL SESSION (IMPROVED) ======================
    elif page == "⏰ Dual Session":
        if not user.get("membership"):
            st.warning("Activate Membership first.")
        else:
            st.markdown("## ⏰ Dual Session Hunter")
            st.caption("Strict Mode: Session time + Down % + Confirmation Bounce")

            st.markdown("### Session 1 (Night)")
            c1, c2, c3 = st.columns(3)
            s1_on = c1.toggle("Activate Session 1", value=False)
            s1_coin = c2.selectbox("Coin", ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT"], key="s1c")
            s1_time = c3.time_input("Start Time", value=datetime.strptime("00:00","%H:%M").time())

            c4, c5, c6 = st.columns(3)
            s1_usdt = c4.number_input("USDT", value=20.0, key="s1u")
            s1_down = c5.number_input("Down %", value=0.5, key="s1d")
            s1_conf = c6.number_input("Confirm %", value=0.2, key="s1f")

            st.divider()
            st.markdown("### Session 2 (Afternoon)")
            c1, c2, c3 = st.columns(3)
            s2_on = c1.toggle("Activate Session 2", value=False)
            s2_coin = c2.selectbox("Coin", ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT"], key="s2c")
            s2_time = c3.time_input("Start Time", value=datetime.strptime("13:00","%H:%M").time())

            c4, c5, c6 = st.columns(3)
            s2_usdt = c4.number_input("USDT", value=20.0, key="s2u")
            s2_down = c5.number_input("Down %", value=0.5, key="s2d")
            s2_conf = c6.number_input("Confirm %", value=0.2, key="s2f")

            st.divider()
            st.markdown("### How Dual Session Works (Strict)")
            st.info("""
            1. Session time start hote hi bot **watch** karega  
            2. Price Down % tak gire → Bot wait karega  
            3. Confirm % bounce aaye → Turant entry  
            4. Dono sessions alag-alag settings se chalenge  
            """)

            if st.button("Save Dual Session", type="primary", use_container_width=True):
                st.session_state.session_settings = {
                    "s1": {"on": s1_on, "coin": s1_coin, "time": str(s1_time), "usdt": s1_usdt, "down": s1_down, "confirm": s1_conf},
                    "s2": {"on": s2_on, "coin": s2_coin, "time": str(s2_time), "usdt": s2_usdt, "down": s2_down, "confirm": s2_conf}
                }
                st.success("Dual Session Settings Saved!")
                st.balloons()

    # REFERRAL
    elif page == "👥 Referral + Share":
        st.markdown("## 👥 Referral + Share")
        st.success(f"Your Referral Code: `{user['referral_code']}`")
        msg = f"🚀 NexBot AI\n\nOpen: {LIVE_LINK}\n\nMy Code: {user['referral_code']}\n\nJoin now!"
        url = "https://wa.me/?text=" + urllib.parse.quote(msg)
        st.markdown(f'<a href="{url}" target="_blank"><button style="background:#25D366;color:white;padding:14px;border:none;border-radius:10px;width:100%;font-weight:bold;">Share on WhatsApp</button></a>', unsafe_allow_html=True)

    # OWNER PANEL
    elif page == "👑 Owner Panel":
        st.markdown("## 👑 Owner Panel")
        pin = st.text_input("Owner Password", type="password")
        if pin == OWNER_PIN:
            st.success("Access Granted")
            users = get_all_users()
            c1, c2, c3 = st.columns(3)
            c1.metric("Owner Vault", f"{st.session_state.owner_income:.2f} USDT")
            c2.metric("Total Users", len(users))
            c3.metric("Active Members", len([u for u in users if u.get("membership")]))
            st.divider()
            st.markdown("### All Users")
            for u in users:
                status = "✅ Active" if u.get("membership") else "❌ Inactive"
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"**{u['name']}** | {u['mobile']} | {status} | `{u['referral_code']}`")
                with col2:
                    if not u.get("membership"):
                        if st.button("Activate", key=f"act_{u['mobile']}"):
                            if update_membership(u["mobile"], True):
                                st.session_state.owner_income += 20
                                st.success(f"{u['name']} Activated!")
                                st.rerun()
        elif pin:
            st.error("Wrong Password")
