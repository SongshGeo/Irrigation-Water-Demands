import os
from asyncio.log import logger

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


def squeeze_nc_time_axis(nc_file, var_name, lon="lon", lat="lat", time="time"):
    p = xr.open_dataset(nc_file)
    p_mean = p.to_array(var_name).mean(dim=time)
    p_values = p_mean.values[0]
    p_mean = xr.DataArray(
        p_values, coords=[p_mean.coords[lat], p_mean.coords[lon]]
    )
    return p_mean


# 读取文件夹中的 nc 文件，代码已经调试完成
def get_files_in_folder(dir_path, postfix=".nc"):
    nc_files = []  # 什么意思，注释掉变为 NameError: name 'nc_files' is not defined
    if not os.path.isdir(dir_path):
        logger.error(f"{dir_path} not a valid folder.")  # 学习日志配置，目前仅输出[]
        return None
    else:
        file_lst = os.listdir(dir_path)
        for a_file in file_lst:
            if a_file.endswith(postfix):
                nc_files.append(os.path.join(dir_path, a_file))
        return nc_files


def main(dir_path):
    result = {}
    nc_files = get_files_in_folder(dir_path, postfix="nc")
    for nc_file in nc_files:
        var_name = os.path.basename(nc_file)[:4]
        var_mean = squeeze_nc_time_axis(
            nc_file, var_name, lon="lon", lat="lat", time="time"
        )
        result[var_name] = var_mean
    return result
