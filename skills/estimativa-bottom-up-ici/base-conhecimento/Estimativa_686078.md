# Estimativa Bottom-Up: Requisição 686078

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 686078 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 18/2/2026 |

---

## Escopo da Estimativa

Realizar ajuste no relatório de vistoria para remover a exibição do campo Observações, conforme solicitado pela área demandante. A atividade contempla a alteração diretamente no processo de geração do relatório em PDF, utilizando a biblioteca iTextSharp, com a remoção do trecho de código responsável pela renderização do referido campo no documento final.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Relatório de Vistoria | - |  | Será realizada a remoção do trecho responsável pela renderização do campo Observações no relatório de vistoria, diretamente no ponto de geração do documento PDF utilizando a biblioteca iTextSharp. A alteração consiste exclusivamente na retirada do bloco de código que escreve o referido campo, sem impacto nas demais seções do relatório ou na estrutura do documento. | 0:20 | 0:30 | 0:10 | 0:00 | 1:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:20 | 33,33% |
| Arquitetura (40%) | 0:30 | 50,00% |
| Implementação (75%) | 0:10 | 16,67% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 1:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
