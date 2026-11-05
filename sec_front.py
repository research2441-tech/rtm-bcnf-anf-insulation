# -*- coding: utf-8 -*-
TITLE = ('Robust Relaxation-Time Tuning of Banana-Nanocellulose/Aramid-Nanofibre Insulation Paper for '
         'Natural-Ester Converter Transformers under Thermal Gradients and Polarity Reversal')
AUTHORS = '[First Author], [Second Author], [Third Author], and [Corresponding Author]'
AFFIL = '[Department, Institution, City, Country]  |  Corresponding author: [email]  |  ORCID: [0000-0000-0000-0000]'

ABSTRACT = (
    'Converter transformers filled with natural ester expose their cellulose barriers to AC, DC and polarity-reversal '
    'stress at the same time. Mismatched dielectric relaxation times of oil and paper then leave Maxwell–Wagner '
    'charge at every interface; the intuitive remedy is a paper whose relaxation time equals that of the ester, '
    'but its behaviour under service temperature gradients was unknown. A composition-to-field design framework is '
    'developed for a paper of aramid nanofibres (ANF) derived from Twaron pulp, '
    'TEMPO-oxidised banana-pseudostem cellulose nanofibrils (B-CNF) and boron nitride nanosheets (BNNS). A '
    'permittivity-coupled ion-dissociation model links composition to permittivity and conductivity, an exact '
    'modal solution of a 30-element barrier ladder reproduces the IEC 60076-57-129 reversal sequence, and a '
    'Gaussian-process Bayesian optimiser minimises the mean stress utilisation over 40 thermal, reversal-time and '
    'ageing scenarios. Exact relaxation-time matching across 60–110 °C cut interface charge by 65% and the '
    'isothermal oil peak by 15%, yet raised the oil peak by 23% under thermal gradients, leaving no net benefit. '
    'The robust, radially graded design instead kept the relaxation-time ratio of its middle barrier between 2.7 and 9.5 and lowered mean '
    'utilisation by 7.9%, worst-case utilisation by 12.5% and peak barrier stress by 20.6% relative to kraft paper. '
    'Over 300 parameter draws the gain averaged 4.4% (95% CI 3.9–4.9%) and was positive in 86% of draws, with '
    'ester conductivity and ionic-channel strength explaining most of the variance. A 2-D axisymmetric model '
    'confirmed a 10.3% lower worst-case oil field. Bayesian optimisation reached the reference optimum within 0.5% '
    'in every run, with a median of 42 evaluations.')
INDEX_TERMS = ('Aramid nanofibre, Bayesian optimisation, converter transformer, interface charge, '
               'Maxwell–Wagner polarisation, nanocellulose insulation paper, natural ester, polarity reversal')

INTRO = [
    ('h1', 'I. INTRODUCTION'),
    ('p', 'Line-commutated HVDC links depend on converter transformers whose valve-side windings carry an AC voltage, '
          'a DC offset and, whenever power flow is reversed, a full change of DC polarity within seconds to minutes '
          '[@IEC57129]. The oil–cellulose barrier system between winding and core has to survive all three '
          'conditions. Under AC the field divides between oil and paper by permittivity; under steady DC it divides '
          'by conductivity; and during a reversal the charge left at each oil–paper interface by the DC stage adds '
          'to the new capacitive field. Kerr-effect measurements on oil–pressboard samples recorded oil fields '
          'about 1.47 times the capacitive value after the first reversal [@QI2015], and the shorter the reversal, the '
          'higher the transient stress [@QI2018; @HE2023]. Utilities now also ask for biodegradable, high-fire-point '
          'natural esters in place of mineral oil [@FOFANA2013], which changes both terms of the problem because '
          'esters have a higher permittivity and a conductivity roughly two decades above that of mineral oil '
          '[@RUMPELT2017].'),
    ('p', 'Two physical facts make the barrier design difficult. The first is that the relaxation time '
          '$\\tau=\\varepsilon/\\sigma$ of ester-impregnated kraft paper is one to two decades longer than that of the '
          'ester itself, so the DC stage parks most of the voltage on the solid layers and leaves interface charge '
          'that persists into the reversal [@DU2015; @MISHRA2017]. The second is that both conductivities are '
          'thermally activated with different activation energies, so the mismatch is not a single number. It '
          'changes by more than an order of magnitude between the hot winding side and the cooler core side, and it '
          'drifts as the oil acidifies and the cellulose depolymerises [@KANUMURI2024; @ALSHEHAWY2025]. Field '
          'calculations that include the temperature dependence of conductivity already show the steady-state oil '
          'field rising by tens of percent relative to isothermal estimates [@LI2021AEERO], and combined '
          'electrical\u2013thermal stress reshapes the charge in multi-layer oil gaps [@ZOU2019].'),
    ('p', 'Material research has attacked the solid side of this system from three directions. Low-permittivity '
          'papers made by blending aramid or other synthetic pulp into cellulose bring the paper permittivity closer '
          'to that of the oil and so relieve the AC oil stress [@MO2019; @WEI2023]. Nanocellulose and inorganic '
          'nanofillers densify the fibre network, fill voids and raise breakdown strength and tensile strength '
          '[@HUANG2017; @ZHANGD2024; @WEIW2025]. Aramid nanofibre (ANF) papers and ANF/BNNS films push breakdown '
          'strength and thermal conductivity higher still [@ZHANGW2025; @YANG2025; @LIM2020]. These routes have '
          'produced better papers, judged one property at a time and mostly under AC or plain DC stress.'),
    ('p', 'What these routes leave open is the coupling that governs polarity reversal. A paper with lower '
          'permittivity also changes the AC field split; a paper with lower conductivity, which most space-charge '
          'suppression strategies aim for [@ZHANGJ2021; @WANGZ2025], increases the relaxation-time mismatch with an '
          'ester and therefore the DC voltage share of the solid. The obvious corrective, borrowed from '
          'permittivity- and conductivity-graded spacers in DC gas-insulated equipment [@RACHMAWATI2021; '
          '@LIANG2022], is to tailor the paper so that its relaxation time equals that of the ester. Under a uniform '
          'temperature this choice removes the Maxwell–Wagner interface charge altogether [@WAGNER1914]. Whether '
          'it survives a radial temperature gradient, slow and fast reversals and ageing-driven conductivity drift '
          'has not been examined, and no composition model exists that tells a papermaker which furnish would '
          'deliver a prescribed $\\varepsilon$ and $\\sigma(T)$.'),
    ('p', 'This gap matters because exact matching makes the paper more conductive than kraft by roughly an order of '
          'magnitude. Under a temperature gradient the DC voltage then redistributes according to the local oil '
          'conductivity, and the colder oil gaps near the core receive more of it. A paper that eliminates interface '
          'charge at one temperature may therefore raise the oil-gap stress elsewhere. The real design question is '
          'which composition, and possibly which radial grading of composition, keeps the whole barrier system least stressed over the range of temperatures, reversal '
          'times and ageing states it will meet.'),
    ('p', 'The study answers that question with a computational design framework. Aramid nanofibres obtained by '
          'deprotonating Twaron pulp [@YANG2019] supply a low-permittivity phase without the void-forming '
          'micro-pulp of earlier aramid–cellulose papers; TEMPO-oxidised banana-pseudostem cellulose '
          'nanofibrils carry a controllable carboxylate content [@ISOGAI2011; @FARADILLA2016] that acts as an ionic '
          'conduction channel; and BNNS platelets regulate that channel by tortuosity. A permittivity-coupled '
          'dissociation model maps composition to $\\varepsilon_p$ and $\\sigma_p(T)$, an exact modal solution of '
          'the barrier ladder computes the full polarity-reversal sequence, and a constrained Gaussian-process '
          'Bayesian optimiser selects the furnish, including a winding-to-core gradient of carboxylate content, '
          'against a robust stress-utilisation objective. A 2-D axisymmetric electro-quasistatic model then checks '
          'the ranking where the 1-D model is weakest: at the winding corner, the end washer and the cylinder ends.'),
    ('h2', 'A. Research Objectives'),
    ('p', 'Three research questions organise the work. RQ1: does exact relaxation-time matching between paper and '
          'natural ester reduce the peak oil-gap and barrier stresses once radial temperature gradients, fast and '
          'slow reversals and ageing drift are included? RQ2: which composition of ANF, B-CNF carboxylate and BNNS, '
          'uniform or radially graded, minimises a scenario-averaged stress utilisation, and by how much relative to '
          'kraft paper and to published material classes? RQ3: how robust is that gain to the uncertain material '
          'constants, and how many design evaluations does a Bayesian loop need to find it?'),
    ('h2', 'B. Contributions'),
    ('p', 'The work makes four contributions. (i) A composition-to-property model in which the dissociation energy '
          'of carboxylate–counterion pairs depends on the composite permittivity, so that adding ANF lowers '
          'permittivity and simultaneously raises the activation energy of the ionic channel; its effect on the '
          'design is isolated by a dedicated ablation (Section V-D). (ii) An exact, time-step-free modal solution of '
          'the multilayer barrier ladder under the IEC reversal sequence with temperature-dependent layers, verified '
          'against stiff numerical integration and a 2-D finite-volume solver (Sections III-D and V-F). (iii) '
          'Evidence that exact Maxwell–Wagner matching is not robust under thermal gradients and that a '
          'partially tuned, radially graded paper is (Sections V-A and V-B). (iv) A constrained Bayesian design loop '
          'whose sample efficiency is compared with CMA-ES, random and quasi-random search over repeated seeds, '
          'together with Sobol and Monte-Carlo analyses that identify which constants must be measured first '
          '(Sections V-C and V-E).'),
    ('p', '{T:TABLE_CONTRIB} maps each contribution to the section and the evidence that supports it.'),
    ('table', 'TABLE_CONTRIB'),
    ('p', 'Section II reviews related work. Section III presents the models and the design loop, Section IV the '
          'protocol, Section V the results, Section VI the discussion, Section VII the limitations and Section VIII '
          'the conclusions.'),
]

TABLE_CONTRIB = dict(
    caption='Contribution-to-Evidence Map',
    header=['Contribution', 'Where', 'Evidence'],
    rows=[['(i) Coupled composition model', 'III-C, V-B, V-D', 'design error of 3.0% when coupling ignored; carboxylate optimum shifts with ANF'],
          ['(ii) Exact ladder solver', 'III-D, V-F', 'error below $10^{-9}$ against BDF; 2-D extrapolation within 0.4%'],
          ['(iii) Matching versus robust tuning', 'V-A, V-B, V-E', 'exact matching +2.3% in $J$; graded optimum \u22127.9%; positive gain for every $\\kappa$'],
          ['(iv) Bayesian loop and sensitivity', 'V-C, V-E', '15/15 runs within 0.5% of $J^\\star$; $S_T$ = 0.56 for ester conductivity']],
    widths=[1.05, 0.65, 1.7], wide=False)
