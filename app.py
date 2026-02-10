import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="Andy's Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for polish (spacing, typography)
st.markdown("""
<style>
    :root {
        --accent: #14b8a6;
        --accent-light: rgba(20, 184, 166, 0.1);
        --accent-hover: #0d9488;
    }
    
    .header-container {
        padding: 5px 0;
        margin-bottom: 20px;
    }
    
    .status-row {
        display: flex;
        gap: 20px;
        margin-top: 10px;
        font-size: 0.85rem;
        color: #bbb;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 32px 0 20px 0;
        color: #ffffff;
        letter-spacing: -0.3px;
        border-left: 3px solid var(--accent);
        padding-left: 12px;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 8px !important;
        letter-spacing: -1px;
    }
    
    p, span, div, button {
        color: #ffffff !important;
    }
    
    /* Metric Cards - Enhanced */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.05) 0%, rgba(20, 184, 166, 0.02) 100%) !important;
        border: 1px solid rgba(20, 184, 166, 0.2) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 24px rgba(20, 184, 166, 0.25) !important;
        border-color: var(--accent) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        letter-spacing: -1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #aaa !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.2) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4) !important;
    }
    
    .stButton button:active {
        transform: translateY(0) !important;
    }
    
    /* Checkboxes & Inputs */
    .stCheckbox {
        margin: 10px 0 !important;
    }
    
    .stCheckbox label {
        font-weight: 500 !important;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        background: rgba(20, 184, 166, 0.05) !important;
        border: 1px solid rgba(20, 184, 166, 0.15) !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stExpander"]:hover {
        border-color: var(--accent) !important;
        box-shadow: 0 2px 8px rgba(20, 184, 166, 0.1) !important;
    }
    
    [data-testid="stExpander"] button {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #0f1419 !important;
        border-right: 1px solid rgba(20, 184, 166, 0.1) !important;
    }
    
    /* Data tables */
    .stDataFrame {
        background: rgba(20, 184, 166, 0.03) !important;
        border: 1px solid rgba(20, 184, 166, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* Sliders */
    .stSlider {
        margin: 12px 0 !important;
    }
    
    .stSlider [role="slider"] {
        accent-color: var(--accent) !important;
    }
    
    /* Plotly Charts - Animation */
    .plotly {
        animation: fadeIn 0.6s ease-in-out !important;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Clean dividers */
    hr {
        border: none !important;
        border-top: 1px solid rgba(20, 184, 166, 0.1) !important;
        margin: 24px 0 !important;
    }
    
    /* Success/info messages */
    .stSuccess, .stInfo, .stWarning {
        border-left: 4px solid var(--accent) !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
DATA_FILE = Path("data.xlsx")

@st.cache_data(show_spinner="Loading Excel data...")
def load_data(file_path: Path, cache_version: int = 2) -> pd.DataFrame:
    """Load Excel file and return DataFrame."""
    if not file_path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(file_path)
        
        # Automatically detect and parse date columns
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
        
        return df
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        return pd.DataFrame()

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")

def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return list of numeric columns."""
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """Return list of categorical/string columns."""
    return [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]

# ============================================================================
# DATA VALIDATION & LOAD
# ============================================================================
df = load_data(DATA_FILE)

# Validate file exists and has data
if not DATA_FILE.exists():
    st.error("❌ **File not found**")
    st.info(f"Expected location: `{DATA_FILE.resolve()}`\n\nPlace `data.xlsx` next to `app.py` and reload the app.")
    st.stop()

if df.empty:
    st.warning("⚠️ **Excel file is empty**")
    st.info("Check that `data.xlsx` contains data and reload.")
    st.stop()

original_row_count = len(df)
original_col_count = len(df.columns)

# ============================================================================
# HEADER: TITLE + METADATA
# ============================================================================
st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.markdown("# 📊 Andy's Analytics")
st.markdown("Interactive exploration of your data with filters, analytics, and visualizations.")
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR: CONTROL CENTER
# ============================================================================
st.sidebar.markdown("### 🎛️ Control Center")

# --- Data Controls ---
with st.sidebar.expander("📂 **Data Controls**", expanded=True):
    reload_col = st.columns(1)[0]
    with reload_col:
        if st.button("🔄 Reload Data", use_container_width=True, key="reload_btn"):
            st.cache_data.clear()
            st.rerun()
    
    file_status = "✅ Found" if DATA_FILE.exists() else "❌ Missing"
    st.caption(f"File status: {file_status}")
    st.markdown("")

# --- Filters ---
st.sidebar.markdown("")
filtered_df = df.copy()

with st.sidebar.expander("🔍 **Filters**", expanded=True):
    # Categorical filter (default: Product)
    categorical_cols = get_categorical_columns(filtered_df)
    if "Product" in categorical_cols:
        products = sorted(filtered_df["Product"].dropna().astype(str).unique().tolist())
        selected_products = []
        
        st.write("**📦 Products**")
        cols = st.columns(2)  # 2 columns for compact layout
        for i, product in enumerate(products):
            with cols[i % 2]:
                if st.checkbox(product, value=True, key=f"prod_{product}"):
                    selected_products.append(product)
        
        # If none selected, select all by default
        if not selected_products:
            selected_products = products
            st.info("No products selected. Showing all.")
        
        filtered_df = filtered_df[filtered_df["Product"].astype(str).isin(selected_products)]
        st.markdown("")  # Add spacing
    elif categorical_cols:
        # Fallback to first categorical column
        default_cat = categorical_cols[0]
        categories = sorted(filtered_df[default_cat].dropna().astype(str).unique().tolist())
        selected_cats = []
        
        st.write(f"**{default_cat}**")
        cols = st.columns(2)
        for i, cat in enumerate(categories):
            with cols[i % 2]:
                if st.checkbox(cat, value=True, key=f"cat_{cat}"):
                    selected_cats.append(cat)
        
        if not selected_cats:
            selected_cats = categories
        
        filtered_df = filtered_df[filtered_df[default_cat].astype(str).isin(selected_cats)]
        st.markdown("")  # Add spacing
    
    # Numeric range filters
    numeric_cols = get_numeric_columns(filtered_df)
    if numeric_cols:
        st.caption("**Numeric Ranges**")
        for col in numeric_cols:
            col_min = float(filtered_df[col].min())
            col_max = float(filtered_df[col].max())
            
            if col_min == col_max:
                continue
            
            selected_range = st.slider(
                label=col,
                min_value=col_min,
                max_value=col_max,
                value=(col_min, col_max),
                key=f"range_{col}"
            )
            filtered_df = filtered_df[
                (filtered_df[col] >= selected_range[0]) & 
                (filtered_df[col] <= selected_range[1])
            ]

# Empty filter check
if filtered_df.empty:
    st.warning("🚫 **No rows match your filters.** Please adjust filters in the sidebar.")
    st.stop()

# --- Visualization Controls ---
st.sidebar.markdown("")
numeric_cols = get_numeric_columns(filtered_df)

with st.sidebar.expander("📈 **Visualization**", expanded=True):
    chart_type = st.selectbox(
        "Chart Type",
        options=["Bar", "Line", "Area", "Scatter", "Pie"],
        index=0,
        key="chart_type_select"
    )
    
    st.caption("**Axes**")
    x_axis = st.selectbox("X-axis", options=filtered_df.columns, index=0, key="x_select")
    
    default_y_idx = 0
    if numeric_cols and (numeric_cols[0] in filtered_df.columns):
        default_y_idx = list(filtered_df.columns).index(numeric_cols[0])
    
    y_axis = st.selectbox("Y-axis", options=filtered_df.columns, index=default_y_idx, key="y_select")
    
    sort_desc = st.checkbox("Sort by Y (descending)", value=False, key="sort_toggle")

# --- Export Controls ---
st.sidebar.markdown("")
with st.sidebar.expander("📥 **Export**", expanded=False):
    st.download_button(
        label="⬇️ Download Filtered Data (CSV)",
        data=to_csv_bytes(filtered_df),
        file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.download_button(
        label="⬇️ Download Full Data (CSV)",
        data=to_csv_bytes(df),
        file_name=f"full_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================================================================
# MAIN CONTENT: KPIs
# ============================================================================
st.markdown('<h3 class="section-title">📊 Key Metrics</h3>', unsafe_allow_html=True)

if numeric_cols and y_axis in numeric_cols:
    y_data = filtered_df[y_axis].astype(float)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total",
            value=f"{y_data.sum():,.2f}",
            help=f"Sum of {y_axis}"
        )
    
    with col2:
        st.metric(
            label="Average",
            value=f"{y_data.mean():,.2f}",
            help=f"Mean of {y_axis}"
        )
    
    with col3:
        max_idx = y_data.idxmax()
        max_val = y_data.max()
        max_label = f"{filtered_df.loc[max_idx, x_axis]}" if x_axis in filtered_df.columns else "N/A"
        st.metric(
            label="Maximum",
            value=f"{max_val:,.2f}",
            help=f"Max {y_axis} ({max_label})"
        )
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Rows", value=len(filtered_df))
    with col2:
        st.metric(label="Total Columns", value=len(filtered_df.columns))
    with col3:
        st.metric(label="Unique X Values", value=filtered_df[x_axis].nunique())

# ============================================================================
# SALES UNITS & COST ANALYSIS
# ============================================================================
if "Units of Sale" in filtered_df.columns and "Cost per Unit" in filtered_df.columns:
    st.markdown('<h3 class="section-title">📦 Units & Cost Analysis</h3>', unsafe_allow_html=True)
    
    units_data = filtered_df["Units of Sale"].astype(float)
    cost_data = filtered_df["Cost per Unit"].astype(float)
    
    # Units of Sale Metrics
    st.write("**Units of Sale Summary**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Units Sold",
            value=f"{units_data.sum():,.0f}",
            help="Total quantity of all units sold"
        )
    
    with col2:
        st.metric(
            label="Avg Units/Sale",
            value=f"{units_data.mean():,.0f}",
            help="Average units per transaction"
        )
    
    with col3:
        st.metric(
            label="Max Units",
            value=f"{units_data.max():,.0f}",
            help="Highest units in single transaction"
        )
    
    with col4:
        st.metric(
            label="Min Units",
            value=f"{units_data.min():,.0f}",
            help="Lowest units in single transaction"
        )
    
    # Cost per Unit Metrics
    st.write("**Cost per Unit Summary**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Avg Cost/Unit",
            value=f"${cost_data.mean():,.2f}",
            help="Average price per unit across all sales"
        )
    
    with col2:
        st.metric(
            label="Max Cost/Unit",
            value=f"${cost_data.max():,.2f}",
            help="Highest unit price"
        )
    
    with col3:
        st.metric(
            label="Min Cost/Unit",
            value=f"${cost_data.min():,.2f}",
            help="Lowest unit price"
        )
    
    with col4:
        total_revenue = filtered_df["Sales"].sum()
        total_units = units_data.sum()
        blended_cost = total_revenue / total_units if total_units > 0 else 0
        st.metric(
            label="Blended Cost/Unit",
            value=f"${blended_cost:,.2f}",
            help="Overall average (Total Sales / Total Units)"
        )
    
    # Product-level analysis
    st.write("**Product-Level Breakdown**")
    product_analysis = filtered_df.groupby("Product").agg({
        "Sales": "sum",
        "Units of Sale": "sum",
        "Cost per Unit": "mean"
    }).round(2)
    product_analysis.columns = ["Total Sales", "Total Units", "Avg Cost/Unit"]
    product_analysis["Avg Price/Unit"] = (product_analysis["Total Sales"] / product_analysis["Total Units"]).round(2)
    product_analysis = product_analysis.sort_values("Total Sales", ascending=False)
    
    st.dataframe(product_analysis, use_container_width=True)

# ============================================================================
# MAIN CONTENT: DATA PREVIEW + CHART (2-COLUMN LAYOUT)
# ============================================================================
st.markdown('<h3 class="section-title">📋 Data & Visualization</h3>', unsafe_allow_html=True)

col_data, col_chart = st.columns([1, 1.2])

# --- Left: Data Preview ---
with col_data:
    st.subheader("Data Preview")
    
    with st.expander("Show options", expanded=False):
        preview_mode = st.radio("Display", options=["Head (20 rows)", "Full"], horizontal=True)
        show_dtypes = st.checkbox("Show column types", value=False)
    
    if preview_mode == "Head (20 rows)":
        display_df = filtered_df.head(20)
    else:
        display_df = filtered_df
    
    if show_dtypes:
        st.write("**Column Types:**")
        dtype_df = pd.DataFrame({
            "Column": filtered_df.columns,
            "Type": filtered_df.dtypes.astype(str)
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)
    
    st.dataframe(display_df, use_container_width=True)

# --- Right: Chart ---
with col_chart:
    st.subheader("Chart")
    
    # Validation
    validation_error = None
    if x_axis == y_axis:
        validation_error = "❌ X-axis and Y-axis cannot be the same. Choose different columns."
    elif chart_type in ["Bar", "Line", "Area", "Scatter"] and not pd.api.types.is_numeric_dtype(filtered_df[y_axis]):
        validation_error = f"❌ Y-axis must be numeric for {chart_type} charts. Choose a numeric column."
    elif chart_type == "Pie" and not pd.api.types.is_numeric_dtype(filtered_df[y_axis]):
        validation_error = "❌ Y-axis must be numeric for Pie charts. Choose a numeric column."
    
    if validation_error:
        st.warning(validation_error)
    else:
        # Check if Date column exists for toggle
        date_cols = filtered_df.select_dtypes(include=['datetime64']).columns.tolist()
        has_date_col = len(date_cols) > 0
        
        # --- Chart View Toggle ---
        if has_date_col and y_axis in numeric_cols:
            view_mode_index = st.radio(
                "View by:",
                options=[0, 1],
                format_func=lambda x: ["📈 By Time Period", "📦 By Product"][x],
                horizontal=True,
                label_visibility="collapsed",
                key="main_chart_toggle"
            )
        else:
            view_mode_index = 0
        
        try:
            if view_mode_index == 0 and has_date_col:
                # Time-based view: X-axis is dates, Y-axis is sales
                date_col = date_cols[0]
                time_df = filtered_df[[date_col, y_axis]].sort_values(date_col)
                
                if chart_type == "Bar":
                    fig = px.bar(
                        time_df,
                        x=date_col,
                        y=y_axis,
                        title=f"{y_axis} Over Time",
                        labels={y_axis: y_axis, date_col: "Date"}
                    )
                elif chart_type == "Line":
                    fig = px.line(
                        time_df,
                        x=date_col,
                        y=y_axis,
                        markers=True,
                        title=f"{y_axis} Over Time",
                        labels={y_axis: y_axis, date_col: "Date"}
                    )
                elif chart_type == "Area":
                    fig = px.area(
                        time_df,
                        x=date_col,
                        y=y_axis,
                        title=f"{y_axis} Over Time",
                        labels={y_axis: y_axis, date_col: "Date"}
                    )
                elif chart_type == "Scatter":
                    fig = px.scatter(
                        time_df,
                        x=date_col,
                        y=y_axis,
                        title=f"{y_axis} Over Time",
                        labels={y_axis: y_axis, date_col: "Date"}
                    )
                else:  # Pie
                    fig = px.bar(
                        time_df,
                        x=date_col,
                        y=y_axis,
                        title=f"{y_axis} Over Time",
                        labels={y_axis: y_axis, date_col: "Date"}
                    )
            else:
                # By Product view: X-axis is product, Y-axis is summed sales
                product_df = filtered_df.groupby("Product")[y_axis].sum().sort_values(ascending=False).reset_index()
                
                if chart_type == "Bar":
                    fig = px.bar(
                        product_df,
                        x="Product",
                        y=y_axis,
                        title=f"{y_axis} by Product",
                        labels={y_axis: y_axis, "Product": "Product"}
                    )
                elif chart_type == "Line":
                    fig = px.line(
                        product_df,
                        x="Product",
                        y=y_axis,
                        markers=True,
                        title=f"{y_axis} by Product",
                        labels={y_axis: y_axis, "Product": "Product"}
                    )
                elif chart_type == "Area":
                    fig = px.area(
                        product_df,
                        x="Product",
                        y=y_axis,
                        title=f"{y_axis} by Product",
                        labels={y_axis: y_axis, "Product": "Product"}
                    )
                elif chart_type == "Scatter":
                    fig = px.scatter(
                        product_df,
                        x="Product",
                        y=y_axis,
                        title=f"{y_axis} by Product",
                        labels={y_axis: y_axis, "Product": "Product"}
                    )
                else:  # Pie
                    fig = px.pie(
                        product_df,
                        names="Product",
                        values=y_axis,
                        title=f"{y_axis} by Product"
                    )
            
            # Polish chart formatting with modern styling
            layout_config = {
                "showlegend": True,
                "font": dict(size=11, family="Source Sans Pro"),
                "margin": dict(l=0, r=0, t=40, b=0),
                "plot_bgcolor": "rgba(0,0,0,0)",
                "paper_bgcolor": "rgba(0,0,0,0)",
                "transition": dict(duration=500, easing="cubic-in-out")
            }
            
            # Set chart-specific title and axis labels based on view
            if chart_type == "Pie":
                layout_config["title"] = dict(
                    text=f"{y_axis} Distribution",
                    font=dict(size=14, color="#ffffff", family="Source Sans Pro")
                )
                layout_config["hovermode"] = "closest"
            else:
                # Determine axis label based on view mode
                x_label = "Date" if view_mode_index == 0 else "Product"
                
                layout_config["title"] = dict(
                    text=f"{y_axis} by {x_label}",
                    font=dict(size=14, color="#ffffff", family="Source Sans Pro")
                )
                layout_config["hovermode"] = "x unified"
                layout_config["xaxis"] = dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor="rgba(20, 184, 166, 0.1)",
                    zeroline=False
                )
                layout_config["yaxis"] = dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor="rgba(20, 184, 166, 0.1)",
                    zeroline=False
                )
            
            fig.update_layout(**layout_config)
            
            # Apply accent color to traces based on chart type
            if chart_type == "Pie":
                # For pie charts, only set marker border
                fig.update_traces(marker=dict(line=dict(color="rgba(13, 148, 136, 0.5)", width=2)))
            elif chart_type in ["Bar"]:
                # For bar charts, use marker color
                fig.update_traces(marker=dict(color="#14b8a6", line=dict(color="#0d9488", width=0.5)))
            elif chart_type in ["Line", "Area"]:
                # For line/area charts, use line color and fill
                fig.update_traces(
                    line=dict(color="#14b8a6", width=2),
                    fillcolor="rgba(20, 184, 166, 0.2)"
                )
            elif chart_type == "Scatter":
                # For scatter, use marker
                fig.update_traces(
                    marker=dict(color="#14b8a6", size=8, line=dict(color="#0d9488", width=1))
                )
            
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        except Exception as e:
            st.error(f"Error creating chart: {e}")

# ============================================================================
# UNITS & COST VISUALIZATION
# ============================================================================
if "Units of Sale" in filtered_df.columns and "Cost per Unit" in filtered_df.columns:
    st.markdown('<h3 class="section-title">📊 Units vs Cost Analysis</h3>', unsafe_allow_html=True)
    
    viz_col1, viz_col2 = st.columns([1, 1.2])
    
    with viz_col1:
        st.subheader("Units by Product")
        product_units = filtered_df.groupby("Product")["Units of Sale"].sum().sort_values(ascending=False)
        
        units_fig = px.bar(
            x=product_units.values,
            y=product_units.index,
            orientation='h',
            title="Total Units Sold by Product",
            labels={"x": "Units", "y": "Product"}
        )
        
        units_fig.update_layout(
            font=dict(size=11, family="Source Sans Pro"),
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title=dict(text="Total Units Sold by Product", font=dict(size=14, color="#ffffff", family="Source Sans Pro")),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
            yaxis=dict(showgrid=False),
            hovermode="y unified"
        )
        
        units_fig.update_traces(marker=dict(color="#14b8a6", line=dict(color="#0d9488", width=0.5)))
        st.plotly_chart(units_fig, use_container_width=True, config={"displayModeBar": False})
    
    with viz_col2:
        st.subheader("Cost per Unit Analysis")
        product_cost = filtered_df.groupby("Product")["Cost per Unit"].mean().sort_values(ascending=False)
        
        cost_fig = px.bar(
            x=product_cost.index,
            y=product_cost.values,
            title="Average Cost per Unit by Product",
            labels={"x": "Product", "y": "Cost per Unit ($)"}
        )
        
        cost_fig.update_layout(
            font=dict(size=11, family="Source Sans Pro"),
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title=dict(text="Average Cost per Unit by Product", font=dict(size=14, color="#ffffff", family="Source Sans Pro")),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
            hovermode="x unified"
        )
        
        cost_fig.update_traces(marker=dict(color="#14b8a6", line=dict(color="#0d9488", width=0.5)))
        st.plotly_chart(cost_fig, use_container_width=True, config={"displayModeBar": False})
    
    # Scatter plot: Sales vs Units
    st.subheader("Sales Revenue vs Units Sold")
    scatter_fig = px.scatter(
        filtered_df,
        x="Units of Sale",
        y="Sales",
        color="Product",
        size="Cost per Unit",
        hover_data={"Date": True},
        title="Sales by Units Sold (size = Cost per Unit)",
        labels={"Units of Sale": "Units Sold", "Sales": "Revenue ($)"}
    )
    
    scatter_fig.update_layout(
        font=dict(size=11, family="Source Sans Pro"),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Sales by Units Sold (size = Cost per Unit)", font=dict(size=14, color="#ffffff", family="Source Sans Pro")),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
        hovermode="closest",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    scatter_fig.update_traces(marker=dict(line=dict(color="#0d9488", width=1)))
    st.plotly_chart(scatter_fig, use_container_width=True, config={"displayModeBar": False})

# ============================================================================
# SUMMARY STATISTICS - TIME-BASED INSIGHTS
# ============================================================================
st.markdown('<h3 class="section-title">📈 Time-Based Insights</h3>', unsafe_allow_html=True)

# Check if Date column exists
date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
has_date = len(date_cols) > 0

if has_date and y_axis in numeric_cols:
    date_col = date_cols[0]
    analysis_df = filtered_df.copy()
    
    if len(analysis_df) > 0:
        # --- Trend Analysis ---
        trend_col, growth_col = st.columns([1, 1])
        
        with trend_col:
            st.write("**📊 Trend Analysis**")
            # Calculate trend - first half vs second half
            mid_point = len(analysis_df) // 2
            first_half_avg = analysis_df[y_axis].iloc[:mid_point].mean()
            second_half_avg = analysis_df[y_axis].iloc[mid_point:].mean()
            trend_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100 if first_half_avg != 0 else 0
            
            if trend_change > 0:
                trend_indicator = f"📈 **+{trend_change:.1f}%** Uptrend"
                trend_color = "green"
            elif trend_change < 0:
                trend_indicator = f"📉 **{trend_change:.1f}%** Downtrend"
                trend_color = "red"
            else:
                trend_indicator = "➡️ **Stable** (No trend)"
                trend_color = "blue"
            
            st.metric(label="Overall Trend", value=trend_indicator, delta=f"Period-over-period")
            st.caption(f"Early avg: {first_half_avg:,.0f} → Recent avg: {second_half_avg:,.0f}")
        
        with growth_col:
            st.write("**💹 Growth Metrics**")
            # Calculate growth rate
            earliest_value = analysis_df[y_axis].iloc[0]
            latest_value = analysis_df[y_axis].iloc[-1]
            total_growth = ((latest_value - earliest_value) / earliest_value) * 100 if earliest_value != 0 else 0
            
            st.metric(label="Overall Growth", value=f"{total_growth:+.1f}%", delta=f"First to last record")
            st.caption(f"Start: {earliest_value:,.0f} → End: {latest_value:,.0f}")
        
        # --- Peak vs Average Analysis ---
        st.write("**🎯 Peak vs Average Analysis**")
        peak_value = analysis_df[y_axis].max()
        peak_product = str(analysis_df.loc[analysis_df[y_axis].idxmax(), x_axis]) if x_axis in analysis_df.columns else "N/A"
        avg_value = analysis_df[y_axis].mean()
        peak_vs_avg = ((peak_value - avg_value) / avg_value) * 100 if avg_value != 0 else 0
        
        peak_col, avg_col, variance_col = st.columns(3)
        
        with peak_col:
            st.metric(label="Peak Value", value=f"{peak_value:,.0f}", delta=peak_product)
        
        with avg_col:
            st.metric(label="Average Value", value=f"{avg_value:,.0f}")
        
        with variance_col:
            st.metric(label="Peak vs Avg", value=f"+{peak_vs_avg:.1f}%")
        
        # --- View Toggle for Trend Chart ---
        st.write("**📊 Visualization View**")
        stats_view_index = st.radio(
            "Choose view:",
            options=[0, 1],
            format_func=lambda x: ["📉 By Time Period", "📦 By Product"][x],
            horizontal=True,
            label_visibility="collapsed",
            key="stats_view_toggle"
        )
        
        if stats_view_index == 0:
            # --- Time Series Trend Line ---
            trend_df = analysis_df[[date_col, y_axis]].sort_values(date_col)
            
            # Create trend chart
            trend_fig = px.line(
                trend_df,
                x=date_col,
                y=y_axis,
                markers=True,
                title=f"{y_axis} Over Time",
                labels={y_axis: y_axis, date_col: "Date"}
            )
            
            # Add trendline
            trend_fig.add_scatter(
                x=trend_df[date_col],
                y=trend_df[y_axis].rolling(window=min(3, len(trend_df))).mean(),
                mode='lines',
                name='Trend',
                line=dict(color='rgba(20, 184, 166, 0.5)', dash='dash', width=2)
            )
            
            trend_fig.update_layout(
                hovermode="x unified",
                font=dict(size=11, family="Source Sans Pro"),
                margin=dict(l=0, r=0, t=40, b=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title=dict(text=f"{y_axis} Over Time", font=dict(size=14, color="#ffffff", family="Source Sans Pro")),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
                transition=dict(duration=500, easing="cubic-in-out")
            )
            
            trend_fig.update_traces(
                marker=dict(color="#14b8a6", size=8, line=dict(color="#0d9488", width=1)),
                line=dict(color="#14b8a6", width=2),
                selector=dict(mode='lines+markers')
            )
            
            st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})
        
        else:  # By Product view
            # Create product comparison chart - group by Product, not x_axis
            product_df = analysis_df.groupby("Product")[y_axis].sum().sort_values(ascending=False).reset_index()
            
            product_fig = px.bar(
                product_df,
                x="Product",
                y=y_axis,
                title=f"{y_axis} by Product",
                labels={y_axis: y_axis, "Product": "Product"}
            )
            
            product_fig.update_layout(
                hovermode="x unified",
                font=dict(size=11, family="Source Sans Pro"),
                margin=dict(l=0, r=0, t=40, b=0),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title=dict(text=f"{y_axis} by {x_axis}", font=dict(size=14, color="#ffffff", family="Source Sans Pro")),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(20, 184, 166, 0.1)"),
                transition=dict(duration=500, easing="cubic-in-out")
            )
            
            product_fig.update_traces(
                marker=dict(color="#14b8a6", line=dict(color="#0d9488", width=0.5))
            )
            
            st.plotly_chart(product_fig, use_container_width=True, config={"displayModeBar": False})
        
        
        # --- Distribution Analysis ---
        with st.expander("📊 Detailed Statistics & Distribution", expanded=False):
            stat_col, dist_col = st.columns([1, 1])
            
            with stat_col:
                st.write(f"**{y_axis} - Descriptive Statistics**")
                st.dataframe(
                    analysis_df[y_axis].describe().to_frame(),
                    use_container_width=True
                )
            
            with dist_col:
                st.write(f"**{y_axis} - Distribution**")
                hist_fig = px.histogram(
                    analysis_df,
                    x=y_axis,
                    nbins=20,
                    title=f"{y_axis} Distribution",
                    labels={y_axis: y_axis}
                )
                hist_fig.update_layout(
                    showlegend=False,
                    margin=dict(l=0, r=0, t=30, b=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ffffff")
                )
                hist_fig.update_traces(marker=dict(color="#14b8a6", line=dict(color="#0d9488", width=1)))
                st.plotly_chart(hist_fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data to analyze. Adjust your filters.")
else:
    if not has_date:
        st.info("📅 A Date column is required for time-based insights. Data has been updated with dates!")
    elif y_axis not in numeric_cols:
        st.info("📊 Select a numeric column as Y-axis for time-based analysis.")

# ============================================================================
# FOOTER: ROW COUNT
# ============================================================================
st.markdown("---")
st.caption(f"Showing {len(filtered_df):,} rows (filtered from {original_row_count:,}) | {len(filtered_df.columns)} columns")
