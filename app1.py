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
            
            # Transfer Entropy Proxy (Correlation of Lagged Signal)
            te_proxy = df[node].shift(1).corr(df[target])
            
            risk_score = ( (1 - p_val) + abs(te_proxy) ) / 2
            risk_report[node] = {"risk_impact": round(risk_score, 4), "status": "Critical" if risk_score > 0.7 else "Stable"}
        except:
            risk_report[node] = {"risk_impact": 0, "status": "Inconclusive"}
    return risk_report
