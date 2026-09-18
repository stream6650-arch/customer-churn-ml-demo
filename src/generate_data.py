from pathlib import Path
import numpy as np
import pandas as pd
rng=np.random.default_rng(42); n=1500
tenure=rng.integers(1,73,n); monthly=rng.normal(75,25,n).clip(20,160); support=rng.poisson(1.5,n)
contract=rng.choice(['Month-to-month','One year','Two year'],n,p=[.55,.25,.20]); autopay=rng.choice(['Yes','No'],n)
logit=-1.7+.018*(monthly-70)-.035*(tenure-24)+.28*support+.85*(contract=='Month-to-month')+.35*(autopay=='No')
prob=1/(1+np.exp(-logit))
df=pd.DataFrame({'tenure_months':tenure,'monthly_charge':monthly.round(2),'support_tickets':support,'contract':contract,'autopay':autopay,'churn':rng.binomial(1,prob)})
out=Path(__file__).resolve().parents[1]/'data'/'customers.csv'; out.parent.mkdir(exist_ok=True); df.to_csv(out,index=False)
print(f'Generated {len(df)} synthetic rows -> {out}')
