from __future__ import division, print_function, absolute_import
import numpy as np
import torch

# TO CHANGE
def association_config(eos):

    types = np.array(['B', 'P', 'N'])
    nozero = np.nonzero(eos.sites)
    types = types[nozero]
    ntypes = np.asarray(eos.sites)[nozero]
    nsites = len(types)
    S = np.array(eos.sites)
    S = S[S != 0]
    DIJ = np.zeros([nsites, nsites])
    int_i = []
    int_j = []
    for i in range(nsites):
        for j in range(nsites):
            bool1 = types[i] == 'B'
            bool2 = types[i] == 'P' and (types[j] == 'N' or types[j] == 'B')
            bool3 = types[i] == 'N' and (types[j] == 'P' or types[j] == 'B')
            if bool1 or bool2 or bool3:
                DIJ[i, j] = ntypes[j]
                int_i.append(i)
                int_j.append(j)

    indexabij = (int_i, int_j)
    diagasso = np.diag_indices(nsites)

    return S, DIJ, indexabij, nsites, diagasso


def Xass_solver(nsites, KIJ, diagasso, Xass0=None):

    if Xass0 is None:
        Xass = 0.2 * torch.ones(nsites)
    else:
        Xass = 1. * Xass0
    omega = 0.2

    for i in range(5):
        fo = 1. / (1. + KIJ@Xass)
        dXass = (1 - omega) * (fo - Xass)
        Xass += dXass

    KIJXass = KIJ@Xass
    dQ = (1./Xass - 1.) - KIJXass
    HIJ = - 1. * KIJ
    HIJ[diagasso] -= (1. + KIJXass)/Xass
    for i in range(15):
        dXass = torch.linalg.solve(HIJ, -dQ)
        Xnew = Xass + dXass

        is_nan = torch.isnan(Xnew)
        Xnew[is_nan] = 0.2

        Xnew_neg = Xnew < 0.
        Xnew[Xnew_neg] = 0.2*Xass[Xnew_neg]

        Xnew_big = Xnew > 1.
        Xnew[Xnew_big] = 1.

        Xass = Xnew
        KIJXass = KIJ@Xass
        dQ = (1./Xass - 1.) - KIJXass
        sucess = torch.linalg.norm(dQ) < 1e-9
        if sucess:
            break
        HIJ = - 1. * KIJ
        HIJ[diagasso] -= (1. + KIJXass)/Xass

    return Xass


def Iab(Kab, eta):

    gdhs = (1 - eta/2) / (1 - eta)**3
    Iab = Kab * gdhs

    return Iab


def dIab_drho(Kab, eta, deta_drho):

    eta_1 = 1-eta
    eta_13 = eta_1**3
    eta_14 = eta_13*eta_1

    gdhs = (1 - eta/2) / eta_13
    dgdhs = (2.5 - eta) * deta_drho / eta_14

    Iab = Kab * gdhs
    dIab = Kab * dgdhs
    return Iab, dIab


def d2Iab_drho(Kab, eta, deta_drho):
    eta_1 = 1-eta
    eta_13 = eta_1**3
    eta_14 = eta_13*eta_1
    eta_15 = eta_14*eta_1

    gdhs = (1 - eta/2) / eta_13
    dgdhs = (2.5 - eta) * deta_drho / eta_14
    d2gdhs = 3 * (3 - eta) * deta_drho**2 / eta_15

    Iab = Kab * gdhs
    dIab = Kab * dgdhs
    d2Iab = Kab * d2gdhs
    return Iab, dIab, d2Iab


def dXass_drho(rho, Xass, DIJ, Dabij, dDabij_drho, CIJ):
    brho = -(DIJ*(Dabij + rho * dDabij_drho))@Xass
    brho *= Xass**2
    dXass = torch.linalg.solve(CIJ, brho)
    return dXass


def d2Xass_drho(rho, Xass, dXass_drho, DIJ, Dabij, dDabij_drho, d2Dabij_drho,
                CIJ):

    b2rho = torch.sum(DIJ*(Xass*d2Dabij_drho + 2*dXass_drho*dDabij_drho), axis=1)
    b2rho *= - rho
    b2rho += 2 * (1/Xass - 1) / (rho**2)
    b2rho *= Xass**2
    b2rho += 2 * dXass_drho / (rho)
    b2rho += 2 * dXass_drho**2 / (Xass)

    d2Xass_drho = torch.linalg.solve(CIJ, b2rho)
    return d2Xass_drho


def association_solver(self, rhom, temp_aux, Xass0=None):
    if Xass0 is None:
        Xass = 0.2 * torch.ones(self.nsites)
    else:
        Xass = 1. * Xass0

    dia3 = temp_aux[4]
    eta, deta = self.eta_bh(rhom, dia3)

    Fab = temp_aux[19]
    Kab = temp_aux[20]
    iab = Iab(Kab, eta)
    Dab = self.sigma3 * Fab * iab
    Dabij = torch.zeros([self.nsites, self.nsites])
    Dabij[self.indexabij] = Dab
    KIJ = rhom * (self.DIJ*Dabij)
    Xass = Xass_solver(self.nsites, KIJ, self.diagasso, Xass0)
    return Xass


def association_check(self, rhom, temp_aux, Xass):

    dia3 = temp_aux[4]
    eta, deta = self.eta_bh(rhom, dia3)

    Fab = temp_aux[19]
    Kab = temp_aux[20]
    iab = Iab(Kab, eta)
    Dab = self.sigma3 * Fab * iab
    Dabij = torch.zeros([self.nsites, self.nsites])
    Dabij[self.indexabij] = Dab
    KIJ = rhom * (self.DIJ*Dabij)
    fo = Xass - 1. / (1. + KIJ@Xass)
    return fo
