# scripts/generate_dataset.py
import csv, random, string
from datetime import datetime, timedelta

def fake_vpa(seed):
    return ''.join(random.choices(seed+string.ascii_lowercase, k=6)) + "@upi"

def gen():
    rows=[]
    base = datetime.utcnow() - timedelta(days=1)
    idx=1
    # normal users
    for _ in range(800):
        t = base + timedelta(seconds=random.randint(0,86400))
        rows.append({
            "txn_id": f"T{idx:06d}",
            "timestamp": t.isoformat(),
            "from_vpa": fake_vpa("user"),
            "to_vpa": fake_vpa(random.choice(["shop","merchant","service"])),
            "amount": round(random.expovariate(1/500)+10,2),
            "message": random.choice(["","for groceries","payment","monthly bill"]),
            "is_new_payee": random.choice([0]*9+[1])
        })
        idx+=1
    # inject micro-scam clusters
    for _ in range(10):
        victim = fake_vpa("victim")
        t0 = base + timedelta(seconds=random.randint(0,86400))
        for i in range(3):
            rows.append({
                "txn_id": f"T{idx:06d}",
                "timestamp": (t0 + timedelta(seconds=30*i)).isoformat(),
                "from_vpa": victim,
                "to_vpa": f"test{i}@upi",
                "amount": round(random.uniform(1,10),2),
                "message": "verify",
                "is_new_payee": 1
            })
            idx+=1
        rows.append({
            "txn_id": f"T{idx:06d}",
            "timestamp": (t0 + timedelta(minutes=2)).isoformat(),
            "from_vpa": victim,
            "to_vpa": "fraudmerch@upi",
            "amount": round(random.uniform(5000,20000),2),
            "message": "payment for order",
            "is_new_payee": 1
        })
        idx+=1

    # final shuffle and save
    random.shuffle(rows)
    keys = ["txn_id","timestamp","from_vpa","to_vpa","amount","message","is_new_payee"]
    with open("data/generated_txns.csv","w",newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    print("Saved data/generated_txns.csv with", len(rows), "rows")

if __name__ == "__main__":
    gen()

