# -*- coding: utf-8 -*-
METHOD = [
    ('h1', 'III. PROPOSED METHODOLOGY'),
    ('h2', 'A. Problem Formulation'),
    ('p', 'The solid insulation of the valve-side main gap consists of a 3 mm conductor wrap and four 3 mm '
          'pressboard barriers separated by ester gaps of 6\u20138 mm ({F:fig2_geometry}a). All five solid layers are made from '
          'one furnish: kraft cellulose, a mass fraction $w_A$ of aramid nanofibres, a mass fraction $w_C$ of '
          'TEMPO-oxidised banana-pseudostem nanofibrils with carboxylate content $c$, and a mass fraction $w_B$ of '
          'BNNS. The carboxylate content may vary linearly from $c_w$ in the wrap to $c_k$ in the barrier next to '
          'the core, so that layer $l\\in\\{0,\\dots,4\\}$ carries $c_l=c_w+(c_k-c_w)\\,l/4$. The design vector is '
          '$\\mathbf{x}=(w_A,w_C,c_w,c_k,w_B)$, bounded by $0\\le w_A\\le 0.35$, $0.05\\le w_C\\le 0.30$, '
          '$0\\le c_w,c_k\\le 1.7$ mmol/g and $0\\le w_B\\le 0.10$, with $w_A+w_C+w_B\\le 0.6$ so that kraft fibre '
          'still forms at least 40% of the sheet. The upper carboxylate bound follows the maximum reported for '
          'TEMPO oxidation [@ISOGAI2011]. A uniform design is the special case $c_w=c_k$.'),
    ('p', 'Each design is judged over a scenario set $\\mathcal{S}$ that combines five thermal profiles (uniform 60, '
          '85 and 110 \u00b0C; linear 85\u219260 \u00b0C and 110\u219270 \u00b0C from winding to core), two reversal times '
          '($t_r$ = 10 s and 120 s) and four ageing states in which the oil and paper conductivities are multiplied '
          'by $D_o,D_p\\in\\{1,4\\}$, giving $|\\mathcal{S}|=40$. In every scenario the stack receives the reversal '
          'sequence of IEC 60076-57-129: $-U$ for 90 min, reversal to $+U$, 90 min, reversal to $-U$ and 45 min '
          '[@IEC57129], with $U$ = 250 kV. The outputs are the peak oil-gap field $E_o^{\\max}$, the peak solid-layer '
          'field $E_p^{\\max}$ and the free charge $Q_i$ summed over the ten oil\u2013solid interfaces at the end of '
          'the first DC stage. {T:TABLE_PARAM} lists the notation and the nominal constants; every constant marked '
          '\u201cassumed\u201d is varied in Section V-E.'),
    ('fig', 'fig2_geometry.png', 'Geometry. (a) One-dimensional stack representing the valve-side main gap, with '
            'a linear temperature profile from the winding (temperature $T_w$) to the core ($T_c$). (b) Material map '
            'of the 2-D axisymmetric model: copper (black), solid layers (gray) and ester (white).', True),
    ('h2', 'B. System Overview'),
    ('p', '{F:fig1_framework} shows the information flow. A composition enters the property model, which returns '
          '$\\varepsilon_p$, $\\sigma_p(T)$ and the through-plane thermal conductivity $k_p$ of each layer. The '
          'scenario generator assigns temperatures, ageing factors and reversal times, and the exact ladder solver '
          'returns the field histories. Their peaks are condensed into a robust utilisation, which the Gaussian '
          'process learns and the expected-improvement rule uses to propose the next composition. Each proposal '
          'stands for one handsheet trial in a laboratory campaign; in this study the model plays the role of the '
          'laboratory. The best design is finally checked in a 2-D axisymmetric model ({F:fig2_geometry}b).'),
    ('fig', 'fig1_framework.png', 'Design framework. Solid arrows carry data forward; the dashed reverse path returns '
            'the next composition proposed by the Bayesian loop, and the dashed branch sends the best design to the '
            '2-D verification model.', True),
    ('h2', 'C. Composition-to-Property Model'),
    ('p', 'Nanofibrils occupy the pores between kraft fibres, so the porosity $p$ of the impregnated sheet falls as '
          'their mass fraction grows. With $p_0$ the porosity of a kraft handsheet and $\\beta_f$ a filling '
          'coefficient,'),
    ('eq', 'p=\\max\\left(p_{\\min},\\,p_0-\\beta_f\\left(w_C+w_A\\right)\\right)'),
    ('p', 'and the solid volume fractions $v_C$, $v_A$ and $v_B$ of cellulose, ANF and BNNS follow from the mass '
          'fractions and densities, scaled to $1-p$. The pores are filled with ester. Looyenga\u2019s cube-root rule '
          '[@LOOYENGA1965], which reproduces presspaper permittivity well [@HUANG2016], gives the relative '
          'permittivity of the impregnated sheet:'),
    ('eq', '\\varepsilon_p^{1/3}=v_C\\,\\varepsilon_C^{1/3}+v_A\\,\\varepsilon_A^{1/3}+v_B\\,\\varepsilon_B^{1/3}+p\\,\\varepsilon_o^{1/3}'),
    ('p', 'Here $\\varepsilon_B$ = 3.76 is the out-of-plane static permittivity of bulk h-BN [@LATURIA2018], '
          'appropriate for platelets lying in the sheet plane, and $\\varepsilon_o$ = 3.2 is the ester value '
          '[@RUMPELT2017]. Equation (2) contains the main trade-off on the permittivity side: ANF lowers '
          '$\\varepsilon_p$, but every nanofibril also removes oil-filled pore volume, whose permittivity is lower '
          'still.'),
    ('p', 'Conduction is split into a base channel inherited from impregnated cellulose and an ionic channel '
          'supplied by the carboxylate groups. The base channel is anchored to ester-impregnated pressboard at '
          '$T_{50}$ = 323.15 K, $\\sigma_{b,50}$ = 54.5 fS/m [@RUMPELT2017], with the activation energy '
          '$E_{a,b}$ = 1.07 eV reported for impregnated pressboard [@KIER2024], and it scales with the cellulose '
          'fraction because ANF and BNNS replace conducting cellulose:'),
    ('eq', '\\sigma_b(T)=\\sigma_{b,50}\\left(\\frac{v_C}{v_{C,0}}\\right)^{m}\\exp\\left[-\\frac{E_{a,b}\\,\\theta(T)}{k_B}\\right]'),
    ('p', 'where $\\theta(T)=1/T-1/T_{50}$, $v_{C,0}$ is the cellulose fraction of kraft and $m$ = 1.5 an assumed '
          'connectivity exponent. '
          'Sodium carboxylate pairs dissociate only partly in a medium of relative permittivity '
          '$\\varepsilon_m$. Following the ion-pair treatment of Fuoss [@FUOSS1958], the Coulomb binding energy of '
          'a pair with contact distance $a$ is'),
    ('eq', 'U_d=\\frac{e^2}{4\\pi\\varepsilon_0\\,\\varepsilon_m\\,a}'),
    ('p', 'and the free-ion density of a weak electrolyte grows as $\\exp(-U_d/2k_BT)$. Adding an ion-hopping '
          'barrier $E_\\mu$ gives the activation energy of the ionic channel,'),
    ('eq', 'E_{\\mathrm{ion}}=E_\\mu+\\tfrac{1}{2}U_d'),
    ('p', 'Setting $\\varepsilon_m=\\varepsilon_p$ couples the two property models: whatever lowers the permittivity '
          'also raises $U_d$, reduces the number of free ions and steepens their temperature dependence. The ionic '
          'conductivity, referenced to a sheet with $w_C^{r}$ = 0.2, $c^{r}$ = 1 mmol/g and '
          '$\\varepsilon_m$ = 4.7, is'),
    ('eq', '\\sigma_{\\mathrm{ion}}(T)=G_{\\mathrm{ion}}\\,\\sigma_{b,50}\\,r_C\\,\\exp\\left[-\\frac{\\Delta E_{\\mathrm{ion}}}{k_BT_{50}}-\\frac{E_{\\mathrm{ion}}\\,\\theta(T)}{k_B}\\right]'),
    ('p', 'where $r_C=w_Cc/(w_C^{r}c^{r})$ is the relative carboxylate loading, '
          '$\\Delta E_{\\mathrm{ion}}=E_{\\mathrm{ion}}-E_{\\mathrm{ion}}^{r}$ is the shift of the activation '
          'energy from the reference sheet and $G_{\\mathrm{ion}}$ = 10 the assumed gain of that sheet over the base '
          'channel. The '
          'proportionality to $w_C c$ reflects the observation that the charge-carrier density of TEMPO-oxidised '
          'fibril films rises with their surface charge density [@ZHU2024]. BNNS platelets block ion paths; with '
          'aspect ratio $\\alpha_B$, Nielsen\u2019s tortuosity [@NIELSEN1967] reduces both channels:'),
    ('eq', '\\sigma_p(T)=\\frac{\\sigma_b(T)+\\sigma_{\\mathrm{ion}}(T)}{1+\\tfrac{1}{2}\\alpha_B v_B}'),
    ('p', 'The through-plane thermal conductivity of the sheet is estimated with a Maxwell\u2013Garnett form for '
          'flat-lying platelets [@NAN1997], using the base value $k_0$ = 0.19 W/(m\u00b7K) of impregnated paper '
          '[@DOMBEK2020], an out-of-plane platelet conductivity $k_{B\\perp}$ and a depolarisation factor '
          '$L\\approx 0.95$:'),
    ('eq', 'k_p=k_0\\left[1+\\frac{v_B\\left(k_{B\\perp}-k_0\\right)}{k_0+L\\left(1-v_B\\right)\\left(k_{B\\perp}-k_0\\right)}\\right]'),
    ('p', '{F:fig_props} shows how the model behaves. ANF lowers the sheet permittivity by at most about 0.3, and '
          'nanofibril densification pushes it back up, so the permittivity lever is weak inside the composition '
          'bounds (panel a). The carboxylate channel can raise the 50 \u00b0C conductivity by more than a decade, and '
          'the coupling through (4) makes the same carboxylate content less effective in an ANF-rich sheet than an '
          'uncoupled model would predict (panel b). Panel c anticipates the main result: kraft paper crosses the '
          'design window with a ratio falling from 16 to 2, exact matching places the ratio near one in the middle '
          'of the window, and the robust graded design keeps it between about 2 and 12 with a flatter slope.'),
    ('fig', 'fig_props.png', 'Behaviour of the property model. (a) Permittivity of the ester-impregnated sheet versus '
            'ANF fraction ($c$ = 1 mmol/g, no BNNS). (b) Conductivity at 50 \u00b0C relative to kraft versus carboxylate '
            'content; the gray curve omits the dissociation coupling. (c) Paper-to-ester relaxation-time ratio of '
            'kraft, the exactly matched D5 and the wrap and core-side layers of the robust graded D7.', True),
    ('h2', 'D. Barrier Ladder and Polarity-Reversal Solver'),
    ('p', 'The ester conductivity follows the same Arrhenius form as (3), with $\\sigma_{o,50}$ = 1 pS/m and '
          '$E_{a,o}$ = 0.6 eV. The nominal $\\sigma_{o,50}$ reproduces the steady conductivity of about 100 fS/m '
          'measured for a 2 mm ester gap in series with 2 mm of ester-impregnated pressboard [@RUMPELT2017]. The '
          'quantity that decides how the stack behaves is the paper-to-oil relaxation-time ratio'),
    ('eq', '\\rho_\\tau(T)=\\frac{\\varepsilon_p\\,\\sigma_o(T)}{\\varepsilon_o\\,\\sigma_p(T)}'),
    ('p', 'For kraft paper in the nominal ester, $\\rho_\\tau$ = 16.4 at 60 \u00b0C and 1.93 at 110 \u00b0C. The '
          'potential $\\phi$ obeys the electro-quasistatic balance'),
    ('eq', '\\nabla\\cdot\\left(\\sigma\\nabla\\phi\\right)+\\frac{\\partial}{\\partial t}\\nabla\\cdot\\left(\\varepsilon_0\\varepsilon_r\\nabla\\phi\\right)=0'),
    ('p', 'For a single paper layer of thickness $d_p$ in series with an oil layer of thickness $d_o$ under a '
          'DC voltage $V$, (10) gives the steady free charge per unit area at the interface,'),
    ('eq', 'q_s=\\varepsilon_0V\\,\\frac{\\varepsilon_o\\sigma_p-\\varepsilon_p\\sigma_o}{\\sigma_od_p+\\sigma_pd_o}'),
    ('p', 'which vanishes when $\\rho_\\tau$ = 1 [@WAGNER1914]. This is the formal basis of exact matching. Inside '
          'a layer with a temperature gradient, however, the steady current density $J$ also deposits space charge,'),
    ('eq', '\\rho_v=\\varepsilon_0\\varepsilon_o\\,J\\,\\frac{\\mathrm{d}}{\\mathrm{d}x}\\left[\\frac{1}{\\sigma_o\\left(T\\left(x\\right)\\right)}\\right]'),
    ('p', 'and no choice of paper removes it, because it arises in the oil itself. The same gradient pushes the DC '
          'voltage toward the colder, less conductive oil gaps. Equations (11) and (12) together state the dilemma: '
          'a conductive paper removes interface charge but exposes the oil to its own thermal non-uniformity, while a '
          'resistive paper shields the oil under DC and stores interface charge that is released at reversal.'),
    ('p', 'Each oil gap is divided into four sub-layers and each solid layer into two, giving $n$ = 30 parallel RC '
          'elements whose properties follow the local temperature. Per unit area, layer $i$ has capacitance '
          '$C_i=\\varepsilon_0\\varepsilon_i/d_i$ and conductance $G_i=\\sigma_i/d_i$, carries the voltage $u_i$ and '
          'shares the current $J$:'),
    ('eq', 'C_i\\frac{\\mathrm{d}u_i}{\\mathrm{d}t}+G_iu_i=J\\left(t\\right),\\qquad\\sum_{i=1}^{n}u_i=V\\left(t\\right)'),
    ('p', 'Eliminating $J$ and $u_n$ leaves $n-1$ unknowns $\\mathbf{u}$ and a symmetric positive-definite pencil:'),
    ('eq', '\\mathbf{M}\\dot{\\mathbf{u}}+\\mathbf{K}\\mathbf{u}=\\left(C_n\\dot{V}+G_nV\\right)\\mathbf{1}'),
    ('p', 'where $\\mathbf{M}=\\mathrm{diag}(C_1,\\dots,C_{n-1})+C_n\\mathbf{1}\\mathbf{1}^{\\top}$ and '
          '$\\mathbf{K}=\\mathrm{diag}(G_1,\\dots,G_{n-1})+G_n\\mathbf{1}\\mathbf{1}^{\\top}$.'),
    ('p', 'The generalised eigenproblem $\\mathbf{K}\\boldsymbol{\\Phi}=\\mathbf{M}\\boldsymbol{\\Phi}\\boldsymbol{\\Lambda}$ '
          'with $\\boldsymbol{\\Phi}^{\\top}\\mathbf{M}\\boldsymbol{\\Phi}=\\mathbf{I}$ decouples (14). The reversal '
          'sequence is piecewise linear in time, so on each segment the forcing projected on mode $k$ has the form '
          '$g_{0k}+g_{1k}t$ and the modal coordinate evolves exactly as'),
    ('eq', 'q_k\\left(t\\right)=e^{-\\lambda_kt}q_k\\left(0\\right)+\\frac{g_{0k}}{\\lambda_k}\\left(1-e^{-\\lambda_kt}\\right)+g_{1k}\\left[\\frac{t}{\\lambda_k}-\\frac{1-e^{-\\lambda_kt}}{\\lambda_k^2}\\right]'),
    ('p', 'Fields are sampled at 140 log-spaced instants per segment, which resolves the oil relaxation (a few '
          'seconds at 110 \u00b0C) and the paper relaxation (minutes) without any time-step error. Two limits clarify '
          'the transient. Right after an instantaneous reversal the oil field equals the DC field minus twice the '
          'capacitive field, so the overshoot relative to the capacitive value $E_o^{C}$ is'),
    ('eq', '\\Gamma_o^{\\mathrm{inst}}=2-\\frac{E_o^{\\mathrm{DC}}}{E_o^{C}}'),
    ('p', 'which equals 2 for a perfectly resistive paper and 1 for a matched one. A finite $t_r$ lets part of the '
          'interface charge relax during the ramp and lowers the overshoot.'),
    ('h2', 'E. Robust Objective and Bayesian Design Loop'),
    ('p', 'Oil gaps and solid layers fail at different stresses, so their peaks are combined through a '
          'design-stress ratio $\\kappa$ = 3 (assumed and varied in Section V-E). The utilisation of scenario $s$ '
          'and the robust objective are'),
    ('eq', 'u_s\\left(\\mathbf{x}\\right)=\\max\\left(E_{o,s}^{\\max}\\left(\\mathbf{x}\\right),\\,\\frac{E_{p,s}^{\\max}\\left(\\mathbf{x}\\right)}{\\kappa}\\right)'),
    ('eq', 'J\\left(\\mathbf{x}\\right)=\\frac{1}{\\left|\\mathcal{S}\\right|}\\sum_{s\\in\\mathcal{S}}u_s\\left(\\mathbf{x}\\right),\\qquad\\mathbf{x}^{\\star}=\\arg\\min_{\\mathbf{x}\\in\\mathcal{X}}J\\left(\\mathbf{x}\\right)'),
    ('p', 'with $\\mathcal{X}$ the bounded, linearly constrained design set of Section III-A. A Gaussian process '
          'with a Mat\u00e9rn-5/2 kernel and automatic relevance determination is fitted to the evaluations '
          '$\\mathcal{D}_n=\\{(\\mathbf{x}_j,J_j)\\}_{j=1}^{n}$ in the unit cube; its posterior mean and variance are'),
    ('eq', '\\mu_n\\left(\\mathbf{x}\\right)=\\mathbf{k}_n\\left(\\mathbf{x}\\right)^{\\top}\\left(\\mathbf{K}_n+s_\\epsilon^{2}\\mathbf{I}\\right)^{-1}\\mathbf{J}_n'),
    ('eq', 's_n^2\\left(\\mathbf{x}\\right)=k\\left(\\mathbf{x},\\mathbf{x}\\right)-\\mathbf{k}_n\\left(\\mathbf{x}\\right)^{\\top}\\left(\\mathbf{K}_n+s_\\epsilon^{2}\\mathbf{I}\\right)^{-1}\\mathbf{k}_n\\left(\\mathbf{x}\\right)'),
    ('p', 'where $\\mathbf{K}_n$ is the kernel matrix, $\\mathbf{k}_n(\\mathbf{x})$ the vector of covariances with the '
          'evaluated designs and $s_\\epsilon^2$ a small nugget. The next design maximises expected improvement '
          '[@JONES1998] over the feasible set:'),
    ('eq', '\\mathrm{EI}\\left(\\mathbf{x}\\right)=\\left(J_n^{-}-\\mu_n-\\xi\\right)\\Phi\\left(z\\right)+s_n\\,\\varphi\\left(z\\right),\\qquad z=\\frac{J_n^{-}-\\mu_n-\\xi}{s_n}'),
    ('p', 'with $J_n^{-}$ the best value so far, $\\xi$ = 0.01 and $\\Phi$, $\\varphi$ the standard normal cdf and '
          'pdf. EI is evaluated on 3000 feasible random candidates, and the four best are refined by L-BFGS-B; a '
          'refined point is accepted only if it remains feasible. Algorithm 1 summarises the loop and Algorithm 2 '
          'the evaluation of one design.'),
    ('alg', 'Algorithm 1: Robust Bayesian design of the barrier furnish', [
        '<b>Input:</b> bounds and constraint of $\\mathcal{X}$; scenario set $\\mathcal{S}$; budget $N$ = 80; $n_0$ = 10',
        '<b>Output:</b> best composition $\\mathbf{x}^{\\star}$ and $J(\\mathbf{x}^{\\star})$',
        '1: draw $n_0$ feasible scrambled-Sobol designs; evaluate each with Algorithm 2',
        '2: <b>for</b> $n=n_0,\\dots,N-1$ <b>do</b>',
        '3: \u2003fit the GP hyper-parameters by marginal likelihood (two restarts)',
        '4: \u2003compute EI by (21) on 3000 feasible candidates',
        '5: \u2003refine the four best candidates by L-BFGS-B; keep the feasible maximiser $\\mathbf{x}_{n+1}$',
        '6: \u2003evaluate $J(\\mathbf{x}_{n+1})$ with Algorithm 2 and append it to $\\mathcal{D}_n$',
        '7: <b>end for</b>',
        '8: <b>return</b> the evaluated design with the smallest $J$']),
    ('alg', 'Algorithm 2: Scenario evaluation of one composition', [
        '<b>Input:</b> $\\mathbf{x}$; constants of {T:TABLE_PARAM}',
        '<b>Output:</b> $J(\\mathbf{x})$, peak fields and interface charge',
        '1: for each solid layer $l$ compute $c_l$, $p$ by (1), $\\varepsilon_p$ by (2) and $\\sigma_p(T)$ by (3)\u2013(7)',
        '2: <b>for</b> each $s\\in\\mathcal{S}$ <b>do</b>',
        '3: \u2003assign sub-layer temperatures and ageing factors; form $\\mathbf{M}$, $\\mathbf{K}$ of (14)',
        '4: \u2003solve the eigenproblem once; start from the capacitive field of $-U$',
        '5: \u2003propagate the five IEC segments with (15); record $E_o^{\\max}$, $E_p^{\\max}$ and $Q_i$',
        '6: \u2003compute $u_s$ by (17)',
        '7: <b>end for</b>',
        '8: <b>return</b> $J(\\mathbf{x})$ by (18)']),
    ('h2', 'F. Complexity Analysis'),
    ('p', 'For $n$ = 30 sub-layers the eigenproblem costs $\\mathcal{O}(n^3)$ once per scenario and each of the '
          '$5\\times 140$ sampled instants costs $\\mathcal{O}(n^2)$, so one scenario takes about 1.3 ms and one '
          'objective evaluation about 52 ms on one CPU core. The GP step costs $\\mathcal{O}(N^3)$ in the number of '
          'evaluations, about 0.3 s per iteration at $N$ = 80, which is negligible next to a laboratory handsheet '
          'trial. The 2-D model has 66 120 cells at $h$ = 1 mm and 264 480 at $h$ = 0.5 mm; with a time-step ladder '
          'that reuses at most three sparse LU factors, one full reversal sequence takes about 9 s and 59 s, '
          'respectively. Memory is dominated by the LU factors of the 2-D model, which is why the cache is bounded.'),
]

TABLE_PARAM = dict(
    caption='Notation and Nominal Constants of the Property and Field Models',
    header=['Symbol', 'Meaning', 'Nominal value', 'Basis'],
    rows=[
        ['$w_A,w_C,w_B$', 'mass fractions of ANF, B-CNF, BNNS', 'design variables', 'Section III-A'],
        ['$c_w,c_k$', 'carboxylate content, wrap and core side', '0\u20131.7 mmol/g', '[@ISOGAI2011]'],
        ['$p_0,\\beta_f$', 'kraft porosity, filling coefficient', '0.40, 0.40', 'assumed'],
        ['$\\varepsilon_C,\\varepsilon_A,\\varepsilon_B$', 'cellulose, ANF, h-BN permittivity', '6.0, 3.6, 3.76', 'assumed, assumed, [@LATURIA2018]'],
        ['$\\varepsilon_o$', 'natural ester permittivity', '3.2', '[@RUMPELT2017]'],
        ['$\\sigma_{b,50},E_{a,b}$', 'base paper conductivity at 50 \u00b0C, activation', '54.5 fS/m, 1.07 eV', '[@RUMPELT2017], [@KIER2024]'],
        ['$\\sigma_{o,50},E_{a,o}$', 'ester conductivity at 50 \u00b0C, activation', '1 pS/m, 0.60 eV', 'cross-checked [@RUMPELT2017]; assumed'],
        ['$G_{\\mathrm{ion}},E_\\mu,a$', 'ionic gain, hopping barrier, pair distance', '10, 0.45 eV, 0.45 nm', 'assumed'],
        ['$\\alpha_B$', 'BNNS aspect ratio (tortuosity)', '50', 'assumed'],
        ['$k_0,k_{B\\perp}$', 'thermal conductivity of paper, h-BN out of plane', '0.19, 4.0 W/(m\u00b7K)', '[@DOMBEK2020]; assumed'],
        ['$D_o,D_p$', 'ageing multipliers of oil and paper conductivity', '1 or 4', 'assumed, trend of [@KANUMURI2024]'],
        ['$\\kappa$', 'paper-to-oil design-stress ratio', '3', 'assumed'],
        ['$U,t_r$', 'reversal voltage, reversal time', '250 kV; 10 s, 120 s', '[@IEC57129]'],
    ],
    widths=[1.2, 2.55, 1.5, 1.85], wide=True)
