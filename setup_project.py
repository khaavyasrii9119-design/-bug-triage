import os
import pandas as pd
import numpy as np
import random
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

print("Step 1: Generating 10,000-row defect dataset...")
random.seed(42)
np.random.seed(42)

modules_severities = [
    ("Payment Gateway", "P1 - Blocker"),
    ("Authentication", "P1 - Blocker"),
    ("Backend API", "P2 - Critical"),
    ("Database", "P2 - Critical"),
    ("Frontend / UI", "P3 - Major"),
    ("Frontend / UI", "P4 - Minor"),
    ("Backend API", "P3 - Major")
]

raw_templates = {
    ("Payment Gateway", "P1 - Blocker"): [
        "User selects UPI payment on mobile, app freezes after submitting pin, money is deducted from bank account but order status remains 'Payment Failed'.",
        "Credit card transaction hangs on 3D-secure OTP verification; customer is charged twice but invoice is not generated.",
        "Refund processing throws NullPointerException when gateway returns timeout; ledger balance gets desynchronized."
    ],
    ("Authentication", "P1 - Blocker"): [
        "SSO login via Google/Okta returns 401 unauthorized loop for enterprise tenant users.",
        "Two-factor authentication SMS OTP never arrives, locking users out completely without fallback email options.",
        "Logout endpoint does not invalidate refresh tokens, allowing unauthorized access with expired bearer tokens."
    ],
    ("Backend API", "P2 - Critical"): [
        "Product catalog API endpoint /api/v2/items returns 504 Gateway Timeout during peak traffic.",
        "Order placement endpoint fails silently without returning order ID or persisting order in database.",
        "Rate limiting middleware blocks legitimate webhook deliveries from third-party logistics partners."
    ],
    ("Database", "P2 - Critical"): [
        "Deadlock detected in postgres transactional table 'user_balances' under concurrent withdrawal requests.",
        "Primary replica connection pool exhausted due to unindexed query on audit_logs table.",
        "Soft-deleted user records reappear in search index due to missing deleted_at filter in query."
    ],
    ("Frontend / UI", "P3 - Major"): [
        "Checkout button is completely unclickable on mobile viewports below 380px width due to modal z-index overlap.",
        "Filter by price slider jumps erratically and resets pagination to page 1 unexpectedly.",
        "Dark mode toggle makes form input text white-on-white, making text fields invisible."
    ],
    ("Frontend / UI", "P4 - Minor"): [
        "Spelling typo on settings page: 'Notification Prefrences' instead of 'Notification Preferences'.",
        "Footer copyright year displays 2024 instead of the current dynamic year.",
        "Button border alignment is offset by 2px on Safari browser compared to Chrome."
    ],
    ("Backend API", "P3 - Major"): [
        "Email notification for order shipment is delayed by over 4 hours due to celery queue backlog.",
        "PDF receipt generator exports with corrupted UTF-8 special characters for non-ASCII customer names.",
        "CSV export endpoint caps rows at 100 instead of requested 1000 records without pagination link."
    ]
}

data = []
for i in range(1, 10001):
    mod_sev = random.choices(modules_severities, weights=[0.15, 0.15, 0.20, 0.10, 0.20, 0.10, 0.10], k=1)[0]
    module, severity = mod_sev
    desc = random.choice(raw_templates[mod_sev])
    data.append({
        "Bug_ID": f"BUG-{10000 + i}",
        "Raw_User_Report": f"{desc} (Environment: Production)",
        "Severity": severity,
        "Suspected_Module": module
    })

df = pd.DataFrame(data)
df.to_csv("dataset.csv", index=False)
print("-> dataset.csv successfully created with 10,000 rows!")

print("Step 2: Training and saving pipeline.pkl...")
X = df["Raw_User_Report"]
y = df["Severity"]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=500, stop_words="english")),
    ("clf", RandomForestClassifier(n_estimators=30, random_state=42, max_depth=10, n_jobs=-1))
])
pipeline.fit(X, y)
joblib.dump(pipeline, "pipeline.pkl")
print("-> pipeline.pkl trained and saved successfully!")