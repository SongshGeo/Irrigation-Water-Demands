# coding=utf-8

import arcpy
from arcpy import env
from arcpy.sa import *


def month_Day(year, month):
    def is_leap_year(year):
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    Leap_Year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    Common_Year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(year):
        N = Leap_Year
    else:
        N = Common_Year
    month_day = N[month - 1]
    return month_day


"""
以下部分 需要根据不同作物进行对应的修改，其中包括：

                                                                        Irrigation:   灌溉用水量
                                                                        Lini:         生长初期总时长
                                                                        Month_Day_1:  生长初期时，在第一个月生长的时长
                                                                        Month_Day_2:  生长初期时，在第二个月生长的时长
                                                                        h：           植株高度
                                                                        Month_1：     生长初期所在的第一个月份
                                                                        Month_1：     生长初期所在的第二个月份
                                                                        Kcmid_table:  生长中期植被系数 Table
                                                                        Kcend_table:  生长末期植被系数 Table
"""
# ################################################################################################
# ################################################################################################
# ##                              以下系数需要根据不同作物进行修改                                ##
# ################################################################################################
# ################################################################################################

year_list = list(range(1987, 2018))

Crop_list = [
    "Alfalfa_1",
    "Alfalfa_2",
    "Potato",
    "Sweet_Melon",
    "Sugar_beets",
    "Sunflower",
    "Sesame",
    "Rapeseed",
    "Cotton",
    "Barley",
    "Soybeans",
    "Sorghum",
    "Rice",
    "Maize",
    "ReMaize",
    "Winter_Wheat",
    "Wheat",
]

h_list = [0.7, 0.7, 0.6, 0.4, 0.5, 2, 1, 0.6, 1.3, 1, 0.7, 3, 1, 2, 2, 1, 1]
Kcmid_table_list = [
    1.2,
    1.2,
    1.15,
    1.05,
    1.2,
    1.15,
    1.1,
    1.15,
    1.15,
    1.15,
    1.15,
    1.2,
    1.2,
    1.2,
    1.2,
    1.15,
    1.15,
]
Kcend_table_list = [
    1.15,
    1.15,
    0.75,
    0.75,
    0.7,
    0.35,
    0.25,
    0.35,
    0.6,
    0.25,
    0.5,
    1.05,
    0.7,
    0.35,
    0.5,
    0.3,
    0.3,
]
Lini_list = [
    20,
    20,
    30,
    25,
    25,
    25,
    20,
    30,
    30,
    15,
    20,
    20,
    30,
    20,
    15,
    30,
    20,
]

"""
判定生长期是否跨月
"""
Month_1_list = [4, 6, 4, 4, 4, 4, 5, 3, 4, 4, 3, 4, 4, 4, 6, 10, 4]
Month_2_list = [5, 7, 5, 5, 4, 5, 6, 4, 5, 5, 4, 5, 5, 5, 7, 11, 4]
Month_Day_1_list = [
    6,
    7,
    11,
    16,
    25,
    16,
    6,
    6,
    3,
    11,
    12,
    11,
    15,
    11,
    11,
    16,
    25,
]
Month_Day_2_list = [
    14,
    13,
    19,
    9,
    25,
    9,
    14,
    24,
    27,
    4,
    8,
    9,
    15,
    9,
    4,
    14,
    25,
]


for year in year_list:
    for i in range(len(Crop_list)):

        Crop_type = Crop_list[i]

        Lini = Lini_list[i]
        h = h_list[i]

        Kcmid_table = Kcmid_table_list[i]
        Kcend_table = Kcend_table_list[i]

        Month_1 = Month_1_list[i]
        Month_2 = Month_2_list[i]

        Month_Day_1 = Month_Day_1_list[i]
        Month_Day_2 = Month_Day_2_list[i]

        Kcini_out = "F:/Crop  coefficient/%s_%s_Kc_ini.tif" % (Crop_type, year)
        Kcmid_out = "F:/Crop  coefficient/%s_%s_Kc_mid.tif" % (Crop_type, year)
        Kcend_out = "F:/Crop  coefficient/%s_%s_Kc_end.tif" % (Crop_type, year)

        # Lini = 20  # 生长初期总时间                              # 改
        # h = 0.7                                                 # 改
        # Kcmid_table = 1.2                                       # 改
        # Kcend_table = 1.15                                      # 改
        #
        #
        # '''
        # 判定生长期是否跨月
        # '''
        #
        # Month_1 = 4  # 生长初期时 所在的第一个月份                # 改
        # Month_2 = 5  # 生长初期时 所在的第二个月份                # 改
        #
        # Month_Day_1 = 6  # 生长初期时，在第一个月生长的时长       # 改
        # Month_Day_2 = 14  # 生长初期时，在第二个月生长的时长      # 改
        Irrigation = 50
        # ################################################################################################
        # ################################################################################################
        # ##                                   以下系数不需要调整                                        ##
        # ################################################################################################
        # ################################################################################################

        """
        计算过程指标
        """
        Typical_rainfall = 6  # 干旱地区典型降雨大小 5mm （ref: FAO56, P:116, 突尼斯）

        Month_All_day_1 = month_Day(year, Month_1)  # 第一个月总天数
        Month_All_day_2 = month_Day(year, Month_2)  # 第二个月总天数

        time_1 = year * 100 + Month_1
        time_2 = year * 100 + Month_2

        Prec_1 = "Q:/0 Climate/Study_Climate/Prec/Prec_%s.tif" % time_1
        Prec_2 = "Q:/0 Climate/Study_Climate/Prec/Prec_%s.tif" % time_2

        Pett_1 = "Q:/00 Oasis/Climate_data/Pett/Pett_%s.tif" % time_1
        Pett_2 = "Q:/00 Oasis/Climate_data/Pett/Pett_%s.tif" % time_2

        Wind_1 = "Q:/0 Climate/Study_Climate/Wind_2/Wind_%s.tif" % time_1
        Wind_2 = "Q:/0 Climate/Study_Climate/Wind_2/Wind_%s.tif" % time_2

        Temn_1 = "Q:/0 Climate/Study_Climate/Temn/Temn_%s.tif" % time_1
        Temn_2 = "Q:/0 Climate/Study_Climate/Temn/Temn_%s.tif" % time_2

        Temx_1 = "Q:/0 Climate/Study_Climate/Temx/Temx_%s.tif" % time_1
        Temx_2 = "Q:/0 Climate/Study_Climate/Temx/Temx_%s.tif" % time_2

        if Month_1 != Month_2:

            Prec_total = (
                Raster(Prec_1) * Month_Day_1 / Month_All_day_1
                + Raster(Prec_2) * Month_Day_2 / Month_All_day_2
            )  # 大多数植被生长跨月份，根据月内天数比例求生长初期的总降水量
            Wind_mean = (
                Raster(Wind_1) * Month_Day_1 / Lini
                + Raster(Wind_2) * Month_Day_2 / Lini
            )
            Temn_mean = (
                Raster(Temn_1) * Month_Day_1 / Lini
                + Raster(Temn_2) * Month_Day_2 / Lini
            )
            Temx_mean = (
                Raster(Temx_1) * Month_Day_1 / Lini
                + Raster(Temx_2) * Month_Day_2 / Lini
            )
            ET0 = (
                Raster(Pett_1) / Month_All_day_1 * Month_Day_1 / Lini
                + Raster(Pett_2) / Month_All_day_2 * Month_Day_2 / Lini
            )

        else:

            Prec_total = (
                Raster(Prec_1) * Lini / Month_All_day_1
            )  # 大多数植被生长跨月份，根据月内天数比例求生长初期的总降水量
            Wind_mean = Raster(Wind_1)
            Temn_mean = Raster(Temn_1)
            Temx_mean = Raster(Temx_1)
            ET0 = Raster(Pett_1) / Month_All_day_1

        Eso = 1.15 * ET0
        nw = RoundUp(Prec_total / Typical_rainfall) + 1
        I0 = (Prec_total + Irrigation) / nw  # 在播种之前进行一次灌溉，(降水+灌溉)/(降水次数+灌溉次数)
        Tw = Lini / (nw + 0.5)
        e_Tmin = 0.6108 * Exp((Temn_mean * 17.27) / (Temn_mean + 237.3))
        e_Tmax = 0.6108 * Exp((Temx_mean * 17.27) / (Temx_mean + 237.3))
        RH_min = e_Tmin / e_Tmax * 100

        TEW_10 = 10
        TEW_40 = Con((7 * Power(ET0, 0.5)) < 15, (7 * Power(ET0, 0.5)), 15)
        REW_10 = Con(
            (Con((6 / Power(ET0, 0.5)) > 2.5, (6 / Power(ET0, 0.5)), 2.5)) > 7,
            7,
            (Con((6 / Power(ET0, 0.5)) > 2.5, (6 / Power(ET0, 0.5)), 2.5)),
        )
        REW_40 = Con((TEW_40 - 0.01) > 6, 6, (TEW_40 - 0.01))
        T1_10 = REW_10 / Eso
        T1_40 = REW_40 / Eso

        Kcini_10 = Con(
            (
                Con(
                    T1_10 > Tw,
                    1.15,
                    (
                        TEW_10
                        - (TEW_10 - REW_10)
                        * Exp(
                            -(Tw - T1_10)
                            * Eso
                            * (1 + REW_10 / (TEW_10 - REW_10))
                            / TEW_10
                        )
                    )
                    / (Tw * ET0),
                )
            )
            < 1.15,
            (
                Con(
                    T1_10 > Tw,
                    1.15,
                    (
                        TEW_10
                        - (TEW_10 - REW_10)
                        * Exp(
                            -(Tw - T1_10)
                            * Eso
                            * (1 + REW_10 / (TEW_10 - REW_10))
                            / TEW_10
                        )
                    )
                    / (Tw * ET0),
                )
            ),
            1.15,
        )
        Kcini_40 = Con(
            (
                Con(
                    T1_40 > Tw,
                    1.15,
                    (
                        TEW_40
                        - (TEW_40 - REW_40)
                        * Exp(
                            -(Tw - T1_40)
                            * Eso
                            * (1 + REW_40 / (TEW_40 - REW_40))
                            / TEW_40
                        )
                    )
                    / (Tw * ET0),
                )
            )
            < 1.15,
            (
                Con(
                    T1_40 > Tw,
                    1.15,
                    (
                        TEW_40
                        - (TEW_40 - REW_40)
                        * Exp(
                            -(Tw - T1_40)
                            * Eso
                            * (1 + REW_40 / (TEW_40 - REW_40))
                            / TEW_40
                        )
                    )
                    / (Tw * ET0),
                )
            ),
            1.15,
        )
        Kcini = Con(
            I0 < 10,
            Kcini_10,
            Kcini_10 + (I - 10) / (40 - 10) * (Kcini_40 - Kcini_10),
        )
        Kcmid = Kcmid_table + (
            0.04 * (Wind_mean - 2) - 0.004 * (RH_min - 45)
        ) * Power((ET0 * 0 + h) / 3, 0.3)
        Kcend = Con(
            Kcend_table < 0.45,
            ET0 * 0 + Kcend_table,
            Kcend_table
            + (0.04 * (Wind_mean - 2) - 0.004 * (RH_min - 45))
            * Power((ET0 * 0 + h) / 3, 0.3),
        )

        """
        输出植被系数
        """
        Kcini.save(Kcini_out)
        Kcmid.save(Kcmid_out)
        Kcend.save(Kcend_out)

"""



"""
