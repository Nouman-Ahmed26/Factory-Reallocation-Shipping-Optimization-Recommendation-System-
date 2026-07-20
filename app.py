import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Nassau Candy - Factory Optimization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DARK THEME CUSTOM CSS
# ============================================================
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
    .title-text {
        color: #00d4ff;
        font-size: 36px;
        font-weight: bold;
    }
    .subtitle-text {
        color: #a0a0a0;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau_Candy_Distributor.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
    df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

    factory_map = {
        'Wonka Bar - Nutty Crunch Surprise': "Lot's O' Nuts",
        'Wonka Bar - Fudge Mallows': "Lot's O' Nuts",
        'Wonka Bar -Scrumdiddlyumptious': "Lot's O' Nuts",
        'Wonka Bar - Milk Chocolate': "Wicked Choccy's",
        'Wonka Bar - Triple Dazzle Caramel': "Wicked Choccy's",
        'Laffy Taffy': 'Sugar Shack',
        'SweeTARTS': 'Sugar Shack',
        'Nerds': 'Sugar Shack',
        'Fun Dip': 'Sugar Shack',
        'Fizzy Lifting Drinks': 'Sugar Shack',
        'Everlasting Gobstopper': 'Secret Factory',
        'Hair Toffee': 'The Other Factory',
        'Lickable Wallpaper': 'Secret Factory',
        'Wonka Gum': 'Secret Factory',
        'Kazookles': 'The Other Factory'
    }
    df['Factory'] = df['Product Name'].map(factory_map)
    return df

df = load_data()

# ============================================================
# FACTORY DATA
# ============================================================
factory_coords = pd.DataFrame({
    'Factory': ["Lot's O' Nuts", "Wicked Choccy's", 
                'Sugar Shack', 'Secret Factory', 'The Other Factory'],
    'Latitude': [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
    'Longitude': [-111.768036, -81.088371, -96.18115, -90.565487, -89.971107]
})

factory_avg_leadtime = df.groupby('Factory')['Lead Time'].mean().round(2)
factory_avg_profit = df.groupby('Factory')['Gross Profit'].mean().round(2)

# ============================================================
# RECOMMENDATION ENGINE
# ============================================================
def generate_recommendations(priority=0.5):
    recommendations = []
    for product in df['Product Name'].unique():
        product_df = df[df['Product Name'] == product]
        current_factory = product_df['Factory'].iloc[0]
        current_lead_time = product_df['Lead Time'].mean()
        current_profit = product_df['Gross Profit'].mean()

        best_factory = current_factory
        best_score = float('inf')

        for factory in factory_avg_leadtime.index:
            lead_score = factory_avg_leadtime[factory]
            profit_score = -factory_avg_profit[factory]
            combined_score = (priority * lead_score) + ((1 - priority) * profit_score)

            if combined_score < best_score:
                best_score = combined_score
                best_factory = factory

        best_lead_time = factory_avg_leadtime[best_factory]
        improvement = round(current_lead_time - best_lead_time, 2)

        recommendations.append({
            'Product': product,
            'Division': product_df['Division'].iloc[0],
            'Current Factory': current_factory,
            'Recommended Factory': best_factory,
            'Current Lead Time': round(current_lead_time, 2),
            'Predicted Lead Time': round(best_lead_time, 2),
            'Improvement (Days)': improvement,
            'Avg Gross Profit': round(current_profit, 2),
            'Risk': 'Low' if improvement > 50 else 'Medium' if improvement > 0 else 'High'
        })

    return pd.DataFrame(recommendations).sort_values(
        'Improvement (Days)', ascending=False)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
st.sidebar.title("Nassau Candy")
st.sidebar.markdown("**Factory Optimization System**")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "Home Dashboard",
    "Factory Optimizer",
    "What-If Scenario",
    "Recommendations",
    "Risk & Impact"
])

# Sidebar Filters
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
selected_region = st.sidebar.selectbox(
    "Region", ["All"] + list(df['Region'].unique()))
selected_ship_mode = st.sidebar.selectbox(
    "Ship Mode", ["All"] + list(df['Ship Mode'].unique()))
priority_slider = st.sidebar.slider(
    "Optimization Priority",
    min_value=0.0, max_value=1.0, value=0.5, step=0.1,
    help="0 = Profit Focus | 1 = Speed Focus"
)
st.sidebar.markdown(
    f"{'Speed Focus' if priority_slider > 0.7 else 'Profit Focus' if priority_slider < 0.3 else 'Balanced'}")

# Apply filters
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_ship_mode != "All":
    filtered_df = filtered_df[filtered_df['Ship Mode'] == selected_ship_mode]

# ============================================================
# PAGE 1 - HOME DASHBOARD
# ============================================================
if page == "Home Dashboard":
    st.markdown('<p class="title-text">Nassau Candy Factory Optimization</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Factory Reallocation & Shipping Optimization Recommendation System</p>',
                unsafe_allow_html=True)
    st.markdown("---")

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Orders", f"{len(filtered_df):,}")
    with col2:
        st.metric("Avg Lead Time",
                  f"{filtered_df['Lead Time'].mean():.0f} days")
    with col3:
        st.metric("Avg Gross Profit",
                  f"${filtered_df['Gross Profit'].mean():.2f}")
    with col4:
        st.metric("Active Factories", "5")

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Lead Time by Factory")
        factory_lt = filtered_df.groupby(
            'Factory')['Lead Time'].mean().reset_index()
        fig = px.bar(factory_lt, x='Factory', y='Lead Time',
                     color='Lead Time', color_continuous_scale='blues',
                     template='plotly_dark')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Profit by Division")
        div_profit = filtered_df.groupby(
            'Division')['Gross Profit'].mean().reset_index()
        fig = px.pie(div_profit, names='Division', values='Gross Profit',
                     template='plotly_dark',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)

    # Charts Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orders by Ship Mode")
        ship_counts = filtered_df['Ship Mode'].value_counts().reset_index()
        ship_counts.columns = ['Ship Mode', 'Count']
        fig = px.bar(ship_counts, x='Ship Mode', y='Count',
                     color='Count', color_continuous_scale='teal',
                     template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Factory Locations")
        fig = px.scatter_geo(factory_coords,
                             lat='Latitude', lon='Longitude',
                             text='Factory', scope='usa',
                             template='plotly_dark',
                             size=[20, 20, 20, 20, 20])
        fig.update_traces(textposition='top center',
                          marker=dict(color='cyan', size=15))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE 2 - FACTORY OPTIMIZER
# ============================================================
elif page == "Factory Optimizer":
    st.title("Factory Optimization Simulator")
    st.markdown("Select a product to see its predicted performance across all factories")
    st.markdown("---")

    selected_product = st.selectbox(
        "Select Product", sorted(df['Product Name'].unique()))

    product_df = df[df['Product Name'] == selected_product]
    current_factory = product_df['Factory'].iloc[0]

    st.markdown(f"**Current Factory:** `{current_factory}`")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Lead Time",
                  f"{product_df['Lead Time'].mean():.0f} days")
    with col2:
        st.metric("Avg Gross Profit",
                  f"${product_df['Gross Profit'].mean():.2f}")
    with col3:
        st.metric("Total Orders", f"{len(product_df):,}")

    st.markdown("---")

    # Performance across all factories
    st.subheader("Performance Across All Factories")

    factory_comparison = []
    for factory in factory_avg_leadtime.index:
        factory_comparison.append({
            'Factory': factory,
            'Avg Lead Time': factory_avg_leadtime[factory],
            'Avg Profit': factory_avg_profit[factory],
            'Is Current': 'Current' if factory == current_factory else 'Alternative'
        })

    comp_df = pd.DataFrame(factory_comparison)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(comp_df, x='Factory', y='Avg Lead Time',
                     color='Is Current',
                     color_discrete_map={
                         'Current': 'orange', 'Alternative': 'cyan'},
                     template='plotly_dark',
                     title='Lead Time Comparison')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(comp_df, x='Factory', y='Avg Profit',
                     color='Is Current',
                     color_discrete_map={
                         'Current': 'orange', 'Alternative': 'green'},
                     template='plotly_dark',
                     title='Profit Comparison')
        st.plotly_chart(fig, use_container_width=True)

    # Best recommendation
    best_factory = factory_avg_leadtime.idxmin()
    best_lt = factory_avg_leadtime.min()
    improvement = product_df['Lead Time'].mean() - best_lt

    if improvement > 0:
        st.success(
            f"Recommended: Move to **{best_factory}** — Save **{improvement:.0f} days**!")
    else:
        st.info(
            f"**{current_factory}** is already optimal for this product!")

# ============================================================
# PAGE 3 - WHAT-IF SCENARIO
# ============================================================
elif page == "What-If Scenario":
    st.title("What-If Scenario Analysis")
    st.markdown("Compare current vs recommended factory assignments")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        scenario_product = st.selectbox(
            "Select Product", sorted(df['Product Name'].unique()))
    with col2:
        scenario_factory = st.selectbox(
            "Select Alternative Factory",
            factory_avg_leadtime.index.tolist())

    product_df = df[df['Product Name'] == scenario_product]
    current_factory = product_df['Factory'].iloc[0]
    current_lt = product_df['Lead Time'].mean()
    current_profit = product_df['Gross Profit'].mean()

    new_lt = factory_avg_leadtime[scenario_factory]
    new_profit = factory_avg_profit[scenario_factory]

    st.markdown("---")
    st.subheader("Side by Side Comparison")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Current Assignment")
        st.info(f"**Factory:** {current_factory}")
        st.metric("Lead Time", f"{current_lt:.0f} days")
        st.metric("Gross Profit", f"${current_profit:.2f}")

    with col2:
        st.markdown("### Proposed Assignment")
        st.success(f"**Factory:** {scenario_factory}")
        delta_lt = new_lt - current_lt
        delta_profit = new_profit - current_profit
        st.metric("Lead Time", f"{new_lt:.0f} days",
                  delta=f"{delta_lt:.0f} days",
                  delta_color="inverse")
        st.metric("Gross Profit", f"${new_profit:.2f}",
                  delta=f"${delta_profit:.2f}")

    st.markdown("---")

    # Visual comparison
    comparison_data = pd.DataFrame({
        'Scenario': ['Current', 'Proposed'],
        'Lead Time': [current_lt, new_lt],
        'Gross Profit': [current_profit, new_profit]
    })

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(comparison_data, x='Scenario', y='Lead Time',
                     color='Scenario',
                     color_discrete_map={
                         'Current': 'orange', 'Proposed': 'cyan'},
                     template='plotly_dark',
                     title='Lead Time: Current vs Proposed')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(comparison_data, x='Scenario', y='Gross Profit',
                     color='Scenario',
                     color_discrete_map={
                         'Current': 'orange', 'Proposed': 'green'},
                     template='plotly_dark',
                     title='Profit: Current vs Proposed')
        st.plotly_chart(fig, use_container_width=True)

    # Verdict
    if delta_lt < 0:
        st.success(
            f"This move saves **{abs(delta_lt):.0f} days** in lead time!")
    elif delta_lt > 0:
        st.warning(
            f"This move INCREASES lead time by **{delta_lt:.0f} days**!")
    else:
        st.info("No change in lead time for this move.")

# ============================================================
# PAGE 4 - RECOMMENDATIONS
# ============================================================
elif page == "Recommendations":
    st.title("Factory Reassignment Recommendations")
    st.markdown("Ranked factory reassignment suggestions with expected efficiency gains")
    st.markdown("---")

    recommendations_df = generate_recommendations(priority_slider)

    # Summary KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", len(recommendations_df))
    with col2:
        st.metric("Products to Reassign",
                  len(recommendations_df[recommendations_df['Improvement (Days)'] > 0]))
    with col3:
        st.metric("Max Improvement",
                  f"{recommendations_df['Improvement (Days)'].max():.0f} days")
    with col4:
        st.metric("Avg Improvement",
                  f"{recommendations_df['Improvement (Days)'].mean():.0f} days")

    st.markdown("---")

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        division_filter = st.multiselect(
            "Filter by Division",
            options=recommendations_df['Division'].unique(),
            default=recommendations_df['Division'].unique())
    with col2:
        show_only_improvements = st.checkbox(
            "Show only products that benefit from reassignment", value=False)

    filtered_recs = recommendations_df[
        recommendations_df['Division'].isin(division_filter)]
    if show_only_improvements:
        filtered_recs = filtered_recs[
            filtered_recs['Improvement (Days)'] > 0]

    # Color coded table
    st.subheader("Recommendation Table")

    def color_improvement(val):
        if val > 50:
            return 'background-color: #1a472a; color: white'
        elif val > 0:
            return 'background-color: #4a3800; color: white'
        else:
            return 'background-color: #4a1c1c; color: white'

    styled_df = filtered_recs.style.applymap(
        color_improvement, subset=['Improvement (Days)'])
    st.dataframe(styled_df, use_container_width=True)

    # Chart
    st.subheader("Improvement by Product")
    fig = px.bar(filtered_recs, x='Product', y='Improvement (Days)',
                 color='Improvement (Days)',
                 color_continuous_scale='RdYlGn',
                 template='plotly_dark',
                 title='Lead Time Improvement by Product (Days)')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE 5 - RISK & IMPACT
# ============================================================
elif page == "Risk & Impact":
    st.title("Risk & Impact Panel")
    st.markdown("Profit impact alerts and high-risk reassignment warnings")
    st.markdown("---")

    recommendations_df = generate_recommendations(priority_slider)

    # Risk Categories
    low_risk = recommendations_df[recommendations_df['Risk'] == 'Low']
    medium_risk = recommendations_df[recommendations_df['Risk'] == 'Medium']
    high_risk = recommendations_df[recommendations_df['Risk'] == 'High']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"Low Risk: {len(low_risk)} products")
    with col2:
        st.warning(f"Medium Risk: {len(medium_risk)} products")
    with col3:
        st.error(f"High Risk: {len(high_risk)} products")

    st.markdown("---")

    # High Risk Products
    st.subheader("High Risk Reassignments")
    st.markdown("These products should NOT be reassigned — lead time would increase!")
    if len(high_risk) > 0:
        st.dataframe(high_risk[[
            'Product', 'Current Factory',
            'Recommended Factory', 'Improvement (Days)',
            'Avg Gross Profit']], use_container_width=True)
    else:
        st.success("No high risk reassignments!")

    st.markdown("---")

    # Profit Impact
    st.subheader("Profit Impact Analysis")
    fig = px.scatter(recommendations_df,
                     x='Improvement (Days)',
                     y='Avg Gross Profit',
                     color='Risk',
                     size='Avg Gross Profit',
                     hover_name='Product',
                     color_discrete_map={
                         'Low': 'green',
                         'Medium': 'yellow',
                         'High': 'red'},
                     template='plotly_dark',
                     title='Lead Time Improvement vs Profit Impact')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Factory Risk Summary
    st.subheader("Factory Performance Summary")
    factory_summary = pd.DataFrame({
        'Factory': factory_avg_leadtime.index,
        'Avg Lead Time': factory_avg_leadtime.values,
        'Avg Profit': factory_avg_profit.values,
        'Status': ['Slow' if lt > factory_avg_leadtime.mean()
                   else 'Fast' for lt in factory_avg_leadtime.values]
    })
    st.dataframe(factory_summary, use_container_width=True)

    # Map
    st.subheader("Factory Risk Map")
    factory_map_df = factory_coords.merge(
        factory_summary, on='Factory')
    fig = px.scatter_geo(factory_map_df,
                         lat='Latitude', lon='Longitude',
                         text='Factory', scope='usa',
                         color='Status',
                         color_discrete_map={
                             'Slow': 'red', 'Fast': 'green'},
                         template='plotly_dark',
                         title='Factory Status Map')
    fig.update_traces(textposition='top center', marker=dict(size=15))
    st.plotly_chart(fig, use_container_width=True)