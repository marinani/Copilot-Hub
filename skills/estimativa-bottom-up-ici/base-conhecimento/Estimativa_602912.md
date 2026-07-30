# Estimativa Bottom-Up: Requisição 602912

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 602912 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 15/10/2025 |

---

## Escopo da Estimativa

A melhoria exibirá o equipamento urbano associado à ocorrência imediatamente antes do endereço em todas as interfaces. Cadastros, detalhes, listagens, validação, dashboards e módulo legado, garantindo a mesma ordem nas impressões e PDFs. O campo será propagado pelas camadas de serviço, mapeamentos e view models responsáveis por montar a string de endereço, além de ser incorporado aos scripts e componentes interativos. Dessa forma, usuários passam a visualizar o equipamento urbano de referência sem perder o endereço completo.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Revisar fluxo completo do endereço nas telas mapeadas, dependências de AutoMapper/DTOs e impactos em relatórios PDF/impressão. | 0:00 | 2:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Atualização da interface (HTML/CSS) | - | Melhoria | Alterar todas as views identificadas (Atendimento, Ocorrência, listagens de monitoramento/dashboard, módulo legado e impressões) para exibir o equipamento urbano antes do endereço, respeitando responsividade, componentes compartilhados e layouts de relatório. | 0:00 | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Implementação da lógica JavaScript | - | Melhoria | Atualizar scripts de registro/conclusão de atendimento, fluxos específicos e tooltips para carregar o equipamento urbano junto ao endereço. | 0:00 | 0:00 | 2:30 | 0:00 | 0:00 | **2:30** |
| Atualização de serviços backend | - | Melhoria | Propagar o campo em OcorrenciaService, MonitoramentoService, outros serviços usados por relatórios/impressões, ajustes de AutoMapper e view models para concatenar equipamento e endereço de forma consistente. | 0:00 | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Testes e correções | - | Melhoria | Testar manualmente as telas, validar geração de PDF/impressão, cobertura das ocorrências legadas e regressões. | 0:00 | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 2:00 | 13,79% |
| Implementação (75%) | 10:30 | 72,41% |
| Teste (20%) | 2:00 | 13,79% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **14:30** | **100,00%** |
