import streamlit as st

pg = st.navigation([
    st.Page("pages/0_Project_Overview.py", title="Project Overview"),
    st.Page("pages/1_EDA.py", title="EDA"),
    st.Page("pages/2_Traffic_and_Channel.py", title="Traffic and Channel"),
    st.Page("pages/3_Funnel_Analysis.py", title="Funnel Analysis"),
    st.Page("pages/4_Product_Analysis.py", title="Product Analysis"),
    st.Page("pages/5_Budget_Optimization.py", title="Budget Optimization"),
    st.Page("pages/6_Purchase_Prediction.py", title="Purchase Prediction"),
    st.Page("pages/7_Experiment_Design.py", title="Experiment Design"),
])
pg.run()
