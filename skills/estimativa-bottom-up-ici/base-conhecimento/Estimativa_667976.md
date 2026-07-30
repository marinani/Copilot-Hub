# Estimativa Bottom-Up: Requisição 667976

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 667976 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 3/2/2026 |

---

## Escopo da Estimativa

A estimativa contempla a implementação da reordenação manual de rotas de fiscalização no SIGMU Cidades, permitindo que o usuário ajuste a ordem das paradas geradas automaticamente pela Google Routes API, com recálculo imediato da rota, atualização visual no mapa, geração de PDF refletindo a nova ordem e validações técnicas e operacionais.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Interface de Reordenação Manual de Paradas | - | Novo | Disponibilizar uma interface interativa que permita ao usuário reordenar manualmente as paradas da rota, após a geração automática, utilizando drag-and-drop, com feedback visual claro e acessibilidade. | 3:00 | 10:00 | 2:30 | 0:00 | 15:30 | **0:00** |
| Recálculo Automático da Rota Reordenada | - | Novo | Recalcular automaticamente a rota sempre que o usuário confirmar uma nova ordem de paradas, garantindo que distância, tempo estimado e trajeto no mapa reflitam a sequência personalizada. | 1:00 | 4:00 | 0:30 | 0:00 | 5:30 | **0:00** |
| Atualização Visual do Mapa Interativo | - | Melhoria | Manter o mapa sincronizado com a rota reordenada, assegurando coerência visual entre lista de paradas, métricas e representação geográfica. | 0:15 | 1:00 | 0:15 | 0:00 | 1:30 | **0:00** |
| Geração de PDF com Rota Customizada | - | Melhoria | Garantir que o PDF da rota reflita fielmente a ordem customizada definida pelo usuário, mantendo o layout atual e adicionando rastreabilidade da alteração. | 0:15 | 1:00 | 0:15 | 0:00 | 1:30 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 4:30 | 18,75% |
| Arquitetura (40%) | 16:00 | 66,67% |
| Implementação (75%) | 3:30 | 14,58% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 24:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
