from pathlib import Path
import json,pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
ROOT=Path(__file__).resolve().parents[1]; df=pd.read_csv(ROOT/'data'/'customers.csv'); X,y=df.drop(columns='churn'),df['churn']
prep=ColumnTransformer([('num',StandardScaler(),['tenure_months','monthly_charge','support_tickets']),('cat',OneHotEncoder(handle_unknown='ignore'),['contract','autopay'])])
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y); results={}
for name,model in {'logistic_regression':LogisticRegression(max_iter=1000),'random_forest':RandomForestClassifier(n_estimators=250,random_state=42)}.items():
 p=Pipeline([('preprocess',prep),('model',model)]); p.fit(Xtr,ytr); pred=p.predict(Xte); proba=p.predict_proba(Xte)[:,1]
 results[name]={k:round(float(v),4) for k,v in {'accuracy':accuracy_score(yte,pred),'precision':precision_score(yte,pred,zero_division=0),'recall':recall_score(yte,pred,zero_division=0),'f1':f1_score(yte,pred,zero_division=0),'roc_auc':roc_auc_score(yte,proba)}.items()}
print(json.dumps(results,indent=2)); (ROOT/'model_metrics.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
