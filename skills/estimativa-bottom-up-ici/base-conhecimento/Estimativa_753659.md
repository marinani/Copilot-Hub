# Estimativa Bottom-Up: Requisição 753659

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 753659 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 22/5/2026 |

---

## Escopo da Estimativa

Implementar padronização dos componentes de seleção e campos de data do SIGMU Cidades, contemplando criação de componentes reutilizáveis para seleção simples e múltipla, substituição de aproximadamente 209 componentes de seleção distribuídos em 68 arquivos do sistema e padronização de aproximadamente 25 campos de data distribuídos em 15 arquivos. A melhoria visa unificar comportamento de busca, filtragem, ordenação alfabética e preenchimento de datas em formulários, consultas e relatórios dos módulos Geral, Fiscalização e Execução, proporcionando experiência de uso mais consistente e produtiva aos usuários.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Criação dos componentes genéricos padronizados | - | Novo | Implementar componentes genéricos padronizados para listas de seleção simples e múltiplas, centralizando comportamentos de filtragem, busca insensível a maiúsculas/minúsculas, seleção múltipla, limpeza de seleção e ordenação alfabética, estabelecendo padrão único reutilizável para utilização em todo o SIGMU Cidades. | 2:00 | 3:00 | 1:00 | 0:00 | 6:00 | **0:00** |
| Padronização dos dropdowns existentes no sistema | - | Melhoria | Substituir aproximadamente 209 componentes de seleção (RadzenDropDown) distribuídos em 68 arquivos do SIGMU Cidades pelos novos componentes padronizados de seleção simples e múltipla, garantindo comportamento unificado de busca por conteúdo, filtro insensível a maiúsculas/minúsculas, ordenação alfabética e padronização visual em formulários, consultas e relatórios dos módulos Geral, Fiscalização e Execução. | 6:00 | 18:00 | 4:00 | 0:00 | 28:00 | **0:00** |
| Padronização dos campos de data | - | Melhoria | Substituir aproximadamente 25 ocorrências de componentes de data (RadzenDatePicker) distribuídas em 15 arquivos do SIGMU Cidades pelo componente padronizado DateInput, permitindo preenchimento simplificado das datas com máscara automática e padronização da experiência de utilização nos formulários e filtros do sistema. | 1:00 | 4:00 | 1:00 | 0:00 | 6:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 9:00 | 22,50% |
| Arquitetura (40%) | 25:00 | 62,50% |
| Implementação (75%) | 6:00 | 15,00% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 40:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
