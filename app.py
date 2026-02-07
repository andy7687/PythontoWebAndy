import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Python to Browser App", layout="wide")

DATA_FILE = Path("data.xlsx")


@st.cache_data(show_spinner="Loading Excel...")
def load_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        return pd.DataFrame()

    df = pd.read_excel(file_path)
    return df


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


st.title("📊 Python to Browser App")
st.write("Reads Excel data and visualizes it using Streamlit + Plotly.")

# Top controls
top_left, top_right = st.columns([1, 2])
with top_left:
    if st.button("🔄 Reload Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with top_right:
    st.caption(f"Data source: `{DATA_FILE.resolve()}`")

df = load_data(DATA_FILE)

if df.empty:
    if not DATA_FILE.exists():
        st.error("`data.xlsx` not found in the project folder. Put it next to `app.py` and reload.")
    else:
        st.warning("Excel loaded but returned no rows. Check the file contents.")
    st.stop()

# ---- Sidebar: Filters ----
st.sidebar.header("Filters")

filtered_df = df.copy()

# If there is a 'Product' column, provide a multiselect
if "Product" in filtered_df.columns:
    products = sorted(filtered_df["Product"].dropna().astype(str).unique().tolist())
    selected_products = st.sidebar.multiselect(
        "Product",
        options=products,
        default=products,
    )
    filtered_df = filtered_df[filtered_df["Product"].astype(str).isin(selected_products)]

# Numeric range filters for all numeric columns
numeric_cols = [c for c in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[c])]
if numeric_cols:
    st.sidebar.subheader("Numeric ranges")
    for col in numeric_cols:
        col_min = float(filtered_df[col].min())
        col_max = float(filtered_df[col].max())
        if col_min == col_max:
            # No point adding a slider if all values are the same
            continue
        selected_range = st.sidebar.slider(
            label=f"{col}",
            min_value=col_min,
            max_value=col_max,
            value=(col_min, col_max),
        )
        filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]

# If filters remove everything
if filtered_df.empty:
    st.warning("Your filters removed all rows. Relax filters in the sidebar.")
    st.stop()

# ---- Main: Preview + Downloads ----
st.subheader("📄 Data Preview")

preview_left, preview_right = st.columns([3, 1])

with preview_left:
    st.dataframe(filtered_df, use_container_width=True)

with preview_right:
    st.metric("Rows", len(filtered_df))
    st.metric("Columns", len(filtered_df.columns))

    st.download_button(
        label="⬇️ Download filtered CSV",
        data=to_csv_bytes(filtered_df),
        file_name="filtered_export.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.download_button(
        label="⬇️ Download full CSV",
        data=to_csv_bytes(df),
        file_name="full_export.csv",
        mime="text/csv",
        use_container_width=True,
    )

# ---- Visualization ----
st.subheader("📈 Visualization")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    x_axis = st.selectbox("X-axis", options=filtered_df.columns, index=0)

with col2:
    # Default Y to first numeric column if available
    default_y_idx = 0
    if numeric_cols:
        default_y = numeric_cols[0]
        default_y_idx = list(filtered_df.columns).index(default_y)

    y_axis = st.selectbox("Y-axis", options=filtered_df.columns, index=default_y_idx)

with col3:
    chart_type = st.selectbox("Chart", options=["Bar", "Line"], index=0)

# Validation
if x_axis == y_axis:
    st.warning("X-axis and Y-axis cannot be the same.")
    st.stop()

if not pd.api.types.is_numeric_dtype(filtered_df[y_axis]):
    st.warning("Y-axis must be numeric. Pick a numeric column (e.g., Sales).")
    st.stop()

# Build chart
if chart_type == "Bar":
    fig = px.bar(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
else:
    fig = px.line(filtered_df, x=x_axis, y=y_axis, markers=True, title=f"{y_axis} over {x_axis}")

st.plotly_chart(fig, use_container_width=True)

# ---- Summary statistics ----
st.subheader("📌 Summary Statistics")
st.write(filtered_df[y_axis].describe())
