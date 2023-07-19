"""
项目中会重复使用的工具函数
"""

import os
import pandas as pd


def size_convert(size) -> float:
    return round(size / 1048576, 2)


def datalist() -> list:
    """
    列出所有数据集
    @return: data文件夹中的所有数据集
    """
    try:
        datasets = os.listdir('data/')
    except BaseException.args:
        print("文件不存在")
    return datasets


def framlist(datasets: list) -> list:
    """
    @param datasets: 包含数据集的列表
    @return: 处理后的风场信息
    """
    framsets = []
    for filename in datasets:
        framname = filename[:2] + "号风场"
        framsets.append(framname)
    return framsets


def dfloc(start: str, end: str, df):
    """
    根据起止日期对风场数据进行切片
    @param start: 起始日期字符串 格式：2021-11-01 00:00:00
    @param end: 结束日期字符串 格式同上
    @param df:
    @return:
    """
    if int(start[-5:-3]) % 15 != 0:
        i = (int(start[-5:-3]) // 15) * 15
        i = str(i)
        if len(i) != 2:
            i = '0' + i
        start = start[:-5] + i + start[-3:]

    if int(end[-5:-3]) % 15 != 0:
        i = (int(end[-5:-3]) // 15) * 15
        i = str(i)
        if len(i) != 2:
            i = '0' + i
        end = end[:-5] + i + end[-3:]
    print('+++++++++++++', start)
    print('+++++++++++++', end)
    start = df[df['DATATIME'].str.startswith(start)].index[0]
    end = df[df['DATATIME'].str.startswith(end)].index[0]
    return df[start:end]
