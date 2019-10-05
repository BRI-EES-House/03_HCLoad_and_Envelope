from typing import Union, List, Dict
from decimal import Decimal

from f_value import f1f2Value
from DirectionCoefficient import get_nu_H as DC_get_nu_H
from DirectionCoefficient import get_nu_C as DC_get_nu_C

def get_Q_dash(U_A, r_env):

    return U_A * r_env


def get_mu_h(eta_a_h: float, r_env: float) -> float:
    """
    Args:
        eta_a_h: 暖房期の平均日射熱取得率, %
        r_env: 床面積に対する外皮表面積の割合
    Returns:
        暖房期μ値, (W/m2)/(W/m2)
    """

    return eta_a_h * r_env / 100


def get_mu_c(eta_a_c: float, r_env: float) -> float:
    """
    Args:
        eta_a_c: 冷房期の平均日射熱取得率, %
        r_env: 床面積に対する外皮表面積の割合
    Returns:
        冷房期μ値, (W/m2)/(W/m2)
    """

    return eta_a_c * r_env / 100


def get_r_env(A_env, A_A):
    return A_env / A_A


class Orientation():
    def __init__(self,_D0,_D90,_D180,_D270):
        self.D0   = _D0;
        self.D90  = _D90;
        self.D180 = _D180;
        self.D270 = _D270;
    def sum(self):
        return self.D0 + self.D90 + self.D180 + self.D270
    def __mul__(x,y):
        return Orientation(x.D0 * y.D0, x.D90 * y.D90, x.D180 * y.D180, x.D270 * y.D270)


def get_simple_U_A(A, L, H, U, psi):
    # A : Area
    #     roof, floorBath, floorOther, baseEtrcIS, baseBathIS, baseOtherIS, total_env : float
    #     wall, door, window, baseEtrcOS, baseBathOS, baseOtherOS : class 'Orientation' which has D0,D90,D180 and D270 as float
    # L : Length
    #     prmEtrcIS, prmBathIS, prmOtherIS : float
    #     prmEtrcOS, prmBathOS, prmOtherOS : class 'Orientation' which has D0,D90,D180 and D270 as float
    # H : Temperature difference coefficient
    #     roof, wall, door, window, floor, baseOS, baseIS, prmOS, prmIS: float
    # U : U-Value
    #     roof, wall, door, window, floorBath, floorOther, baseEtrc, baseBath, baseOther: float
    # psi : psi value
    #     prmEtrc, prmBath, prmOther : float

    q = A['roof'] * H['roof'] * U['roof'] \
        + A['wall'].sum() * H['wall'] * U['wall'] \
        + A['door'].sum() * H['door'] * U['door'] \
        + A['window'].sum() * H['window'] * U['window'] \
        + A['floorBath'] * H['floor'] * U['floorBath'] \
        + A['floorOther'] * H['floor'] * U['floorOther'] \
        + (A['baseEtrcOS'].sum() * H['baseOS'] + A['baseEtrcIS'] * H['baseIS']) * U['baseEtrc'] \
        + (A['baseBathOS'].sum() * H['baseOS'] + A['baseBathIS'] * H['baseIS']) * U['baseBath'] \
        + (A['baseOtherOS'].sum() * H['baseOS'] + A['baseOtherIS'] * H['baseIS']) * U['baseOther'] \
        + (L['prmEtrcOS'].sum() * H['prmOS'] + L['prmEtrcIS'] * H['prmIS']) * psi['prmEtrc'] \
        + (L['prmBathOS'].sum() * H['prmOS'] + L['prmBathIS'] * H['prmIS']) * psi['prmBath'] \
        + (L['prmOtherOS'].sum() * H['prmOS'] + L['prmOtherIS'] * H['prmIS']) * psi['prmOther']

    return float(Decimal(q / A['total_env']).quantize(Decimal('0.00'), rounding='ROUND_UP'))


def get_simple_eta_A_H(A, nuHTop, nuH, etaH):
    # A : Area
    #     roof, total_env : float
    #     wall, door, window, baseEtrcOS, baseOtherOS : class 'Orientation' which has D0,D90,D180 and D270 as float
    # nuHTop: float
    # nuH: class 'Orientation' which has D0,D90,D180 and D270 as float
    # etaH : eta for heating
    #     roof, wall, door, baseEtrc, baseOther : float
    #     window : class 'Orientation' which has D0,D90,D180 and D270 as float

    mH = A['roof'] * nuHTop * etaH['roof'] \
         + (A['wall'] * nuH).sum() * etaH['wall'] \
         + (A['door'] * nuH).sum() * etaH['door'] \
         + (A['window'] * nuH * etaH['window']).sum() \
         + (A['baseEtrcOS'] * nuH).sum() * etaH['baseEtrc'] \
         + (A['baseBathOS'] * nuH).sum() * etaH['baseBath'] \
         + (A['baseOtherOS'] * nuH).sum() * etaH['baseOther']

    return float(Decimal(mH / A['total_env'] * 100).quantize(Decimal('0.0'), rounding='ROUND_DOWN'))


def get_simple_eta_A_C(A, nuCTop, nuC, etaC):
    # A : Area
    #     roof, total_env : float
    #     wall, door, window, baseEtrcOS, baseOtherOS : class 'Orientation' which has D0,D90,D180 and D270 as float
    # nu_C_top; float
    # nu_C: class 'Orientation' which has D0,D90,D180 and D270 as float
    # etaC
    #     roof, wall, door, baseEtrc, baseOther : float
    #     window : class 'Orientation' which has D0,D90,D180 and D270 as float

    mC = A['roof']          * nuCTop      * etaC['roof'] \
       + ( A['wall']        * nuC ).sum() * etaC['wall'] \
       + ( A['door']        * nuC ).sum() * etaC['door'] \
       + ( A['window']      * nuC         * etaC['window'] ).sum() \
       + ( A['baseEtrcOS']  * nuC ).sum() * etaC['baseEtrc'] \
       + ( A['baseBathOS']  * nuC ).sum() * etaC['baseBath'] \
       + ( A['baseOtherOS'] * nuC ).sum() * etaC['baseOther']

    return float(Decimal( mC / A['total_env'] * 100 ).quantize(Decimal('0.0'), rounding = 'ROUND_UP'))


def get_simple_Orientation_value_from_Direction(direction):
    # direction: [(S,SW,W,NW,N,NE,E,SE,top,bottom)の辞書型]
    return Orientation( direction['SW'], direction['NW'], direction['NE'], direction['SE'] )


def getSimpleAreaAndLength(houseType, bathInsType):

    ht = {'floor_ins': 'f', 'base_ins': 'b'}[houseType]
    if ht == 'f':
        bit = {'bath_floor_ins': 'bf', 'bath_base_ins': 'bb', 'bath_2nd_floor': 'bf'}[bathInsType]
    elif ht == 'b':
        bit = 'bf'  # 当面の措置　本当は定義してはいけない
    else:
        raise ValueError

    area = {
        'total_env': {'f': 266.10,
                      'b': 275.69}[ht],
        'total_floor': 90.0,
        'roof': 50.85,
        'wall': Orientation(30.47, 22.37, 47.92, 22.28),
        'door': Orientation(0.00, 1.89, 1.62, 0.00),
        'window': Orientation(22.69, 2.38, 3.63, 4.37),
        'floorBath': {'f': {'bf': 3.31, 'bb': 0.00}[bit],
                      'b': 0.00}[ht],
        'floorOther': {'f': 45.05,
                       'b': 0.00}[ht],
        'baseEtrcOS': Orientation(0.00, 0.33, 0.25, 0.00),
        'baseEtrcIS': {'f': 0.57,
                       'b': 0.00}[ht],
        'baseBathOS': {'f': {'bf': Orientation(0.00, 0.00, 0.00, 0.00), 'bb': Orientation(0.00, 0.91, 0.91, 0.00)}[bit],
                       'b': Orientation(0.00, 0.91, 0.91, 0.00)}[ht],
        'baseBathIS': {'f': {'bf': 0.00, 'bb': 1.82}[bit],
                       'b': 0.00}[ht],
        'baseOtherOS': {'f': Orientation(0.00, 0.00, 0.00, 0.00),
                        'b': Orientation(5.30, 0.57, 3.71, 2.40)}[ht],
        'baseOtherIS': 0.00
    }

    length = {
        'prmEtrcOS': Orientation(0.00, 1.82, 1.37, 0.00),
        'prmEtrcIS': {'f': 3.19, 'b': 0.00}[ht],
        'prmBathOS': Orientation(0.00, 1.82, 1.82, 0.00),
        'prmBathIS': {'f': 3.64, 'b': 0.00}[ht],
        'prmOtherOS': {'f': Orientation(0.00, 0.00, 0.00, 0.00), 'b': Orientation(10.61, 1.15, 7.42, 4.79)}[ht],
        'prmOtherIS': 0.00
    }

    return (area, length)


def judge_simple_house_type(floor_ins_U_A, base_ins_U_A):
    if floor_ins_U_A > base_ins_U_A:
        return (floor_ins_U_A, 'floor_ins')
    else:
        return (base_ins_U_A, 'base_ins')



def getSimpleHValue():
    return {
        'roof'    : 1.0,
        'wall'    : 1.0,
        'door'    : 1.0,
        'window'  : 1.0,
        'floor'   : 0.7,
        'baseOS' : 1.0,
        'baseIS' : 0.7,
        'prmOS'  : 1.0,
        'prmIS'  : 0.7
    }

def setUValue_floorBath(U, ht, bit = None):
    if ht == 'base_ins':
        return 0.0
    elif ht == 'floor_ins':
        if bit == 'bath_floor_ins':
            return U['floorBath']
        elif bit == 'bath_base_ins':
            return 0.0
        elif bit == 'bath_2nd_floor':
            return U['floorOther']
        else:
            raise ValueError
    else:
        raise ValueError


def setUValue_floorOther(U, ht):
    if ht == 'base_ins':
        return 0.0
    elif ht == 'floor_ins':
        return U['floorOther']
    else:
        raise ValueError

def setUValue_baseEtrc():
    return 0.0


def setUValue_baseBath():
    return 0.0


def setUValue_baseOther():
    return 0.0


def setPsiValue_prmEtrc(psi):
    if psi['useDefaultEtrc'] == 'yes':
        return 1.8
    elif psi['useDefaultEtrc'] == 'no':
        return psi['prmEtrc']
    else:
        raise ValueError


def setPsiValue_prmBath(psi, ht, bit = None):
    if ht == 'floor_ins':
        if bit == 'bath_floor_ins':
            return 0.0
        elif bit == 'bath_base_ins':
            return psi['prmBath']
        elif bit == 'bath_2nd_floor':
            return 0.0
        else:
            raise ValueError
    elif ht == 'base_ins':
        return psi['prmOther']
    else:
        raise ValueError


def setPsiValue_prmOther(psi, ht):
    if ht == 'floor_ins':
        return 0.0
    elif ht == 'base_ins':
        return psi['prmOther']
    else:
        raise ValueError


def setUAndPsiValue(U, psi, ht, bit=None):
    # ht:  house type = 'floor_ins' or 'base_ins'
    # bit: bath floor insulation type = 'bath_floor_ins', 'bath_base_ins' or 'bath_2nd_floor'

    rt_U = {
        'roof': U['roof'],
        'wall': U['wall'],
        'door': U['door'],
        'window': U['window'],
        'floorBath': setUValue_floorBath(U, ht, bit),
        'floorOther': setUValue_floorOther(U, ht),
        'baseEtrc': setUValue_baseEtrc(),
        'baseBath': setUValue_baseBath(),
        'baseOther': setUValue_baseOther(),
    }

    rt_psi = {
        'useDefaultEtrc': psi['useDefaultEtrc'],
        'prmEtrc': setPsiValue_prmEtrc(psi),
        'prmBath': setPsiValue_prmBath(psi, ht, bit),
        'prmOther': setPsiValue_prmOther(psi, ht),
    }

    return rt_U, rt_psi


def get_simple_eta_not_window(U_part):
    gamma_H = 1.0 # 暖房期の日除けの効果係数
    gamma_C = 1.0 # 冷房期の日除けの効果係数
    return ( 0.034 * U_part * gamma_H, 0.034 * U_part * gamma_C)


def get_f_H_default(region):
    my_round = lambda x: (x * 1000 * 2 + 1) // 2 / 1000
    v = f1f2Value()
    return Orientation(
        my_round( v.getValue(glassType = 'Type7', season = 'Heating', region = region, direction = 'SW', lValue = 1/0.3) ),
        my_round( v.getValue(glassType = 'Type7', season = 'Heating', region = region, direction = 'NW', lValue = 1/0.3) ),
        my_round( v.getValue(glassType = 'Type7', season = 'Heating', region = region, direction = 'NE', lValue = 1/0.3) ),
        my_round( v.getValue(glassType = 'Type7', season = 'Heating', region = region, direction = 'SE', lValue = 1/0.3) )
    )

def get_simple_eta_H_window(region, eta_d_H, f_value):
    if f_value['useDefault'] == 'yes':
        default_f_H = get_f_H_default(region)
        return Orientation(eta_d_H * default_f_H.D0, eta_d_H * default_f_H.D90, eta_d_H * default_f_H.D180, eta_d_H * default_f_H.D270)
    elif f_value['useDefault'] == 'no':
        f_H = f_value['heating']
        return Orientation(eta_d_H * f_H, eta_d_H * f_H, eta_d_H * f_H, eta_d_H * f_H)
    else:
        raise ValueError


def get_f_C_default(region):
    my_round = lambda x: (x * 1000 * 2 + 1) // 2 / 1000
    v = f1f2Value()
    return Orientation(
        my_round( v.getValue(glassType = 'Type1', season = 'Cooling', region = region, direction = 'SW', lValue = 20.0) ),
        my_round( v.getValue(glassType = 'Type1', season = 'Cooling', region = region, direction = 'NW', lValue = 20.0) ),
        my_round( v.getValue(glassType = 'Type1', season = 'Cooling', region = region, direction = 'NE', lValue = 20.0) ),
        my_round( v.getValue(glassType = 'Type1', season = 'Cooling', region = region, direction = 'SE', lValue = 20.0) ),
    )

def get_simple_eta_C_window(region, eta_d_C, f_value):
    if f_value['useDefault'] == 'yes' :
        default_f_C = get_f_C_default(region)
        return Orientation(eta_d_C * default_f_C.D0, eta_d_C * default_f_C.D90, eta_d_C * default_f_C.D180, eta_d_C * default_f_C.D270)
    elif f_value['useDefault'] == 'no':
        f_C = f_value['cooling']
        return Orientation(eta_d_C * f_C, eta_d_C * f_C, eta_d_C * f_C, eta_d_C * f_C)
    else:
        raise ValueError


def calc_standard_indices(spec: Dict) -> Dict:

    def get_U_A_provisional(ht, bit, U, psi):
        A, L = getSimpleAreaAndLength(houseType=ht, bathInsType=bit)
        H = getSimpleHValue()
        return get_simple_U_A(A=A, L=L, H=H, U=U, psi=psi)

    # decide whether the floor insulated house or the base insulated house is applied for the evaluation,
    # when the actual house is the floor and base insulated house
    def calc_UA(spec):
        if spec['house_type'] == 'floor_ins':

            rt_U, rt_psi = setUAndPsiValue(U=spec['U'], psi=spec['psi'], ht='floor_ins', bit=spec['bath_ins_type'])
            spec['U'] = rt_U
            spec['psi'] = rt_psi
            return (get_U_A_provisional(ht='floor_ins', bit=spec['bath_ins_type'], U=spec['U'], psi=spec['psi']),
                    spec['house_type'])

        elif spec['house_type'] == 'base_ins':

            rt_U, rt_psi = setUAndPsiValue(U=spec['U'], psi=spec['psi'], ht='base_ins', bit=None)
            spec['U'] = rt_U
            spec['psi'] = rt_psi
            return (get_U_A_provisional(ht='base_ins', bit=None, U=spec['U'], psi=spec['psi']), spec['house_type'])

        elif spec['house_type'] == 'floor_and_base_ins':

            rt_U, rt_psi = setUAndPsiValue(U=spec['U'], psi=spec['psi'], ht='floor_ins', bit=spec['bath_ins_type'])
            U_A_floor_ins = get_U_A_provisional(ht='floor_ins', bit=spec['bath_ins_type'], U=rt_U, psi=rt_psi)

            rt_U, rt_psi = setUAndPsiValue(U=spec['U'], psi=spec['psi'], ht='base_ins', bit=None)
            U_A_base_ins = get_U_A_provisional(ht='base_ins', bit=None, U=rt_U, psi=rt_psi)

            U_A, house_type_on_calc = judge_simple_house_type(U_A_floor_ins, U_A_base_ins)

            if house_type_on_calc == 'floor_ins':
                rt_U, rt_psi = setUAndPsiValue(U=spec['U'], psi=spec['psi'], ht='floor_ins', bit=spec['bath_ins_type'])
            elif house_type_on_calc == 'base_ins':
                rt_U, rt_psi = setUAndPsiValue(U=spec['U'], psi=spec['psi'], ht='base_ins', bit=None)
            else:
                raise ValueError()

            spec['U'] = rt_U  # 引数まで書き換えているのであまりよくない→要修正
            spec['psi'] = rt_psi  # 引数まで書き換えているのであまりよくない→要修正

            return (U_A, house_type_on_calc)
        else:
            raise ValueError()

    U_A, house_type_on_calc = calc_UA(spec)

    # area and length
    if house_type_on_calc == 'base_ins':
        A, L = getSimpleAreaAndLength(houseType=house_type_on_calc, bathInsType=None)
    else:
        A, L = getSimpleAreaAndLength(houseType=house_type_on_calc, bathInsType=spec['bath_ins_type'])

    # eta in heating and cooling season
    etaH = {}
    etaC = {}
    etaH['roof'], etaC['roof'] = get_simple_eta_not_window(spec['U']['roof'])
    etaH['wall'], etaC['wall'] = get_simple_eta_not_window(spec['U']['wall'])
    etaH['door'], etaC['door'] = get_simple_eta_not_window(spec['U']['door'])
    etaH['baseEtrc'], etaC['baseEtrc'] = get_simple_eta_not_window(spec['U']['baseEtrc'])
    etaH['baseBath'], etaC['baseBath'] = get_simple_eta_not_window(spec['U']['baseBath'])
    etaH['baseOther'], etaC['baseOther'] = get_simple_eta_not_window(spec['U']['baseOther'])

    # r_env
    r_env = get_r_env(A['total_env'], A['total_floor'])

    # Q'
    Q_dash = get_Q_dash(float(U_A), r_env)

    # --- heating season ---
    if spec['region'] == 'region8':
        eta_a_h = 'ND'
        mu_h = 'ND'
    else:
        # eta for windows
        etaH['window'] = get_simple_eta_H_window(region=spec['region'],
                                                 eta_d_H=spec['eta_d']['heating'],
                                                 f_value=spec['fValue'])
        # nu
        nuH = DC_get_nu_H(spec['region'])
        nuTopH, nuHorizontalH = (nuH['top'], get_simple_Orientation_value_from_Direction(nuH))
        # eta_A
        eta_a_h = get_simple_eta_A_H(A, nuTopH, nuHorizontalH, etaH)
        # 暖房期μ値
        mu_h = get_mu_h(eta_a_h, r_env)

    # --- cooling season ---
    # eta for windows
    etaC['window'] = get_simple_eta_C_window(region=spec['region'],
                                             eta_d_C=spec['eta_d']['cooling'],
                                             f_value=spec['fValue'])
    # nu
    nuC = DC_get_nu_C(spec['region'])
    nuTopC, nuHorizontalC = (nuC['top'], get_simple_Orientation_value_from_Direction(nuC))

    # eta_A
    eta_a_c = get_simple_eta_A_C(A, nuTopC, nuHorizontalC, etaC)

    # 冷房期μ値
    mu_c = get_mu_c(eta_a_c, r_env)

    return {
        'UA': U_A,
        'etaAH': eta_a_h,
        'etaAC': eta_a_c,
        'Qdash': Q_dash,
        'muH': mu_h,
        'muC': mu_c
    }

def calc_standard_indices_wrapper(
        region: int, floor_ins_type: str,
        upper_u, wall_u, lower_u, base_psi_outside, base_psi_inside,
        window_u, window_attachment_u, window_eta, window_attachment_eta
) -> Dict:

    if floor_ins_type == 'floor':
        house_type = 'floor_ins'
        bath_ins_type = 'bath_base_ins'
    elif floor_ins_type == 'base':
        house_type = 'base_ins'
        bath_ins_type = None
    else:
        raise  ValueError

    region_str = ['region1', 'region1', 'region1', 'region1', 'region1', 'region1', 'region1', 'region8'][region-1]

    spec = {
        'house_type': house_type,
        'bath_ins_type': bath_ins_type,
        'region': region_str,
        'U': {
            'roof': upper_u,
            'wall': wall_u,
            'door': window_u,
            'window': window_u,
            'floorBath': lower_u,
            'floorOther': lower_u
        },
        'psi': {
            'useDefaultEtrc': 'no',
            'prmEtrc': 1.8,
            'prmBath': base_psi_outside,
            'prmOther': base_psi_outside
        },
        'eta_d': {
            'heating': window_attachment_eta,  # eta d value in heating season
            'cooling': window_eta  # eta d value in cooling season
        },
        'fValue': {
            'useDefault': 'yes',  # 'yes' or 'no'  which is default f-value used or not
            'heating': 1.0,  # f-value in heating season, which is not used in case that 'UseDefault' is 'yes'
            'cooling': 1.0  # f-value in cooling season, which is not used in case that 'UseDefault' is 'yes'
        }
    }

    idx = calc_standard_indices(spec)

    return idx['UA'], idx['etaAH'], idx['etaAC']


if __name__ == '__main__':

    spec1 = {
        'house_type': 'base_ins',
        'bath_ins_type': 'bath_base_ins',
        'region': 'region6',
        'U': {
            'roof': 0.240,
            'wall': 0.530,
            'door': 2.330,
            'window': 3.490,
            'floorBath': 0.000,
            'floorOther': 0.480
        },
        'psi': {
            'useDefaultEtrc': 'yes',
            'prmEtrc': 1.8,
            'prmBath': 1.8,
            'prmOther': 1.8
        },
        'eta_d': {
            'heating': 0.510,  # eta d value in heating season
            'cooling': 0.510  # eta d value in cooling season
        },
        'fValue': {
            'useDefault': 'yes',  # 'yes' or 'no'  which is default f-value used or not
            'heating': 1.0,  # f-value in heating season, which is not used in case that 'UseDefault' is 'yes'
            'cooling': 1.0  # f-value in cooling season, which is not used in case that 'UseDefault' is 'yes'
        }
    }

    spec2 = {
        'house_type': 'floor_ins',
        'bath_ins_type': 'bath_floor_ins',
        'region': 'region1',
        'U': {
            'roof': 7.700,
            'wall': 6.670,
            'floorOther': 5.270,
            'floorBath': 5.270,
            'door': 4.650,
            'window': 6.510,
        },
        'psi': {
            'useDefaultEtrc': 'no',
            'prmEtrc': 1.8,
            'prmBath': 1.8,
            'prmOther': 1.8
        },
        'eta_d': {
            'heating': 0.700,  # eta d value in heating season
            'cooling': 0.700  # eta d value in cooling season
        },
        'fValue': {
            'useDefault': 'yes',  # 'yes' or 'no'  which is default f-value used or not
            'cooling': 0.93,  # f-value in cooling season, which is not used in case that 'UseDefault' is 'yes'
            'heating': 0.51,  # f-value in heating season, which is not used in case that 'UseDefault' is 'yes'
        }
    }

    result1 = calc_standard_indices(spec=spec1)
    result2 = calc_standard_indices(spec=spec2)

    print(result1)
    print(result2)
