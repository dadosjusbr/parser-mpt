import sys
import os
import pandas as pd

# Se for erro de não existir planilhas o retorno vai ser esse:
STATUS_DATA_UNAVAILABLE = 4
# Caso o erro for a planilha, que é invalida por algum motivo, o retorno vai ser esse:
STATUS_INVALID_FILE = 5


def _readODS(file):
    try:
        data = pd.read_excel(file, engine='odf').to_numpy()
    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        sys.exit(STATUS_INVALID_FILE)
    return data


def _readXLS(file):
    try:
        data = pd.read_excel(file, engine='xlrd').to_numpy()
    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        sys.exit(STATUS_INVALID_FILE)
    return data


def load(file_names, year, month, output_folder):
    """Carrega os arquivos passados como parâmetros.
       :param file_names: slice contendo os arquivos baixados pelo coletor.
      Os nomes dos arquivos devem seguir uma convenção e começar com
      Membros ativos-contracheque e Membros ativos-Verbas Indenizatorias
       :param year e month: usados para fazer a validação na planilha de controle de dados
       :return um objeto Data() pronto para operar com os arquivos
      """

    contracheque = _readXLS(
        [c for c in file_names if "contracheques" in c][0])

    indenizacoes = _readODS(
        [c for c in file_names if "indenizacoes" in c][0])

    return Data(contracheque, indenizacoes, year, month, output_folder)


class Data:
    def __init__(self, contracheque, indenizacoes, year, month, output_folder):
        self.year = year
        self.month = month
        self.output_folder = output_folder
        self.contracheque = contracheque
        self.indenizacoes = indenizacoes

    def validate(self):
        """
         Validação inicial dos arquivos passados como parâmetros.
        Aborta a execução do script em caso de erro.
         Caso o validade fique pare o script na leitura da planilha 
        de controle de dados dara um erro retornando o codigo de erro 4,
        esse codigo significa que não existe dados para a data pedida.
        """

        if not (
                os.path.isfile(
                    f"{self.output_folder}/membros-ativos-contracheques-{self.month}-{self.year}.xls"
                )
                or os.path.isfile(
                    f"{self.output_folder}/membros-ativos-indenizacoes-{self.month}-{self.year}.ods"
                )
        ):
            sys.stderr.write(
                f"Não existe planilhas para {self.month}/{self.year}.")
            sys.exit(STATUS_DATA_UNAVAILABLE)
