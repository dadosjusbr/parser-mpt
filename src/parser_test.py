from parser import parse
import unittest
from google.protobuf.json_format import MessageToDict
import data
import json


class TestParser(unittest.TestCase):
    def test_05_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_05_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-05-2020.xls',
                 'src/output_test/sheets/membros-ativos-indenizacoes-05-2020.ods']
        dados = data.load(files, '2020', '05', 'src/output_test/sheets')
        result_data = parse(dados, 'mpt/05/2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0],
                         result_to_dict['contraCheque'][0])

    def test_06_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_06_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-06-2020.xls',
                 'src/output_test/sheets/membros-ativos-indenizacoes-06-2020.ods']
        dados = data.load(files, '2020', '06', 'src/output_test/sheets')
        result_data = parse(dados, 'mpt/06/2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0],
                         result_to_dict['contraCheque'][0])

    def test_07_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_07_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-07-2020.xls',
                 'src/output_test/sheets/membros-ativos-indenizacoes-07-2020.ods']
        dados = data.load(files, '2020', '07', 'src/output_test/sheets')
        result_data = parse(dados, 'mpt/07/2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0],
                         result_to_dict['contraCheque'][0])

    def test_04_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_04_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-04-2020.xls',
                 'src/output_test/sheets/membros-ativos-indenizacoes-04-2020.ods']
        dados = data.load(files, '2020', '04', 'src/output_test/sheets')
        result_data = parse(dados, 'mpt/04/2020')

        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0],
                         result_to_dict['contraCheque'][0])

    def test_05_2019(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_05_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-05-2019.xls',
                 'src/output_test/sheets/membros-ativos-indenizacoes-05-2019.ods']
        dados = data.load(files, '2019', '05', 'src/output_test/sheets')
        result_data = parse(dados, 'mpt/05/2019')

        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0],
                         result_to_dict['contraCheque'][0])
