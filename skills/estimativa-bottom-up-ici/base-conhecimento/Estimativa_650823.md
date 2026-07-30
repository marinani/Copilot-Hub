# Estimativa Bottom-Up: Requisição 650823

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

Esta solicitação tem como objetivo alterar o comportamento do botão "Marcar como lido e tramitar via 156", presente no modal de detalhes de protocolo da tela de Monitoramento (_ModalProtocolo156.cshtml). Atualmente, ao clicar nesse botão, o sistema registra o protocolo como lido na base de dados local (tabela ProtocolosLidos) e o move para a aba "Protocolos lidos", sem nenhuma interação com a API externa do SIAC 156.
O novo comportamento exige que, ao clicar no botão, seja aberta a modal de Devolução 156 (_ModalDevolucao156.cshtml) para que o operador informe o motivo e a observação — e o protocolo seja efetivamente devolvido à central 156 via API externa, sem que o operador precise antes "assumir" o chamado e criar um atendimento formal.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Novo | Leitura e mapeamento dos fluxos atuais de MarcarLido() e DevolverOcorrencia156(), identificação das dependências entre monitoramento.js, atendimento-siac.js, ApiSiac156Service e DevolverOcorrencia156ViewModel; definição da abordagem de implementação | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Novo ViewModel | - | Novo | Criação de DevolverProtocolo156MonitoramentoViewModel contendo apenas NumeroProtocolo, Motivo156, Data156 e Obs156 — sem AtendimentoGuid, Naturezas ou flags de encerramento exigidos pelo fluxo atual da página de Atendimento | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Novo método de serviço | - | Novo | Implementação de novo método na ApiSiac156Service que chame _repositorio.DevolverSolicitacao() (API externa SIAC 156) usando apenas o número do protocolo, registre o ProtocoloLido local e grave o log de auditoria, sem precisar localizar ou alterar um Atendimento existente | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Novo endpoint na controller | - | Novo | Criação de action POST em MonitoramentoController mapeada em /monitoramento/devolver-protocolo-156, que receba o novo ViewModel e delegue ao serviço acima | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Inclusão da modal na view de Monitoramento | - | Novo | Adição do @await Html.PartialAsync("_ModalDevolucao156") na view de Monitoramento e verificação de que os arquivos CSS/JS necessários já estão referenciados no layout compartilhado | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Adaptação do Javascript de Monitoramento | - | Novo | Alteração do handler de btn-marcar-lido em monitoramento.js para: abrir #ModalDevolucao156; popular o <select id="Motivo156"> via chamada AJAX ao endpoint existente /siac/obter-motivo-devolucao/{protocolo}; preencher #Data156 com a data atual; e acionar o novo endpoint de devolução ao clicar em #btnDevolverFinalizar156 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Isolamento de contexto no handler de finalização | - | Novo | Ajuste no handler de #btnDevolverFinalizar156 (atualmente em atendimento-siac.js) para detectar o contexto em que a modal foi aberta (Monitoramento vs. Atendimento) e acionar a função correta, sem quebrar o fluxo existente de devolução pelo Atendimento | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Testes e correções | - | Novo | Testes do fluxo completo em ambiente de desenvolvimento: abertura da modal a partir do Monitoramento, preenchimento do formulário, envio à API SIAC, verificação do registro local ProtocoloLido, atualização dos totalizadores e da grade; além de testes de regressão do fluxo original de devolução pela tela de Atendimento | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Implementação (75%) | 8:30 | 80,95% |
| Teste (20%) | 2:00 | 19,05% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **10:30** | **100,00%** |
