# Robust relaxation-time tuning of B-CNF/ANF insulation paper for natural-ester converter transformers

Code, result files and manuscript build for the paper
*Robust Relaxation-Time Tuning of Banana-Nanocellulose/Aramid-Nanofibre Insulation Paper for Natural-Ester
Converter Transformers under Thermal Gradients and Polarity Reversal*.

Everything is computational. The property constants are listed in Table III of the paper; constants marked as
assumed there have not yet been measured on B-CNF/ANF handsheets.

## What the code does

| Step | File | Output |
|---|---|---|
| Composition → permittivity, conductivity, thermal conductivity (Looyenga mixing, pore filling, Fuoss ion-pair dissociation, Nielsen tortuosity, Maxwell–Garnett) | `props.py` | – |
| Exact RC-ladder solution of the IEC 60076-57-129 polarity-reversal sequence for a multilayer oil/paper barrier in a radial temperature gradient | `mw1d.py` | – |
| Scenario set (5 thermal × 2 reversal times × 4 ageing states), design vector, robust objective | `design.py` | – |
| Axisymmetric finite-volume electro-quasistatic solver with winding corner, wrap, cylinders and washer | `fe2d.py` | – |
| Designs D0–D7 | `exp_designs.py`, `add_d8.py` (D8) | `res_designs.json` |
| Layer table of D7 | `layers.py` | `res_layers.json` |
| GP-EI Bayesian optimisation vs CMA-ES, random and Sobol search; paired statistics | `exp_bo.py`, `stats.py` | `res_bo.json`, `res_bo_stats.json` |
| Ablation | `exp_ablation.py` | `res_ablation.json` |
| Sobol indices and paired Monte-Carlo | `exp_uncertainty.py`, `mc_stats.py` | `res_sobol.json`, `res_mc.json`, `res_mc_stats.json` |
| Design-space scan and κ sweep | `exp_space.py` | `res_space.json`, `res_kappa.json` |
| Field/charge traces | `exp_maps.py` | `res_maps.json` |
| Solver verification and 2-D check | `verify_fe.py`, `exp_fe2d.py` | `verify_fe.json`, `res_fe2d.json` |
| Figures (grayscale) | `fig_*.py`, `figstyle.py` | `fig*.png` |
| Manuscript (native Word equations via pandoc → OMML) | `build_docx.py`, `omml.py`, `sec_*.py`, `refs_raw.txt` | `manuscript.docx` |

## Running

```bash
pip install -r requirements.txt
FAST=1 ./run_all.sh     # figures + manuscript from the shipped result files (minutes)
./run_all.sh            # full recomputation (several hours; the 2-D solver and Sobol study dominate)
```

Building the manuscript needs `pandoc` on the PATH and the IEEE Transactions template saved as
`ieee_template.docx` in this folder (or its path in the `IEEE_TEMPLATE` environment variable). The template is
not redistributed here.

All result files are deterministic: random seeds are fixed inside each script.
