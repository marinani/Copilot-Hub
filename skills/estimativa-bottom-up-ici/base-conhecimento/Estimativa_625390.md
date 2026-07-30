# Estimativa Bottom-Up: Requisição 625390

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 625390 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 4/12/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo criar um novo tipo de ocorrência "DTI" no Sigesguarda Pro, seguindo as mesmas regras de contagem e numeração distintas já aplicadas aos tipos existentes (GM, Defesa Civil e SETRAN).
A implementação desta melhoria é fundamental para atender a necessidade do cliente de registrar e gerenciar ocorrências específicas da DTI, com sequência numérica independente (ex: DTI-00001/2025, DTI-00002/2025) e possibilidade de vincular naturezas específicas a este novo tipo.
A solução contemplará a atualização dos enumeradores de tipos de ocorrência, tipo de natureza para incluir a opção DTI, adaptação da lógica de numeração no serviço de despacho, modificação dos filtros de natureza nos controllers e services para reconhecer o novo tipo, atualização das Views e código JavaScript que realizam comparações entre tipos de ocorrência (relatórios, visualizações, formulários), além da inclusão do tipo DTI no cadastro de naturezas para que gestores possam vincular quais naturezas serão atendidas por este novo tipo.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Mapear todos os arquivos que utilizam TipoOcorrencia. | 0:00 | 1:00 | 0:00 | 0:00 | 0:00 | **1:00** |
| Atualização dos enumeradores | - | Melhoria | Adicionar valor DTI=5 nos enums TipoOcorrencia, TipoNatureza. | 0:00 | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Atualização dos serviços de backend | - | Melhoria | Ajustar mapeamentos de tipo nos métodos ListarNaturezasPorTipo, NaturezasPorTipo, ObterNaturezaAutoComplete nos services e controllers. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Atualização das Views Razor | - | Melhoria | Adicionar tratamento para DTI nas Views que fazem comparação de tipos: ImprimirRelatorioOcorrencias, ImprimirRelNaturezaDisparoArma, Informacao, Detalhes, ValidaOcorrencia, etc. | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Implementação da lógica no JavaScript | - | Melhoria | Atualizar arquivos JS (registro-atendimento.js, atendimento-natureza.js, relatorioOcorrencia/consulta.js) para reconhecer e tratar o novo tipo DTI. | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Atualização da interface de natureza | - | Melhoria | Garantir que o dropdown de TipoNatureza no cadastro de naturezas mostre a opção DTI e que os filtros de pesquisa funcionem corretamente. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Testes e validações | - | Melhoria | Testar criação de ocorrência DTI, verificar numeração sequencial, testar vinculação de naturezas, validar relatórios e filtros. | 0:00 | 0:00 | 0:00 | 3:00 | 0:00 | **3:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 1:00 | 6,90% |
| Implementação (75%) | 10:30 | 72,41% |
| Teste (20%) | 3:00 | 20,69% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **14:30** | **100,00%** |
