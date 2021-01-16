
import numpy
import scipy.constants

frequency_0 = 2E+9
wavelength_0 = scipy.constants.c / frequency_0          # 600nm
thickness_0 = 5E-2             # 5cm
conductivity_1 = 0.0023


dielectric_0 = 1
permeability_0 = 1
dielectric_1 = 6.76 + 1j * conductivity_1 / (2 * numpy.pi * frequency_0)
permeability_1 = 1
dielectric_2 = 1
permeability_2 = 1


def Reflection_s(angle_i, eps_i, mu_i, eps_j, mu_j):
    n_i = numpy.sqrt(eps_i * mu_i)
    n_j = numpy.sqrt(eps_j * mu_j)
    n_ij = n_j / n_i

    fraction = mu_j * numpy.cos(angle_i) - mu_i * numpy.sqrt((1+0j) * (n_ij ** 2 - numpy.sin(angle_i) ** 2))
    denominator = mu_j * numpy.cos(angle_i) + mu_i * numpy.sqrt((1+0j) * (n_ij ** 2 - numpy.sin(angle_i) ** 2))
    return fraction / denominator

def Reflection_p(angle_i, eps_i, mu_i, eps_j, mu_j):
    n_i = numpy.sqrt(eps_i * mu_i)
    n_j = numpy.sqrt(eps_j * mu_j)
    n_ij = n_j / n_i

    fraction = mu_i * (n_ij ** 2) * numpy.cos(angle_i) - mu_j * numpy.sqrt((1+0j) * (n_ij ** 2 - numpy.sin(angle_i) ** 2))
    denominator = mu_i * (n_ij ** 2) * numpy.cos(angle_i) + mu_j * numpy.sqrt((1+0j) * (n_ij ** 2 - numpy.sin(angle_i) ** 2))
    return fraction / denominator

def PhaseShiftElement( angle_i, lamb_0, h_0, eps_0, mu_0, eps_1, mu_1):
    n_0 = numpy.sqrt(eps_0 * mu_0)
    n_1 = numpy.sqrt(eps_1 * mu_1)
    n_01 = n_1 / n_0
    return (2 * numpy.pi * h_0 / lamb_0) * numpy.sqrt((n_01 ** 2 - numpy.sin(angle_i) ** 2))

# 東北大学　計算分子科学研究室講義より
# Fresnelの式書いてあるよ
# https://comp.chem.tohoku.ac.jp/hirose/chap1-3.pdf


calc_number = 100
max_angle = 90
for i in range(0, calc_number):
    angle_deg = i * max_angle / calc_number
    angle_rad = numpy.pi * angle_deg / 180

    phaseshift = PhaseShiftElement(angle_rad, wavelength_0, thickness_0, dielectric_0, permeability_0, dielectric_1, permeability_1)
    

    ref_01_s = Reflection_s( angle_rad, dielectric_0, permeability_0, dielectric_1, permeability_1)
    ref_01_p = Reflection_p( angle_rad, dielectric_0, permeability_0, dielectric_1, permeability_1)
    ref_10_s = Reflection_s( -angle_rad, dielectric_1, permeability_1, dielectric_0, permeability_0)
    ref_10_p = Reflection_p( -angle_rad, dielectric_1, permeability_1, dielectric_0, permeability_0)

    ref_12_s = Reflection_s( angle_rad, dielectric_1, permeability_1, dielectric_2, permeability_2)
    ref_12_p = Reflection_p( angle_rad, dielectric_1, permeability_1, dielectric_2, permeability_2)
    ref_21_s = Reflection_s( -angle_rad, dielectric_2, permeability_2, dielectric_1, permeability_1)
    ref_21_p = Reflection_p( -angle_rad, dielectric_2, permeability_2, dielectric_1, permeability_1)

    #ref_all_s = (ref_01_s + ref_12_s * (tr_01_s * tr_10_s - ref_01_s * ref_10_s) * numpy.exp(2j * phaseshift)) / ( 1 - ref_10_s * ref_12_s * numpy.exp(2j * phaseshift))
    #ref_all_p = (ref_01_p + ref_12_p * (tr_01_p * tr_10_p - ref_01_p * ref_10_p) * numpy.exp(2j * phaseshift)) / ( 1 - ref_10_p * ref_12_p * numpy.exp(2j * phaseshift))

    #ref_all_s = (ref_01_s + ref_12_s * numpy.exp( 2j * phaseshift)) / (1 + ref_01_s * ref_12_s * numpy.exp(2j * phaseshift))
    #ref_all_p = (ref_01_p + ref_12_p * numpy.exp( 2j * phaseshift)) / (1 + ref_01_p * ref_12_p * numpy.exp(2j * phaseshift))

    text = ""
    text += str(angle_deg) + ","
    text += str(abs(ref_01_s)) + ","
    text += str(abs(ref_01_p)) + ","
    #text += str(ref_12_s) + ","
    #text += str(ref_12_p) + ","
    #text += str(abs(ref_all_s)) + ","
    #text += str(abs(ref_all_p)) + ","
    #text += str(phaseshift)

    print(text)







