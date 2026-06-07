import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# 1. Page Configuration Setup
st.set_page_config(page_title="DataEngine Pro", layout="wide", page_icon="🧼")

# 2. Header & Branding Section
st.title("🧼 DataEngine™ Pro")
st.markdown("Enterprise-grade file preprocessing, automated anomaly isolation, and unified reporting architecture.")
st.markdown("---")

# 3. Sidebar Workflow Selector
st.sidebar.header("🎛️ Control Panel")
app_mode = st.sidebar.radio(
    "Select Target Workflow Matrix:",
    ["📄 Task 1: Single File Engine", "🔗 Task 2: Multi-File Cross-Blender"]
)

st.sidebar.markdown("<br><br>---", unsafe_allow_html=True)
st.sidebar.markdown("### 🚀 Need a Custom Data Pipeline?")
st.sidebar.markdown("System Architecture engineered by **DARRY OWEN** for automated business file orchestration.")
# 👇 Paste the link you copied from Calendly between the parenthesis below!
st.sidebar.markdown("[👉 Book a Free 15-Min Strategy Session](https://calendly.com/darryowen3/30min)")



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
                
                st.subheader("📊 Dynamic Visualization Workspace")
                
                vc1, vc2 = st.columns(2)
                with vc1:
                    col_x = st.selectbox("Assign Baseline Horizontal Dimension (X-Axis):", options=df.columns, key="s_x")
                with vc2:
                    col_y = st.selectbox("Assign Primary Performance Metric (Y-Axis):", options=df.columns, key="s_y")
                
                if col_x in df.columns:
                    df = df.dropna(subset=[col_x])
                    df = df.sort_values(by=col_x)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df[col_x], y=df[col_y], 
                    mode='lines+markers', 
                    name=str(col_y),
                    connectgaps=True,
                    line=dict(color='#1a73e8', width=3),
                    marker=dict(size=6, color='#1557b0')
                ))
                fig.update_layout(
                    xaxis_title=str(col_x), 
                    yaxis_title=str(col_y), 
                    template="plotly_white"
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
            target_clean_file = st.selectbox("Target isolation workspace stream:", file_names, key="m_cl_sel")
            
            mc1, mc2 = st.columns(2)
            with mc1:
                remove_dup = st.checkbox("Purge file records duplicates", value=True, key="m_dup")
                strip_spaces = st.checkbox("Scrub internal text column paddings", value=True, key="m_space")
            with mc2:
                clean_money = st.checkbox("Scrub numeric column string currency items", value=True, key="m_money")
                standardize_dates = st.checkbox("Auto-standardize layout timestamps", value=True, key="m_date")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Execute Optimization Profile on Stream", key="m_run"):
                cleaned = file_dict[target_clean_file].copy()
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
                
                if 'multi_cleaned_files' not in st.session_state:
                    st.session_state['multi_cleaned_files'] = {}
                st.session_state['multi_cleaned_files'][target_clean_file] = cleaned
                st.success(f"🎉 Cleansed data matrix stream for '{target_clean_file}' held successfully in staging memory.")
                
            if 'multi_cleaned_files' in st.session_state:
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(f"Verified Streams Staged in Memory: {list(st.session_state['multi_cleaned_files'].keys())}")

        
        with tab3:
            st.subheader("🔗 Multi-Matrix Intersect / Blend Settings")
            if 'multi_cleaned_files' in st.session_state and len(st.session_state['multi_cleaned_files']) >= 2:
                clean_names = list(st.session_state['multi_cleaned_files'].keys())
                
                jc1, jc2 = st.columns(2)
                with jc1:
                    col_a = st.selectbox("Primary Baseline Dataset (Matrix A):", clean_names, key="join_a")
                    key_a = st.selectbox("Assign Primary Key Identifier:", st.session_state['multi_cleaned_files'][col_a].columns, key="key_a")
                with jc2:
                    col_b = st.selectbox("Relational Target Dataset (Matrix B):", [n for n in clean_names if n != col_a], key="join_b")
                    key_b = st.selectbox("Assign Relational Match Key:", st.session_state['multi_cleaned_files'][col_b].columns, key="key_b")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔗 Execute Relational Structural Blend", key="merge_run"):
                    df_a = st.session_state['multi_cleaned_files'][col_a].copy()
                    df_b = st.session_state['multi_cleaned_files'][col_b].copy()
                    
                    df_a[key_a] = df_a[key_a].astype(str)
                    df_b[key_b] = df_b[key_b].astype(str)
                    
                    merged = pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how="outer", suffixes=('_A', '_B'))
                    
                    if key_a == 'Date' and 'Date_A' in merged.columns and 'Date_B' in merged.columns:
                        merged['Date'] = merged['Date_A'].fillna(merged['Date_B'])
                        merged = merged.drop(columns=['Date_A', 'Date_B'])
                        
                    st.session_state['final_merged_data'] = merged
                    st.success("🎉 Cross-platform relational blend successful! Master matrix built.")
                    st.dataframe(merged.head(10), use_container_width=True)
            else:
                st.warning("⚠️ Cross-platform blending blocks require optimizing at least two individual data streams inside Tab 2.")

        with tab4:
            if 'final_merged_data' in st.session_state:
                df = st.session_state['final_merged_data'].copy()
                
                # Numeric formatting protection layers
                if 'Gross_Revenue' in df.columns:
                    df['Gross_Revenue'] = pd.to_numeric(df['Gross_Revenue'], errors='coerce').fillna(0)
                if 'Amount_Spent' in df.columns:
                    df['Amount_Spent'] = pd.to_numeric(df['Amount_Spent'], errors='coerce').fillna(0)
                
                st.subheader("📊 Cross-Channel Business Executive Analytics")
                
                m_col1, m_col2, m_col3 = st.columns(3)
                if 'Gross_Revenue' in df.columns:
                    total_rev = df['Gross_Revenue'].sum()
                    m_col1.metric("💰 Consolidated Gross Revenue", f"${total_rev:,.2f}")
                if 'Amount_Spent' in df.columns:
                    total_spend = df['Amount_Spent'].sum()
                    m_col2.metric("📉 Aggregate Operational Outlay", f"${total_spend:,.2f}")
                if 'Gross_Revenue' in df.columns and 'Amount_Spent' in df.columns:
                    if total_spend > 0:
                        m_col3.metric("🚀 Compounded Return Metrics", f"{(total_rev/total_spend):.2f}x ROAS", delta=f"{((total_rev/total_spend)-1)*100:.1f}% Net Return")
                
                st.markdown("---")
                st.subheader("📈 Unified Multi-Channel Plotting Engine")
                
                cc1, cc2, cc3 = st.columns(3)
                with cc1:
                    col_x = st.selectbox("Horizontal Scale Core Index:", options=df.columns, key="m_x")
                with cc2:
                    col_y1 = st.selectbox("Plot Line Vector Alpha:", options=df.columns, key="m_y1")
                with cc3:
                    opts = list(df.columns)
                    opts.insert(0, "None")
                    col_y2 = st.selectbox("Plot Line Vector Beta (Optional):", options=opts, key="m_y2")
                
                if col_x in df.columns:
                    df = df.dropna(subset=[col_x])
                    df[col_x] = df[col_x].astype(str)
                    df = df.sort_values(by=col_x)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df[col_x], y=df[col_y1], mode='lines+markers', name=str(col_y1), connectgaps=True, line=dict(color='#1a73e8', width=3)))
                if col_y2 != "None":
                    fig.add_trace(go.Scatter(x=df[col_x], y=df[col_y2], mode='lines+markers', name=str(col_y2), connectgaps=True, line=dict(color='#e74c3c', width=3)))
                    
                fig.update_layout(xaxis_title=str(col_x), yaxis_title="Operational Value Metrics", template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Establish the matrix correlation mapping options inside the 'Relational Blend Engine' tab to generate tracking lines.")

