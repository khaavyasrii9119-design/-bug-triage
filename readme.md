# AI Bug Report Triage & Severity Classifier

Machine learning pipeline and benchmark dataset for automated software defect classification.

## Directory Structure
```text
bug_triage_ml_project/
├── dataset.csv         # 10,000-row benchmark corpus
├── pipeline.pkl        # Trained Scikit-Learn TF-IDF + Random Forest Pipeline
├── requirements.txt    # Project dependencies
├── setup_project.py    # Auto-generation script for dataset & model
├── test_run.py         # Script to run inference
└── readme.md           # Documentation