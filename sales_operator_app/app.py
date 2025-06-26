from dotenv import load_dotenv
load_dotenv()
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Sales Operator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and welcome message
st.title("🎯 Sales Operator")
st.markdown("---")

# Welcome section
st.header("Welcome to Sales Operator")
st.markdown("""
Your intelligent sales assistant designed to help you:
- **Analyze** sales data and performance metrics
- **Generate** insights and recommendations
- **Automate** repetitive sales tasks
- **Optimize** your sales strategy

Get started by exploring the features in the sidebar or dive right into your sales data!
""")

# Quick stats placeholder
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Sales", value="$0", delta="0%")

with col2:
    st.metric(label="Leads", value="0", delta="0")

with col3:
    st.metric(label="Conversion Rate", value="0%", delta="0%")

with col4:
    st.metric(label="Revenue", value="$0", delta="0%")

# Main content area
st.markdown("---")
st.subheader("Getting Started")
st.markdown("""
1. **Upload your sales data** using the file uploader below
2. **Configure your settings** in the sidebar
3. **Explore insights** and recommendations
4. **Generate reports** and analytics
""")

# File uploader placeholder
uploaded_file = st.file_uploader(
    "Upload your sales data (CSV, Excel, or JSON)",
    type=['csv', 'xlsx', 'json'],
    help="Upload your sales data to get started with analysis"
)

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    st.info("Data processing and analysis features will be available here.")
