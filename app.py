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
