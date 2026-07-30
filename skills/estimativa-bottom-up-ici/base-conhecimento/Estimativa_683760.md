# Estimativa Bottom-Up: Requisição 683760

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 683760 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 26/2/2026 |

---

## Escopo da Estimativa

Implementação da geração e anexação automática de relatório SIAC156 durante a vinculação manual de solicitações no SIGMU Cidades, garantindo consistência com os fluxos automáticos já existentes (Hangfire e RabbitMQ), processamento assíncrono em background e não bloqueio da operação principal.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Validação de Elegibilidade e Disparo Assíncrono | - | Melhoria | Implementar validações para identificar solicitações filhas com origem SIAC156 e Protocolo de Origem preenchido, verificar se a solicitação mãe possui Protocolo SUP válido e, após commit da vinculação, realizar envio da mensagem para RabbitMQ, garantindo processamento assíncrono em background sem impacto na performance da operação principal. | 2:00 | 9:00 | 1:30 | 0:00 | 12:30 | **0:00** |
| Geração, Anexação e Tratamento de Erros de Relatório SIAC | - | Novo | Implementar geração do relatório SIAC em PDF para cada solicitação filha elegível, realizar anexação consolidada em único trâmite no protocolo SUP e implementar captura de exceções, garantindo que falhas externas (SUP/ICIDOC) não bloqueiem a vinculação. | 2:00 | 9:00 | 1:30 | 0:00 | 12:30 | **0:00** |

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
