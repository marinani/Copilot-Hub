# Estimativa Bottom-Up: Requisição 732919

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 732919 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 3/4/2026 |

---

## Escopo da Estimativa

Implementação de validação e correção automática de regional durante a importação de protocolos SIAC 156, utilizando a regional retornada pela integração GTM como prioridade no processo de resolução da regional da solicitação, realizando fallback para a regra atual por nome quando necessário, incluindo ajuste no fluxo do job de importação, compatibilidade com o cadastro de regionais do SIGMU e registro de logs das correções automáticas realizadas.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Validação e Correção Automática de Regional via GTM na Importação SIAC 156 | RF 001 ao RF 006 / T01 ao T08 | Melhoria | Implementar validação automática da regional durante a importação de protocolos SIAC 156, priorizando a regional retornada pelo GTM através do código GTM configurado no SIGMU, realizando fallback para busca por nome quando necessário, ajustando o fluxo do job Hangfire para resolução correta da regional antes da validação de pendências, registrando logs estruturados das correções realizadas e garantindo compatibilidade para os módulos Geral, Fiscalização e Execução. | 1:00 | 3:00 | 1:00 | 0:00 | 5:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 1:00 | 20,00% |
| Arquitetura (40%) | 3:00 | 60,00% |
| Implementação (75%) | 1:00 | 20,00% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 5:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
