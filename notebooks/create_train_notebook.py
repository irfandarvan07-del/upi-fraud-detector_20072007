# notebooks/create_train_notebook.py
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

nb = new_notebook()
nb.cells = [
    new_markdown_cell("# Train IsolationForest (UPI Fraud)"),
    new_markdown_cell("This notebook generates features from `data/generated_txns.csv` and trains an IsolationForest. Run the cells in order."),
    new_code_cell("""# cell 1: imports
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
print("Libraries loaded")"""),
    new_code_cell("""# cell 2: load data
df = pd.read_csv('../data/generated_txns.csv', parse_dates=['timestamp'])
df.head()"""),
    new_code_cell("""# cell 3: feature engineering
X = pd.DataFrame()
X['amount_log'] = np.log1p(df['amount'])
X['hour'] = df['timestamp'].dt.hour
X['is_new_payee'] = df['is_new_payee'].fillna(0).astype(int)
X['from_count'] = df.groupby('from_vpa')['from_vpa'].transform('count')
X = X.fillna(0)
X.head()"""),
    new_code_cell("""# cell 4: train
iso = IsolationForest(contamination=0.03, random_state=42)
iso.fit(X)
joblib.dump(iso, '../models/model.joblib')
print('Model trained and saved to ../models/model.joblib')"""),
    new_markdown_cell("**Notes:** If `data/generated_txns.csv` doesn't exist run `python3 scripts/generate_dataset.py` first.")
]

nb.metadata = {
    "kernelspec": {"name": "python3", "display_name": "Python 3"},
    "language_info": {"name": "python"}
}

with open("notebooks/train.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Wrote notebooks/train.ipynb (valid notebook).")

