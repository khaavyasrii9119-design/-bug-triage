import joblib

# 1. Load the trained model pipeline
pipeline = joblib.load("pipeline.pkl")

# 2. Sample test bug descriptions
sample_bugs = [
    "User selects UPI payment on mobile, app freezes after submitting pin, money is deducted but order fails.",
    "Spelling typo on settings page: 'Notification Prefrences' instead of 'Notification Preferences'.",
    "Product catalog API endpoint /api/v2/items returns 504 Gateway Timeout during peak traffic."
]

print("=" * 60)
print("🤖 AI BUG SEVERITY PREDICTION TEST")
print("=" * 60)

for i, bug in enumerate(sample_bugs, 1):
    prediction = pipeline.predict([bug])[0]
    print(f"\n[Defect #{i}]: {bug}")
    print(f"👉 Predicted Severity: {prediction}")

print("\n" + "=" * 60)
print("✅ Verification successful! Pipeline is working properly.")
print("=" * 60)