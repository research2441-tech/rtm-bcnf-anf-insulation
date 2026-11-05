# -*- coding: utf-8 -*-
DISC = [
    ('h1', 'VI. DISCUSSION'),
    ('h2', 'A. Interpretation of Findings'),
    ('p', 'The central result is that removing interface charge and minimising stress call for different '
          'papers. Equation (11) is exact for an isothermal pair of layers, and the isothermal maps confirm it. '
          'Equation (12) is equally exact and has no counterpart on the paper side: with a radial gradient the oil '
          'deposits its own space charge and the cold gaps take a larger share of the DC voltage. A resistive paper '
          'shields those gaps under DC because it absorbs most of the voltage; a matched paper removes that '
          'shielding. The optimum is therefore a compromise in which the paper relaxes a few times more slowly than '
          'the oil, enough to keep part of the DC voltage on the barriers, but quickly enough to limit the charge '
          'stored for the reversal. The optimal ratios found by the map (2.5–3.2 at 85 °C for gradients of '
          '20–40 K) and by the robust optimiser (2.7–9.5 over 60–110 °C) agree on that picture.'),
    ('p', 'The ablation explains how composition delivers it. The carboxylate channel is the only ingredient that '
          'can raise conductivity by the required factor, so its removal costs most. Its activation energy, about '
          '0.8 eV, lies between that of the base channel and that of the oil, which helps the paper track the oil '
          'across the window; the map with an oil-like activation energy showed the same benefit. ANF contributes '
          'less through permittivity than expected, because every nanofibril also removes oil-filled pore volume; '
          'its larger effect is to raise the dissociation energy and so temper the ionic channel. BNNS acts in the '
          'same direction through tortuosity. Grading then places the more conductive layers near the core, where '
          'the oil is coldest and the shielding argument is weakest.'),
    ('h2', 'B. Comparison with Prior Literature'),
    ('p', 'The finding that temperature-dependent conductivity raises the steady oil field is consistent with '
          'coupled converter-transformer calculations [@LI2021AEERO] and with the temperature dependence of '
          'interface charge in multi-layer gaps [@ZOU2019]. The finding that esters even out the DC field between '
          'oil and pressboard [@JACOB2026] appears here as the moderate ratio of kraft in ester at high temperature '
          '(1.93 at 110 °C), and the measured overshoot of about 1.5 after a first reversal [@QI2015] falls '
          'inside the 1.2–1.9 range that the isothermal map gives for ratios of 10–100 and reversal times of '
          '1–10 s. The work departs from the nano-modification literature in one respect: fillers that lower '
          'conductivity and suppress space charge in mineral-oil systems [@ZHANGJ2021; @ZHANGD2025] increased the '
          'utilisation in ester (D3, D4). It also adds a caveat to the graded-material idea from gas-insulated '
          'equipment [@RACHMAWATI2021; @XUE2023]: in an oil–cellulose stack, grading has to follow the oil '
          'temperature profile because the oil itself is temperature-graded.'),
    ('h2', 'C. Practical and Scientific Implications'),
    ('p', 'For a papermaker the design specification is a target $\\varepsilon_p$ and '
          '$\\sigma_p(T)$: a 50 °C conductivity 1.6–2.5 times that of kraft in the same ester, an activation '
          'energy near 0.9 eV and a grading of about 1.6 from wrap to core. Section V-E shows which measurements '
          'decide whether a given furnish meets it: the conductivity of the specific ester batch and the ionic gain '
          'of the B-CNF, both cheap to measure. For a transformer designer the main gain is on the barrier side (a '
          '20.6% lower worst-case barrier stress) and on the oil side under fast reversal and gradients, while the '
          'largest oil stress over all scenarios is essentially unchanged. Combining a low-permittivity matrix with '
          'the tuned conductivity (D8) indicates a further reduction of the mean oil stress, which gives a concrete '
          'target for future furnish development. On the method side, the exact ladder solution makes robust '
          'optimisation over dozens of scenarios cheap enough for a Bayesian loop, and the loop finds the optimum '
          'within about 40 evaluations, a realistic number of laboratory handsheet trials.'),
    ('h2', 'D. Failure Cases'),
    ('p', 'Three situations limit the benefit. When the ester is markedly less conductive than assumed, the '
          'tuned paper overshoots its target and behaves like the exactly matched D5; the Monte-Carlo draws with '
          'negative gain concentrate there, which is why $\\sigma_{o,50}$ leads the Sobol ranking. At a uniform high '
          'temperature kraft paper is already close to the optimum ratio, so a fixed furnish gains little in '
          'uniformly hot units. And the wrap at the winding corner of the graded design carried a higher field '
          'than kraft in the isothermal 2-D case, a local effect that the 1-D design loop cannot see and that a '
          'corner-aware objective, or a separate wrap composition, would have to address.'),
    ('h2', 'E. Pathway to Experimental Validation'),
    ('p', 'The predictions can be falsified with standard laboratory methods, and the order of the tests follows the '
          'sensitivity ranking. The DC conductivity of the ester batch should be measured first, by '
          'polarisation\u2013depolarisation currents on a guarded cell at 60, 85 and 110 \u00b0C, because it carries '
          'the largest Sobol index. Handsheets should then be formed along the predicted design direction: kraft '
          'furnish with 35% ANF, 10% BNNS and 10\u201315% B-CNF at three carboxylate levels between 1.0 and '
          '1.7 mmol/g, dried, impregnated with the same ester and conditioned to a fixed moisture. For each sheet the '
          'relaxation-time ratio follows from frequency-domain permittivity and the same current measurements; these '
          'data identify the ionic gain, the pair distance and the filling coefficient that the present model had to '
          'assume. With those constants fixed, the Bayesian loop of Algorithm 1 can propose the next handsheets '
          'directly, and the 40-evaluation budget found here is a realistic size for such a campaign. Pulsed '
          'electro-acoustic measurements on oil\u2013paper\u2013oil sandwiches held at a controlled temperature '
          'difference would then test the central claim of Section V-A: that interface charge falls with the ratio '
          'while the cold-side oil field rises once the ratio approaches one. AC, DC and polarity-reversal breakdown '
          'with two-parameter Weibull statistics, tensile index and accelerated ageing in ester at 130 \u00b0C and '
          '150 \u00b0C would complete the qualification before any furnish is used in a barrier system.'),
    ('h1', 'VII. LIMITATIONS'),
    ('p', 'The study is computational, and four limitations bound its conclusions. First, eleven of the twelve '
          'constants varied in Section V-E are assumptions; the ionic gain, the dissociation contact distance and the pore-filling '
          'coefficient in particular have not been measured for B-CNF/ANF sheets. The Sobol and Monte-Carlo analyses '
          'show the ranking is reasonably stable, but the absolute gains could change once handsheets are made, '
          'which threatens external validity more than internal validity. Second, the conduction model is ohmic. '
          'Charge injection, field-dependent conductivity [@SHI2023] and bipolar transport [@LU2025] are omitted, so '
          'homocharge near electrodes and the asymmetric behaviour of the two reversals are not represented. Third, '
          'mechanical strength, partial-discharge inception and breakdown strength are outside the objective; the '
          'composition bounds keep the furnish within loadings reported for strong papers [@HU2022; @YANG2025], but '
          'tensile and breakdown tests are required before any furnish is adopted. Fourth, ageing enters only as '
          'conductivity multipliers. Moisture migration between ester and paper, acid formation and the faster '
          'depolymerisation of oxidised cellulose [@VASOVIC2019; @JUSNER2021] could shift the optimum over the '
          'service life. Future work should measure the permittivity $\\varepsilon_p$, the conductivity $\\sigma_p(T)$ and the breakdown strength on '
          'handsheets along the predicted design direction, replace the ohmic model by a bipolar transport model '
          'calibrated with pulsed electro-acoustic data, and run the Bayesian loop on real handsheet trials.'),
    ('h1', 'VIII. CONCLUSION'),
    ('p', 'Converter transformers filled with natural ester need barrier papers that tolerate AC, DC and polarity '
          'reversal under radial temperature gradients. A composition-to-field framework was built that predicts '
          'the permittivity and temperature-dependent conductivity of an ANF/B-CNF/BNNS paper from its furnish, '
          'computes the IEC reversal sequence exactly for a multilayer barrier stack, and selects the furnish by '
          'Bayesian optimisation of a robust stress utilisation over 40 thermal, reversal-time and ageing scenarios. '
          'Exact Maxwell–Wagner matching removed interface charge and lowered the isothermal oil overshoot, but '
          'under thermal gradients it raised the oil peak by 23% and gave no net benefit. The robust, radially '
          'graded paper kept the relaxation of its middle barrier 2.7–9.5 times slower than the ester and lowered the mean '
          'utilisation by 7.9%, the worst-case utilisation by 12.5% and the worst barrier stress by 20.6% relative to '
          'kraft; under parameter uncertainty the mean gain was 4.4% and was positive in 86% of draws, and a 2-D '
          'model confirmed a 10.3% lower worst-case oil field. The Bayesian loop found the optimum within 0.5% in '
          'every run, with a median of 42 evaluations. The design target that emerges is partial tuning '
          'of the relaxation time. The main limitation is that the ionic-channel and pore-filling constants are assumed, and the '
          'next step is to measure them on handsheets and close the Bayesian loop with laboratory trials.'),
]

BACK = [
    ('h1', 'DATA AVAILABILITY'),
    ('p', 'All results were generated by the released code from the constants listed in {T:TABLE_PARAM}. No experimental '
          'dataset was produced. Literature values used for calibration are cited in the text.'),
    ('h1', 'CODE AVAILABILITY'),
    ('p', 'The Python code for the property model, the ladder and 2-D solvers, the design loop and all figures is '
          'provided as supplementary material and will be deposited in a public repository upon acceptance.'),
    ('h1', 'AUTHOR CONTRIBUTIONS'),
    ('p', '[To be completed by the authors using the CRediT taxonomy.]'),
    ('h1', 'CONFLICT OF INTEREST'),
    ('p', 'The authors declare no competing interests.'),
    ('h1', 'ACKNOWLEDGMENT'),
    ('p', '[Funding and institutional support to be stated by the authors.]'),
]
