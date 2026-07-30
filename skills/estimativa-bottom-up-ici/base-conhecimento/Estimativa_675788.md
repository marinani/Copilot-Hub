# Estimativa Bottom-Up: Requisição 675788

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 675788 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 3/2/2026 |

---

## Escopo da Estimativa

A estimativa contempla a implementação completa da atualização automática de proprietários via GTM no SIGMU Cidades, combinando processamento batch semanal via Hangfire e atualização sob demanda assíncrona via RabbitMQ, com validações de negócio, controle por data, logs, auditoria, tratamento de exceções e ajustes técnicos necessários, sem impacto em telas, relatórios ou notificações, mantendo aderência estrita ao requisito funcional definido.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Atualização Automática, por Hangfire, de Proprietários via Integração GTM | - | Novo | Atualizar automaticamente os dados de proprietários das solicitações a partir da integração com o GTM, garantindo aderência às regras de negócio, consistência dos dados e rastreabilidade operacional, sem intervenção manual. Executar periodicamente a atualização de proprietários por meio de um job semanal orquestrado pelo Hangfire, garantindo processamento controlado, sequencial e resiliente. | 2:00 | 9:00 | 1:30 | 0:00 | 12:30 | **0:00** |
| Atualização Sob Demanda Assíncrona via RabbitMQ | - | Novo | Permitir a atualização automática do proprietário no momento de abertura da solicitação, utilizando processamento assíncrono para garantir desempenho e desacoplamento. | 2:00 | 9:00 | 1:30 | 0:00 | 12:30 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 4:00 | 16,00% |
| Arquitetura (40%) | 18:00 | 72,00% |
| Implementação (75%) | 3:00 | 12,00% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 25:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
