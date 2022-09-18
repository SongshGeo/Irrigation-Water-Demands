#!/usr/bin/env python 3.9
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from src.data_processing import get_files_in_folder, main

valid_paths = ("data/natural", "data/natural/")

invalid_path = "data/natural_data.zip"


def test_load_data():
    for path in valid_paths:
        # Only get nc file
        nc_files = get_files_in_folder(path)
        assert len(nc_files) == 7

        # All other files
        all_files = get_files_in_folder(path, postfix="")
        assert len(all_files) == 13


def test_error_message():
    result = get_files_in_folder(invalid_path)
    assert result is None


def test_process_nc_file():
    result = main(valid_paths[0])
    assert len(result) == 7
    for var, val in result.items():
        assert len(val.shape) == 2
