#!/usr/bin/env python 3.9
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from src.calculate_pet import calculate_drought_index
from src.data_processing import main

# drought_index = calculate_pet.calculate_drought_index(result['temp'], result['shum'],result['pres'], result['srad'], result['lrad'], result['wind'], result['prec'])
# drought_index.plot()

result = main("data/natural")


def test_calculate_drought_index():
    drought_index = calculate_drought_index(**result)
    min_index = drought_index.min()
    assert min_index >= 0
    assert min_index < 1
    max_index = drought_index.max()
    assert max_index <= 100
