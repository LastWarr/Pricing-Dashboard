import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from pathlib import Path

# 🔐 Authentication check
if not st.session_state.get("logged_in"):
    st.warning("🔒 You must be logged in to access the dashboard.")
    st.stop()

# 🔒 Role check: only 'editor' and 'admin' can edit
editable_roles = ["editor", "admin"]
can_edit = st.session_state.get("role") in editable_roles

# 📂 Load or create data
DATA_PATH = Path("data/data.csv")
if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame({
        'ITEM': ['G8V-110-EX', 'GC-110-EX'],
        'LAST PRICE PAID': [115.95, 96.71],
        'CURRENT PRICE': [115.95, 110.71],
        'NEW PRICE': [115.95, 120.00],
        'MARGIN': [26.0, 36.7],
        'PRICE CHANGE': ['-', '8.4%'],
        'L12M NET SALES': [14858.76, 5545.96]
    })
    df.to_csv(DATA_PATH, index=False)

# 🛠️ Configure editable table
st.title("📊 Price Management Dashboard")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_default_column(editable=False)

# Customize editable columns with highlights
if can_edit:
    editable_columns = ['NEW PRICE', 'MARGIN', 'PRICE CHANGE']
    for col in editable_columns:
        gb.configure_column(col, editable=True, cellStyle={'backgroundColor': '#d4f7c1'})  # Light green background for editable cells

# Additional table styling
gb.configure_column("ITEM", width=200)
gb.configure_column("LAST PRICE PAID", width=150)
gb.configure_column("CURRENT PRICE", width=150)
gb.configure_column("L12M NET SALES", width=180)

# Apply grid options and build the table
grid_options = gb.build()

# Display the table
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.VALUE_CHANGED,
    allow_unsafe_jscode=True,
    theme='alpine',
    height=400,  # Adjust the height for a cleaner look
    fit_columns_on_grid_load=True,  # Ensure columns fit properly
    enable_enterprise_modules=True,  # Enable advanced features if needed
    rowSelection='multiple',  # Allow multiple row selection
    selectionMode='single'  # Allow single row selection
)

updated_df = grid_response['data']

# 💾 Save changes (only for editors/admins)
if can_edit and st.button("💾 Save Changes"):
    updated_df.to_csv(DATA_PATH, index=False)
    st.success("✅ Changes saved successfully!")

# 🔍 View table
st.subheader("📋 Current Table View")
st.dataframe(updated_df)
