from typing import List, Tuple

from nu_value import get_nu_c, get_nu_h
from f_value import get_f, Sunshade, get_f_value


def get_direction(main_direction: str) -> Tuple[str, str, str, str]:
    """
    Args:
        main_direction: 主方位
    Returns:
        主方位、主方位＋90°、主方位＋180°、主方位＋270°　の方位（タプル）
    """

    directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']

    idx = directions.index(main_direction)

    return directions[idx], directions[idx-6], directions[idx-4], directions[idx-2]


def calc_designed_indices(
        model_house: dict,
        region: int,
        main_direction: str,
        upper_u: float,
        wall_u: float,
        lower_u: float,
        base_psi_outside: float,
        base_psi_inside: float,
        window_u: float,
        window_attached_u: float,
        window_eta: float,
        window_attached_eta: float,
        l_value_h: float,
        l_value_c: float
):
    """
    Args:
        model_house: モデルハウス（面積等）の辞書
        region: 地域の区分
        main_direction: 主方位
        upper_u: 上部のU値, W/m2K
        wall_u: 外壁のU値, W/m2K
        lower_u: 下部のU値, W/m2K
        base_psi_outside: 土間床外壁側のψ値, W/mK
        base_psi_inside: 土間床床下側のψ値, W/mK
        window_u: 窓のU値, W/m2K
        window_attached_u: 窓（障子）のU値, U値, W/m2K
        window_eta: 窓のη値
        window_attached_eta: 窓（障子）のη値
        l_value_h: 暖房期の日除けのl_value
        l_value_c: 冷房期の日除けのl_value
    Returns:

    """

    house_type = model_house['house_type']
    if house_type == 'attached':
        raise ValueError

    # 外皮の面積の合計, m2
    a_evp_total = model_house['a_evp_total']

    # 屋根又は天井の面積, m2
    a_evp_roof = model_house['a_evp_roof']

    # 断熱した床面積の合計, m2
    a_evp_f_total = model_house['a_evp_f_total']

    # その他の土間床等の外周部の長さ（室外側）（4方位）, m
    # その他の土間床等の外周部の長さ（室内側）, m
    l_base_total_outside = model_house['l_base_total_outside']
    l_base_total_inside = model_house['l_base_total_inside']

    # 窓の面積の合計（4方位）, m2
    a_evp_window = model_house['a_evp_window']

    # ドアの面積（4方位）, m2
    a_evp_door = model_house['a_evp_door']

    # 壁の面積（4方位）, m2
    a_evp_wall = model_house['a_evp_wall']

    q = a_evp_roof * upper_u\
        + a_evp_f_total * lower_u\
        + sum(l_base_total_outside) * base_psi_outside\
        + l_base_total_inside * base_psi_inside * 0.7\
        + (a_evp_window[0] + a_evp_window[2] + a_evp_window[3]) * window_u\
        + a_evp_window[1] * window_attached_u\
        + sum(a_evp_door) * window_u\
        + sum(a_evp_wall) * wall_u

    u_a = q / a_evp_total

    d0, d90, d180, d270 = get_direction(main_direction)

    f_c_0 = get_f_value(glass_type='Type1', season='Cooling', region=region, direction=d0, l_value=l_value_c)
    f_c_90 = get_f_value(glass_type='Type1', season='Cooling', region=region, direction=d90, l_value=l_value_c)
    f_c_180 = get_f_value(glass_type='Type1', season='Cooling', region=region, direction=d180, l_value=l_value_c)
    f_c_270 = get_f_value(glass_type='Type1', season='Cooling', region=region, direction=d270, l_value=l_value_c)

    m_c = a_evp_roof * upper_u * 0.034 * get_nu_c(region=region, direction='top')\
        + a_evp_window[0] * window_eta * f_c_0 * get_nu_c(region=region, direction=d0)\
        + a_evp_window[1] * window_attached_eta * f_c_90 * get_nu_c(region=region, direction=d90)\
        + a_evp_window[2] * window_eta * f_c_180 * get_nu_c(region=region, direction=d180)\
        + a_evp_window[3] * window_eta * f_c_270 * get_nu_c(region=region, direction=d270)\
        + a_evp_door[0] * window_u * 0.034 * get_nu_c(region=region, direction=d0)\
        + a_evp_door[1] * window_u * 0.034 * get_nu_c(region=region, direction=d90)\
        + a_evp_door[2] * window_u * 0.034 * get_nu_c(region=region, direction=d180)\
        + a_evp_door[3] * window_u * 0.034 * get_nu_c(region=region, direction=d270) \
        + a_evp_wall[0] * wall_u * 0.034 * get_nu_c(region=region, direction=d0)\
        + a_evp_wall[1] * wall_u * 0.034 * get_nu_c(region=region, direction=d90)\
        + a_evp_wall[2] * wall_u * 0.034 * get_nu_c(region=region, direction=d180)\
        + a_evp_wall[3] * wall_u * 0.034 * get_nu_c(region=region, direction=d270)

    eta_a_c = m_c / a_evp_total

    if region != 8:

        f_h_0 = get_f_value(glass_type='Type7', season='Heating', region=region, direction=d0, l_value=l_value_h)
        f_h_90 = get_f_value(glass_type='Type7', season='Heating', region=region, direction=d90, l_value=l_value_h)
        f_h_180 = get_f_value(glass_type='Type7', season='Heating', region=region, direction=d180, l_value=l_value_h)
        f_h_270 = get_f_value(glass_type='Type7', season='Heating', region=region, direction=d270, l_value=l_value_h)

        m_h = a_evp_roof * upper_u * 0.034 * get_nu_h(region=region, direction='top')\
            + a_evp_window[0] * window_eta * f_h_0 * get_nu_h(region=region, direction=d0)\
            + a_evp_window[1] * window_attached_eta * f_h_90 * get_nu_h(region=region, direction=d90)\
            + a_evp_window[2] * window_eta * f_h_180 * get_nu_h(region=region, direction=d180)\
            + a_evp_window[3] * window_eta * f_h_270 * get_nu_h(region=region, direction=d270)\
            + a_evp_door[0] * window_u * 0.034 * get_nu_h(region=region, direction=d0)\
            + a_evp_door[1] * window_u * 0.034 * get_nu_h(region=region, direction=d90)\
            + a_evp_door[2] * window_u * 0.034 * get_nu_h(region=region, direction=d180)\
            + a_evp_door[3] * window_u * 0.034 * get_nu_h(region=region, direction=d270) \
            + a_evp_wall[0] * wall_u * 0.034 * get_nu_h(region=region, direction=d0)\
            + a_evp_wall[1] * wall_u * 0.034 * get_nu_h(region=region, direction=d90)\
            + a_evp_wall[2] * wall_u * 0.034 * get_nu_h(region=region, direction=d180)\
            + a_evp_wall[3] * wall_u * 0.034 * get_nu_h(region=region, direction=d270)

        eta_a_h = m_h / a_evp_total

    else:

        eta_a_h = None

    return u_a, eta_a_h, eta_a_c


if __name__ == '__main__':

    model_house = {
        'house_type': 'detached',
        'floor_ins_type': 'floor',
        'bath_ins_type': 'base',
        'a_f': [50.847457627118644, 39.152542372881356],
        'a_evp_ef_etrc': 2.4843,
        'a_evp_f_etrc': 0.0,
        'l_base_etrc_outside': (0.0, 1.82, 1.365, 0.0),
        'l_base_etrc_inside': 3.185,
        'a_evp_ef_bath': 3.3124000000000002,
        'a_evp_f_bath': 0.0,
        'l_base_bath_outside': (0.0, 1.82, 1.82, 0.0),
        'l_base_bath_inside': 3.64,
        'f_s': [1.08, 1.04],
        'l_prm': [30.80479821749104, 26.029948852968104],
        'l_ms': [10.609982280729707, 8.29490083566609],
        'l_os': [4.7924168280158135, 4.720073590817963],
        'a_evp_ef_other': 0.0,
        'a_evp_ef_total': 5.7967,
        'a_evp_f_other': 45.05075762711864,
        'a_evp_f_total': 45.05075762711864,
        'l_base_other_outside': (0.0, 0.0, 0.0, 0.0),
        'l_base_other_inside': 0.0,
        'l_base_total_outside': (0.0, 3.64, 3.185, 0.0),
        'l_base_total_inside': 6.825,
        'a_evp_roof': 50.847457627118644,
        'a_evp_base_etrc_outside': (0.0, 0.3276, 0.2457, 0.0),
        'a_evp_base_etrc_inside': 0.5733,
        'a_evp_base_bath_outside': (0.0, 0.91, 0.91, 0.0),
        'a_evp_base_bath_inside': 1.82,
        'a_evp_base_other_outside': (0.0, 0.0, 0.0, 0.0),
        'a_evp_base_other_inside': 0.0,
        'a_evp_base_total_outside': (0.0, 1.2376, 1.1557, 0.0),
        'a_evp_base_total_inside': 2.3933,
        'a_evp_srf': ([30.768948614116148, 22.396232256298443], [13.898008801245858, 12.7441986952085], [30.768948614116148, 22.396232256298443], [13.898008801245858, 12.7441986952085]),
        'a_evp_total_not_base': 261.30969198797516,
        'a_evp_total': 266.0962919879752,
        'a_evp_open_total': 36.58335687831652,
        'a_evp_window_total': 33.073356878316524,
        'a_evp_window': (22.6949374899008, 2.3845890309266213, 3.628147249551323, 4.365683107937781),
        'a_evp_door': (0.0, 1.89, 1.62, 0.0),
        'a_evp_wall': (30.47024338051379, 22.367618465527734, 47.917033620863265, 22.276524388516577)
    }

    u_a = calc_designed_indices(
        model_house=model_house,
        region=6,
        main_direction='sw',
        upper_u=0.1,
        wall_u=0.1,
        lower_u=0.1,
        base_psi_outside=0.1,
        base_psi_inside=0.1,
        window_u=0.1,
        window_attached_u=0.1,
        window_eta=0.1,
        window_attached_eta=0.1,
        l_value_h=1/0.3,
        l_value_c=1/0.3)

    print(u_a)

