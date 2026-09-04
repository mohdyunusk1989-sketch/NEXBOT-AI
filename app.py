import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NexBot AI - Institutional Elite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CSS ======================
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
    h1, h2, h3, h4 { color: #00E5FF !important; }
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
    [data-testid="stMetricValue"] { color: #00E676 !important; }
    #MainMenu, footer {visibility: hidden;}
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
defaults = {
    "authenticated": False,
    "owner_income": 0.0,
    "fuel_wallet": 10.0,
    "total_profit": 0.0,
    "daily_profit": 0.0,
    "binance_connected": False,
    "profit_history": [],
    "royal_q_grid": [{"usdt": "", "target": "", "down": "", "stoploss": ""} for _ in range(30)],
    "referral_code": "NEXBOT" + str(hash("user") % 10000),
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

MASTER_PIN = "8312"

# ====================== LOGIN ======================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#FF1744;'>🔒 NEXBOT SECURITY GATEWAY</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#aaa;'>Private Encrypted Node • Institutional Access Only</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        pin = st.text_input("Enter Security PIN", type="password")
        if st.button("🔓 AUTHORIZE ACCESS", use_container_width=True):
            if pin == MASTER_PIN:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid PIN")
else:
    # ====================== SIDEBAR ======================
    st.sidebar.markdown("### 🧭 Compass NexBot")
    st.sidebar.markdown(f"**👑 Owner Vault:** `{round(st.session_state.owner_income, 2)} USDT`")
    st.sidebar.markdown(f"**⛽ Fuel Wallet:** `{round(st.session_state.fuel_wallet, 2)} USDT`")
    st.sidebar.markdown(f"**🔗 Your Referral Code:** `{st.session_state.referral_code}`")
    
    app_mode = st.sidebar.selectbox("Navigation Menu", [
        "🤖 Trading Core Suite",
        "📜 Membership Ledger",
        "🎛️ NexBot Smart Grid Pro",
        "🔗 Binance Connect",
        "👥 Referral System"
    ])

    st.sidebar.info("💡 Mobile/PC pe Install ke liye browser se **Add to Home Screen** choose karo.")

    # ====================== TRADING CORE ======================
    if app_mode == "🤖 Trading Core Suite":
        st.markdown("<h2 style='color:#00E5FF;'>🤖 NEXBOT AI • Institutional Elite</h2>", unsafe_allow_html=True)
        st.caption("Advanced Quant Calculator")

        st.markdown("### 🔥 Live Coin Hit List")
        for item in binance_live_hit_list:
            st.markdown(f"**{item['coin']}** | <span style='color:#00E676'>{item['gain']}</span> | *{item['status']}*", unsafe_allow_html=True)

        st.divider()
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

        # Live Target Profit Calculation
        try:
            live_profit = float(usdt_val) * (float(target_val) / 100)
        except:
            live_profit = 0.0

        d1, d2, d3 = st.columns(3)
        with d1:
            price_from = st.text_input("Current Entry Price", value="4000", key="pfrom")
        with d2:
            price_to = st.text_input("Target Hit Price", value="5000", key="pto")
        with d3:
            st.text_input("🎯 Target Profit Hit (Live)", value=f"{round(live_profit, 4)} USDT", disabled=True, key="live_profit")

        compound_active = st.checkbox("♻️ Auto-Compound Growth", value=True)

        if st.button("🚀 ENTER & LAUNCH STRATEGY", type="primary", use_container_width=True):
            try:
                capital = float(usdt_val)
                ratio = float(target_val)
                daily_profit = capital * (ratio / 100)
                st.session_state.daily_profit = daily_profit

                # Owner 5%
                owner_share = daily_profit * 0.05
                st.session_state.owner_income += owner_share
                st.session_state.total_profit += (daily_profit - owner_share)
                st.session_state.fuel_wallet = max(0, st.session_state.fuel_wallet - daily_profit * 0.02)

                st.session_state.profit_history.append({
                    "capital": capital, "ratio": ratio, "daily": round(daily_profit, 4), "coin": coin_selected
                })

                st.success(f"✅ Launched! Daily: **{round(daily_profit,4)} USDT** | Owner 5%: **{round(owner_share,4)} USDT**")
                st.balloons()
                st.rerun()
            except:
                st.error("❌ Valid numbers only")

        if st.session_state.daily_profit > 0:
            st.divider()
            st.markdown("### 📈 Results & Projections")

            capital = float(usdt_val)
            ratio = float(target_val)
            days = int(days_input)
            realistic_monthly = ratio * 22

            risk = "Low 🟢" if ratio <= 0.5 else "Medium 🟡" if ratio <= 0.9 else "High 🔴"

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Daily Profit", f"{round(st.session_state.daily_profit,4)} USDT")
            m2.metric("Realistic Monthly", f"{round(realistic_monthly,1)}%")
            m3.metric("Risk Level", risk)
            m4.metric("Your Net Profit", f"{round(st.session_state.total_profit,2)} USDT")

            projected = capital * ((1 + ratio/100) ** days) if compound_active else capital + (capital * ratio/100 * days)
            st.markdown(f"#### 🔮 Projected after {days} days: **{round(projected,2)} USDT**")

            growth = []
            curr = capital
            step = max(1, days // 10)
            for d in range(0, days+1, step):
                growth.append({"Day": d, "Value": round(curr, 2)})
                curr = curr * (1 + ratio/100) if compound_active else curr + capital * ratio/100
            st.line_chart(pd.DataFrame(growth).set_index("Day"))

            st.warning("""
            ⚠️ **DISCLAIMER**  
            Yeh sirf calculation tool hai. Koi guaranteed profit nahi hai.  
            Crypto market volatile hai. Sirf utna invest karo jitna lose kar sakte ho.
            """)

        if st.session_state.profit_history:
            with st.expander("📜 Session History"):
                for i, h in enumerate(reversed(st.session_state.profit_history[-8:]), 1):
                    st.write(f"{i}. {h['coin']} | {h['capital']} USDT | {h['ratio']}% | Daily: {h['daily']}")

    # ====================== MEMBERSHIP ======================
    elif app_mode == "📜 Membership Ledger":
        st.markdown("<h2 style='color:#FFB300;'>📜 Membership Ledger</h2>", unsafe_allow_html=True)
        st.success("""
        ### 👤 Membership Status
        - **Plan:** 1-Year Premium  
        - **Fee:** **30 USDT**  
        - **Distribution:** 20 USDT → Owner | 10 USDT → Direct Referrer  
        - **Status:** ✅ ACTIVE
        """)

    # ====================== SMART GRID PRO ======================
    elif app_mode == "🎛️ NexBot Smart Grid Pro":
        st.markdown("<h2 style='color:#00E5FF;'>🎛️ NexBot Smart Grid Pro</h2>", unsafe_allow_html=True)
        st.caption("30-Layer Martingale High-Frequency DCA Grid")
        st.divider()

        cols = st.columns([0.7, 1.5, 1.5, 1.5, 1.5])
        headers = ["#", "USDT", "Target %", "Down %", "Stop Loss"]
        for col, h in zip(cols, headers):
            col.markdown(f"**{h}**")

        for i in range(30):
            c1, c2, c3, c4, c5 = st.columns([0.7, 1.5, 1.5, 1.5, 1.5])
            c1.markdown(f"**{i+1}**")
            st.session_state.royal_q_grid[i]["usdt"] = c2.text_input(f"u{i}", value=st.session_state.royal_q_grid[i]["usdt"], key=f"u{i}", label_visibility="collapsed", placeholder="USDT")
            st.session_state.royal_q_grid[i]["target"] = c3.text_input(f"t{i}", value=st.session_state.royal_q_grid[i]["target"], key=f"t{i}", label_visibility="collapsed", placeholder="Target")
            st.session_state.royal_q_grid[i]["down"] = c4.text_input(f"d{i}", value=st.session_state.royal_q_grid[i]["down"], key=f"d{i}", label_visibility="collapsed", placeholder="Down")
            st.session_state.royal_q_grid[i]["stoploss"] = c5.text_input(f"s{i}", value=st.session_state.royal_q_grid[i]["stoploss"], key=f"s{i}", label_visibility="collapsed", placeholder="Optional")

        if st.button("💾 SAVE & ACTIVATE GRID", type="primary", use_container_width=True):
            filled = sum(1 for x in st.session_state.royal_q_grid if x["usdt"].strip() and x["target"].strip() and x["down"].strip())
            if filled == 0:
                st.error("At least 1 level required")
            else:
                st.session_state.royal_q_active = True
                st.session_state.royal_q_filled = filled
                st.success(f"✅ {filled} Levels Activated!")
                st.balloons()

        if st.session_state.get("royal_q_active"):
            st.success(f"🟢 Smart Grid LIVE • {st.session_state.get('royal_q_filled', 0)} Levels Active")

    # ====================== BINANCE ======================
    elif app_mode == "🔗 Binance Connect":
        st.markdown("<h2 style='color:#F0B90B;'>🔗 Binance API Connection</h2>", unsafe_allow_html=True)
        st.warning("⚠️ Keys only stored in current session.")
        api_key = st.text_input("API Key", type="password")
        api_secret = st.text_input("Secret Key", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔌 Connect", use_container_width=True):
                if api_key and api_secret:
                    st.session_state.binance_connected = True
                    st.success("✅ Connected (Demo)")
                else:
                    st.error("Enter both keys")
        with c2:
            if st.button("Disconnect", use_container_width=True):
                st.session_state.binance_connected = False
        if st.session_state.binance_connected:
            st.success("🟢 Binance Connected")

    # ====================== REFERRAL SYSTEM ======================
    elif app_mode == "👥 Referral System":
        st.markdown("<h2 style='color:#00E5FF;'>👥 Referral System</h2>", unsafe_allow_html=True)
        st.divider()

        st.success(f"### 🔗 Your Referral Code: `{st.session_state.referral_code}`")
        
        st.markdown("""
        ### 💰 Income Structure

        **On Membership (30 USDT):**
        - Direct Referrer gets → **10 USDT**
        - Owner gets → **20 USDT**

        **On Trading Profit:**
        | Level | Share |
        |-------|-------|
        | Owner | **5%** |
        | Level 1 (Direct) | **5%** |
        | Level 2 | **4%** |
        | Level 3 | **3%** |
        | Level 4 | **2%** |
        | Level 5 | **1%** |
        """)

        st.info("Full automatic tracking next update mein aayega. Abhi structure ready hai.")
