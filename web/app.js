'use strict';
const $ = id => document.getElementById(id);
const names = {logistic_regression:'Logistic Regression',random_forest:'Random Forest'};
const labels = {accuracy:'Accuracy',precision:'Precision',recall:'Recall',f1:'F1',roc_auc:'ROC-AUC'};
fetch('model.json').then(r => {if (!r.ok) throw Error('model');return r.json();}).then(m => {
  $('auc').textContent=m.metrics.logistic_regression.roc_auc.toFixed(3);
  $('metrics').innerHTML=Object.entries(m.metrics).map(([k,v])=>`<tr><th scope="row">${names[k]}</th>${Object.keys(labels).map(key=>`<td>${v[key].toFixed(3)}</td>`).join('')}</tr>`).join('');
  $('bars').innerHTML=Object.entries(labels).map(([key,label])=>`<div class="bar-row"><span>${label}</span><div class="bars">${Object.values(m.metrics).map((v,i)=>`<div class="bar ${i?'alt':''}" style="width:${v[key]*100}%"><span>${v[key].toFixed(3)}</span></div>`).join('')}</div></div>`).join('');
  $('repro').textContent=`Seed 42 · 訓練集 ${m.trainRows} 筆 / 測試集 ${m.testRows} 筆 · scikit-learn ${m.version} · 套件版本可能影響結果`;
  function update(){
    const raw=[+$('tenure').value,+$('monthly').value,+$('support').value];
    const values=raw.map((x,i)=>(x-m.mean[i])/m.scale[i]);
    [$('contract').value,$('autopay').value].forEach((x,i)=>m.categories[i].forEach(c=>values.push(Number(c===x))));
    const p=1/(1+Math.exp(-(m.intercept+values.reduce((s,v,i)=>s+v*m.coef[i],0))));
    const t=+$('threshold').value/100;
    $('tenureValue').value=`${raw[0]} 個月`;$('monthlyValue').value=raw[1];$('supportValue').value=`${raw[2]} 次`;$('thresholdValue').value=`${Math.round(t*100)}%`;
    $('probability').innerHTML=`${(p*100).toFixed(1)}<small>%</small>`;
    $('risk-fill').style.width=`${p*100}%`;
    $('decision').textContent=p>=t?'↗ 高於門檻：列入留存關注名單':'↘ 低於門檻：維持一般互動';
    let tp=0,fp=0,fn=0;
    m.holdout.forEach(r=>{if(r.p>=t){if(r.y)tp++;else fp++;}else if(r.y)fn++;});
    $('precision').textContent=tp+fp?`${(tp/(tp+fp)*100).toFixed(1)}%`:'—';
    $('recall').textContent=tp+fn?`${(tp/(tp+fn)*100).toFixed(1)}%`:'—';
    $('flagged').textContent=`${tp+fp} / ${m.testRows}`;
  }
  $('inputs').addEventListener('input',update);$('inputs').addEventListener('submit',e=>e.preventDefault());$('threshold').addEventListener('input',update);
  $('reset').addEventListener('click',()=>{$('inputs').reset();$('threshold').value=50;update();});
  $('loading').hidden=true;$('demo').hidden=false;update();
}).catch(()=>{$('loading').textContent='模型載入失敗，請重新整理頁面再試一次。';});
