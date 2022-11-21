import number
import re

from coleta import coleta_pb2 as Coleta

# from headers_keys import (HEADERS, INDENIZACOES_ANTES, OBRIGATORIOS_ANTES, REMTEMP_ANTES, REMUNERACAOBASICA,
#   EVENTUALTEMP, OBRIGATORIOS)


def parse_employees_after(file, colect_key, month, year):
    employees = {}
    counter = 1
    file = file[8:] # As informações dos membros começam somente a partir da 9ª linha
    for row in file:
        if 'Fonte da Informação' in row[0]:
            break
        # As planilhas do MPT possui células vazias (NaN) entre os dados,
        # aqui removemos essas células e deixamos apenas as informações dos membros
        new_row = [x for x in row if not number.is_nan(x)]
        
        member = Coleta.ContraCheque()
        member.id_contra_cheque = colect_key + "/" + str(counter)
        member.chave_coleta = colect_key
        matNome = re.split(r'-', new_row[0]) # A matrícula é fornecida juntamente ao nome, aqui separamos nome e matrícula.
        member.matricula = matNome[0]
        member.nome = matNome[1]
        member.funcao = new_row[1]
        member.local_trabalho = new_row[2]
        member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
        member.ativo = True
        # member.remuneracoes.CopyFrom(
        #     create_remuneration(row, month, year)
        # )

        employees[str(row[0])] = member
        counter += 1

    return employees


# def create_remuneration(row, month, year):
#     remuneration_array = Coleta.Remuneracoes()
#     # REMUNERAÇÃO BÁSICA
#     for key, value in HEADERS[REMUNERACAOBASICA].items():
#         remuneration = Coleta.Remuneracao()
#         remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
#         remuneration.categoria = REMUNERACAOBASICA
#         remuneration.item = key
#         remuneration.valor = float(number.format_value(row[value]))
#         remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
#         remuneration_array.remuneracao.append(remuneration)
#     # REMUNERAÇÃO EVENTUAL OU TEMPORÁRIA
#     for key, value in HEADERS[EVENTUALTEMP].items():
#         remuneration = Coleta.Remuneracao()
#         remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
#         remuneration.categoria = EVENTUALTEMP
#         remuneration.item = key
#         remuneration.valor = float(number.format_value(row[value]))
#         remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
#         remuneration_array.remuneracao.append(remuneration)
#     # OBRIGATÓRIOS/LEGAIS
#     if int(year) > 2019 or (int(year) == 2019 and int(month) >= 7):
#         for key, value in HEADERS[OBRIGATORIOS].items():
#             remuneration = Coleta.Remuneracao()
#             remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
#             remuneration.categoria = OBRIGATORIOS
#             remuneration.item = key
#             remuneration.valor = abs(
#                 float(number.format_value(row[value]))) * (-1)
#             remuneration_array.remuneracao.append(remuneration)
#     else:
#         for key, value in HEADERS[OBRIGATORIOS_ANTES].items():
#             remuneration = Coleta.Remuneracao()
#             remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
#             remuneration.categoria = OBRIGATORIOS
#             remuneration.item = key
#             remuneration.valor = abs(
#                 float(number.format_value(row[value]))) * (-1)
#             remuneration_array.remuneracao.append(remuneration)
#     return remuneration_array

def parse(data, colect_key):
    employees = {}
    payroll = Coleta.FolhaDePagamento()

    if int(data.year) > 2019 or (int(data.year) == 2019 and int(data.month) >= 7):
        employees.update(parse_employees_after(
            data.contracheque, colect_key, data.month, data.year))

    for i in employees.values():
        payroll.contra_cheque.append(i)

    return payroll
