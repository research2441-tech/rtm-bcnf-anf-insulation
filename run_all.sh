#!/usr/bin/env bash
# Full reproduction of every result, figure and the manuscript.
# FAST=1 skips the expensive studies and rebuilds figures/manuscript from the shipped res_*.json files.
set -euo pipefail
cd "$(dirname "$0")"
if [ "${FAST:-0}" != "1" ]; then
  python3 exp_designs.py              # D0-D7 optimisation over the 40-scenario set -> res_designs.json
  python3 add_d8.py                   # hypothetical low-permittivity matrix D8   -> res_designs.json
  python3 layers.py                   # layer-by-layer properties of D7           -> res_layers.json
  python3 exp_bo.py 15                # GP-EI vs CMA-ES / random / Sobol          -> res_bo.json
  python3 stats.py                    # Wilcoxon + Holm + rank-biserial           -> res_bo_stats.json
  python3 exp_ablation.py             # one-ingredient-out re-optimisation        -> res_ablation.json
  python3 exp_uncertainty.py sobol 256 # Saltelli N=256                           -> res_sobol.json
  python3 exp_uncertainty.py mc 300   # paired Monte-Carlo, 300 draws             -> res_mc.json
  python3 mc_stats.py > res_mc_stats.json
  python3 exp_space.py grid           # uniform design-space scan                 -> res_space.json
  python3 exp_space.py kappa          # paper/oil stress weighting sweep          -> res_kappa.json
  python3 exp_maps.py                 # field and charge traces for Figs. 3-4     -> res_maps.json
  python3 verify_fe.py                # ladder vs BDF and planar 2-D check        -> verify_fe.json
  python3 exp_fe2d.py                 # axisymmetric 2-D verification             -> res_fe2d.json
fi
for f in fig_framework.py fig_geom.py fig_mech.py fig_props.py fig_results.py fig_space.py; do python3 "$f"; done
if [ -f "${IEEE_TEMPLATE:-ieee_template.docx}" ]; then
  python3 build_docx.py manuscript.docx
else
  echo "Template not found: set IEEE_TEMPLATE or place ieee_template.docx here to build the manuscript."
fi
