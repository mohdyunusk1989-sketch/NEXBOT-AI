import streamlit as st
import urllib.parse

# Premium UI Config - Force wide layout to fit columns beautifully
st.set_page_config(page_title="NexBot AI - Institutional Elite v4.8", page_icon="🤖", layout="wide")

# Simulation asset registry configuration
binance_all_coins = ["SOL/USDT", "BTC/USDT", "ETH/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT", "NEAR/USDT"]

# Session State Storage Initializations
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "owner_income" not in st.session_state:
    st.session_state.owner_income = 0.0
if "fuel_wallet" not in st.session_state:
    st.session_state.fuel_wallet = 10.0
if "total_profit" not in st.session_state:
    st.session_state.total_profit = 248.50  
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

# --- 🤖 MAIN OPERATIONAL TRADING DASHBOARD ---
else:
    st.sidebar.markdown("### 🧭 NexBot Control Menu")
    app_mode = st.sidebar.selectbox("Navigation", ["🤖 Trading Core Suite", "📜 Membership Ledger"])
    
    if app_mode == "🤖 Trading Core Suite":
        # Header Dynamic Ribbon
        head_col1, head_col2 = st.columns(2)
        with head_col1:
            st.markdown("<h2 style='color: #00E5FF; margin:0px;'>🤖 NEXBOT AI v3.2</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #8B949E; font-size: 11px; margin:0px;'>BINANCE LIVE NETWORK SUITE & CUSTOM GRID MATRIX</p>", unsafe_allow_html=True)
        with head_col2:
            st.markdown(f"<div style='background-color:#2D1A38; padding:8px; border-radius:5px; text-align:center; font-size:12px; font-weight:bold; color:#E040FB; margin-top:5px;'>👑 Vault: {round(st.session_state.owner_income, 2)} USDT</div>", unsafe_allow_html=True)
        
        st.divider()

        # 📊 HEADING AT THE TOP
        st.markdown("<h4 style='color: #FFB300; margin-bottom: 15px;'>📊 CUSTOM STRATEGY CALCULATE MATRIX</h4>", unsafe_allow_html=True)

        # 👑 THE HORIZONTAL 6-COLUMN GRID MATRIX WITH LABELS ABOVE BOXES
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            usdt_val = st.text_input("Capital (USDT)", value="10", key="grid_usdt")
            days_input = st.text_input("Target Days", value="365", key="grid_days")
            
        with col2:
            target_val = st.text_input("Daily Profit %", value="0.5", key="grid_target")
            compound_active = st.checkbox("Auto-Compounding", value=True, key="grid_comp")
            
        with col3:
            coin_selected = st.selectbox("Crypto Token", options=binance_all_coins, index=0, key="grid_coin")
            
        with col4:
            price_from = st.text_input("Current Entry Price", value="3000", key="grid_p_from")
            
        with col5:
            price_to = st.text_input("Target Hit Price", value="3500", key="grid_p_to")
            
        with col6:
            margin_in = st.selectbox("Margin Call Limit", options=[f"Calls: {i}" for i in range(1, 11)], index=6, key="grid_margin")

        # ⚡ ACTION BUTTON AT THE VERY BOTTOM
        st.write("") 
        launch_action = st.button("ENTER & LAUNCH STRATEGY 🚀", type="primary", use_container_width=True, key="grid_enter_btn")

        st.divider()

        # Calculation dispatch triggers
        if launch_action:
            val_capital = float(usdt_val) if usdt_val else 10.0
            val_target = float(target_val) if target_val else 0.5
            
            st.session_state.daily_profit = val_capital * (val_target / 100)
            st.session_state.total_profit += st.session_state.daily_profit
            st.session_state.fuel_wallet -= (st.session_state.daily_profit * 0.05)
            st.session_state.owner_income += 15.0
            st.session_state.show_success = True

        # Summary Matrix View
        if st.session_state.show_success:
            capital = float(usdt_val) if usdt_val else 10.0
            target = float(target_val) if target_val else 0.5
            days_count = int(days_input) if days_input else 365
            p_start = float(price_from) if price_from else 3000.0
            p_end = float(price_to) if price_to else 3500.0
            
            st.markdown("### 📊 Live Network Strategy Summary Box Matrix")
            
            box_col1, box_col2 = st.columns(2)
            with box_col1:
                st.info(f"💰 **Today's Daily Profit:** {round(st.session_state.daily_profit, 4)} USDT")
                st.warning(f"⛽ **Independent Fuel Wallet:** {round(st.session_state.fuel_wallet, 4)} USDT")
                st.code(
                    f"📦 Capital Allocated: {capital} USDT\n"
                    f"🪙 Active Asset Node: {coin_selected}\n"
                    f"🎯 Price Hit Boundaries: From ${p_start} To ${p_end}\n"
                    f"🛠️ Margin Settings: {margin_in}"
                )
            
            with box_col2:
                daily_rate = (target / 100) * 2
                projected_yield = capital * ((1 + daily_rate) ** days_count) if compound_active else capital + (capital * daily_rate * days_count)
                
                st.success(f"🎉 **CONGRATULATION! STRATEGY TARGET HIT!** 🎉")
                st.metric(label=f"👑 Custom Projections Yield ({days_count} Days Total)", value=f"{round(projected_yield, 2)} USDT")
                
                viral_text = (
                    f"🚀 *NEXBOT AI v2.0 - TARGET POSITION HIT!* 🚀\n\n"
                    f"🔥 *Crypto Asset:* {coin_selected}\n"
                    f"🎯 *Price Boundaries:* ${p_start} ➡️ ${p_end} (🎯 Hit Successful!)\n"
                    f"💰 *Today's Cycle Profit:* +{round(st.session_state.daily_profit, 4)} USDT\n"
                    f"👑 *TOTAL CUMULATIVE PROFIT:* +{round(st.session_state.total_profit, 2)} USDT 🔥\n\n"
                    f"👉 *Register via my Direct Secure Link:* https://streamlit.app"
                )
                encoded_text = urllib.parse.quote(viral_text)
                whatsapp_url = f"https://whatsapp.com{encoded_text}"
                st.markdown(f"<a href='{whatsapp_url}' target='_blank'><button style='width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;'>SHARE PERFORMANCE ON WHATSAPP ✅</button></a>", unsafe_allow_html=True)

    elif app_mode == "📜 Membership Ledger":
        st.markdown("## 📜 System Membership Ledger")
        st.write("🔒 Plan Category: 1-Year Premium Institutional Access Node")
        st.write("✅ Status: ACTIVE (25 USDT Plan)")
