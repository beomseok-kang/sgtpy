from mixture import component

# # coarse grained methane and dodecane
# water = component('water', ms = 1.7311, sigma = 2.4539 , eps = 110.85,
#                     lambda_r = 8.308, lambda_a = 6., eAB = 1991.07, rcAB = 0.5624,
#                     rdAB = 0.4, sites = [0,2,2], Mw = 18.01528, cii = 1.5371939421515458e-20)
# eos = saftgammamie(water)
# eos.cii_correlation(overwrite=True)

# print('Critical point calculation success: ', eos.critical)
# if eos.critical:
#     print('Critical temperature:', eos.Tc, 'K')
#     print('Critical pressure:', eos.Pc, 'Pa')
#     print('Critical density:', eos.rhoc, 'mol/m^3')

hexane = component('hexane', ms=1.96720036, sigma=4.54762477,
                    eps=377.60127994, lambda_r=18.41193194,
                    cii=3.581510586936205e-19)

eos = saftvrmie(hexane)
eos.density(298.15, 101325, "L")