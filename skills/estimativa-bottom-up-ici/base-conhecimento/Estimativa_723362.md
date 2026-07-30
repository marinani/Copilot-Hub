# Estimativa Bottom-Up: Requisição 723362

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 723362 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 3/4/2026 |

---

## Escopo da Estimativa

Ajustar o comportamento do mapa na tela inicial da Fiscalização para que a consulta de solicitações considere apenas a área visível (bounding box), melhorando desempenho e usabilidade.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Ajustar consulta por área do mapa (bounding box) | - | Melhoria | Alterar a lógica de busca para considerar apenas solicitações dentro da área visível do mapa definida pelo usuário (zoom, pan ou localização atual), incluindo o envio dessas informações para a API e o ajuste no backend para retornar apenas os dados dentro da área. | 2:30 | 7:00 | 0:30 | 0:00 | 10:00 | **0:00** |
| Atualização automática ao interagir com o mapa | - | Melhoria | Implementar atualização automática da consulta ao alterar zoom ou mover o mapa, com controle de frequência para evitar excesso de requisições. | 1:30 | 4:00 | 0:30 | 0:00 | 6:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 4:00 | 25,00% |
| Arquitetura (40%) | 11:00 | 68,75% |
| Implementação (75%) | 1:00 | 6,25% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 16:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
