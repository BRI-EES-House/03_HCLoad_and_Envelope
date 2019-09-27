# envelope performance simple unit test
import unittest
import nbimporter
import csv

from calc_indices import calc_indices as SEPS


class TestSEPS(unittest.TestCase):

    def test_gen_includingQdashMhMc(self):

        #        f = open('EnvelopePerformanceSimpleTestCase.csv','r',encoding='utf8')
        f = open('test_envelope_simple.txt', 'r', encoding='shift-JIS')
        # reader = csv.reader(f)
        # header = next(reader.split('\t'))
        header = next(f)
        #        for i, row in enumerate(reader):
        for i, row in enumerate(f):
            # row = row[:-1].split('\t')
            row = row.rstrip().split('\t')
            testcase, region, area_total, area_main, area_other, house_type, bath_ins_type, U_roof, U_wall, U_floorOther, U_floorBath, U_door, U_window, eta_d_cooling, eta_d_heating, fValue_useDefault, fValue_cooling, fValue_heating, psi_perimeterOther, psi_perimeterEntrance, psi_perimeterBath, expected_UA, expected_etaAC, expected_etaAH = tuple(
                row)
            print(testcase)
            with self.subTest(testcase):

                spec = {}

                spec['region'] = {
                    '1': 'region1',
                    '2': 'region2',
                    '3': 'region3',
                    '4': 'region4',
                    '5': 'region5',
                    '6': 'region6',
                    '7': 'region7',
                    '8': 'region8'
                }[region]

                spec['house_type'] = {
                    '1': 'floor_ins',
                    '2': 'base_ins',
                    '3': 'floor_and_base_ins'
                }[house_type]

                if spec['house_type'] == 'floor_ins' or spec['house_type'] == 'floor_and_base_ins':
                    spec['bath_ins_type'] = {
                        '1': 'bath_floor_ins',
                        '2': 'bath_base_ins',
                        '3': 'bath_2nd_floor'
                    }[bath_ins_type]

                spec['U'] = {
                    'roof': float(U_roof),
                    'wall': float(U_wall),
                    'door': float(U_door),
                    'window': float(U_window),
                }

                if spec['house_type'] == 'floor_ins' or spec['house_type'] == 'floor_and_base_ins':
                    spec['U']['floorOther'] = float(U_floorOther)

                if spec['house_type'] == 'floor_ins' or spec['house_type'] == 'floor_and_base_ins':
                    if spec['bath_ins_type'] == 'bath_floor_ins':
                        spec['U']['floorBath'] = float(U_floorBath)

                spec['psi'] = {
                    'useDefaultEtrc': 'no',
                    'prmEtrc': float(psi_perimeterEntrance),
                }

                if spec['house_type'] == 'base_ins' or spec['house_type'] == 'floor_and_base_ins':
                    spec['psi']['prmOther'] = float(psi_perimeterOther)

                if spec['house_type'] == 'floor_ins' or spec['house_type'] == 'floor_and_base_ins':
                    if spec['bath_ins_type'] == 'bath_base_ins':
                        spec['psi']['prmBath'] = float(psi_perimeterBath)

                spec['eta_d'] = {'cooling': float(eta_d_cooling)}
                if not spec['region'] == 'region8':
                    spec['eta_d']['heating'] = float(eta_d_heating)

                spec['fValue'] = {
                    'useDefault': {'1': 'yes', '2': 'no'}[fValue_useDefault]
                }
                if spec['fValue']['useDefault'] == 'no':
                    spec['fValue']['cooling'] = float(fValue_cooling)
                    if not spec['region'] == 'region8':
                        spec['fValue']['heating'] = float(fValue_heating)

                # if testcase == 'ケース126':
                if True:
                    actual_UA = SEPS(spec)['UA']
                    actual_etaAH = SEPS(spec)['etaAH']
                    actual_etaAC = SEPS(spec)['etaAC']
                    self.assertAlmostEqual(actual_UA, 'ND' if expected_UA == 'ND' else float(expected_UA),
                                           delta=0.000001)
                    self.assertAlmostEqual(actual_etaAH, 'ND' if expected_etaAH == 'ND' else float(expected_etaAH),
                                           delta=0.000001)
                    self.assertAlmostEqual(actual_etaAC, 'ND' if expected_etaAC == 'ND' else float(expected_etaAC),
                                           delta=0.000001)


if __name__ == "__main__":
    unittest.main()
