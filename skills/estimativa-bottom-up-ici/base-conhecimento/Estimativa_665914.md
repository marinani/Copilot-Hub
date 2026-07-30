# Estimativa Bottom-Up: Requisição 665914

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 665914 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 2/2/2026 |

---

## Escopo da Estimativa

Ajustes de layout, implementação de novas regras de exibição, validações de negócio e testes funcionais

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Página de Solicitação | - | Melhoria | A região de Solicitações Vinculadas passará a ser exibida permanentemente, independentemente da existência de vínculos. O botão Vincular Solicitações ficará sempre visível, desde que a solicitação não esteja encerrada ou devolvida, mantendo a regra atual de bloqueio para esses status. O DataList de solicitações vinculadas será exibido somente quando existirem solicitações filhas associadas à solicitação principal. | 1:00 | 3:00 | 0:10 | 0:00 | 4:10 | **0:00** |
| Tela de Detalhes | - | Melhoria | A aba Vinculadas passará a ser exibida em todos os cenários, não ficando mais condicionada à existência de solicitações vinculadas. | 0:10 | 0:30 | 0:10 | 0:00 | 0:50 | **0:00** |
| Componente de Agrupamento | - | Melhoria | O botão Vincular Solicitações permanecerá sempre visível, desde que a solicitação não esteja encerrada ou devolvida, conforme regra atual. Inclusão de nova regra de negócio: O botão somente será exibido caso ainda não tenha ocorrido nenhuma vistoria na solicitação principal. Justificativa: após a realização da primeira vistoria, caso uma nova solicitação seja vinculada, ela não será devolvida ao SIAC 156, uma vez que a devolução da solicitação principal e de suas filhas ocorre sempre ao final da primeira vistoria. O DataGrid de solicitações vinculadas será exibido exclusivamente quando houver solicitações filhas. | 1:00 | 3:00 | 0:30 | 0:00 | 4:30 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:10 | 22,81% |
| Arquitetura (40%) | 6:30 | 68,42% |
| Implementação (75%) | 0:50 | 8,77% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 9:30 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
