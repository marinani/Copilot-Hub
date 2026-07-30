# Estimativa Bottom-Up: Requisição 475693

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 475693 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 19/5/2025 |

---

## Escopo da Estimativa

Esta solicitação visa à implementação de melhorias no sistema, com o objetivo de integrar os dados de CPFs e placas de veículos com restrições, fornecidos por meio da API do Ministério da Justiça. A funcionalidade permitirá o consumo da referida API e o retorno das informações em formato compatível com o HIKCENTRAL, atendendo às necessidades operacionais de segurança. Além disso, será criada uma tela de consulta destinada a administradores e operadores, possibilitando a visualização detalhada das informações retornadas pela API, como dados de restrições associados a CPFs e placas.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Criar tela para realizar a consulta de dados de pessoas e placas de veículos com restrições | - | Novo | A tela deverá permitir que o usuário consulte pessoas por CPF e placas de veículos para saber se existe restrição com o Ministério da Justiça. Essa tela deverá possuir nível de acesso apenas para administradores e usuários pertencentes um novo grupo destinado apenas a essa funcionalidade. | 0:00 | 0:00 | 18:00 | 2:00 | 0:00 | **20:00** |
| Criar integração com a API do Ministério da Justiça | - | Novo | Deverá ser criada uma nova integração no sistema para permitir consultar dados do Ministério da Justiça. Serão duas consultas diferentes, uma para verificar o situação de pessoa com restrição via CPF e outra para verificar a situação de veículos via número da placa. | 0:00 | 0:00 | 12:00 | 2:00 | 0:00 | **14:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 30:00 | 88,24% |
| Teste (20%) | 4:00 | 11,76% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **34:00** | **100,00%** |
