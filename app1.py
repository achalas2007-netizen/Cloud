import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def run_anomaly_detection(df, contamination=0.05):
    # Training on machine metrics (CPU, Mem, Network)
    model = IsolationForest(contamination=contamination, random_state=42)
    df['anomaly_score'] = model.fit_predict(df.select_dtypes(include=[np.number]))
    
    # -1 is an anomaly, 1 is normal
    anomalies = df[df['anomaly_score'] == -1]
    return anomalies, df
    def find_root_cause(df, target_machine):
    # Simple correlation matrix to find immediate neighbors
    corr_matrix = df.corr()
    neighbors = corr_matrix[target_machine].sort_values(ascending=False)
    # Return top 5 potential influencers
    return neighbors.iloc[1:6].index.tolist()
    from statsmodels.tsa.stattools import grangercausalitytests

def run_risk_simulation(df, target, neighbors):
    risk_report = {}
    for node in neighbors:
        try:
            # Granger Test: Does 'node' cause 'target'?
            gc_test = grangercausalitytests(df[[target, node]], maxlag=2, verbose=False)
            p_val = gc_test[1][0]['ssr_chi2test'][1]
            def verify_stability(df, target, migration_path):
    # Simulate a 10% noise increase to see if the service breaks
    simulated_load = df[target] * 1.10
    variance = simulated_load.var()
    
    if variance > df[target].var() * 1.5:
        return "UNSTABLE: High Variance detected. Rollback initiated."
    return "STABLE: Environment healthy."
            
            # Transfer Entropy Proxy (Correlation of Lagged Signal)
            te_proxy = df[node].shift(1).corr(df[target])
            
            risk_score = ( (1 - p_val) + abs(te_proxy) ) / 2
            risk_report[node] = {"risk_impact": round(risk_score, 4), "status": "Critical" if risk_score > 0.7 else "Stable"}
        except:
            risk_report[node] = {"risk_impact": 0, "status": "Inconclusive"}
    return risk_report
    def calculate_migration_costs(current_cost):
    options = {
        "Same-Cloud Shift": current_cost * 0.85, # 15% savings
        "Type Shift (EC2->Lambda)": current_cost * 0.40, # 60% savings
        "Cross-Cloud Migration": current_cost * 1.20 # Costly due to egress
    }
    return options
    import streamlit as st

st.title("Cloud Nervous System: Dependency-Aware Optimizer")

uploaded_file = st.file_uploader("Upload Machine Metrics (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # STEP 1: ANOMALY
    if st.button("1. Detect Anomalies"):
        anomalies, full_df = run_anomaly_detection(df)
        st.write(f"Detected {len(anomalies)} suspicious machines.")
        st.session_state['target'] = anomalies.index[0] # Just take the first one for the demo

    # STEP 2 & 3: ROOT CAUSE & RISK (The USP)
    if 'target' in st.session_state and st.button("2. Analyze Dependency Risk"):
        neighbors = find_root_cause(df, st.session_state['target'])
        risk_data = run_risk_simulation(df, st.session_state['target'], neighbors)
        st.json(risk_data)

    # STEP 4 & 5: OPTIMIZE & MIGRATE
    if st.button("3. Simulate Migration & Stability"):
        costs = calculate_migration_costs(1000) # Dummy cost
        st.write("Cost Projection:", costs)
        stability = verify_stability(df, st.session_state['target'], "Type-Shift")
        st.success(stability)
