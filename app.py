import streamlit as st
import pandas as pd
from datetime import datetime

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
    label { color: #00E5FF !important; font-weight: bold !important; }
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
    "referral_code": "NEXBOT4348",
    "activated_users": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

MASTER_PIN = "8312"
OWNER_PIN = "Aqsa@7860"          # New Owner Password

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
        "👥 Referral System",
        "👑 Owner Panel"
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
            st.markdown("**Capital (USDT)**")
            usdt_val = st.text_input("cap", value="30", key="cap", label_visibility="collapsed")
        with c2:
            st.markdown("**Target Days**")
            days_input = st.text_input("days", value=default_days, key="days", label_visibility="collapsed")
        with c3:
            st.markdown("**Daily Ratio %**")
            target_val = st.text_input("ratio", value=default_ratio, key="ratio", label_visibility="collapsed")
        with c4:
            st.markdown("**Crypto Token**")
            coin_selected = st.selectbox("token", binance_all_coins, key="coin", label_visibility="collapsed")

        try:
            capital = float(usdt_val)
            ratio = float(target_val)
            live_profit = capital * (ratio / 100)
        except:
            capital = 30.0
            ratio = 0.5
            live_profit = 0.0

        st.markdown("### 🎯 Price Range & Profit")
        p1, p2 = st.columns([2, 1])
        with p1:
            st.markdown("**Entry Price → Target Price**")
            price_range = st.text_input("range", value="4000 - 5000", key="price_range", label_visibility="collapsed", placeholder="Example: 70000 - 71000")
        with p2:
            st.markdown("**🎯 Target Profit Hit**")
            st.text_input("profit", value=f"{round(live_profit, 4)} USDT", key="live_profit", disabled=True, label_visibility="collapsed")

        compound_active = st.checkbox("♻️ Auto-Compound Growth", value=True)

        if st.button("🚀 ENTER & LAUNCH STRATEGY", type="primary", use_container_width=True):
            try:
                daily_profit = capital * (ratio / 100)
                st.session_state.daily_profit = daily_profit
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
            days = int(days_input) if days_input else 365
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

            st.warning("⚠️ **DISCLAIMER** — Yeh sirf calculation tool hai. Koi guaranteed profit nahi hai.")

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
        for col, h in zip(cols, ["#", "USDT", "Target %", "Down %", "Stop Loss"]):
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

    # ====================== REFERRAL ======================
    elif app_mode == "👥 Referral System":
        st.markdown("<h2 style='color:#00E5FF;'>👥 Referral System</h2>", unsafe_allow_html=True)
        st.success(f"### 🔗 Your Referral Code: `{st.session_state.referral_code}`")
        st.markdown("""
        ### 💰 Income Structure
        **Membership (30 USDT):**
        - Direct Referrer → **10 USDT**
        - Owner → **20 USDT**

        **Trading Profit Share:**
        | Level | Share |
        |-------|-------|
        | Owner | **5%** |
        | Level 1 | **5%** |
        | Level 2 | **4%** |
        | Level 3 | **3%** |
        | Level 4 | **2%** |
        | Level 5 | **1%** |
        """)

    # ====================== OWNER PANEL ======================
    elif app_mode == "👑 Owner Panel":
        st.markdown("<h2 style='color:#FFD700;'>👑 Owner Panel</h2>", unsafe_allow_html=True)
        st.caption("Only for Owner • Full Control Center")

        owner_pin = st.text_input("Enter Owner Password", type="password", key="owner_pin")
        
        if owner_pin == OWNER_PIN:
            st.success("✅ Owner Access Granted")
            st.divider()

            # Dashboard
            st.markdown("### 📊 Owner Dashboard")
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Total Activated Users", len(st.session_state.activated_users))
            d2.metric("Owner Vault", f"{round(st.session_state.owner_income, 2)} USDT")
            d3.metric("Fuel Wallet", f"{round(st.session_state.fuel_wallet, 2)} USDT")
            d4.metric("Total Membership Value", f"{len(st.session_state.activated_users) * 30} USDT")

            st.divider()

            # Manual Activation
            st.markdown("### 🔓 Manually Activate User")
            st.info("Jab koi user aapko directly 30 USDT de, to yahan uska ID daal ke Activate kar do.")

            col1, col2 = st.columns(2)
            with col1:
                user_id = st.text_input("User ID / Referral Code / Name", placeholder="Example: NEXBOT8899")
            with col2:
                note = st.text_input("Note (optional)", placeholder="Cash / UPI / Bank")

            if st.button("✅ ACTIVATE THIS USER", type="primary", use_container_width=True):
                if user_id.strip():
                    st.session_state.activated_users.append({
                        "id": user_id.strip(),
                        "note": note,
                        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
                        "amount": 30
                    })
                    st.session_state.owner_income += 20
                    st.success(f"✅ **{user_id}** Activated Successfully! +20 USDT added to Owner Vault")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please enter User ID")

            st.divider()

            # Activated Users List
            st.markdown("### 📋 Activated Users List")
            if st.session_state.activated_users:
                for i, user in enumerate(reversed(st.session_state.activated_users), 1):
                    st.write(f"**{i}.** `{user['id']}` | {user['time']} | Note: {user['note']}")
            else:
                st.info("Abhi koi user activate nahi hua.")

            st.divider()

            # ====================== AI ASSISTANT ======================
            st.markdown("### 🤖 NexBot AI Assistant")
            st.caption("Har function ke baare mein poocho")

            question = st.selectbox("Kya jaanna chahte ho?", [
                "Select a question...",
                "Trading Core Suite kya karta hai?",
                "NexBot Smart Grid Pro kaise use kare?",
                "Referral System kaise kaam karta hai?",
                "Binance se kaise connect kare?",
                "Owner Panel kaise use kare?",
                "Membership fee ka distribution kya hai?",
                "Target Profit Hit live kaise kaam karta hai?"
            ])

            if question == "Trading Core Suite kya karta hai?":
                st.info("""
                **Trading Core Suite** main calculator hai.  
                - Capital, Daily Ratio, Days daalo  
                - Live Target Profit dikhega  
                - Launch dabate hi Owner ko 5% milta hai  
                - Projection chart bhi dikhta hai  
                - Safe / Balanced / Aggressive presets hain
                """)
            elif question == "NexBot Smart Grid Pro kaise use kare?":
                st.info("""
                **NexBot Smart Grid Pro** 30-level Martingale grid hai.  
                - Har level pe USDT, Target %, Down %, Stop Loss daal sakte ho  
                - Save & Activate dabate hi grid live ho jata hai  
                - Yeh Royal Q style advanced grid hai
                """)
            elif question == "Referral System kaise kaam karta hai?":
                st.info("""
                **Referral Structure:**  
                - Membership 30 USDT → Direct ko 10 USDT, Owner ko 20 USDT  
                - Trading Profit pe:  
                  Owner 5% | L1 5% | L2 4% | L3 3% | L4 2% | L5 1%
                """)
            elif question == "Binance se kaise connect kare?":
                st.info("""
                **Binance Connect karne ka tarika:**  
                1. Binance app/website pe jao  
                2. API Management mein new API banao  
                3. Sirf **Enable Reading** + **Enable Spot Trading** allow karo  
                4. API Key + Secret Key copy karo  
                5. NexBot ke Binance Connect page pe paste karke Connect dabao  

                ⚠️ Kabhi bhi Withdraw permission mat dena.
                """)
            elif question == "Owner Panel kaise use kare?":
                st.info("""
                **Owner Panel** sirf aapke liye hai.  
                - Password: `Aqsa@7860`  
                - Yahan se aap manually kisi bhi user ko Activate kar sakte ho  
                - Jab koi cash/USDT de, to uska ID daal ke Activate kar do  
                - +20 USDT automatic Owner Vault mein add ho jayega
                """)
            elif question == "Membership fee ka distribution kya hai?":
                st.info("""
                **30 USDT Membership:**  
                - 20 USDT → Owner (aapke paas)  
                - 10 USDT → Jisne refer kiya (Direct)
                """)
            elif question == "Target Profit Hit live kaise kaam karta hai?":
                st.info("""
                Capital × Daily Ratio % = Target Profit Hit  
                Example: 30 USDT × 0.4% = 0.12 USDT  
                Yeh live calculate hota hai (Launch se pehle bhi dikhta hai)
                """)

        elif owner_pin:
            st.error("❌ Wrong Owner Password")
