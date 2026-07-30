# Estimativa Bottom-Up: Requisição 561520

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 561520 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 25/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo ajustar o Sigesguarda Pro para exibir o campo “dados importantes” proveniente da API do 156 diretamente na tela de monitoramento de protocolos e também na tela de protocolo já assumido no sistema.
A inclusão deste campo é essencial para a triagem inicial dos protocolos, permitindo que o agente identifique rapidamente se deve assumir o protocolo, gerar uma ocorrência ou devolvê-lo ao fluxo do 156.
A solução contemplará ajustes na integração com a API, no back-end para transporte e armazenamento dos dados, bem como alterações no front-end para exibição clara e destacada da informação. Serão realizados testes funcionais e de usabilidade para garantir que os agentes consigam utilizar o campo de forma eficaz durante o processo de atendimento.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Definição de regras de negócio | - | Melhoria | Definir em quais telas e situações o campo “Dados Importantes” deve aparecer e como será apresentado. | 2:00 | 0:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Integração com API do 156 | - | Melhoria | Ajuste na integração com o 156 para passar a retornar o campo de dados importantes. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Ajuste de DTOs/ViewModels | - | Melhoria | Incluir o campo nos objetos de transporte de dados para uso no front-end. | 0:00 | 1:00 | 2:00 | 0:00 | 0:00 | **3:00** |
| Alteração da tela de monitoramento | - | Melhoria | Exibir o campo "Dados Importantes" na tela de monitoramento de protocolos. | 0:00 | 0:00 | 4:00 | 0:30 | 0:00 | **4:30** |
| Alteração da tela de protocolo assumido | - | Melhoria | Exibir o campo "Dados Importantes" também quando o protocolo já foi assumido. | 0:00 | 0:00 | 3:00 | 0:30 | 0:00 | **3:30** |
| Testes unitários | - | Melhoria | Garantir que a integração e transporte do campo funcionem corretamente | 0:00 | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:00 | 12,50% |
| Arquitetura (40%) | 1:00 | 6,25% |
| Implementação (75%) | 11:00 | 68,75% |
| Teste (20%) | 2:00 | 12,50% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **16:00** | **100,00%** |
