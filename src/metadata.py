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
    
    # As planilhas de indenizações possuem um padrão de 2018 a maio de 2019
    # As planilhas seguem um padrão diferente a partir de junho de 2019 a abril de 2020
    # A planilha de indenizações de maio de 2020 é diferente dos demais meses, tendo mais de 200 colunas.
    # A planilha de indenizações de junho de 2020 possui menos colunas
    # As planilhas seguem um padrão diferente a partir de junho de 2020
    if (year == 2020 and month in [5, 6, 7]) or (year == 2019 and month == 6) or (year == 2024 and month == 1):
        metadata.formato_consistente = False
    else:
        metadata.formato_consistente = True
        
    if year >= 2024:
        metadata.estritamente_tabular = True

    return metadata
