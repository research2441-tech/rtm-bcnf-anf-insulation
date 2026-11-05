import json, numpy as np
from scipy.stats import wilcoxon
BO=json.load(open('res_bo.json')); DZ=json.load(open('res_designs.json'))
Js=7.2003483350748425
out={}
fin={}
for m,runs in BO.items():
    best=[]; hit=[]; nf=[]
    for r in runs:
        a=np.array([np.inf if v is None else v for v in r]); c=np.minimum.accumulate(a)
        best.append(c[-1]-Js); idx=np.where(c<=Js*1.005)[0]; hit.append(idx[0]+1 if len(idx) else np.nan)
        nf.append(sum(v is None for v in r))
    fin[m]=np.array(best)
    out[m]=dict(med=float(np.median(best)),q1=float(np.percentile(best,25)),q3=float(np.percentile(best,75)),
                hit_frac=float(np.mean(~np.isnan(hit))),hit_med=float(np.nanmedian(hit)) if np.any(~np.isnan(hit)) else None,infeas=float(np.mean(nf)))
ps={m:wilcoxon(fin['gpei'],fin[m]).pvalue for m in ['random','sobol','cma']}
order=sorted(ps,key=ps.get); k=len(order); holm={}
run=0
for i,m in enumerate(order):
    run=max(run,min(1,(k-i)*ps[m])); holm[m]=run
for m in ps:
    d=fin[m]-fin['gpei']; out[m]['p']=ps[m]; out[m]['p_holm']=holm[m]
    # matched-pairs rank-biserial
    from scipy.stats import rankdata
    r=rankdata(np.abs(d)); out[m]['rbc']=float((r[d>0].sum()-r[d<0].sum())/r.sum())
print(json.dumps(out,indent=1))
json.dump(out,open('res_bo_stats.json','w'),indent=1)
