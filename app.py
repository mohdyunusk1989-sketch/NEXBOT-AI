import streamlit as st
import pandas as pd
import urllib.parse
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
    "referral_code": "NEXBOT4348",
    "activated_users": [],
    "grid_running": False,
    "auto_compound": True,
    "grid_levels": [{"base_usdt": "", "current_usdt": 0.0, "target": "", "down": "", "stoploss": "", "profit": 0.0} for _ in range(30)],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

MASTER_PIN = "8312"
OWNER_PIN = "Aqsa@7860"

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
    st.sidebar.markdown(f"**🔗 Referral:** `{st.session_state.referral_code}`")
    
    status = "🟢 RUNNING" if st.session_state.grid_running else "🔴 STOPPED"
    st.sidebar.markdown(f"**Grid Status:** {status}")

    app_mode = st.sidebar.selectbox("Navigation Menu", [
        "🤖 Trading Core Suite",
        "📜 Membership Ledger",
        "🎛️ NexBot Smart Grid Pro",
        "⚙️ Smart Compound Engine",
        "🔗 Binance Connect",
        "👥 Referral System",
        "👑 Owner Panel"
    ])

    # ====================== TRADING CORE SUITE ======================
    if app_mode == "🤖 Trading Core Suite":
        st.markdown("<h2 style='color:#00E5FF;'>🤖 NEXBOT AI • Trading Core Suite</h2>", unsafe_allow_html=True)
        st.caption("Advanced Strategy Calculator + Research Based Projections")

        st.markdown("### 🔥 Live Coin Hit List")
        for item in binance_live_hit_list:
            st.markdown(f"**{item['coin']}** | <span style='color:#00E676'>{item['gain']}</span> | *{item['status']}*", unsafe_allow_html=True)

        st.divider()

        st.markdown("### ⚡ Quick Presets")
        p1, p2, p3 = st.columns(3)
        with p1:
            if st.button("🛡️ Safe (0.4%)", use_container_width=True):
                st.session_state.preset_ratio = "0.4"
                st.rerun()
        with p2:
            if st.button("⚖️ Balanced (0.7%)", use_container_width=True):
                st.session_state.preset_ratio = "0.7"
                st.rerun()
        with p3:
            if st.button("🔥 Aggressive (1.2%)", use_container_width=True):
                st.session_state.preset_ratio = "1.2"
                st.rerun()

        default_ratio = st.session_state.get("preset_ratio", "0.5")

        st.markdown("### 📊 Strategy Parameters")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("**Capital (USDT)**")
            usdt_val = st.text_input("cap", value="30", key="cap", label_visibility="collapsed")
        with c2:
            st.markdown("**Target Days**")
            days_input = st.text_input("days", value="365", key="days", label_visibility="collapsed")
        with c3:
            st.markdown("**Daily Ratio %**")
            target_val = st.text_input("ratio", value=default_ratio, key="ratio", label_visibility="collapsed")
        with c4:
            st.markdown("**Crypto Token**")
            coin_selected = st.selectbox("token", binance_all_coins, key="coin", label_visibility="collapsed")

        try:
            capital = float(usdt_val)
            ratio = float(target_val)
            days = int(days_input)
            live_profit = capital * (ratio / 100)
        except:
            capital, ratio, days, live_profit = 30.0, 0.5, 365, 0.0

        st.markdown("### 🎯 Price Range & Live Profit")
        p1, p2 = st.columns([2, 1])
        with p1:
            st.markdown("**Entry Price → Target Price**")
            st.text_input("range", value="4000 - 5000", key="price_range", label_visibility="collapsed", placeholder="Example: 70000 - 71000")
        with p2:
            st.markdown("**🎯 Target Profit Hit**")
            st.markdown(
                f"""
                <div style="
                    background-color: #1e1e2f;
                    border: 1px solid #00E5FF55;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #00FFCC;
                    margin-top: 5px;
                ">
                    {round(live_profit, 4)} USDT
                </div>
                """,
                unsafe_allow_html=True
            )

        compound = st.checkbox("♻️ Auto-Compound Growth", value=True)

        if st.button("🚀 ENTER & LAUNCH STRATEGY", type="primary", use_container_width=True):
            daily_profit = live_profit
            st.session_state.daily_profit = daily_profit
            owner_share = daily_profit * 0.05
            st.session_state.owner_income += owner_share
            st.session_state.total_profit += (daily_profit - owner_share)

            st.session_state.profit_history.append({
                "capital": capital,
                "ratio": ratio,
                "daily": round(daily_profit, 4),
                "coin": coin_selected,
                "time": datetime.now().strftime("%H:%M")
            })
            st.success(f"✅ Strategy Launched! Daily Profit: **{round(daily_profit,4)} USDT**")
            st.balloons()
            st.rerun()

        if st.session_state.daily_profit > 0:
            st.divider()
            st.markdown("### 📈 Live Results & Research Based Projection")

            realistic_monthly = ratio * 22
            risk = "Low 🟢" if ratio <= 0.5 else "Medium 🟡" if ratio <= 0.9 else "High 🔴"

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Daily Profit", f"{round(st.session_state.daily_profit,4)} USDT")
            m2.metric("Realistic Monthly", f"{round(realistic_monthly,1)}%")
            m3.metric("Risk Level", risk)
            m4.metric("Your Net Profit", f"{round(st.session_state.total_profit,2)} USDT")

            if compound:
                projected = capital * ((1 + ratio/100) ** days)
            else:
                projected = capital + (capital * ratio/100 * days)

            st.markdown(f"#### 🔮 Projected Value after {days} days: **{round(projected,2)} USDT**")

            growth = []
            curr = capital
            step = max(1, days // 12)
            for d in range(0, days+1, step):
                growth.append({"Day": d, "Value": round(curr, 2)})
                curr = curr * (1 + ratio/100) if compound else curr + capital * ratio/100
            st.line_chart(pd.DataFrame(growth).set_index("Day"))

            # WhatsApp Share
            st.markdown("### 📤 Share Your Result")
            share_text = f"""🚀 *NexBot AI - Profit Update!*

💰 Capital: {capital} USDT
📈 Daily Ratio: {ratio}%
🎯 Today's Profit: {round(st.session_state.daily_profit,4)} USDT
👑 Total Net Profit: {round(st.session_state.total_profit,2)} USDT
🔮 {days} Days Projection: {round(projected,2)} USDT

🔗 Join with my code: *{st.session_state.referral_code}*
"""
            encoded = urllib.parse.quote(share_text)
            whatsapp_url = f"https://wa.me/?text={encoded}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background:#25D366;color:white;padding:12px 24px;border:none;border-radius:8px;font-weight:bold;width:100%;cursor:pointer;">📲 Share on WhatsApp</button></a>', unsafe_allow_html=True)

            st.warning("⚠️ **DISCLAIMER** — Yeh calculation tool hai. Koi guaranteed profit nahi hai. Market risk hai.")

        if st.session_state.profit_history:
            with st.expander("📜 Recent History"):
                for h in reversed(st.session_state.profit_history[-6:]):
                    st.write(f"• {h['time']} | {h['coin']} | {h['capital']} USDT | {h['ratio']}% | Profit: {h['daily']}")

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
        st.caption("30-Layer Settings + Control Panel")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.grid_running = st.toggle("🟢 Grid Running", value=st.session_state.grid_running)
        with col2:
            st.session_state.auto_compound = st.toggle("♻️ Auto Compound", value=st.session_state.auto_compound)
        with col3:
            st.markdown(f"**Status:** {'🟢 RUNNING' if st.session_state.grid_running else '🔴 STOPPED'}")

        st.divider()
        h = st.columns([0.6, 1.4, 1.3, 1.3, 1.3])
        h[0].markdown("**#**")
        h[1].markdown("**Base USDT**")
        h[2].markdown("**Target %**")
        h[3].markdown("**Down %**")
        h[4].markdown("**Stop Loss**")

        for i in range(30):
            c1, c2, c3, c4, c5 = st.columns([0.6, 1.4, 1.3, 1.3, 1.3])
            c1.markdown(f"**{i+1}**")
            base = c2.text_input(f"b{i}", value=st.session_state.grid_levels[i]["base_usdt"], key=f"base_{i}", label_visibility="collapsed", placeholder="USDT")
            target = c3.text_input(f"t{i}", value=st.session_state.grid_levels[i]["target"], key=f"tar_{i}", label_visibility="collapsed", placeholder="Target")
            down = c4.text_input(f"d{i}", value=st.session_state.grid_levels[i]["down"], key=f"down_{i}", label_visibility="collapsed", placeholder="Down")
            sl = c5.text_input(f"s{i}", value=st.session_state.grid_levels[i]["stoploss"], key=f"sl_{i}", label_visibility="collapsed", placeholder="SL")

            st.session_state.grid_levels[i]["base_usdt"] = base
            st.session_state.grid_levels[i]["target"] = target
            st.session_state.grid_levels[i]["down"] = down
            st.session_state.grid_levels[i]["stoploss"] = sl

            if base.strip() and st.session_state.grid_levels[i]["current_usdt"] == 0.0:
                try:
                    st.session_state.grid_levels[i]["current_usdt"] = float(base)
                except:
                    pass

        if st.button("💾 SAVE SETTINGS", type="primary", use_container_width=True):
            st.success("✅ Settings Saved!")
            st.balloons()

    # ====================== SMART COMPOUND ENGINE ======================
    elif app_mode == "⚙️ Smart Compound Engine":
        st.markdown("<h2 style='color:#00E5FF;'>⚙️ Smart Compound Engine</h2>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"### {'🟢 RUNNING' if st.session_state.grid_running else '🔴 STOPPED'}")
        c2.markdown(f"### Compound: {'✅ ON' if st.session_state.auto_compound else '❌ OFF'}")
        total_invested = sum(lvl["current_usdt"] for lvl in st.session_state.grid_levels)
        c3.markdown(f"### Invested: `{round(total_invested,2)} USDT`")

        st.divider()
        h = st.columns([0.5, 1.2, 1.2, 1.2, 1.2, 1.2])
        for col, name in zip(h, ["#", "Base", "Current", "Profit", "Next Order", "Target %"]):
            col.markdown(f"**{name}**")

        total_profit = 0.0
        for i, lvl in enumerate(st.session_state.grid_levels):
            base = lvl["base_usdt"]
            current = lvl["current_usdt"]
            profit = lvl["profit"]
            next_order = round(current + profit, 4) if st.session_state.auto_compound and current > 0 else (float(base) if base.strip() else 0)
            total_profit += profit

            c = st.columns([0.5, 1.2, 1.2, 1.2, 1.2, 1.2])
            c[0].markdown(f"**{i+1}**")
            c[1].write(base or "-")
            c[2].write(round(current,4) if current else "-")
            c[3].write(round(profit,4) if profit else "-")
            c[4].write(f"**{next_order}**" if next_order else "-")
            c[5].write(lvl["target"] or "-")

        st.metric("💰 Total Profit", f"{round(total_profit,4)} USDT")

        if st.button("🔄 Simulate Profit (Demo)", use_container_width=True):
            for lvl in st.session_state.grid_levels:
                if lvl["current_usdt"] > 0:
                    p = lvl["current_usdt"] * 0.01
                    lvl["profit"] += p
                    if st.session_state.auto_compound:
                        lvl["current_usdt"] += p
            st.success("Demo profit added!")
            st.rerun()

    # ====================== BINANCE ======================
    elif app_mode == "🔗 Binance Connect":
        st.markdown("<h2 style='color:#F0B90B;'>🔗 Binance API Connection</h2>", unsafe_allow_html=True)
        st.warning("⚠️ Keys only for current session. Never give Withdraw permission.")
        api_key = st.text_input("API Key", type="password")
        api_secret = st.text_input("Secret Key", type="password")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔌 Connect", use_container_width=True):
                if api_key and api_secret:
                    st.session_state.binance_connected = True
                    st.success("✅ Connected (Demo Mode)")
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
        st.success(f"### 🔗 Your Code: `{st.session_state.referral_code}`")
        st.markdown("""
        **Membership (30 USDT):** Direct → 10 USDT | Owner → 20 USDT  

        **Profit Share:** Owner 5% | L1 5% | L2 4% | L3 3% | L4 2% | L5 1%
        """)

    # ====================== OWNER PANEL ======================
    elif app_mode == "👑 Owner Panel":
        st.markdown("<h2 style='color:#FFD700;'>👑 Owner Panel</h2>", unsafe_allow_html=True)
        owner_pin = st.text_input("Owner Password", type="password", key="owner_pin")
        
        if owner_pin == OWNER_PIN:
            st.success("✅ Access Granted")
            d1, d2, d3 = st.columns(3)
            d1.metric("Activated Users", len(st.session_state.activated_users))
            d2.metric("Owner Vault", f"{round(st.session_state.owner_income,2)} USDT")
            d3.metric("Membership Value", f"{len(st.session_state.activated_users)*30} USDT")

            st.divider()
            user_id = st.text_input("User ID / Name")
            note = st.text_input("Note")
            if st.button("✅ ACTIVATE USER", type="primary", use_container_width=True):
                if user_id.strip():
                    st.session_state.activated_users.append({
                        "id": user_id.strip(),
                        "note": note,
                        "time": datetime.now().strftime("%d-%m-%Y %H:%M")
                    })
                    st.session_state.owner_income += 20
                    st.success(f"✅ {user_id} Activated! +20 USDT")
                    st.rerun()

            st.divider()
            if st.session_state.activated_users:
                for i, u in enumerate(reversed(st.session_state.activated_users), 1):
                    st.write(f"**{i}.** `{u['id']}` | {u['time']} | {u['note']}")
            else:
                st.info("No users activated yet.")
        elif owner_pin:
            st.error("❌ Wrong Password")
