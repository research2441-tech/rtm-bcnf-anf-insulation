"""Paired statistics of the Monte-Carlo robustness study (res_mc.json -> res_mc_stats.json)."""
import json
import numpy as np
from scipy.stats import wilcoxon

MC = {k: np.array(v) for k, v in json.load(open('res_mc.json')).items()}
K = MC['kraft']
rng = np.random.default_rng(0)
out = {}
for name in ['aramid_proxy', 'strict', 'uniform', 'graded']:
    X = MC[name]
    g = 100 * (1 - X[:, 0] / K[:, 0])                       # gain in mean utilisation (%)
    boot = [rng.choice(g, len(g)).mean() for _ in range(4000)]
    out[name] = dict(mean=float(g.mean()), lo=float(np.percentile(boot, 2.5)), hi=float(np.percentile(boot, 97.5)),
                     p5=float(np.percentile(g, 5)), p95=float(np.percentile(g, 95)), pos=float((g > 0).mean()),
                     p=float(wilcoxon(K[:, 0], X[:, 0]).pvalue),
                     oil=float(100 * np.mean(1 - X[:, 1] / K[:, 1])), pap=float(100 * np.mean(1 - X[:, 2] / K[:, 2])),
                     q=float(100 * np.mean(1 - X[:, 3] / K[:, 3])))
print(json.dumps(out, indent=1))
