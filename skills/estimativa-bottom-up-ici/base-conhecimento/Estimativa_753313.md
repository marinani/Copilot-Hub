# Estimativa Bottom-Up: Requisição 753313

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 753313 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 21/5/2026 |

---

## Escopo da Estimativa

Implementar persistência do endereço original recebido do SIAC 156 no momento da importação da solicitação, garantindo que o espelho PDF utilizado na juntada do SUP sempre apresente o endereço original informado pelo cidadão, independentemente de alterações posteriores na Indicação Fiscal da solicitação. A melhoria também contempla compatibilidade para solicitações antigas por meio de fallback para o endereço atual quando não existir endereço original armazenado.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Persistência do endereço original do SIAC 156 | RF-01, RF-02 e RF-05 | Melhoria | Implementar persistência do endereço original recebido do SIAC 156 no momento da importação da solicitação, garantindo armazenamento imutável das informações originais do endereço independentemente de alterações posteriores realizadas na IF da solicitação. | 1:00 | 2:30 | 0:30 | 0:00 | 4:00 | **0:00** |
| Geração do espelho SIAC 156 utilizando endereço original | RF-03 e RF-04 | Melhoria | Ajustar a geração do espelho PDF do SIAC 156 para utilizar o endereço original importado da solicitação, incluindo fallback para o endereço atual em solicitações anteriores à implantação da funcionalidade, garantindo compatibilidade retroativa do processo. | 1:00 | 2:30 | 0:30 | 0:00 | 4:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:00 | 25,00% |
| Arquitetura (40%) | 5:00 | 62,50% |
| Implementação (75%) | 1:00 | 12,50% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 8:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
