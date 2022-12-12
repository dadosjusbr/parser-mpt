from coleta import coleta_pb2 as Coleta


def catch(month, year):
    metadata = Coleta.Metadados()
    metadata.acesso = Coleta.Metadados.FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO
    metadata.extensao = Coleta.Metadados.Extensao.ODS
    metadata.estritamente_tabular = False
    metadata.tem_matricula = True
    metadata.tem_lotacao = True
    metadata.tem_cargo = True
    metadata.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadata.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadata.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO

    if year == 2020 and month in [5, 6, 7] or year == 2019 and month == 6:
        metadata.formato_consistente = False
    else:
        metadata.formato_consistente = True

    return metadata
