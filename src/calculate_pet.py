import imp
import logging
import math
import os
from asyncio.constants import SSL_HANDSHAKE_TIMEOUT
from ipaddress import v4_int_to_packed
from pydoc import plain
from turtle import width

import matplotlib.pyplot as plt
import numpy as np


def calculate_drought_index(temp, shum, pres, srad, lrad, wind, prec, G=0):
    VPD_0 = 0.6108 * (math.e ** ((17.27 * temp) / (temp + 237.3)))
    delta = (4098 * VPD_0) / ((temp + 237.3) * (temp + 237.3))
    VPD = VPD_0 * (1 - shum)
    r = 0.665 * 0.001 * pres
    R_n = srad - lrad
    ET_0 = (
        0.408 * delta * (R_n - G) + r * (900 / (temp + 273)) * wind * VPD
    ) / (delta + r * (1 + 0.34 * wind))
    drought_index = ET_0 / prec
    return drought_index
