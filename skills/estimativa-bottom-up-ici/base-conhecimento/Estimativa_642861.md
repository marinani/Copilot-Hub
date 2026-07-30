# Estimativa Bottom-Up: Requisição 642861

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Andrea Cristina Lima Duarte Ferreira |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 642861 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 3/2/2026 |

---

## Escopo da Estimativa

A estimativa contempla a implementação de um serviço automatizado de sincronização diária das Unidades de Trâmite dos usuários com Login SUP, garantindo que as permissões registradas no sistema SIGMU estejam sempre alinhadas às definições oficiais do SUP. O escopo inclui processamento em background via Hangfire, integração com a API do SUP, aplicação de regras de negócio para inclusão, remoção e definição de unidade principal, além de ajustes pontuais na interface de Execução de Vistoria para refletir corretamente as unidades sincronizadas. A entrega foca em segurança, conformidade e redução de esforço operacional, sem introduzir sincronização em tempo real, telas administrativas adicionais ou alterações estruturais em usuários.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Sincronização Automática de Unidades de Trâmite (Job Hangfire) | - | Novo | Executar diariamente um job Hangfire responsável por sincronizar as unidades de trâmite dos usuários ativos com Login SUP, mantendo a base do SIGMU consistente com as permissões vigentes no SUP. Garantir que cada usuário possua uma unidade de trâmite principal válida, ajustando automaticamente essa definição sempre que houver mudanças nas permissões vindas do SUP. Assegurar que o processo de sincronização seja robusto, auditável e monitorável, mesmo em cenários de erro, indisponibilidade do SUP ou crescimento do volume de usuários. | 4:00 | 15:00 | 2:00 | 0:00 | 21:00 | **0:00** |
| Seleção de Unidade de Origem na Execução de Vistoria | - | Melhoria | Disponibilizar, na tela de Execução de Vistoria, um campo de seleção editável para Unidade de Origem, alimentado automaticamente pelas unidades de trâmite sincronizadas do SUP, com pré-seleção da unidade principal, permitindo ao usuário escolher livremente entre as unidades autorizadas, garantindo usabilidade, consistência com as permissões vigentes e desempenho adequado. | 0:30 | 2:00 | 0:30 | 0:00 | 3:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 4:30 | 18,75% |
| Arquitetura (40%) | 17:00 | 70,83% |
| Implementação (75%) | 2:30 | 10,42% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 24:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
