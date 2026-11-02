# Customer Churn Prediction — ML Demo

**English** | [繁體中文](README.zh-TW.md)

> A visual, reproducible classification demo for AI / data science.  
> **Synthetic data · No API key · No company data**

## Interactive portfolio

[Open the website](https://stream6650-arch.github.io/customer-churn-ml-demo/)

The Traditional Chinese portfolio includes model comparisons, browser-local logistic regression predictions, and threshold-dependent holdout metrics. Source: `web/`. Preview with `python -m http.server 8000 --directory web`. Regenerate the exported model with `python scripts/export_web.py`; the exporter checks all 375 holdout predictions against sklearn. The website reports the current export; package versions may cause small differences from the historical results below.

Pushes to `main` deploy through `.github/workflows/pages.yml`. If automatic Pages enablement is restricted, select GitHub Actions in Settings → Pages.

## What this project demonstrates

```mermaid
flowchart LR
A[Customer data] --> B[Preprocessing]
B --> C1[Logistic Regression]
B --> C2[Random Forest]
C1 --> D[Model evaluation]
C2 --> D
D --> E[Retention insight]
```

### Model evaluation dashboard

| Metric | What students learn |
|---|---|
| Accuracy | Overall correctness |
| Precision | How many predicted churners really churn |
| Recall | How many actual churners we find |
| F1 | Balance of precision and recall |
| ROC-AUC | Ranking ability across thresholds |

```mermaid
flowchart TD
A[Business question: Who may churn?] --> B{Prediction}
B -->|High risk| C[Retention action]
B -->|Low risk| D[Normal engagement]
C --> E[Discuss false-positive cost]
C --> F[Discuss false-negative cost]
```

## Teaching storyline

**Business problem → features → preprocessing → model → metrics → business decision**

This makes the project suitable for explaining why a model with high accuracy is not automatically the best business model.

## Actual result charts

The following results are generated from the repository's synthetic dataset (fixed seed = 42), not manually invented values.

### Model metrics

```mermaid
xychart-beta
    title "Model evaluation"
    x-axis ["Accuracy","Precision","Recall","F1","ROC-AUC"]
    y-axis "Score" 0 --> 1
    bar [0.749,0.646,0.436,0.520,0.788]
    bar [0.685,0.494,0.359,0.416,0.714]
```

**Series 1: Logistic Regression · Series 2: Random Forest**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.749 | 0.646 | 0.436 | 0.520 | 0.788 |
| Random Forest | 0.685 | 0.494 | 0.359 | 0.416 | 0.714 |

A more complex model does not automatically outperform a simpler model.

## Quick start
```bash
python -m venv .venv
pip install -r requirements.txt
python src/generate_data.py
python src/train.py
```

The training script produces `model_metrics.json`, making it easy to compare models and extend the demo with charts.

## Topics we can discuss with this project
Classification · feature engineering · one-hot encoding · train/test split · Logistic Regression · Random Forest · Precision/Recall/F1 · ROC-AUC · threshold tuning · model interpretation

## Privacy & security
All records are generated synthetically with a fixed random seed. No credentials, API keys, customer records or company information are used.
