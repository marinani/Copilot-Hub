# Estimativa Bottom-Up: Requisição 638680

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 638680 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 4/12/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo adicionar a coluna "REGIONAL" na tela de Pendências 156 do Sigesguarda Pro, permitindo aos usuários visualizar e filtrar os protocolos por regional de forma mais eficiente.
A implementação desta melhoria é simples e de baixo impacto, pois o dado da regional já existe no retorno da API 156 (campo endereco.regional no DTO Pendencia). A alteração necessária consiste apenas em propagar esse dado que já está disponível para a camada de apresentação.
A solução contemplará a adição da propriedade Regional no ViewModel ConsultaMonitoramentoOcorrenciaSiac, configuração do mapeamento no AutoMapper para extrair o valor de endereco.regional, e a inclusão da nova coluna na grid _GridListaOcorrenciasSiac.cshtml.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Mapear o fluxo de dados desde a API 156 até a View, identificar arquivos envolvidos e verificar existência do campo Regional no DTO. | 0:00 | 0:30 | 0:00 | 0:00 | 0:00 | **0:30** |
| Atualização da ViewModel | - | Melhoria | Adicionar propriedade Regional (tipo string) na classe ConsultaMonitoramentoOcorrenciaSiac. | 0:00 | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Atualização do AutoMapper | - | Melhoria | Adicionar mapeamento .ForMember(o => o.Regional, d => d.MapFrom(s => s.endereco.regional)) no profile. | 0:00 | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Atualização da interface (Grid) | - | Melhoria | Adicionar coluna Regional na grid _GridListaOcorrenciasSiac.cshtml com ordenação e CSS adequados | 0:00 | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Testes e validações | - | Melhoria | Testar exibição da coluna, verificar se o dado está sendo populado corretamente, ajustar largura e posição da coluna se necessário. | 0:00 | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:30 | 16,67% |
| Implementação (75%) | 1:30 | 50,00% |
| Teste (20%) | 1:00 | 33,33% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **3:00** | **100,00%** |
