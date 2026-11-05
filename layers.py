"""Layer-by-layer properties of the robust graded design D7 (res_designs.json -> res_layers.json)."""
import json, sys
import props as pp, design as D

T_ION = float(sys.argv[1]) if len(sys.argv) > 1 else 85.0
v = json.load(open('res_designs.json'))['opt_graded']['v']
out = []
for k in range(5):
    x = D.to_x(v, k)
    x0 = dict(x); x0['c'] = 0.0
    T = T_ION + 273.15
    out.append(dict(layer=k, c=x['c'], eps=float(pp.permittivity(x)), s50=float(pp.paper_conductivity(x, 323.15)),
                    Ea=float(pp.apparent_activation(x)),
                    tr=[float(pp.tau_ratio(x, t + 273.15)) for t in (60, 85, 110)],
                    ion_frac=float(1 - pp.paper_conductivity(x0, T) / pp.paper_conductivity(x, T))))
if __name__ == '__main__':
    json.dump(out, open('res_layers.json', 'w'), indent=1)
    print(json.dumps(out[2], indent=1))
