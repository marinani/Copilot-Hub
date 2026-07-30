# Estimativa Bottom-Up: Requisição 585001

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 585001 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 22/9/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo transformar o cadastro de 'Funções na Equipe' do Sigesguarda Pro em um sistema configurável pelo usuário, substituindo o atual modelo baseado em enumeradores fixos (Condutor, Apoio, Integrante e K9) por um cadastro dinâmico.
A implementação desta melhoria é fundamental para atender a necessidade do cliente de gerenciar as funções de equipe conforme sua demanda operacional, permitindo incluir ou excluir opções sem depender de intervenção técnica no código fonte.
A solução contemplará a criação de uma nova entidade para armazenar as funções configuráveis, desenvolvimento de interface administrativa para gestão dessas funções, adaptação dos componentes existentes que utilizam o enumerador atual, além da migração dos dados já cadastrados para preservar o histórico. Serão realizados testes de integração e validação de dados para garantir que todos os processos que dependem das funções de equipe continuem funcionando corretamente após a mudança.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise | - | Melhoria | Levantamento detalhado dos requisitos, análise da estrutura atual do banco de dados e dos componentes afetados. | 0:00 | 4:00 | 0:00 | 0:00 | 0:00 | **4:00** |
| Modelagem de dados | - | Melhoria | Criação de nova tabela para funções e ajuste nas relações existentes. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Desenvolvimento back-end | - | Melhoria | Criação de serviço para gerenciamento de funções e adaptação dos existentes. | 0:00 | 0:00 | 8:00 | 0:00 | 0:00 | **8:00** |
| Desenvolvimento front-end | - | Melhoria | Criação de tela para gerenciamento de funções e adaptação das telas existentes. | 0:00 | 0:00 | 12:00 | 0:00 | 0:00 | **12:00** |
| Migração de dados | - | Melhoria | Script para migrar os dados existentes para o novo modelo. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Testes e correções | - | Melhoria | Verificação do funcionamento correto da nova funcionalidade e validação da integridade dos dados. | 0:00 | 0:00 | 0:00 | 4:00 | 0:00 | **4:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 4:00 | 12,50% |
| Implementação (75%) | 24:00 | 75,00% |
| Teste (20%) | 4:00 | 12,50% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **32:00** | **100,00%** |
