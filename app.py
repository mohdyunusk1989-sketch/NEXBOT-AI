import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NexBot AI - Institutional Elite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== PREMIUM CSS ======================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
        border-right: 1px solid #00E5FF33;
    }
    h1, h2, h3, h4 {
        color: #00E5FF !important;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1e1e2f !important;
        color: #00FFCC !important;
        border: 1px solid #00E5FF55 !important;
        border-radius: 8px !important;
        text-align: center !important;
        font-weight: bold !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #FF1744, #D500F9) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #FF174488;
    }
    [data-testid="stMetricValue"] {
        color: #00E676 !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== DATA ======================
binance_all_coins = ["SOL/USDT", "BTC/USDT", "ETH/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT", "NEAR/USDT", "BNB/USDT"]

binance_live_hit_list = [
    {"coin": "🔥 SOL/USDT", "gain": "+12.45%", "status": "Strong Bullish 🚀"},
    {"coin": "🔥 NEAR/USDT", "gain": "+9.12%", "status": "Target Boundary Break ⚡"},
    {"coin": "🔥 DOGE/USDT", "gain": "+7.84%", "status": "High Volume Surge 📈"},
    {"coin": "🔥 BTC/USDT", "gain": "+4.21%", "status": "Steady Climb 📊"},
]

# ====================== SESSION STATE ======================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "owner_income" not in st.session_state:
    st.session_state.owner_income = 0.0
if "fuel_wallet" not in st.session_state:
    st.session_state.fuel_wallet = 10.0
if "total_profit" not in st.session_state:
    st.session_state.total_profit = 0.0
if "daily_profit" not in st.session_state:
    st.session_state.daily_profit = 0.0
if "binance_connected" not in st.session_state:
    st.session_state.binance_connected = False
if "profit_history" not in st.session_state:
    st.session_state.profit_history = []
if "royal_q_grid" not in st.session_state:
    st.session_state.royal_q_grid = [{"usdt": "", "target": "", "down": "", "stoploss": ""} for _ in range(30)]

MASTER_PIN = "8312"

# ====================== LOGIN ======================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#FF1744;'>🔒 NEXBOT SECURITY GATEWAY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Private Encrypted Node • Institutional Access Only</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin_input = st.text_input("Enter Security PIN", type="password", key="pin_gate")
        if st.button("🔓 AUTHORIZE ACCESS", use_container_width=True):
            if pin_input == MASTER_PIN:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid PIN • Access Denied")

else:
    # ====================== SIDEBAR ======================
    st.sidebar.markdown("### 🧭 Compass NexBot")
    st.sidebar.markdown(f"**👑 Owner Vault:** `{round(st.session_state.owner_income, 2)} USDT`")
    st.sidebar.markdown(f"**⛽ Fuel Wallet:** `{round(st.session_state.fuel_wallet, 2)} USDT`")
    
    app_mode = st.sidebar.selectbox(
        "Navigation Menu",
        ["🤖 Trading Core Suite", "📜 Membership Ledger", "🎛️ Royal Q Quant Settings", "🔗 Binance Connect"],
        key="nav_menu"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Mobile/PC pe Install karne ke liye browser menu se **Add to Home Screen** choose karo.")

    # ====================== PAGE 1: TRADING CORE ======================
    if app_mode == "🤖 Trading Core Suite":
        st.markdown("<h2 style='color:#00E5FF;'>🤖 NEXBOT AI • Institutional Elite</h2>", unsafe_allow_html=True)
        st.caption("Advanced Quant Calculator • Better than traditional grid bots")

        st.markdown("### 🔥 Live Coin Hit List")
        for item in binance_live_hit_list:
            st.markdown(f"**{item['coin']}** &nbsp;|&nbsp; <span style='color:#00E676'>{item['gain']}</span> &nbsp;|&nbsp; *{item['status']}*", unsafe_allow_html=True)

        st.divider()

        # Presets
        st.markdown("### ⚡ Quick Presets")
        p1, p2, p3 = st.columns(3)
        with p1:
            if st.button("🛡️ Safe Mode", use_container_width=True):
                st.session_state.preset_ratio = "0.4"
                st.session_state.preset_days = "365"
                st.rerun()
        with p2:
            if st.button("⚖️ Balanced Mode", use_container_width=True):
                st.session_state.preset_ratio = "0.7"
                st.session_state.preset_days = "180"
                st.rerun()
        with p3:
            if st.button("🔥 Aggressive Mode", use_container_width=True):
                st.session_state.preset_ratio = "1.2"
                st.session_state.preset_days = "90"
                st.rerun()

        default_ratio = st.session_state.get("preset_ratio", "0.5")
        default_days = st.session_state.get("preset_days", "365")

        st.markdown("### 📊 Strategy Parameters")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            usdt_val = st.text_input("Capital (USDT)", value="30", key="cap")
        with c2:
            days_input = st.text_input("Target Days", value=default_days, key="days")
        with c3:
            target_val = st.text_input("Daily Ratio %", value=default_ratio, key="ratio")
        with c4:
            coin_selected = st.selectbox("Crypto Token", binance_all_coins, key="coin")

        d1, d2, d3 = st.columns(3)
        with d1:
            price_from = st.text_input("Current Entry Price", value="4000", key="pfrom")
        with d2:
            price_to = st.text_input("Target Hit Price", value="5000", key="pto")
        with d3:
            profit_display = f"{round(st.session_state.daily_profit, 4)} USDT" if st.session_state.daily_profit > 0 else "0.0000 USDT"
            st.text_input("🎯 Target Profit Hit", value=profit_display, disabled=True, key="profit_display")

        compound_active = st.checkbox("♻️ Auto-Compound Growth", value=True)

        if st.button("🚀 ENTER & LAUNCH STRATEGY", type="primary", use_container_width=True):
            try:
                capital = float(usdt_val)
                ratio = float(target_val)
                days = int(days_input)

                daily_profit = capital * (ratio / 100)
                st.session_state.daily_profit = daily_profit

                owner_fee = daily_profit * 0.05
                st.session_state.owner_income += owner_fee
                st.session_state.total_profit += (daily_profit - owner_fee)
                st.session_state.fuel_wallet = max(0, st.session_state.fuel_wallet - daily_profit * 0.02)

                st.session_state.profit_history.append({
                    "capital": capital,
                    "ratio": ratio,
                    "daily": round(daily_profit, 4),
                    "coin": coin_selected
                })

                st.success(f"✅ Launched! Daily: **{round(daily_profit,4)} USDT** | Owner 5%: **{round(owner_fee,4)} USDT**")
                st.balloons()
                st.rerun()
            except:
                st.error("❌ Please enter valid numbers only")

        if st.session_state.daily_profit > 0:
            st.divider()
            st.markdown("### 📈 Live Results & Projections")

            capital = float(usdt_val) if usdt_val else 30
            ratio = float(target_val) if target_val else 0.5
            days = int(days_input) if days_input else 365

            realistic_monthly = ratio * 22

            if ratio <= 0.5:
                risk_level = "Low 🟢"
            elif ratio <= 0.9:
                risk_level = "Medium 🟡"
            else:
                risk_level = "High 🔴"

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Daily Profit", f"{round(st.session_state.daily_profit,4)} USDT")
            m2.metric("Realistic Monthly", f"{round(realistic_monthly,1)}%")
            m3.metric("Risk Level", risk_level)
            m4.metric("Your Net Profit", f"{round(st.session_state.total_profit,2)} USDT")

            if compound_active:
                projected = capital * ((1 + ratio/100) ** days)
            else:
                projected = capital + (capital * ratio/100 * days)

            st.markdown(f"#### 🔮 Projected Value after {days} days: **{round(projected,2)} USDT**")

            growth_data = []
            current = capital
            step = max(1, days // 10)
            for day in range(0, days + 1, step):
                growth_data.append({"Day": day, "Value": round(current, 2)})
                current = current * (1 + ratio/100) if compound_active else current + (capital * ratio/100)

            df = pd.DataFrame(growth_data)
            st.line_chart(df.set_index("Day"))

            st.warning("""
            ⚠️ **IMPORTANT DISCLAIMER**  
            - Yeh sirf calculation tool hai.  
            - Koi bhi guaranteed profit nahi hai.  
            - Crypto market bahut volatile hai.  
            - Past performance future results ki guarantee nahi hai.  
            - Sirf utna paise lagao jitna lose kar sakte ho.
            """)

        if st.session_state.profit_history:
            with st.expander("📜 Session Profit History"):
                for i, h in enumerate(reversed(st.session_state.profit_history[-10:]), 1):
                    st.write(f"**{i}.** {h['coin']} | Capital: {h['capital']} | Ratio: {h['ratio']}% | Daily: {h['daily']} USDT")

    # ====================== PAGE 2: MEMBERSHIP ======================
    elif app_mode == "📜 Membership Ledger":
        st.markdown("<h2 style='color:#FFB300;'>📜 Membership Ledger</h2>", unsafe_allow_html=True)
        st.divider()
        st.success("""
        ### 👤 Your Membership Status
        - **Plan:** 1-Year Premium Access
        - **Fee:** **30 USDT**
        - **Status:** ✅ ACTIVE
        - **Validity:** 365 Days
        """)
        st.info("Payment system next update mein aayega.")

    # ====================== PAGE 3: ROYAL Q ======================
    elif app_mode == "🎛️ Royal Q Quant Settings":
        st.markdown("<h2 style='color:#00E5FF;'>🎛️ Royal Q Advanced Quant Console</h2>", unsafe_allow_html=True)
        st.caption("30-Layer Martingale High-Frequency DCA Grid")
        st.divider()

        h1, h2, h3, h4, h5 = st.columns([0.7, 1.5, 1.5, 1.5, 1.5])
        h1.markdown("**#**")
        h2.markdown("**USDT**")
        h3.markdown("**Target %**")
        h4.markdown("**Down %**")
        h5.markdown("**Stop Loss %**")

        for i in range(30):
            c1, c2, c3, c4, c5 = st.columns([0.7, 1.5, 1.5, 1.5, 1.5])
            with c1:
                st.markdown(f"**{i+1}**")
            with c2:
                st.session_state.royal_q_grid[i]["usdt"] = st.text_input(f"u{i}", value=st.session_state.royal_q_grid[i]["usdt"], key=f"u{i}", label_visibility="collapsed", placeholder="USDT")
            with c3:
                st.session_state.royal_q_grid[i]["target"] = st.text_input(f"t{i}", value=st.session_state.royal_q_grid[i]["target"], key=f"t{i}", label_visibility="collapsed", placeholder="Target")
            with c4:
                st.session_state.royal_q_grid[i]["down"] = st.text_input(f"d{i}", value=st.session_state.royal_q_grid[i]["down"], key=f"d{i}", label_visibility="collapsed", placeholder="Down")
            with c5:
                st.session_state.royal_q_grid[i]["stoploss"] = st.text_input(f"s{i}", value=st.session_state.royal_q_grid[i]["stoploss"], key=f"s{i}", label_visibility="collapsed", placeholder="Optional")

        if st.button("💾 SAVE & ACTIVATE GRID", type="primary", use_container_width=True):
            filled = sum(1 for lvl in st.session_state.royal_q_grid if lvl["usdt"].strip() and lvl["target"].strip() and lvl["down"].strip())
            if filled == 0:
                st.error("At least 1 complete level required")
            else:
                st.session_state.royal_q_active = True
                st.session_state.royal_q_filled = filled
                st.success(f"✅ {filled} Levels Activated Successfully!")
                st.balloons()

        if st.session_state.get("royal_q_active"):
            st.success(f"🟢 Royal Q Grid LIVE • {st.session_state.get('royal_q_filled', 0)} Levels Active")

    # ====================== PAGE 4: BINANCE CONNECT ======================
    elif app_mode == "🔗 Binance Connect":
        st.markdown("<h2 style='color:#F0B90B;'>🔗 Binance API Connection</h2>", unsafe_allow_html=True)
        st.divider()
        st.warning("⚠️ API keys only stored in your current session. Never share your keys.")

        api_key = st.text_input("Binance API Key", type="password")
        api_secret = st.text_input("Binance Secret Key", type="password")

        colx, coly = st.columns(2)
        with colx:
            if st.button("🔌 Connect Binance", use_container_width=True):
                if api_key and api_secret:
                    st.session_state.binance_connected = True
                    st.success("✅ Binance Connected (Demo Mode)")
                else:
                    st.error("Please enter both keys")
        with coly:
            if st.button("🔌 Disconnect", use_container_width=True):
                st.session_state.binance_connected = False
                st.info("Disconnected")

        if st.session_state.binance_connected:
            st.success("🟢 Binance Status: CONNECTED")
            st.info("Real trading features coming after security audit.")
