from __future__ import division, print_function, absolute_import
import numpy as np
import torch

# Third pertubation Eq 19
def a3m(x03, nsigma, eps3, f4, f5, f6):
    ter1 = -eps3*f4*nsigma
    ter2 = torch.exp(f5*nsigma + f6*nsigma**2)
    return ter1*ter2


def da3m_deta(x03, nsigma, eps3, f4, f5, f6):

    aux = torch.exp(f5*nsigma + f6*nsigma**2)
    a = -eps3*f4*nsigma
    a *= aux

    da = -eps3*f4*aux
    da *= (1. + nsigma * (f5 + 2*f6*nsigma))
    da *= x03
    return torch.hstack([a, da])


def d2a3m_deta(x03, nsigma, eps3, f4, f5, f6):

    aux = torch.exp(f5*nsigma + f6*nsigma**2)
    a = -eps3*f4*nsigma
    a *= aux

    da = -eps3*f4*aux
    da *= (1 + nsigma * (f5 + 2*f6*nsigma))
    da *= x03

    d2a = -eps3*f4*aux
    d2a *= (f5**2*nsigma+2*f6*nsigma*(3+2*f6*nsigma**2)+f5*(2+4*f6*nsigma**2))
    d2a *= x03**2
    return torch.hstack([a, da, d2a])
