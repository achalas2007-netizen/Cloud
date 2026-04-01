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
