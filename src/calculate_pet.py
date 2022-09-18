import math

CONSTANT = 273.3  # TODO 这里类似，常量要以这样的形式输入函数。


def calculate_drought_index(temp, shum, pres, srad, lrad, wind, prec, G=0):
    """
    _summary_

    Args:
        temp (_type_): _description_
        shum (_type_): _description_
        pres (_type_): _description_
        srad (_type_): _description_
        lrad (_type_): _description_
        wind (_type_): _description_
        prec (_type_): _description_
        G (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    VPD_0 = 0.6108 * (math.e ** ((17.27 * temp) / (temp + CONSTANT)))
    delta = (4098 * VPD_0) / ((temp + CONSTANT) * (temp + CONSTANT))
    VPD = VPD_0 * (1 - shum)
    r = 0.665 * 0.001 * pres
    R_n = srad - lrad
    ET_0 = (
        0.408 * delta * (R_n - G) + r * (900 / (temp + 273)) * wind * VPD
    ) / (delta + r * (1 + 0.34 * wind))
    drought_index = ET_0 / prec
    return drought_index
