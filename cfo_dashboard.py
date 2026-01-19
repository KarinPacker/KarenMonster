import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec

# --- MOCK DATA GENERATION (For Local Testing Only) ---
# In Power BI, 'dataset' is automatically provided.
if 'dataset' not in locals():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']

    data = {
        'Date': np.random.choice(dates, 1000),
        'Revenue': np.random.uniform(1000, 5000, 1000),
        'Profit': np.random.uniform(200, 1500, 1000),
        'Region': np.random.choice(regions, 1000)
    }
    dataset = pd.DataFrame(data)

# --- CONFIGURATION & STYLING ---
# Colors extracted from the provided JSX
BG_COLOR = '#0A0E14'
TEXT_COLOR = '#F0F6FC'
ACCENT_GREEN = '#00FF41'
ACCENT_CYAN = '#00F0FF'
ACCENT_RED = '#FF003C'
GRID_COLOR = '#30363D'
CARD_BG = '#161B22'

# Set global style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = TEXT_COLOR
plt.rcParams['axes.labelcolor'] = '#8B949E'
plt.rcParams['xtick.color'] = '#8B949E'
plt.rcParams['ytick.color'] = '#8B949E'
plt.rcParams['axes.edgecolor'] = GRID_COLOR

# --- DATA PROCESSING ---
# Ensure Date is datetime
dataset['Date'] = pd.to_datetime(dataset['Date'])

# 1. KPI Calculations
total_revenue = dataset['Revenue'].sum()
net_profit = dataset['Profit'].sum()
profit_margin = (net_profit / total_revenue) * 100

# 2. Monthly Trend Data
monthly_trend = dataset.set_index('Date').resample('ME')['Revenue'].sum().reset_index()
monthly_trend['Month'] = monthly_trend['Date'].dt.strftime('%b')

# 3. Revenue by Region Data
region_revenue = dataset.groupby('Region')['Revenue'].sum().sort_values(ascending=False).reset_index()

# --- PLOTTING ---
fig = plt.figure(figsize=(12, 8), facecolor=BG_COLOR)
gs = GridSpec(2, 2, height_ratios=[1, 1.2], hspace=0.3, wspace=0.2)

# Subplot 1: KPI Cards (Top Left)
ax_kpi = fig.add_subplot(gs[0, 0])
ax_kpi.set_facecolor(CARD_BG)
ax_kpi.axis('off')

# Draw "Cards" visually
ax_kpi.text(0.1, 0.75, "Total Revenue", fontsize=10, color='#8B949E', fontweight='bold', ha='left')
ax_kpi.text(0.1, 0.55, f"${total_revenue/1e6:.2f}M", fontsize=28, color=ACCENT_GREEN, fontweight='bold', fontfamily='monospace', ha='left')

ax_kpi.text(0.1, 0.35, "Net Profit", fontsize=10, color='#8B949E', fontweight='bold', ha='left')
ax_kpi.text(0.1, 0.15, f"${net_profit/1e6:.2f}M", fontsize=28, color=ACCENT_CYAN, fontweight='bold', fontfamily='monospace', ha='left')
ax_kpi.text(0.6, 0.20, f"({profit_margin:.1f}%)", fontsize=12, color=TEXT_COLOR, ha='left')

ax_kpi.set_title("Financial Overview", loc='left', color=TEXT_COLOR, fontsize=12, pad=10, fontweight='bold')


# Subplot 2: Monthly Revenue Trend (Top Right)
ax_trend = fig.add_subplot(gs[0, 1])
ax_trend.set_facecolor(CARD_BG)

# Plot Line
sns.lineplot(data=monthly_trend, x='Month', y='Revenue', ax=ax_trend, color=ACCENT_CYAN, linewidth=2.5, marker='o')
ax_trend.fill_between(range(len(monthly_trend)), monthly_trend['Revenue'], alpha=0.1, color=ACCENT_CYAN)

ax_trend.set_title("Monthly Revenue Trend", loc='left', color=TEXT_COLOR, fontsize=12, pad=10, fontweight='bold')
ax_trend.set_xlabel("")
ax_trend.set_ylabel("Revenue", fontsize=9)
ax_trend.grid(color=GRID_COLOR, linestyle='--', linewidth=0.5, axis='y')
ax_trend.spines['top'].set_visible(False)
ax_trend.spines['right'].set_visible(False)
ax_trend.spines['bottom'].set_visible(False)
ax_trend.spines['left'].set_visible(False)

# Subplot 3: Revenue by Region (Bottom)
ax_region = fig.add_subplot(gs[1, :])
ax_region.set_facecolor(CARD_BG)

# Plot Bar
bars = sns.barplot(data=region_revenue, x='Region', y='Revenue', hue='Region', legend=False, ax=ax_region, palette=[ACCENT_GREEN, ACCENT_CYAN, '#8B949E', '#30363D'])

# Add Value Labels
for i, v in enumerate(region_revenue['Revenue']):
    ax_region.text(i, v + (v*0.02), f"${v/1e6:.1f}M", color=TEXT_COLOR, ha='center', fontweight='bold')

ax_region.set_title("Revenue by Region", loc='left', color=TEXT_COLOR, fontsize=12, pad=10, fontweight='bold')
ax_region.set_xlabel("")
ax_region.set_ylabel("Revenue", fontsize=9)
ax_region.grid(color=GRID_COLOR, linestyle='--', linewidth=0.5, axis='y')
ax_region.spines['top'].set_visible(False)
ax_region.spines['right'].set_visible(False)
ax_region.spines['bottom'].set_visible(False)
ax_region.spines['left'].set_visible(False)

# Final Layout Adjustments
plt.tight_layout()

# Save locally for verification (Power BI would render 'plt.show()')
plt.savefig('cfo_dashboard.png', dpi=100, bbox_inches='tight')
print("Dashboard generated successfully.")
