import numpy as np
import pandas as pd
from scipy.interpolate  import  interp1d
import itertools
from functools import lru_cache

from collections import namedtuple
from typing import Optional, List, Dict, Union, Tuple


# obtain the list from csv data
def get_f_list():

    f_list = pd.read_csv('f_value.csv', skiprows = 1)
    f_list['ガラス仕様の区分'] = f_list['ガラス仕様の区分'].fillna(method='ffill')
    f_list['期間'] = f_list['期間'].fillna(method='ffill')
    f_list.columns=['Glass Spec',
                    'Season',
                    'l_value',
                    '1N','1NE','1E','1SE','1S','1SW','1W','1NW',
                    '2N','2NE','2E','2SE','2S','2SW','2W','2NW',
                    '3N','3NE','3E','3SE','3S','3SW','3W','3NW',
                    '4N','4NE','4E','4SE','4S','4SW','4W','4NW',
                    '5N','5NE','5E','5SE','5S','5SW','5W','5NW',
                    '6N','6NE','6E','6SE','6S','6SW','6W','6NW',
                    '7N','7NE','7E','7SE','7S','7SW','7W','7NW',
                    '8N','8NE','8E','8SE','8S','8SW','8W','8NW']
    f_list['Season'] = f_list['Season'].replace( { '冷房':'Cooling', '暖房':'Heating' } )
    f_list['Glass Spec'] = f_list['Glass Spec'].replace( { 1:'Type1', 2:'Type2', 3:'Type3', 4:'Type4', 5:'Type5', 6:'Type6', 7:'Type7' } )

    return f_list

# get l and nu list in table
def get_table_value(glass_type: str, season: str, region: int, direction: str):

    r = str(region)

    d = {
        'n': 'N',
        'ne': 'NE',
        'e': 'E',
        'se': 'SE',
        's': 'S',
        'sw': 'SW',
        'w': 'W',
        'nw': 'NW'
    }[direction]

    f_list = get_f_list()

    return f_list[(f_list['Season'] == season) & (f_list['Glass Spec'] == glass_type)].loc[:, ['l_value', r + d]]


# get f1 or f2 value
@lru_cache(maxsize=None)
def get_f_value(glass_type: str, season: str, region: int, direction: str, l_value: float) -> float:

    if l_value > 20.0:
        l_value = 20.0

    dat = get_table_value(glass_type, season, region, direction)

    return float(interp1d(dat.iloc[:, 0], dat.iloc[:, 1])(l_value))


Sunshade = namedtuple('Sunshade', [
    'existence',
    'input_method',
    'depth',
    'd_h',
    'd_e',
    'x1',
    'x2',
    'x3',
    'y1',
    'y2',
    'y3',
    'z_x_pls',
    'z_x_mns',
    'z_y_pls',
    'z_y_mns',
])


def get_f_not_input(season: str, region: int) -> Optional[float]:
    """
    Args:
        season: 期間
        region: 地域の区分
    Returns:
        f値
    """

    if season == 'heating':
        if region == 8:
            return None
        else:
            return 0.51
    elif season == 'cooling':
        return 0.93
    else:
        raise ValueError()


def get_f(season: str, region: int, direction: str, sunshade: Optional[Sunshade]) -> Optional[float]:
    """
    Args:
        season: 期間
        region: 地域の区分
        direction: 方位
        sunshade: 日除けの形状
    Returns:
        f値
    """

    if sunshade is None:
        return get_f_not_input(season, region)
    elif sunshade.existence:
        return get_f_existence(season, region, direction, sunshade)
    elif not sunshade.existence:
        return get_f_not_existence(season, region, direction)
    else:
        raise ValueError()


def get_f_existence(season: str, region: int, direction: str, sunshade: Sunshade) -> Optional[float]:
    """
    Args:
        season: 期間
        region: 地域の区分
        direction: 方位
        sunshade: 日除けの形状
    Returns:
        f値
    """

    if sunshade.input_method == 'simple':
        if season == 'heating':
            if region == 8:
                return None
            else:
                if direction == 'sw' or direction == 's' or direction == 'se':
                    return min(0.01 * (5 + 20 * (3 * sunshade.d_e + sunshade.d_h)/sunshade.depth), 0.72)
                elif (direction == 'n' or direction == 'ne' or direction == 'e'
                      or direction == 'nw' or direction == 'w'):
                    return min(0.01 * (10 + 15 * (2 * sunshade.d_e + sunshade.d_h) / sunshade.depth), 0.72)
                elif direction == 'top':
                    return 1.0
                elif direction == 'bottom':
                    return 0.0
                else:
                    raise ValueError()
        elif season == 'cooling':
            if region == 8:
                if direction == 'sw' or direction == 's' or direction == 'se':
                    return min(0.01 * (16 + 19 * (2 * sunshade.d_e + sunshade.d_h)/sunshade.depth), 0.93)
                elif (direction == 'n' or direction == 'ne' or direction == 'e'
                      or direction == 'nw' or direction == 'w'):
                    return min(0.01 * (16 + 24 * (2 * sunshade.d_e + sunshade.d_h) / sunshade.depth), 0.93)
                elif direction == 'top':
                    return 1.0
                elif direction == 'bottom':
                    return 0.0
                else:
                    raise ValueError()
            else:
                if direction == 's':
                    return min(0.01 * (24 + 9 * (3 * sunshade.d_e + sunshade.d_h)/sunshade.depth), 0.93)
                elif (direction == 'n' or direction == 'ne' or direction == 'e' or direction == 'se'
                      or direction == 'nw' or direction == 'w' or direction == 'sw'):
                    return min(0.01 * (16 + 24 * (2 * sunshade.d_e + sunshade.d_h) / sunshade.depth), 0.93)
                elif direction == 'top':
                    return 1.0
                elif direction == 'bottom':
                    return 0.0
                else:
                    raise ValueError()
        else:
            raise ValueError()
    elif sunshade.input_method == 'detailed':
        raise NotImplementedError()
    else:
        raise ValueError()


def get_f_not_existence(season: str, region: int, direction: str) -> Optional[float]:
    """
    Args:
        season: 期間
        region: 地域の区分
        direction: 方位
    Returns:
        f値
    Notes:
        第3章第4部「日射熱取得率」における表１・表２のうち、ガラスの仕様の区分1の値を採用した。
    """

    return {
        'heating': {
            'top': {1: 0.90, 2: 0.91, 3: 0.91, 4: 0.91, 5: 0.90, 6: 0.90, 7: 0.90, 8: None}[region],
            'n': {1: 0.862, 2: 0.860, 3: 0.862, 4: 0.861, 5: 0.867, 6: 0.870, 7: 0.873, 8: None}[region],
            'ne': {1: 0.848, 2: 0.851, 3: 0.850, 4: 0.846, 5: 0.838, 6: 0.839, 7: 0.833, 8: None}[region],
            'e': {1: 0.871, 2: 0.873, 3: 0.869, 4: 0.874, 5: 0.874, 6: 0.874, 7: 0.868, 8: None}[region],
            'se': {1: 0.892, 2: 0.888, 3: 0.885, 4: 0.883, 5: 0.894, 6: 0.896, 7: 0.892, 8: None}[region],
            's': {1: 0.892, 2: 0.880, 3: 0.884, 4: 0.874, 5: 0.894, 6: 0.889, 7: 0.896, 8: None}[region],
            'sw': {1: 0.888, 2: 0.885, 3: 0.885, 4: 0.882, 5: 0.891, 6: 0.885, 7: 0.894, 8: None}[region],
            'w': {1: 0.869, 2: 0.874, 3: 0.871, 4: 0.872, 5: 0.871, 6: 0.874, 7: 0.870, 8: None}[region],
            'nw': {1: 0.850, 2: 0.850, 3: 0.850, 4: 0.845, 5: 0.840, 6: 0.844, 7: 0.834, 8: None}[region],
            'bottom': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: None}[region],
        }[direction],
        'cooling': {
            'top': {1: 0.93, 2: 0.93, 3: 0.93, 4: 0.94, 5: 0.93, 6: 0.94, 7: 0.94, 8: 0.93}[region],
            'n': {1: 0.853, 2: 0.857, 3: 0.853, 4: 0.852, 5: 0.860, 6: 0.847, 7: 0.838, 8: 0.848}[region],
            'ne': {1: 0.865, 2: 0.864, 3: 0.862, 4: 0.861, 5: 0.863, 6: 0.862, 7: 0.861, 8: 0.857}[region],
            'e': {1: 0.882, 2: 0.877, 3: 0.870, 4: 0.881, 5: 0.874, 6: 0.880, 7: 0.881, 8: 0.877}[region],
            'se': {1: 0.864, 2: 0.858, 3: 0.853, 4: 0.853, 5: 0.854, 6: 0.852, 7: 0.849, 8: 0.860}[region],
            's': {1: 0.807, 2: 0.812, 3: 0.799, 4: 0.784, 5: 0.807, 6: 0.795, 7: 0.788, 8: 0.824}[region],
            'sw': {1: 0.860, 2: 0.861, 3: 0.859, 4: 0.850, 5: 0.858, 6: 0.852, 7: 0.847, 8: 0.858}[region],
            'w': {1: 0.880, 2: 0.878, 3: 0.883, 4: 0.876, 5: 0.875, 6: 0.880, 7: 0.880, 8: 0.876}[region],
            'nw': {1: 0.866, 2: 0.864, 3: 0.865, 4: 0.861, 5: 0.862, 6: 0.864, 7: 0.862, 8: 0.859}[region],
            'bottom': 0.0,
        }[direction],
    }[season]

