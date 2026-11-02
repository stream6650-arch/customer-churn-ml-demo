"""Reproduce training and export a small, browser-readable logistic model."""
import json
import runpy
from pathlib import Path
import numpy as np
import sklearn

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / 'src/generate_data.py'))
state = runpy.run_path(str(ROOT / 'src/train.py'))
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([('preprocess', state['prep']), ('model', LogisticRegression(max_iter=1000))])
pipeline.fit(state['Xtr'], state['ytr'])
prep = pipeline['preprocess']
scaler = prep.named_transformers_['num']
model = pipeline['model']
payload = {
    'version': sklearn.__version__,
    'metrics': state['results'],
    'rows': len(state['df']),
    'trainRows': len(state['Xtr']),
    'testRows': len(state['Xte']),
    'mean': scaler.mean_.tolist(),
    'scale': scaler.scale_.tolist(),
    'categories': [v.tolist() for v in prep.named_transformers_['cat'].categories_],
    'coef': model.coef_[0].tolist(),
    'intercept': float(model.intercept_[0]),
    'holdout': [{'y': int(y), 'p': float(p)} for y, p in zip(state['yte'], pipeline.predict_proba(state['Xte'])[:, 1])],
}
(ROOT / 'web/model.json').write_text(json.dumps(payload), encoding='utf-8')
# Check browser formula against sklearn on every held-out record.
for row, expected in zip(state['Xte'].to_dict('records'), pipeline.predict_proba(state['Xte'])[:, 1]):
    values = [(row[k] - m) / s for k, m, s in zip(['tenure_months', 'monthly_charge', 'support_tickets'], payload['mean'], payload['scale'])]
    values += [float(row[k] == value) for k, cats in zip(['contract', 'autopay'], payload['categories']) for value in cats]
    actual = 1 / (1 + np.exp(-(payload['intercept'] + np.dot(values, payload['coef']))))
    assert abs(actual - expected) < 1e-12
print('Exported model; 375 browser-formula predictions match sklearn.')
