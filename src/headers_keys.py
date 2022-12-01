REM_BASICA = "Remuneração Básica"
REM_EVENTUAL = "Remuneração Eventual ou Temporária"
OBRIGATORIOS = "Obrigatórios / Legais"
VERBAS = "Verbas Indenizatórias"
TEMPORARIAS = "Outras Remunerações Temporárias"

HEADERS = {
    REM_BASICA: {
        "Remuneração do Cargo Efetivo": 3,
        "Outras Verbas Remuneratórias Legais ou Judiciais": 4,
    },
    REM_EVENTUAL: {
        "Função de Confiança ou Cargo em Comissão": 5,
        "Gratificação Natalina": 6,
        "Férias (1/3 constitucional)": 7,
        "Abono de Permanência": 8,
    },
    OBRIGATORIOS: {
        "Contribuição Previdênciária": 12,
        "Imposto de Renda": 13,
        "Retenção por Teto Constitucional": 14,
    },
    VERBAS: {
      "Auxílio-alimentação":4,
      "Auxílio-creche":5,
      "Auxílio-moradia":6,
      "Auxílio-natalidade":7,
      "Auxílio-transporte":8,  
    },
    TEMPORARIAS: {
      "Adicional Insalubridade":10,
      "Adicional Atividade Penosa": 11,
      "Devolução IR":12,
      "Devolução Plan-Assiste":13,
      "Gratificação de Perícia e Projeto":14,
      "Gratificação Encargo de Curso e Concurso":15,
      "Gratificação Exercício Cumulativo de Ofício":16,
      "Gratificação Local de Trabalho":17,
      "Hora Extra":18,
      "Licença Prêmio em Pecúnia":19,
      "Outras Verbas Remuneratórias Retroativas/Temporárias":20,
      "Outras Verbas Remuneratórias":21,
      "Substituição":22,
    },
}
