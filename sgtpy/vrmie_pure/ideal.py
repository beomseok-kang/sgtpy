from __future__ import division, print_function, absolute_import
import numpy as np
import torch

h = 6.626070150e-34  # J s
me = 9.10938291e-31  # 1/Kg


# Equation 68
def aideal(rho, beta):
    broglie_vol = h / torch.sqrt(2*torch.pi * me / beta)
    a = torch.log(rho * broglie_vol**3) - 1
    print(a)
    return a


def daideal_drho(rho, beta):
    broglie_vol = h / torch.sqrt(2*torch.pi * me / beta)
    a = torch.log(rho * broglie_vol**3) - 1
    da = 1./rho
    return torch.hstack([a, da])


def d2aideal_drho(rho, beta):
    broglie_vol = h / torch.sqrt(2*torch.pi * me / beta)
    a = torch.log(rho * broglie_vol**3) - 1
    da = 1./rho
    d2a = -1/rho**2
    return torch.hstack([a, da, d2a])
