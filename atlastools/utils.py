import math

sign_zero = lambda x: 1 if x > 0 else -1 if x < 0 else 0

sign = lambda x: 1 if x >= 0 else -1

dphi = lambda phi1, phi2 : abs(math.fmod((math.fmod(phi1, 2*math.pi) - math.fmod(phi2, 2*math.pi)) + 3*math.pi, 2*math.pi) - math.pi)

dR = lambda eta1, phi1, eta2, phi2: math.sqrt((eta1 - eta2)**2 + dphi(phi1, phi2)**2)

def et2pt(et, eta, m):

    return math.sqrt(et**2 - (m**2)/(math.cosh(eta)**2))

def pt2et(pt, eta, m):

    return math.sqrt(pt**2 + (m**2)/(math.cosh(eta)**2))

def Mvis(et1, phi1, et2, phi2):

    return math.sqrt(2. * et1 * et2 * (1. - math.cos(dphi(phi1, phi2))))

import os
import fnmatch

def all_files_matching(dir, pattern):
    
    matched = []
    for path, dirs, files in os.walk(dir):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                matched.append(os.path.join(path, file))
    return matched
