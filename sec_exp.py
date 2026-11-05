# -*- coding: utf-8 -*-
EXP = [
    ('h1', 'IV. DATA AND EXPERIMENTAL PROTOCOL'),
    ('h2', 'A. Data Sources and Calibration'),
    ('p', 'No handsheets were made for this study; every number in Section V is computed. The measured inputs are '
          'the ester permittivity and the conductivity of ester-impregnated pressboard [@RUMPELT2017], the '
          'activation energy of impregnated pressboard [@KIER2024], whose value lies within 0.03 eV of the dry '
          'synthetic-ester pressboard result [@ZENKER2017], the out-of-plane permittivity of h-BN [@LATURIA2018], '
          'the attainable carboxylate content [@ISOGAI2011] and the base thermal conductivity of impregnated paper '
          '[@DOMBEK2020]. The remaining constants of {T:TABLE_PARAM} are assumptions chosen inside physically reasonable '
          'ranges and are varied jointly in the uncertainty study. With these values the model gives '
          '$\\varepsilon_p$ = 4.74 for ester-impregnated kraft and 4.18 for the same sheet in mineral oil, and '
          'the nominal ester conductivity reproduces the series measurement used for cross-checking. The ageing '
          'multiplier of four is a bounding scenario motivated by the marked conductivity rise of aged FR3 '
          '[@KANUMURI2024], not a fitted value.'),
    ('h2', 'B. Candidate Papers and Baselines'),
    ('p', 'Nine papers are compared. D0 is kraft paper in natural ester. D1 is a proxy of the aramid-pulp hybrid of '
          '[@MO2019]: kraft conductivity with permittivity reduced by the reported 29.6%. D2 represents '
          'nanofibrillated-cellulose presspaper [@HUANG2017] (10% unoxidised fibrils) and D3 a BNNS/CNF paper '
          '[@ZHANGD2025] (10% fibrils, 5% BNNS), both computed with the property model. D4 minimises $\\varepsilon_p$ '
          'inside the design space without carboxylate. D5 implements exact window matching: the uniform composition '
          'that minimises the mean of $(\\ln\\rho_\\tau)^2$ over 60–110 °C. D6 and D7 are the robust optima '
          'of (18) without and with radial grading. D8 is a hypothetical paper that carries the conductivity profile '
          'of D7 on the low-permittivity matrix of D1; it is reported to show how the two levers combine and is not '
          'claimed to be manufacturable with the present composition model. D1–D3 are property-level proxies of '
          'published material classes, not reproductions of those papers.'),
    ('p', 'For the design loop, GP-EI is compared with random search, scrambled Sobol sampling and CMA-ES '
          '[@HANSEN2001] (population 8, initial step 0.3 in the unit cube, infeasible proposals penalised and '
          'counted). Every method receives 80 evaluations, and 15 seeds are paired across methods. The reference '
          'optimum $J^\\star$ is the best value found by differential evolution (population 12, 40 generations, '
          'polished) or by any benchmark run.'),
    ('h2', 'C. Implementation Details'),
    ('p', 'All code is written in Python 3.13 with NumPy 2.5, SciPy 1.18 (eigh, sparse LU, differential evolution, '
          'solve_ivp), scikit-learn 1.9 (Gaussian processes), cma 4.5 and SALib, and runs on two CPU cores of a Linux '
          'container without a GPU. Random seeds are fixed for every stochastic step. The 2-D model uses '
          'cell-centred finite volumes on uniform grids with harmonic face averaging, backward Euler in time with '
          'steps of $t_r/80$ during ramps and a doubling ladder from 0.05 s to 102.4 s during holds, a steady thermal '
          'solution for the temperature field, and face-based field evaluation so that interface cells do not mix '
          'materials. The complete code and result files are released with the paper.'),
    ('h2', 'D. Evaluation Metrics'),
    ('p', 'The primary metric is the robust utilisation $J$ of (18) in kV/mm; its maximum over scenarios is also '
          'reported. Secondary metrics are the scenario means and maxima of $E_o^{\\max}$ and $E_p^{\\max}$, the '
          'interface charge $Q_i$ in \u03bcC/m\u00b2, the overshoot $\\Gamma_o$ and the largest ohmic dissipation '
          'density $\\sigma E^2$. Two subsets isolate mechanisms: the isothermal, unaged, fast-reversal scenarios, '
          'where matching should help most, and the gradient scenarios, where it should help least. Design gains '
          'relative to kraft are expressed as'),
    ('eq', 'g=1-\\frac{J\\left(\\mathbf{x}\\right)}{J\\left(\\mathbf{x}_{0}\\right)}'),
    ('p', 'with $\\mathbf{x}_0$ the kraft sheet. For the optimisers the metric is the simple regret '
          '$J_{\\mathrm{best}}-J^\\star$ after each evaluation and the number of evaluations needed to come within '
          '0.5% of $J^\\star$.'),
    ('h2', 'E. Sensitivity, Robustness and Statistical Analysis'),
    ('p', 'Twelve uncertain inputs are varied: $\\varepsilon_C$, $\\varepsilon_A$, $p_0$, $\\beta_f$, $E_{a,b}$, '
          '$\\sigma_{o,50}$ (log-uniform over one decade), $E_{a,o}$, $G_{\\mathrm{ion}}$ (log-uniform over one '
          'decade), $E_\\mu$, $a$, $\\alpha_B$ and the ageing multiplier $D$ (2–8). Sobol indices of the gain $g$ '
          'of D7 are estimated with Saltelli sampling [@SALTELLI2010] ($N$ = 256, 3584 model pairs); the total '
          'index of input $i$ is'),
    ('eq', 'S_{T,i}=\\frac{\\mathbb{E}_{\\mathbf{X}_{\\sim i}}\\left[\\mathrm{Var}_{X_i}\\left(g\\mid\\mathbf{X}_{\\sim i}\\right)\\right]}{\\mathrm{Var}\\left(g\\right)}'),
    ('p', 'A separate Monte-Carlo study draws 300 parameter sets uniformly from the same ranges and evaluates D0, '
          'D1, D5, D6 and D7 on identical draws, keeping the compositions fixed at their nominal optima. Paired '
          'differences are tested with the Wilcoxon signed-rank test [@WILCOXON1945]; mean gains carry 95% '
          'bootstrap confidence intervals (4000 resamples). Optimiser comparisons use the final regret of the 15 '
          'paired seeds, the Wilcoxon test with Holm correction over three comparisons and the matched-pairs '
          'rank-biserial correlation as effect size. The significance level is 0.05. The 1-D model is deterministic, '
          'so differences between designs at nominal constants are exact and are not tested statistically.'),
    ('p', 'Numerical accuracy is checked in three ways: the modal ladder against stiff BDF integration of the same '
          'equations, the 2-D solver against the ladder for planar isothermal layers, and the 2-D results at two '
          'mesh sizes, combined by Richardson extrapolation,'),
    ('eq', 'E_{0}\\approx 2E_{h/2}-E_{h}'),
    ('p', 'which assumes the first-order convergence produced by harmonic face averaging at material interfaces.'),
]
