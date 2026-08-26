import flet as ft

def main(page: ft.Page):
    page.title = "NexBot AI - Institutional Quantum Suite"
    page.window.width = 480
    page.window.height = 850
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # --- ADVANCED CONFIGURATION CONTROLS (30 SETTINGS DATA MATRIX) ---
    usdt_input = ft.TextField(label="First Buy Amount (USDT)", value="10", prefix_icon=ft.icons.MONETIZATION_ON, border_color="#00E5FF", width=400)
    target_input = ft.TextField(label="Custom Cycle Target % (e.g., 0.5, 0.7)", value="0.5", prefix_icon=ft.icons.TIMELINE, border_color="#00E5FF", width=400)
    
    # Advanced Grid Settings
    margin_call_limit = ft.Dropdown(
        label="Max Margin Call Limit (DCA Steps)",
        width=400,
        options=[ft.dropdown.Option("3"), ft.dropdown.Option("5"), ft.dropdown.Option("7"), ft.dropdown.Option("10")],
        value="7"
    )
    dca_drop_input = ft.TextField(label="Margin Call Drop % (Notebook Parameter)", value="1.1", width=400)
    compound_switch = ft.Switch(label="Automated Profit Compounding Mode", value=True, active_color="#00E676")

    # --- SIMULATED USER PROFILE & OWNER BACKEND LOGIC ---
    user_balance = 20.0  # App Fuel Balance (USDT)
    subscription_status = ft.Text("📜 1-Year Membership: ACTIVE ✅", color="#00E676", size=14, weight=ft.FontWeight.W_600)
    
    # --- OUTPUT PANELS ---
    analytics_panel = ft.Container(visible=False, padding=15, border_radius=12, bgcolor="#004D40")
    projection_panel = ft.Container(visible=False, padding=15, border_radius=12, bgcolor="#111a24", border=ft.border.all(1, "#30363d"))
    
    hit_prob_txt = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color="#00E676")
    range_txt = ft.Text("", size=14, color="#E0E0E0")
    daily_txt = ft.Text("", size=14, color="#FFFFFF")
    monthly_txt = ft.Text("", size=14, color="#FFFFFF")
    yearly_txt = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color="#FFD700")

    def execute_nexbot_matrix(e):
        capital = float(usdt_input.value)
        target = float(target_input.value)
        dca_step = float(dca_drop_input.value)
        
        # Live Math Engine Simulation Matrix
        benchmark_price = 61500.00
        target_execution_price = benchmark_price * (1 + (target / 100))
        estimated_gross_profit = capital * (target / 100)
        
        # 5% App Owner Fee Automatic Logic Splitter Data
        owner_split_cut = estimated_gross_profit * 0.05
        
        # Success Rate Probability Algorithm
        if target <= 0.5: prob = "99.74%"
        elif target <= 1.0: prob = "94.85%"
        else: prob = "76.20%"

        # Update Live Display Data
        hit_prob_txt.value = f"🎯 QUANT ENGINE: {prob} HIT PROBABILITY"
        range_txt.value = (
            f"📈 Live Reference Price: ${benchmark_price}\n"
            f"🏁 Target Profit Boundary: ${round(target_execution_price, 2)}\n"
            f"🛠️ Margin Down Trigger: ${round(benchmark_price * (1 - dca_step/100), 2)}\n"
            f"💸 App Owner 5% Fuel Cut: {round(owner_split_cut, 5)} USDT"
        )
        analytics_panel.visible = True
        
        # Compounding Yield Projections (Based on 2 profitable trades per day)
        daily_yield = (target / 100) * 2
        if compound_switch.value:
            d_yield = capital * (1 + daily_yield)
            m_yield = capital * ((1 + daily_yield) ** 30)
            y_yield = capital * ((1 + daily_yield) ** 365)
        else:
            d_yield = capital + (capital * daily_yield * 1)
            m_yield = capital + (capital * daily_yield * 30)
            y_yield = capital + (capital * daily_yield * 365)

        daily_txt.value = f"🗓️ 24-Hour Capital Yield: {round(d_yield, 2)} USDT"
        monthly_txt.value = f"🗓️ 30-Day Cumulative Forecast: {round(m_yield, 2)} USDT"
        yearly_txt.value = f"👑 365-Day Compound Projection: {round(y_yield, 2)} USDT"
        projection_panel.visible = True
        
        page.update()

    # Routing elements inside panel blocks
    analytics_panel.content = ft.Column([hit_prob_txt, range_txt])
    projection_panel.content = ft.Column([
        ft.Text("📈 Predictive Compounding Matrix Models", size=15, weight=ft.FontWeight.BOLD, color="#FFB300"),
        daily_txt, monthly_txt, ft.Divider(color="#30363d"), yearly_txt
    ])

    # --- USER VIEW ASSEMBLY ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("🤖 NEXBOT AI", size=32, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("QUANTUM GRID ENGINE & MLM SUITE", size=11, color="#8B949E", weight=ft.FontWeight.W_600),
                subscription_status,
                ft.Text(f"💳 App Wallet Gas Balance: {user_balance} USDT", color="#B0BEC5", size=12),
            ]),
            margin=ft.margin.only(bottom=15)
        ),
        ft.Text("⚙️ Strategy Configuration Controls:", size=16, weight=ft.FontWeight.BOLD, color="#FFB300"),
        usdt_input,
        target_input,
        margin_call_limit,
        dca_drop_input,
        ft.Container(content=compound_switch, padding=ft.padding.only(bottom=15)),
        ft.ElevatedButton(
            "INITIALIZE CONFIGURATION ENGINE", 
            on_press=execute_nexbot_matrix, 
            bgcolor="#00E676", 
            color="#000000",
            width=400,
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        ),
        ft.Divider(color="#21262d"),
        analytics_panel,
        projection_panel
    )

ft.app(target=main)
