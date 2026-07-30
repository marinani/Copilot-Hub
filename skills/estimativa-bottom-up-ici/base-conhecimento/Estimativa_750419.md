# Estimativa Bottom-Up: Requisição 750419

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 750419 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 20/5/2026 |

---

## Escopo da Estimativa

Implementar ajustes no fluxo de cancelamento de protocolos SIAC 156, contemplando devolução automática ao sistema de origem quando a solicitação não possuir vistoria registrada, atualização de status para “Devolvida”, registro de histórico no SIGMU quando o cancelamento não puder ser efetivado e tratamento das regras de desvinculação e reorganização de solicitações principais e vinculadas durante o processo de cancelamento.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Cancelamento de protocolo SIAC 156 sem vistoria | RF-1 e RF-5 | Melhoria | Ajustar o comportamento do cancelamento de protocolos SIAC 156 para permitir devolução automática ao sistema de origem quando a solicitação estiver sem vistoria registrada, incluindo atualização de status para “Devolvida” e registro adequado de histórico conforme as regras de negócio. | 1:00 | 2:00 | 0:15 | 0:00 | 3:15 | **0:00** |
| Tratamento de cancelamento com vistoria registrada | RF-2 | Melhoria | Implementar tratamento para solicitações com vistoria registrada, impedindo a devolução ao SIAC 156 e registrando automaticamente no histórico do SIGMU a informação de tentativa de cancelamento pelo interessado. | 0:15 | 1:00 | 0:15 | 0:00 | 1:30 | **0:00** |
| Tratamento de solicitações principais e vinculadas | RF-3 e RF-4 | Melhoria | Implementar regras de desvinculação e reorganização de solicitações principais e vinculadas durante o cancelamento de protocolos SIAC 156, garantindo consistência dos vínculos e manutenção correta da estrutura das solicitações relacionadas. | 1:00 | 2:00 | 0:15 | 0:00 | 3:15 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:15 | 28,13% |
| Arquitetura (40%) | 5:00 | 62,50% |
| Implementação (75%) | 0:45 | 9,38% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 8:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
