# Estimativa Bottom-Up: Requisição 739294

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 739294 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 3/2/2026 |

---

## Escopo da Estimativa

Implementação de filtro por Subdivisão de Assunto nas consultas e relatórios do módulo Fiscalização, permitindo pesquisas mais detalhadas e segmentadas conforme as subdivisões vinculadas às intervenções selecionadas. A melhoria será aplicada na Consulta de Solicitações, Relatório Produção de Vistoria, Relatório Resumido, Relatório de Quantidade de Documento de Fiscalização, Relatório de Agendamento de Vistoria e Relatório de Quantidade de Registros 156, proporcionando maior precisão na análise e acompanhamento das informações oriundas do SIAC 156.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Adicionar filtro de Subdivisão de Assunto em diversas Consultas e Relatórios do módulo Fiscalização | RF 000 ao RF 007 | Melhoria | Implementar filtro de Subdivisão de Assunto nas consultas e relatórios do módulo Fiscalização, incluindo comportamento cascata baseado nas intervenções selecionadas, seleção múltipla, renderização condicional para organizações integradas ao SIAC 156, adaptação dos DTOs, repositórios, endpoints e componentes Blazor, permitindo filtrar solicitações e relatórios utilizando as subdivisões importadas do SIAC 156. Os relatórios impactados serão: Relatório Produção de Vistoria, Relatório Resumido, Relatório de Quantidade de Documento de Fiscalização, Relatório de Agendamento de Vistoria e Relatório de Quantidade de Registros 156, além da Consulta de Solicitações do módulo Fiscalização. | 5:00 | 12:00 | 3:00 | 0:00 | 20:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 5:00 | 25,00% |
| Arquitetura (40%) | 12:00 | 60,00% |
| Implementação (75%) | 3:00 | 15,00% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 20:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
