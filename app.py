import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# 1. Page Configuration Setup
st.set_page_config(page_title="DataEngine Pro", layout="wide", page_icon="🧼")

# 2. Premium Custom CSS Styling Injector
st.markdown("""
    <style>
        /* Main page adjustments */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        /* Style Streamlit Tabs to look like premium dashboard switches */
        button[data-baseweb="tab"] {
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #4a5568 !important;
            border-bottom: 2px solid transparent !important;
            padding: 10px 20px !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #1a73e8 !important;
            border-bottom: 2px solid #1a73e8 !important;
        }
        /* Custom Button Styling */
        .stButton>button {
            background-color: #1a73e8 !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        .stButton>button:hover {
            background-color: #1557b0 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            transform: translateY(-1px);
        }
        /* Clean header styling */
        h1 {
            color: #1e293b !important;
            font-weight: 700 !important;
        }
        h3 {
            color: #334155 !important;
            font-weight: 600 !important;
            margin-top: 1rem !important;
        }
        /* Sidebar layout enhancements */
        section[data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-right: 1px solid #e2e8f0;
        }
        /* Styled Metric Cards Wrapper */
        div[data-testid="stMetricValue"] {
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #1e293b !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Header & Branding Section
st.title("🧼 DataEngine™ Pro")
st.markdown("<p style='font-size:16px; color:#64748b; margin-top:-10px;'>Enterprise-grade file preprocessing, automated anomaly isolation, and unified reporting architecture.</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Sidebar Workflow Selector
st.sidebar.markdown("<h2 style='font-size:20px; color:#1e293b; margin-bottom:15px;'>🎛️ Control Panel</h2>", unsafe_allow_html=True)
app_mode = st.sidebar.radio(
    "Select Target Workflow Matrix:",
    ["📄 Task 1: Single File Engine", "🔗 Task 2: Multi-File Cross-Blender"]
)

st.sidebar.markdown("<br><br>---", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='color:#475569; margin-bottom:5px;'>⚙️ Core Engine Profile</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:13px; color:#64748b; line-height:1.4;'>System Architecture engineered by <strong>DARRY OWEN</strong> for automated business file orchestration.</p>", unsafe_allow_html=True)

# --- TASK 1: SINGLE FILE PROCESSING WORKFLOW ---
if app_mode == "📄 Task 1: Single File Engine":
    st.sidebar.subheader("📥 Upload Stream Source")
    uploaded_file = st.sidebar.file_uploader("Drop raw target CSV dataset here", type=["csv"], key="single_file")

    if uploaded_file is not None:
        df_single = pd.read_csv(uploaded_file)
        
        tab1, tab2, tab3 = st.tabs(["📋 Structural Audit", "🧹 Automated Cleansing", "📊 Business Intelligence Matrix"])
        
        with tab1:
            st.subheader("Raw File Architecture Preview")
            st.dataframe(df_single.head(10), use_container_width=True)
            
            st.subheader("🔍 Automated Structural Flaw Profiler")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Null Matrix Fields", value=f"{df_single.isnull().sum().sum():,}")
            with col2:
                st.metric(label="Redundant / Duplicate Rows", value=f"{df_single.duplicated().sum():,}")
            with col3:
                st.metric(label="Total Ingested Data Columns", value=len(df_single.columns))
            
        with tab2:
            st.subheader("Configure Target Cleansing Configurations")
            
            c1, c2 = st.columns(2)
            with c1:
                remove_dup = st.checkbox("Purge exact matching data duplicates", value=True, key="s_dup")
                strip_spaces = st.checkbox("Strip blank padding from string values", value=True, key="s_space")
                clean_money = st.checkbox("Scrub currency syntax elements ($, %, symbols)", value=True, key="s_money")
            with c2:
                handle_missing = st.selectbox("Missing structural matrix strategy:", ["Fill with Zero (0)", "Drop rows"], key="s_miss")
                standardize_dates = st.checkbox("Synchronize chronological string formats", value=True, key="s_date")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Run Comprehensive Cleansing Routine", key="s_run"):
                with st.spinner("Executing deep structural transformations..."):
                    cleaned = df_single.copy()
                    if remove_dup: cleaned = cleaned.drop_duplicates()
                    if strip_spaces:
                        for col in cleaned.select_dtypes(include=['object']).columns:
                            cleaned[col] = cleaned[col].astype(str).str.strip()
                    if clean_money:
                        for col in cleaned.columns:
                            if cleaned[col].dtype == 'object' and cleaned[col].str.contains(r'[\$,%]', regex=True, na=False).any():
                                cleaned[col] = cleaned[col].str.replace(r'[\$,% ]', '', regex=True)
                                cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
                    if standardize_dates:
                        for col in cleaned.columns:
                            if 'date' in col.lower() or 'time' in col.lower():
                                cleaned[col] = pd.to_datetime(cleaned[col], errors='coerce')
                    
                    st.session_state['single_cleaned_data'] = cleaned
                    st.success("🎉 Transformation runtime complete! Data matrices structured.")
                
            if 'single_cleaned_data' in st.session_state:
                st.markdown("<br>### 📁 Final Processed Dataset Preview", unsafe_allow_html=True)
                st.dataframe(st.session_state['single_cleaned_data'].head(5), use_container_width=True)
                
                csv_buffer = io.StringIO()
                st.session_state['single_cleaned_data'].to_csv(csv_buffer, index=False)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button("⬇️ Download Optimized Production CSV", data=csv_buffer.getvalue().encode('utf-8'), file_name="optimized_master_report.csv", mime="text/csv")

        with tab3:
            if 'single_cleaned_data' in st.session_state:
                df = st.session_state['single_cleaned_data']
                if 'Date' in df.columns: df = df.sort_values(by='Date')
                
                st.subheader("📈 Dynamic Visualization Workspace")
                
                vc1, vc2 = st.columns(2)
                with vc1:
                    col_x = st.selectbox("Assign Baseline Horizontal Dimension (X-Axis):", options=df.columns, key="s_x")
                with vc2:
                    col_y = st.selectbox("Assign Primary Performance Metric (Y-Axis):", options=df.columns, key="s_y")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df[col_x], y=df[col_y], 
                    mode='lines+markers', 
                    name=str(col_y),
                    line=dict(color='#1a73e8', width=3),
                    marker=dict(size=6, color='#1557b0')
                ))
                fig.update_layout(
                    xaxis_title=str(col_x), 
                    yaxis_title=str(col_y), 
                    template="plotly_white",
                    margin=dict(l=40, r=40, t=20, b=40)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Please execute the automated cleansing operation routine in the previous tab to initialize plotting maps.")
    else:
        st.info("💡 Initialize system: Please upload an unstructured raw CSV file via the sidebar module.")

# --- TASK 2: MULTI-FILE MERGING WORKFLOW ---
elif app_mode == "🔗 Task 2: Multi-File Cross-Blender":
    st.sidebar.subheader("📥 Upload Stream Sources")
    uploaded_files = st.sidebar.file_uploader("Select multiple raw target datasets (Hold Ctrl)", type=["csv"], accept_multiple_files=True, key="multi_file")

    if uploaded_files:
        file_dict = {file.name: pd.read_csv(file) for file in uploaded_files}
        file_names = list(file_dict.keys())
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Structural Audit", "🧹 File Isolation Cleansing", "🔗 Relational Blend Engine", "📊 Cross-Channel Intelligence"])
        
        with tab1:
            selected_file = st.selectbox("Select specific index stream to audit:", file_names, key="m_ins")
            raw_df = file_dict[selected_file]
            st.subheader(f"Raw Pipeline Grid View: {selected_file}")
            st.dataframe(raw_df.head(10), use_container_width=True)
            
        with tab2:
            st.subheader("Configure Sequential File Cleansing")
