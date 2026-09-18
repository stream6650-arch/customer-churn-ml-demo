# Customer Churn Prediction — Machine Learning Demo

A compact, reproducible teaching project using **synthetic data only** and **no API key required**.

## Learning goals
- Frame churn as a classification problem
- Build preprocessing with scikit-learn Pipeline
- Compare Logistic Regression and Random Forest
- Evaluate Accuracy, Precision, Recall, F1 and ROC-AUC
- Connect model output to business actions

## Architecture
Synthetic Customer Data → Preprocessing → Models → Evaluation

## Quick start
```bash
python -m venv .venv
pip install -r requirements.txt
python src/generate_data.py
python src/train.py
```

## Privacy & security
Synthetic data only. No credentials, tokens, API keys or company data.

See `TEACHING_GUIDE.md` for the lesson flow.