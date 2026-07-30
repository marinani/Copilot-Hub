# Estimativa Bottom-Up: Requisição 537415

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 537415 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 8/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo implementar um alerta automático durante a abertura de ocorrências, com o intuito de evitar registros duplicados no mesmo endereço em um curto intervalo de tempo. A funcionalidade verificará, de forma parametrizável, se já existe uma ocorrência aberta no endereço informado nos últimos 60 minutos, alertando o usuário por meio de um popup. O usuário poderá optar por seguir com o registro ou apenas registrar o atendimento realizado, garantindo maior controle, otimização dos recursos e organização da base de dados.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Implementação de lógica de verificação de ocorrência | - | Novo | Implementação de lógica de verificação da ocorrência | 0:00 | 0:00 | 6:00 | 1:00 | 0:00 | **7:00** |
| Criar tela de parametrização | - | Novo | Criar tela de parametrização | 0:00 | 0:00 | 6:00 | 1:00 | 0:00 | **7:00** |
| Desenvolvimento do popup com lógica condicional e botões Sim/Não | - | Novo | Desenvolvimento do popup com lógica condicional e botões Sim/Não | 0:00 | 0:00 | 4:00 | 1:00 | 0:00 | **5:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 16:00 | 84,21% |
| Teste (20%) | 3:00 | 15,79% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **19:00** | **100,00%** |
