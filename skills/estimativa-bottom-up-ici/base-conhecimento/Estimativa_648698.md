# Estimativa Bottom-Up: Requisição 648698

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 648698 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 11/12/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo implementar um sistema configurável de permissões por cargo para controlar a abertura de ocorrências no Sigesguarda Pro. A implementação desta melhoria é fundamental para atender a necessidade de restringir operadores por tipo de atuação: Guardas Municipais devem abrir apenas ocorrências dos tipos "GM" e "Defesa Civil", enquanto Agentes da SETRAN devem abrir apenas ocorrências do tipo "SETRAN".

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Analisar cargos existentes, mapear fluxo de validação de tipo de ocorrência. Definir regras de negócio e casos de exceção (administradores, funcionários sem cargo). | 0:00 | 2:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Criação da classe TipoOcorrenciaPermissao | - | Melhoria | Mapear na classe a relação cargo e permissão de tipo de ocorrência. | 0:00 | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Atualização do Controller de Atendimento | - | Melhoria | Modificar AtendimentoController.RegistroAtendimento para usar TiposOcorrenciaPermissao. Passar lista para ViewBag. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Atualização do Service de Atendimento | - | Melhoria | Refatorar RegistroAtendimentoService.RegistrarAtendimento e métodos de listagem (ListarPorFiltroOcorrenciaPendente, Totalizadores). Adicionar validação de tipos permitidos antes de salvar. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Atualização da View Razor | - | Melhoria | Modificar _Atendimento.cshtml para receber e renderizar apenas os radio buttons dos tipos de ocorrência permitidos. | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Testes | - | Melhoria | Realizar os testes com diferentes cenários de cadastro e edição. | 0:00 | 0:00 | 0:00 | 1:30 | 0:00 | **1:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 2:00 | 20,00% |
| Implementação (75%) | 6:30 | 65,00% |
| Teste (20%) | 1:30 | 15,00% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **10:00** | **100,00%** |
