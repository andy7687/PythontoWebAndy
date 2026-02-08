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
    .kpi-card {
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #0d7377;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 25px 0 15px 0;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    p, span, div, button {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================
DATA_FILE = Path("data.xlsx")

@st.cache_data(show_spinner="Loading Excel data...")
def load_data(file_path: Path) -> pd.DataFrame:
    """Load Excel file and return DataFrame."""
    if not file_path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(file_path)
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
    if st.button("🔄 Reload Data", use_container_width=True, key="reload_btn"):
        st.cache_data.clear()
        st.rerun()
    
    file_status = "✅ Found" if DATA_FILE.exists() else "❌ Missing"
    st.caption(f"File status: {file_status}")

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
        # Build chart based on selection
        chart_df = filtered_df.copy()
        
        if sort_desc and y_axis in numeric_cols:
            chart_df = chart_df.sort_values(by=y_axis, ascending=False)
        
        try:
            if chart_type == "Bar":
                fig = px.bar(
                    chart_df,
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} by {x_axis}",
                    labels={y_axis: y_axis, x_axis: x_axis}
                )
            elif chart_type == "Line":
                fig = px.line(
                    chart_df,
                    x=x_axis,
                    y=y_axis,
                    markers=True,
                    title=f"{y_axis} over {x_axis}",
                    labels={y_axis: y_axis, x_axis: x_axis}
                )
            elif chart_type == "Area":
                fig = px.area(
                    chart_df,
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} by {x_axis}",
                    labels={y_axis: y_axis, x_axis: x_axis}
                )
            elif chart_type == "Scatter":
                fig = px.scatter(
                    chart_df,
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} vs {x_axis}",
                    labels={y_axis: y_axis, x_axis: x_axis}
                )
            elif chart_type == "Pie":
                fig = px.pie(
                    chart_df,
                    names=x_axis,
                    values=y_axis,
                    title=f"{y_axis} by {x_axis}"
                )
            
            # Polish chart formatting
            fig.update_layout(
                hovermode="x unified",
                showlegend=True,
                font=dict(size=11),
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error creating chart: {e}")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
st.markdown('<h3 class="section-title">📈 Summary Statistics</h3>', unsafe_allow_html=True)

if numeric_cols:
    # Show describe() for the y-axis if it's numeric
    if y_axis in numeric_cols:
        stats_col, dist_col = st.columns([1, 1])
        
        with stats_col:
            st.write(f"**{y_axis} - Descriptive Statistics**")
            st.dataframe(
                filtered_df[y_axis].describe().to_frame(),
                use_container_width=True
            )
        
        with dist_col:
            st.write(f"**{y_axis} - Distribution**")
            hist_fig = px.histogram(
                filtered_df,
                x=y_axis,
                nbins=30,
                title=f"{y_axis} Distribution",
                labels={y_axis: y_axis}
            )
            hist_fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(hist_fig, use_container_width=True)
    
    # Additional numeric columns summary
    other_numeric = [c for c in numeric_cols if c != y_axis]
    if other_numeric:
        with st.expander(f"More columns: {', '.join(other_numeric)}", expanded=False):
            summary_stats = filtered_df[numeric_cols].describe()
            st.dataframe(summary_stats, use_container_width=True)
else:
    st.info("No numeric columns to summarize.")

# ============================================================================
# FOOTER: ROW COUNT
# ============================================================================
st.markdown("---")
st.caption(f"Showing {len(filtered_df):,} rows (filtered from {original_row_count:,}) | {len(filtered_df.columns)} columns")
