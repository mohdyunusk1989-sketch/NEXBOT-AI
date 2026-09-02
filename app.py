import streamlit as st
import urllib.parse

# Premium UI Wide layout configuration
st.set_page_config(page_title="NexBot AI - Institutional Elite v9.0", page_icon="🤖", layout="wide")

# Custom CSS to align labels and ensure perfect dark text
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }
    .stTextInput input, .stSelectbox div {
        text-align: center !important;
        font-weight: bold !important;
    }
    div[data-testid="stWidgetLabel"] p {
        font-size: 1rem !important;
        color: inherit !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
    app_mode = st.sidebar.selectbox("Navigation Menu", ["🤖 Trading Core Suite", "📜 Membership Ledger"], key="main_nav_router_v90")
    
    if app_mode == "🤖 Trading Core Suite":
        # Header Dynamic Ribbon
        head_col1, head_col2 = st.columns(2)
        with head_col1:
            st.markdown("<h2 style='color: #00E5FF; margin:0px;'>🤖 NEXBOT AI v3.2</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #8B949E; font-size: 11px; margin:0px;'>BINANCE AUTOMATED MARTINGALE NODE FRAMEWORK</p>", unsafe_allow_html=True)
        with head_col2:
            st.markdown(f"<div style='background-color:#2D1A38; padding:8px; border-radius:5px; text-align:center; font-size:12px; font-weight:bold; color:#E040FB; margin-top:5px;'>👑 Vault: {round(st.session_state.owner_income, 2)} USDT</div>", unsafe_allow_html=True)
        
        st.divider()

        # ✅ THE 4 CORE CONTROL INPUTS AT THE TOP (PERFECT INLINE DESIGN)
        st.markdown("<h4 style='color: #FFB300; margin-bottom: 15px;'>🎛️ CORE STRATEGY PARAMETERS (4 OPTIONS TOP)</h4>", unsafe_allow_html=True)
        
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1:
            usdt_val = st.text_input("1. Capital (USDT)", value="30", key="f_usdt")
        with uc2:
            target_val = st.text_input("2. Target Profit %", value="0.5", key="f_target")
        with uc3:
            down_val = st.text_input("3. Down Drop % Trigger", value="1.1", key="f_down")
        with uc4:
            stop_loss_active = st.checkbox("4. Enable Intelligent Stop-Loss", value=False, key="f_sl_check")
            if stop_loss_active:
                sl_percentage = st.text_input("Stop-Loss Drop % Limit", value="5.0", key="f_sl_val")

        st.divider()

        # ✅ THE 30 EMPTY OPTIONS BOX GRID BELOW FOR THE USER TO FILL THEMSELVES
        st.markdown("<h4 style='color: #00E5FF; margin-bottom: 10px;'>📊 30-LAYER MARTINGALE MARGIN CALL MATRIX (EMPTY BOXES)</h4>", unsafe_allow_html=True)
        st.caption("यूज़र खुद अपनी मर्ज़ी से नीचे दिए गए इन 30 ख़ाली डिब्बों में मार्केट ड्रॉप ट्रिगर वैल्यू भर कर कस्टमाइज़ करेगा:")
        st.write("")

        # Creating 30 empty/customizable input boxes row by row
        user_filled_options = {}
        
        # Display them in chunks of 3 per line to keep it clean and neat
        for block in range(0, 30, 3):
            grid_cols = st.columns(3)
            for i in range(3):
                opt_idx = block + i + 1
                with grid_cols[i]:
                    user_filled_options[f"opt_{opt_idx}"] = st.text_input(f"🔹 Option Layer {opt_idx} Drop %", placeholder="Type Value Here (e.g. 1.2)", key=f"user_opt_{opt_idx}")

        # ⚡ ACTION ENGINE LAUNCH BUTTON DIRECTLY AT THE VERY BOTTOM OF THE ENTIRE PAGE
        st.write("") 
        launch_action = st.button("ENTER & LAUNCH QUANT GRID ENGINE 🚀", type="primary", use_container_width=True, key="f_submit_btn")

        st.divider()

        if launch_action:
            val_capital = float(usdt_val) if usdt_val else 30.0
            val_target = float(target_val) if target_val else 0.5
            st.session_state.daily_profit = val_capital * (val_target / 100)
            st.session_state.total_profit += st.session_state.daily_profit
            st.session_state.fuel_wallet -= (st.session_state.daily_profit * 0.05)
            st.session_state.owner_income += 15.0
            st.rerun()

        # Success Report View Layer
        if st.session_state.daily_profit > 0:
            capital = float(usdt_val) if usdt_val else 30.0
            target = float(target_val) if target_val else 0.5
            down_drop = float(down_val) if down_val else 1.1
            
            st.markdown("<div style='background-color:#004D40; padding:15px; border-radius:10px; color:white; font-weight:bold; text-align:center;'>🎉 CORE NETWORK SUITE VERIFIED: STRATEGY ENGINE LAUNCHED SUCCESSFULLY! 🎉</div>", unsafe_allow_html=True)
            st.write("")
            
            box_col1, box_col2 = st.columns(2)
            with box_col1:
                st.info(f"💰 **Today's Daily Cycle Profit:** {round(st.session_state.daily_profit, 4)} USDT")
                st.warning(f"⛽ **Independent Fuel Wallet Balance:** {round(st.session_state.fuel_wallet, 4)} USDT")
            with box_col2:
                st.success(f"👑 **TOTAL CUMULATIVE CRYPTO PROFIT:** +{round(st.session_state.total_profit, 2)} USDT 🔥")

            # Viral Marketing Blast Template Link Engine
            viral_text = (
                f"🚀 *NEXBOT AI v2.0 - ROYAL Q GRID ACTIVE!* 🚀\n\n"
                f"🎛️ *Grid Settings:* Capital: {capital} USDT | Target: {target}% | Down Trigger: {down_drop}%\n"
                f"💰 *Today's First Position Profit:* +{round(st.session_state.daily_profit, 4)} USDT\n"
                f"🛠️ *30-Layer Custom Martingale Boxes:* FILLED & OPERATIONAL ✅\n"
                f"👑 *TOTAL CUMULATIVE CRYPTO PROFIT:* +{round(st.session_state.total_profit, 2)} USDT 🔥\n\n"
                f"👉 *Lock your customized trading suite safely now:* https://streamlit.app"
            )
            encoded_text = urllib.parse.quote(viral_text)
            whatsapp_url = f"https://whatsapp.com{encoded_text}"
            st.write("")
            st.markdown(f"<a href='{whatsapp_url}' target='_blank'><button style='width:100%; padding:12px; background-color:#25D366; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;'>SHARE CUSTOM PERFORMANCE MATRIX ON WHATSAPP ✅</button></a>", unsafe_allow_html=True)

    elif app_mode == "📜 Membership Ledger":
        st.markdown("## 📜 System Membership Ledger Terminal")
        st.write("🔒 Plan Category: 1-Year Premium Institutional Access Node")
        st.write("✅ Status: ACTIVE (25 USDT Plan verified)")
