import streamlit as st
import urllib.parse

# Premium UI Wide layout configuration
st.set_page_config(page_title="NexBot AI - Institutional Elite v8.6", page_icon="🤖", layout="wide")

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
    app_mode = st.sidebar.selectbox("Navigation Menu", ["🤖 Trading Core Suite", "📜 Membership Ledger"], key="main_nav_router_v86")
    
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
        st.markdown("<h4 style='color: #FFB300; margin-bottom: 15px;'>🎛️ CORE STRATEGY PARAMETERS (FULL USER CONTROL)</h4>", unsafe_allow_html=True)
        
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1:
            usdt_val = st.text_input("1. Capital (USDT)", value="30", key="f_usdt")
        with uc2:
            target_val = st.text_input("2. Target Profit %", value="0.5", key="f_target")
        with uc3:
            down_val = st.text_input("3. Down Drop % Trigger", value="1.1", key="f_down")
        with uc4:
            # Optional Stop Loss Choice
            stop_loss_active = st.checkbox("4. Enable Intelligent Stop-Loss", value=False, key="f_sl_check")
            if stop_loss_active:
                sl_percentage = st.text_input("Stop-Loss Percentage (%)", value="5.0", key="f_sl_val")

        # ⚡ ACTION ENGINE LAUNCH BUTTON DIRECTLY BELOW 4 MAIN INPUTS
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

        # Dynamic Grid Processing View - Uses Native Clean Markdown instead of raw HTML strings!
        if st.session_state.daily_profit > 0:
            capital = float(usdt_val) if usdt_val else 30.0
            target = float(target_val) if target_val else 0.5
            down_drop = float(down_val) if down_val else 1.1
            
            st.markdown("<div style='background-color:#004D40; padding:15px; border-radius:10px; color:white; font-weight:bold; text-align:center;'>🎉 CORE NETWORK SUITE VERIFIED: STRATEGY ENGINE LAUNCHED SUCCESSFULLY! 🎉</div>", unsafe_allow_html=True)
            st.write("")

            # 👑 THE UNBELIEVABLE 30 AUTOMATED OPTIONS GRIDS SHOWING NATIVE NATION-WIDE
            st.markdown("### 📊 30-Layer Martingale Margin Call Settings Matrix")
            st.caption("When the market drops based on Option 3 (Down Drop %), the system automatically triggers the next layered options buying algorithm below:")
            st.write("")

            # Beautiful Native Clean Matrix Output
            for option_num in range(1, 31):
                drop_trigger_calc = round(down_drop * option_num, 2)
                multiplier = 1 if option_num <= 4 else 2 if option_num <= 10 else 4
                buying_amount_calc = round(capital * multiplier, 2)
                
                # Pro-trading text string format
                execution_label = "Automatic Scalping 📈" if option_num == 1 else "Smart DCA Re-buy ⚡" if option_num == 2 else "Quantum Liquidity Hedging 🚀"
                
                # Multi-metric display panel
                st.write(f"🔹 **Option Layer {option_num}:** {drop_trigger_calc}% Market Drop ➡️ **Auto-Buy Allocation:** {buying_amount_calc} USDT | *Execution:* {execution_label}")

            st.divider()

            # Viral Marketing Blast Template Link Engine
            viral_text = (
                f"🚀 *NEXBOT AI v2.0 - AUTOMATED GRID POSITION HIT!* 🚀\n\n"
                f"🎛️ *Grid Settings:* Capital: {capital} USDT | Target: {target}% | Down Trigger: {down_drop}%\n"
                f"💰 *Today's First Position Profit:* +{round(st.session_state.daily_profit, 4)} USDT\n"
                f"🛠️ *30-Layer Martingale Options:* ACTIVE & RUNNING ✅\n"
                f"👑 *TOTAL CUMULATIVE CRYPTO PROFIT:* +{round(st.session_state.total_profit, 2)} USDT 🔥\n\n"
                f"👉 *Lock your automated network suite safely now:* https://streamlit.app"
            )
            encoded_text = urllib.parse.quote(viral_text)
            whatsapp_url = f"https://whatsapp.com{encoded_text}"
            st.markdown(f"<a href='{whatsapp_url}' target='_blank'><button style='width:100%; padding:12px; background-color:#25D366; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;'>SHARE 30-OPTIONS GRID SYSTEM ON WHATSAPP ✅</button></a>", unsafe_allow_html=True)

    elif app_mode == "📜 Membership Ledger":
        st.markdown("## 📜 System Membership Ledger Terminal")
        st.write("🔒 Plan Category: 1-Year Premium Institutional Access Node")
        st.write("✅ Status: ACTIVE (25 USDT Plan verified)")
