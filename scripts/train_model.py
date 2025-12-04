# scripts/train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

def load_data(path="data/generated_txns.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df

def featurize(df):
    X = pd.DataFrame()
    X['amount_log'] = np.log1p(df['amount'])
    X['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    X['is_new_payee'] = df['is_new_payee'].fillna(0).astype(int)
    # group counts as a simple feature
    X['from_count'] = df.groupby('from_vpa')['from_vpa'].transform('count')
    X = X.fillna(0)
    return X

def train():
    df = load_data()
    X = featurize(df)
    iso = IsolationForest(contamination=0.03, random_state=42)
    iso.fit(X)
    os.makedirs("models", exist_ok=True)
    joblib.dump(iso, "models/model.joblib")
    print("Model saved to models/model.joblib")

if __name__ == "__main__":
    train()

