from __future__ import division, print_function, absolute_import
import numpy as np
import torch

def lngmie(ghs, g1s, g2s, be, be2):

    lng = torch.log(ghs) + (be*g1s+be2*g2s)/ghs
    return lng


def dlngmie_drho(ghs, g1s, g2s, be, be2):

    ghs, dghs = ghs

    g1, dg1 = g1s
    g2, dg2 = g2s

    aux = (be*g1+be2*g2)

    lng = torch.log(ghs) + aux/ghs

    dlng = be * ghs * (dg1 + be * dg2)
    dlng += dghs * (ghs - aux)
    dlng /= ghs**2
    return torch.hstack([lng, dlng])


def d2lngmie_drho(ghs, g1s, g2s, be, be2):

    ghs, dghs, d2ghs = ghs
    g1, dg1, d2g1 = g1s
    g2, dg2, d2g2 = g2s

    ghs2 = ghs**2
    ghs3 = ghs2 * ghs
    dghs2 = dghs**2
    aux1 = be*g1+be2*g2
    aux2 = be*dg1+be2*dg2

    lng = torch.log(ghs) + aux1/ghs

    dlng = ghs * aux2
    dlng += dghs * (ghs - aux1)
    dlng /= ghs2

    d2lng = 2*dghs2*aux1
    d2lng += ghs2*(d2ghs + be * (d2g1+be*d2g2))
    d2lng += ghs*(-2*dghs*aux2-dghs2 - aux1*d2ghs)
    d2lng /= ghs3

    return torch.hstack([lng, dlng, d2lng])
