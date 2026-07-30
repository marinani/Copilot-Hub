# Estimativa Bottom-Up: Requisição 639689

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 650823 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 18/2/2026 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo aprimorar o fluxo de atendimento das pendências oriundas da integração com a API SIAC 156, identificando e sinalizando visualmente quando um protocolo retorna à fila por recusa do cidadão (motivo 2 — "Resposta não aceita pelo cidadão").
A implementação aproveitará o campo motivo já presente na DTO Pendencia.motivo, que a API SIAC já retorna mas que nunca é mapeado, propagado ou exibido pelo sistema. A melhoria consiste em propagar esse valor por toda a cadeia — do AutoMapper em DomaintoViewModelProfile.cs, passando pelo ViewModel ConsultaMonitoramentoOcorrenciaSiac.cs, pela grid _GridListaOcorrenciasSiac.cshtml com badge visual, pelo JavaScript de monitoramento.js, pelo AtendimentoController.cs e ApiSiac156Service.cs, até o RegistroAtendimento.cshtml e atendimento-siac.js.
Quando o operador assumir um chamado com motivo 2, o sistema identificará que se trata de uma reabertura por negativa e habilitará diretamente o botão "Finalizar e Devolver 156", dispensando o fluxo normal de geração de ocorrência. Não são necessárias migrações de banco de dados para o fluxo principal, uma vez que a flag é transitória e determinada em tempo de execução pela API SIAC.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Novo | Rastreamento do campo motivo da Pendencia até a interface e leitura dos arquivos envolvidos. | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| ViewModel e AutoMaper | - | Novo | Adicionar Motivo e EhRecusaCidadao em ConsultaMonitoramentoOcorrenciaSiac.cs; adicionar .ForMember(o => o.Motivo, ...) em DomaintoViewModelProfile.cs; adicionar MotivoReabertura em RegistroAtendimentoViewModel.cs | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Serviço e Controller | - | Novo | Popularar model.MotivoReabertura a partir de detalhes.motivo em ApiSiac156Service.cs; aceitar parâmetro motivo na action RegistroAtendimento() em AtendimentoController.cs | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Interface grid e modal | - | Novo | Adicionar coluna com badge "Recusa" e atributo data-motivo em _GridListaOcorrenciasSiac.cshtml; expor MotivoReabertura no objeto JS do modelo em RegistroAtendimento.cshtml | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Propagação do motivo | - | Novo | Em monitoramento.js: incluir Motivo no objeto dados do click handler e concatenar &motivo= na URL do botão "Assumir" em MontarDadosModal156() | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Fluxo motivo 2 no atendimento | - | Novo | Em atendimento-siac.js: detectar MotivoReabertura == 2, pular geração de ocorrência, abrir ModalDevolucao156 diretamente e ajustar a validação de naturezas para o caminho de devolução direta | 0:00 | 2:30 | 0:00 | 0:00 | **2:30** |
| Testes e correções | - | Novo | Validar fluxo normal (motivo ≠ 2) sem regressão; testar fluxo motivo 2 de ponta a ponta (grid → badge → modal → assumir → devolver); verificar edge cases como ausência de campo na resposta da API | 0:00 | 0:00 | 2:30 | 0:00 | **2:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Implementação (75%) | 7:30 | 75,00% |
| Teste (20%) | 2:30 | 25,00% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **10:00** | **100,00%** |
