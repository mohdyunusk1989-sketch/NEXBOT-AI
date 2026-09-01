import streamlit as st
import urllib.parse

# Royal Q Custom Premium UI Theme Config
st.set_page_config(page_title="NexBot AI - Institutional Elite v4.1", page_icon="🤖", layout="centered")

# --- 🏦 LIVE DATA SIMULATION FOR HARDCORE API SYNC ---
binance_all_coins = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", 
    "DOGE/USDT", "DOT/USDT", "SHIB/USDT", "AVAX/USDT", "LINK/USDT",
    "MATIC/USDT", "BNB/USDT", "TRX/USDT", "LTC/USDT", "NEAR/USDT"
]

binance_live_hit_list = [
    {"coin": "🔥 SOL/USDT", "gain": "+12.45%", "status": "Strong Bullish 🚀"},
    {"coin": "🔥 NEAR/USDT", "gain": "+9.12%", "status": "Target Boundary Break ⚡"},
    {"coin": "🔥 DOGE/USDT", "gain": "+7.84%", "status": "High Volume Surge 📈"}
]

# Session State Storage Initializations
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "owner_income" not in st.session_state:
    st.session_state.owner_income = 0.0
if "fuel_wallet" not in st.session_state:
    st.session_state.fuel_wallet = 10.0
if "total_profit" not in st.session_state:
    st.session_state.total_profit = 248.50  # Simulated Cumulative Total for marketing
if "daily_profit" not in st.session_state:
    st.session_state.daily_profit = 0.0
if "show_success" not in st.session_state:
    st.session_state.show_success = False

MASTER_PIN = "8312"

# --- 🔒 SECURITY GATEWAY TERMINAL VIEW ---
if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #FF1744;'>🔒 SECURITY GATEWAY ACTIVE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8B949E;'>NEXBOT PRIVATE ENCRYPTED NODE VERIFICATION</p>", unsafe_allow_html=True)
    
    pin_input = st.text_input("Enter Enforced Security PIN to Unlock Network", type="password", key="pin_gate")
    
    if st.button("AUTHORIZE ACCESS LOCK ✅", use_container_width=True):
        if pin_input == MASTER_PIN:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ INVALID UN-ENFORCED ACCESS PIN! ACCESS STRICTLY DENIED!")

# --- 🤖 MAIN OPERATIONAL TRADING DASHBOARD (ROYAL Q STYLE) ---
else:
    app_mode = st.sidebar.selectbox("🧭 Navigation Menu", ["🤖 Trading Core Suite", "📜 Membership Ledger", "⚙️ Advanced Parameters"])
    
    if app_mode == "🤖 Trading Core Suite":
        st.markdown("<h1 style='color: #00E5FF;'>🤖 NEXBOT AI v3.2</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 11px;'>BINANCE LIVE NETWORK SUITE & GAINERS LEDGER</p>", unsafe_allow_html=True)
        st.divider()

        # 👑 Branded Owner Revenue Vault Container Inside Core Framework View
        st.info(f"👑 Confidential Owner Income Vault: {round(st.session_state.owner_income, 2)} USDT")

        # 🔥 Binance Live Coin Hit List Display Panel Layout
        st.markdown("### 🔥 BINANCE LIVE COIN HIT LIST (Top Gainers)")
        for item in binance_live_hit_list:
            st.markdown(f"**{item['coin']}** | <span style='color: #00E676;'>{item['gain']}</span> | *{item['status']}*", unsafe_allow_html=True)
        st.divider()

        # 💳 Account Balances & Metrics Layout View
        st.markdown("### 💳 Account Balances & Metrics:")
        st.markdown("<span style='color: #00E676;'>📜 1-Year Membership: ACTIVE ✅ (25 USDT Plan)</span>", unsafe_allow_html=True)
        st.write(f"⛽ Independent Fuel Wallet: {round(st.session_state.fuel_wallet, 4)} USDT")
        st.write(f"💰 Today's Daily Profit: {round(st.session_state.daily_profit, 4)} USDT")
        st.divider()

        # ⚙️ Strategy Configuration Controls Layout Panel
        st.markdown("### ⚙️ Strategy Configuration Controls:")
        usdt_val = st.text_input("1. First Buy Amount (USDT)", value="10", key="usdt_in")
        target_val = st.text_input("2. Custom Target Profit % (No Limit)", value="0.5", key="target_in")
        
        st.selectbox("5. Max Margin Call Limit", options=[str(i) for i in range(1, 11)], index=6, key="margin_in")
        st.text_input("6. 1st Margin Call Drop %", value="1.1", key="dca_in")
        coin_selected = st.selectbox("7. Active Asset Tracker (Binance Live Sync ✅)", options=binance_all_coins, index=2, key="coin_in")
        compound_active = st.checkbox("8. Auto-Compounding Mode", value=True)

        if st.button("LAUNCH STRATEGY ENGINE & CALCULATE", type="primary", use_container_width=True, key="launch_btn"):
            capital = float(usdt_val)
            target = float(target_val)
            
            # Processing Logic
            current_cycle_profit = capital * (target / 100)
            st.session_state.daily_profit = current_cycle_profit
            st.session_state.total_profit += current_cycle_profit
            st.session_state.fuel_wallet -= (current_cycle_profit * 0.05)
            st.session_state.owner_income += 15.0
            st.session_state.show_success = True
            st.rerun()

        # ✅ FIXED DISPLAY LOOP: Keeps the WhatsApp button permanently visible on click!
        if st.session_state.show_success:
            capital = float(usdt_val)
            target = float(target_val)
            live_price = 61500.00
            target_hit_price = live_price * (1 + (target / 100))
            prob = "99.42%" if target <= 0.5 else "94.15%" if target <= 1.0 else "74.80%"
            
            st.success(f"🎉 CONGRATULATION! TARGET HIT! 🎉\n\n📈 Asset Executed: {coin_selected}\n💰 Today's Profit: +{round(st.session_state.daily_profit, 4)} USDT")
            
            daily_rate = (target / 100) * 2
            m_yield = capital * ((1 + daily_rate) ** 30) if compound_active else capital + (capital * daily_rate * 30)
            y_yield = capital * ((1 + daily_rate) ** 365) if compound_active else capital + (capital * daily_rate * 365)

            st.markdown(f"🎯 **AI Strategy Hit Probability:** {prob} SUCCESS RATE")
            st.code(f"🏁 Target boundaries: ${live_price} - ${round(target_hit_price, 2)}\n🗓️ 1-Month Projections: {round(m_yield, 2)} USDT\n👑 1-Year Total Yield: {round(y_yield, 2)} USDT")

            # --- 🚀 VIRAL TEXT MARKETING GENERATION ENGINE (TOTAL PROFITS BLAST) ---
            viral_text = (
                f"🚀 *NEXBOT AI v2.0 - STRATEGY TARGET HIT!* 🚀\n\n"
                f"🔥 *Active Asset:* {coin_selected}\n"
                f"💰 *Today's Cycle Profit:* +{round(st.session_state.daily_profit, 4)} USDT\n"
                f"🎯 *AI Success Probability:* {prob}\n"
                f"👑 *TOTAL CUMULATIVE PROFIT:* +{round(st.session_state.total_profit, 2)} USDT 🔥\n\n"
                f"💸 My automated passive revenue matrix is booming! Stop wasting time and lock your node now!\n"
                f"👉 *Register via my Direct Secure Link:* https://streamlit.app"
            )
            encoded_text = urllib.parse.quote(viral_text)
            whatsapp_url = f"https://whatsapp.com{encoded_text}"
            
            st.markdown(f"<a href='{whatsapp_url}' target='_blank'><button style='width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;'>SHARE PERFORMANCE ON WHATSAPP ✅</button></a>", unsafe_allow_html=True)
            
    elif app_mode == "📜 Membership Ledger":
        st.markdown("<h2 style='color: #FFB300;'>📜 System Membership Ledger</h2>", unsafe_allow_html=True)
        st.write("🔒 Plan Category: 1-Year Premium Institutional Access Node")
        st.write("✅ Status: ACTIVE")
        st.write("💳 Registration Fee Paid: 25.00 USDT")
        
    elif app_mode == "⚙️ Advanced Parameters":
        st.markdown("<h2 style='color: #00E5FF;'>⚙️ Advanced Quant Parameters</h2>", unsafe_allow_html=True)
        st.write("📊 Margin Calling Grid Level Matrix (30 Options Pre-Configured)")
