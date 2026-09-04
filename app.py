    # ========== PAGE 1: TRADING CORE SUITE (IMPROVED) ==========
    if app_mode == "🤖 Trading Core Suite":
        st.markdown("<h2 style='color:#00E5FF;'>🤖 NEXBOT AI • Institutional Elite</h2>", unsafe_allow_html=True)
        st.caption("Advanced Quant Calculator • Better than traditional grid bots")

        # ---------- LIVE HITS ----------
        st.markdown("### 🔥 Live Coin Hit List")
        for item in binance_live_hit_list:
            st.markdown(
                f"**{item['coin']}** &nbsp;|&nbsp; "
                f"<span style='color:#00E676'>{item['gain']}</span> &nbsp;|&nbsp; "
                f"*{item['status']}*",
                unsafe_allow_html=True
            )

        st.divider()

        # ---------- PRESET BUTTONS ----------
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

        # Default values from preset
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

        # ---------- LAUNCH BUTTON ----------
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

                # Save history
                if "profit_history" not in st.session_state:
                    st.session_state.profit_history = []
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

        # ---------- RESULTS + PROJECTIONS ----------
        if st.session_state.daily_profit > 0:
            st.divider()
            st.markdown("### 📈 Live Results & Projections")

            capital = float(usdt_val) if usdt_val else 30
            ratio = float(target_val) if target_val else 0.5
            days = int(days_input) if days_input else 365

            # Realistic Monthly Estimate
            realistic_monthly = ratio * 22   # approx 22 trading days
            if ratio <= 0.5:
                risk_level = "Low 🟢"
                risk_color = "#00E676"
            elif ratio <= 0.9:
                risk_level = "Medium 🟡"
                risk_color = "#FFB300"
            else:
                risk_level = "High 🔴"
                risk_color = "#FF1744"

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Daily Profit", f"{round(st.session_state.daily_profit,4)} USDT")
            m2.metric("Realistic Monthly", f"{round(realistic_monthly,1)}%")
            m3.metric("Risk Level", risk_level)
            m4.metric("Your Net Profit", f"{round(st.session_state.total_profit,2)} USDT")

            # Projected Growth
            if compound_active:
                projected = capital * ((1 + ratio/100) ** days)
            else:
                projected = capital + (capital * ratio/100 * days)

            st.markdown(f"#### 🔮 Projected Value after {days} days: **{round(projected,2)} USDT**")

            # Simple growth data for chart
            import pandas as pd
            growth_data = []
            current = capital
            for day in range(0, days+1, max(1, days//10)):
                growth_data.append({"Day": day, "Value": round(current, 2)})
                current = current * (1 + ratio/100) if compound_active else current + (capital * ratio/100)

            df = pd.DataFrame(growth_data)
            st.line_chart(df.set_index("Day"))

            # ---------- DISCLAIMER ----------
            st.warning("""
            ⚠️ **IMPORTANT DISCLAIMER**  
            - Yeh sirf calculation tool hai.  
            - Koi bhi guaranteed profit nahi hai.  
            - Crypto market bahut volatile hai.  
            - Past performance future results ki guarantee nahi hai.  
            - Sirf utna paise lagao jitna lose kar sakte ho.
            """)

        # ---------- SESSION HISTORY ----------
        if st.session_state.get("profit_history"):
            with st.expander("📜 Session Profit History"):
                for i, h in enumerate(reversed(st.session_state.profit_history[-10:]), 1):
                    st.write(f"**{i}.** {h['coin']} | Capital: {h['capital']} | Ratio: {h['ratio']}% | Daily: {h['daily']} USDT")
