
def calc_designed_indices(
        model_house: dict,
        upper_u: float,
        wall_u: float,
        lower_u: float,
        base_psi_outside: float,
        base_psi_inside: float,
        window_u: float,
        window_attached_u: float,
        window_eta: float,
        window_attached_eta: float
):
    """
    Args:
        model_house: モデルハウス（面積等）の辞書
        upper_u: 上部のU値, W/m2K
        wall_u: 外壁のU値, W/m2K
        lower_u: 下部のU値, W/m2K
        base_psi_outside: 土間床外壁側のψ値, W/mK
        base_psi_inside: 土間床床下側のψ値, W/mK
        window_u: 窓のU値, W/m2K
        window_attached_u: 窓（障子）のU値, U値, W/m2K
        window_eta: 窓のη値
        window_attached_eta: 窓（障子）のη値
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

    return u_a




if __name__ == '__main__':

    calc_designed_indices()