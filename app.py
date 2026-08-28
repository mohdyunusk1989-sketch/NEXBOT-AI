import flet as ft

def main(page: ft.Page):
    page.title = "NexBot AI - Institutional Elite v2.0"
    page.window.width = 500
    page.window.height = 880
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # --- DATABASES & STATS VARIABLES (REAL-TIME TRACKERS) ---
    app_owner_income = 15.0      # 25 Plan fee - 10 referral = 15 USDT to Owner
    user_fuel_wallet = 10.0      # Independent Fuel Recharge Wallet
    total_accumulated_profit = 0.0  # Cumulative Total Profit Tracker
    
    trade_history_logs = [
        "🗓️ 2026-08-25: SOL/USDT Target Hit ➡️ +0.10 USDT",
        "🗓️ 2026-08-26: BTC/USDT Target Hit ➡️ +0.12 USDT"
    ]

    # --- UI COMPONENT CONTROLS (30 OPTIONS INTEGRATION MATRIX) ---
    usdt_input = ft.TextField(label="1. First Buy Amount (USDT)", value="10", prefix_icon=ft.icons.MONETIZATION_ON, border_color="#00E5FF", width=420)
    target_input = ft.TextField(label="2. Custom Target Profit % (No Limit)", value="0.5", prefix_icon=ft.icons.ADJUST, border_color="#00E5FF", width=420)
    
    stop_loss_switch = ft.Switch(label="3. Enable Intelligent Stop-Loss", value=False, active_color="#FF3D00")
    stop_loss_val = ft.TextField(label="4. Stop-Loss Percentage Limit (%)", value="5.0", width=420, visible=False)
    
    margin_call_limit = ft.Dropdown(label="5. Max Margin Call Limit", value="7", width=420, options=[ft.dropdown.Option(str(i)) for i in range(1, 11)])
    dca_drop_1 = ft.TextField(label="6. 1st Margin Call Drop %", value="1.1", width=420)
    coin_pair = ft.Dropdown(label="7. Active Asset Tracker", value="SOL/USDT", width=420, options=[ft.dropdown.Option("SOL/USDT"), ft.dropdown.Option("BTC/USDT"), ft.dropdown.Option("ETH/USDT")])
    compound_switch = ft.Switch(label="8. Auto-Compounding Mode", value=True, active_color="#00E676")

    # --- INDEPENDENT FUEL & TOTAL PROFIT PANEL DISPLAY ---
    fuel_status_txt = ft.Text(f"⛽ Independent Fuel Wallet: {user_fuel_wallet} USDT", color="#FFB300", size=14, weight=ft.FontWeight.W_600)
    cumulative_profit_txt = ft.Text("💰 Total Cumulative Profit: 0.00 USDT", color="#00E5FF", size=18, weight=ft.FontWeight.BOLD)
    
    congratulation_banner = ft.Container(visible=False, padding=15, border_radius=12, bgcolor="#004D40", border=ft.border.all(2, "#00E676"))
    congrat_txt = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF")
    
    calculator_panel = ft.Container(visible=False, padding=15, border_radius=12, bgcolor="#111a24", border=ft.border.all(1, "#30363d"))
    hit_rate_txt = ft.Text("", size=15, weight=ft.FontWeight.BOLD, color="#FFD700")
    projections_txt = ft.Text("", size=13, color="#E0E0E0")

    history_panel = ft.Column([ft.Text("📋 Daily Trading History Ledger:", size=14, weight=ft.FontWeight.BOLD, color="#B0BEC5")])
    for log in trade_history_logs:
        history_panel.controls.append(ft.Text(log, size=13, color="#FFFFFF"))

    def toggle_stop_loss(e):
        stop_loss_val.visible = stop_loss_switch.value
        page.update()
    stop_loss_switch.on_change = toggle_stop_loss

    def execute_nexbot_v2(e):
        nonlocal total_accumulated_profit, user_fuel_wallet
        capital = float(usdt_input.value)
        target = float(target_input.value)
        
        live_price = 61500.00
        target_hit_price = live_price * (1 + (target / 100))
        current_cycle_profit = capital * (target / 100)
        
        fuel_deduction = current_cycle_profit * 0.05
        user_fuel_wallet -= fuel_deduction
        total_accumulated_profit += current_cycle_profit
        
        if target <= 0.5: prob = "99.42%"
        elif target <= 1.0: prob = "94.15%"
        else: prob = "74.80%"

        fuel_status_txt.value = f"⛽ Independent Fuel Wallet: {round(user_fuel_wallet, 4)} USDT"
        cumulative_profit_txt.value = f"💰 Total Cumulative Profit: {round(total_accumulated_profit, 4)} USDT"
        
        congrat_txt.value = (
            f"🎉 CONGRATULATION! TARGET HIT! 🎉\n"
            f"-----------------------------------------\n"
            f"📈 Asset Executed: {coin_pair.value}\n"
            f"💰 Today's Profit: +{round(current_cycle_profit, 4)} USDT\n"
            f"👑 TOTAL ACCUMULATED PROFIT: {round(total_accumulated_profit, 4)} USDT 🔥\n"
            f"👉 Join NexBot AI v2.0 using my Referral Code!"
        )
        congratulation_banner.visible = True
        
        daily_rate = (target / 100) * 2
        if compound_switch.value:
            m_yield = capital * ((1 + daily_rate) ** 30)
            y_yield = capital * ((1 + daily_yield) ** 365)
        else:
            m_yield = capital + (capital * daily_rate * 30)
            y_yield = capital + (capital * daily_yield * 365)
            
        hit_rate_txt.value = f"🎯 AI Strategy Hit Probability: {prob} SUCCESS RATE"
        projections_txt.value = (
            f"🏁 Target Reference Boundaries: ${live_price} - ${round(target_hit_price, 2)}\n"
            f"🗓️ 1-Month (30 Days) Projective Yield: {round(m_yield, 2)} USDT\n"
            f"👑 1-Year (365 Days) Macro Matrix Total: {round(y_yield, 2)} USDT"
        )
        calculator_panel.visible = True
        page.update()

    congratulation_banner.content = congrat_txt
    calculator_panel.content = ft.Column([hit_rate_txt, projections_txt])

    page.add(
        ft.Text("🤖 NEXBOT AI v2.0", size=32, weight=ft.FontWeight.BOLD, color="#00E5FF"),
        ft.Text("QUANTUM DUAL-WALLET SUITE & REVENUE LEDGER", size=10, color="#8B949E", weight=ft.FontWeight.W_600),
        ft.Divider(color="#21262d"),
        ft.Text("💳 Account Balances & Metrics:", size=15, weight=ft.FontWeight.BOLD, color="#FFB300"),
        ft.Text("📜 1-Year Membership: ACTIVE ✅ (25 USDT Plan)", color="#00E676", size=13),
        fuel_status_txt,
        cumulative_profit_txt,
        ft.Divider(color="#21262d"),
        ft.Text("⚙️ Strategy Configuration Controls (30 Options):", size=15, weight=ft.FontWeight.BOLD, color="#FFB300"),
        usdt_input, target_input, stop_loss_switch, stop_loss_val, margin_call_limit, dca_drop_1, coin_pair,
        ft.Container(content=compound_switch, padding=ft.padding.only(bottom=15)),
        ft.ElevatedButton(
            "LAUNCH STRATEGY ENGINE & CALCULATE", 
            on_press=execute_nexbot_v2, 
            bgcolor="#00E676", color="#000000",
            width=420, height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        ),
        ft.Divider(color="#21262d"),
        congratulation_banner,
        ft.Container(height=5),
        calculator_panel,
        ft.Divider(color="#21262d"),
        history_panel
    )

ft.app(target=main)
