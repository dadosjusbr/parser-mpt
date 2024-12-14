"""
Script responsável por iterar sobre os membros da folha, 
listando cada rubrica do contracheque e das indenizações e seus respectivos valores recebidos por cada membro.
"""

import number
import re
import numpy as np

from coleta import coleta_pb2 as Coleta

from headers_keys import (
    HEADERS,
    REM_BASICA,
    REM_EVENTUAL,
    OBRIGATORIOS,
    VERBAS,
    TEMPORARIAS,
    VERBAS_06_20,
    TEMPORARIAS_06_20,
    TEMPORARIAS_07_20,
)


# Listando os membros da folha de contracheque
def parse_employees(file, colect_key, month, year):
    employees = {}
    counter = 1
    # As informações dos membros começam somente a partir da 9ª linha
    file = file[8:]
    for row in file:
        if "Fonte da Informação" in row[0]:
            break
        # As planilhas do MPT possui células vazias (NaN) entre os dados,
        # aqui removemos essas células e deixamos apenas as informações dos membros
        new_row = [x for x in row if not number.is_nan(x)]
        member = Coleta.ContraCheque()
        member.id_contra_cheque = colect_key + "/" + str(counter)
        member.chave_coleta = colect_key
        # A matrícula é fornecida juntamente ao nome, aqui separamos nome e matrícula.
        matNome = re.split(r"-", new_row[0])
        member.matricula = matNome[0]
        member.nome = matNome[1]
        member.funcao = new_row[1]
        member.local_trabalho = new_row[2]
        member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
        member.ativo = True
        member.remuneracoes.CopyFrom(create_remuneration(new_row, month, year))

        employees[matNome[0]] = member
        counter += 1

    return employees


# Listando cada rubrica do contracheque e seus valores
# Apenas a Remuneração do Cargo Efetivo é do tipo B = Base
# Os demais são O, outras remunerações, ou D, descontos
def create_remuneration(row, month, year):
    remuneration_array = Coleta.Remuneracoes()
    # REMUNERAÇÃO BÁSICA
    for key, value in HEADERS[REM_BASICA].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = REM_BASICA
        remuneration.item = key
        valor = re.sub("[R$] ?", "", row[value])  # Tirando o "R$" da string
        remuneration.valor = float(number.format_value(valor))
        if value == 3:
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        else:
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    # REMUNERAÇÃO EVENTUAL OU TEMPORÁRIA
    for key, value in HEADERS[REM_EVENTUAL].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = REM_EVENTUAL
        remuneration.item = key
        valor = re.sub("[R$] ?", "", row[value])  # Tirando o "R$" da string
        remuneration.valor = float(number.format_value(valor))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    # OBRIGATÓRIOS/LEGAIS
    for key, value in HEADERS[OBRIGATORIOS].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
        remuneration.categoria = OBRIGATORIOS
        remuneration.item = key
        valor = re.sub("[R$] ?", "", row[value])  # Tirando o "R$" da string
        remuneration.valor = abs(float(number.format_value(valor))) * (-1)
        remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


# Listando cada rubrica da folha de indenizações e seus valores a partir de 07/2020
# R = Receita; O = Outras
def remunerations_2020_07(row):
    remuneration_array = Coleta.Remuneracoes()
    # VERBAS INDENIZATÓRIAS
    for key, value in HEADERS[VERBAS].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = VERBAS
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    # OUTRAS REMUNERAÇÕES TEMPORÁRIAS
    try:
        for key, value in HEADERS[TEMPORARIAS].items():
            remuneration = Coleta.Remuneracao()
            remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
            remuneration.categoria = TEMPORARIAS
            remuneration.item = key
            remuneration.valor = float(number.format_value(row[value]))
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
            remuneration_array.remuneracao.append(remuneration)
    except:
        # O cabeçalho da planilha de julho de 2020 tem 2 colunas a menos
        for key, value in HEADERS[TEMPORARIAS_07_20].items():
            remuneration = Coleta.Remuneracao()
            remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
            remuneration.categoria = TEMPORARIAS
            remuneration.item = key
            remuneration.valor = float(number.format_value(row[value]))
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
            remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


# Listando cada rubrica da folha de indenizações e seus valores em 06/2020
# R = Receita; O = Outras
# A planilha de indenizações de junho de 2020 possui menos colunas
def remunerations_06_20(row):
    remuneration_array = Coleta.Remuneracoes()
    # VERBAS INDENIZATÓRIAS
    for key, value in HEADERS[VERBAS_06_20].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = VERBAS
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    # OUTRAS REMUNERAÇÕES TEMPORÁRIAS
    for key, value in HEADERS[TEMPORARIAS_06_20].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = TEMPORARIAS
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


# Listando cada rubrica da folha de indenizações e seus valores até 04/2020
# R = Receita; O = Outras
def remunerations_2019_2020(row):
    remuneration_array = Coleta.Remuneracoes()
    # VERBAS INDENIZATÓRIAS
    if not number.is_nan(row[4]) and row[4] != "N/A":
        rem = Coleta.Remuneracao()
        rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
        rem.categoria = "Verbas indenizatórias"
        # O nome do item e seu valor vêm na mesma célula, aqui separamos esses valores
        value = re.split(r"\(R\$", row[4])
        # value[1] recebe o valor, sem parênteses e sem 'R$'.
        value[1] = re.sub("[)]?", "", value[1])
        # Evitando o erro 'Invalid escape character in string' nos testes
        value[0] = re.sub("[\xa0\xa0\xa0]?", "", value[0])
        rem.item = value[0]  # value[0] contém o nome do item/verba
        rem.valor = float(number.format_value(value[1]))
        rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(rem)
    # OUTRAS REMUNERAÇÕES TEMPORÁRIAS
    if not number.is_nan(row[6]) and row[6] != "N/A":
        rem = Coleta.Remuneracao()
        rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
        rem.categoria = "Outras Remunerações Temporárias"
        # O nome do item e seu valor vêm na mesma célula, aqui separamos esses valores
        value = re.split(r"\(R\$", row[6])
        # value[1] recebe o valor, sem parênteses e sem 'R$'.
        value[1] = re.sub("[)]?", "", value[1])
        rem.item = value[0]  # value[0] contém o nome do item/verba
        rem.valor = float(number.format_value(value[1]))
        rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(rem)
    return remuneration_array


# Listando cada rubrica da folha de indenizações e seus valores a partir de 2024
# R = Receita; O = Outras
def remunerations_2024(row):
    remuneration_array = Coleta.Remuneracoes()
    # VERBAS INDENIZATÓRIAS
    if not number.is_nan(row[4]) and row[4] != "N/A":
        rem = Coleta.Remuneracao()
        rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
        rem.categoria = "Verbas indenizatórias"
        rem.item = row[4]
        rem.valor = float(number.format_value(row[5]))
        rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(rem)
    # OUTRAS REMUNERAÇÕES TEMPORÁRIAS
    if not number.is_nan(row[6]) and row[6] != "N/A":
        rem = Coleta.Remuneracao()
        rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
        rem.categoria = "Outras Remunerações Temporárias"
        rem.item = row[6]
        rem.valor = float(number.format_value(row[7]))
        rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(rem)
    return remuneration_array


# A planilha mantém esse formato até 05/2019
def remunerations_2018(row):
    remuneration_array = Coleta.Remuneracoes()
    rem = Coleta.Remuneracao()
    rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
    rem.categoria = row[2]
    rem.item = row[3]
    rem.valor = float(number.format_value(row[4]))
    rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
    remuneration_array.remuneracao.append(rem)
    return remuneration_array


def update_employees_05_20(data, employees):
    # A planilha de indenizações de maio de 2020 é diferente dos demais meses, tendo mais de 200 colunas.
    for row in data.indenizacoes:
        if "Auxílio-Alimentação" in row:
            head = row
        registration = str(row[0])
        if registration in employees.keys():
            emp = employees[registration]
            remu = remunerations_05_20(head, row)
            emp.remuneracoes.MergeFrom(remu)
            employees[registration] = emp
    return employees


# Listando cada rubrica da folha de indenizações e seus valores em 05/2020
# R = Receita; O = Outras
def remunerations_05_20(head, row):
    remuneration_array = Coleta.Remuneracoes()
    for i in range(4, len(row)):
        rem = Coleta.Remuneracao()
        rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
        rem.categoria = "Verbas indenizatórias e outras remunerações temporárias"
        rem.item = head[i]
        rem.valor = float(number.format_value(row[i]))
        rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(rem)
    return remuneration_array


# As planilhas seguem um padrão diferente a partir de junho de 2019 a abril de 2020
def update_employees_2019_2020(indenizacoes, employees):
    for i in range(len(indenizacoes)):
        # As células referentes à matrícula são mescladas, retornando 'nan' na linha posterior.
        # Caso esta célula seja 'nan', ragistration receberá a matrícula informada na linha anterior.
        if not number.is_nan(indenizacoes[i][0]):
            registration = str(indenizacoes[i][0])
        else:
            registration = str(indenizacoes[i - 1][0])

        if registration in employees.keys():
            emp = employees[registration]
            remu = remunerations_2019_2020(indenizacoes[i])
            emp.remuneracoes.MergeFrom(remu)
            employees[registration] = emp
    return employees


# As planilhas seguem um padrão diferente a partir de junho de 2020
def update_employees_2020_06(data, employees):
    for row in data.indenizacoes:
        registration = str(row[0])
        if registration in employees.keys():
            new_row = [x for x in row if not number.is_nan(x)]
            emp = employees[registration]
            if int(data.year) == 2020 and int(data.month) == 6:
                remu = remunerations_06_20(new_row)
            else:
                remu = remunerations_2020_07(new_row)
            emp.remuneracoes.MergeFrom(remu)
            employees[registration] = emp
    return employees


# As planilhas seguem um padrão diferente a partir de 2024
def update_employees_2024(data, employees):
    registration = np.nan
    for row in data.indenizacoes:
        if str(row[0]) != "nan":
            registration = str(row[0])
        if registration in employees.keys():
            emp = employees[registration]
            if int(data.year) == 2020 and int(data.month) == 6:
                remu = remunerations_06_20(row)
            else:
                remu = remunerations_2024(row)
            emp.remuneracoes.MergeFrom(remu)
            employees[registration] = emp
    return employees


# As planilhas de indenizações possuem um padrão de 2018 a maio de 2019
def update_employees_2018(data, employees):
    for row in data:
        if "Observações:" in str(row[0]) or "Fonte" in str(row[0]):
            break
        if (
            not number.is_nan(row[0])
            and "NOME" not in row[0]
            and "(a)" not in row[0]
            and "Nome" not in row[0]
        ):
            # A matrícula vem juntamente ao nome, entre parênteses
            value = re.split(r"\(", row[0])
            registration = re.sub("[)]?", "", value[1])
            if registration in employees.keys():
                emp = employees[registration]
                remu = remunerations_2018(row)
                emp.remuneracoes.MergeFrom(remu)
                employees[registration] = emp
    return employees


# Executando todas as funções,
# iterando os contracheques e indenizações e retornando a folha completa
def parse(data, colect_key):
    employees = {}
    payroll = Coleta.FolhaDePagamento()

    employees.update(
        parse_employees(data.contracheque, colect_key, data.month, data.year)
    )

    if int(data.year) == 2018 or int(data.year) == 2019 and int(data.month) <= 5:
        update_employees_2018(data.indenizacoes, employees)

    elif (
        int(data.year) == 2019
        and int(data.month) > 5
        or int(data.year) == 2020
        and int(data.month) <= 4
    ):
        update_employees_2019_2020(data.indenizacoes, employees)

    elif int(data.year) == 2020 and int(data.month) == 5:
        update_employees_05_20(data, employees)

    elif (
        (int(data.year) > 2020 and int(data.year) < 2024)
        or int(data.year) == 2020
        and int(data.month) >= 6
    ):
        update_employees_2020_06(data, employees)
    else:
        update_employees_2024(data, employees)

    for i in employees.values():
        payroll.contra_cheque.append(i)

    return payroll
