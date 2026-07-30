# Estimativa Bottom-Up: Requisição 583464

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 583464 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 22/9/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo ajustar o Sigesguarda Pro para incluir a opção "Outros" no campo "Grau de Parentesco" no cadastro de noticiado (agressor) do módulo Processo Patrulha Maria da Penha, complementando as opções já existentes.
A inclusão desta opção é essencial para atender casos em que o relacionamento entre vítima e agressor não se enquadra nas categorias pré-definidas, permitindo que o operador do sistema registre com precisão todos os tipos de relacionamentos encontrados nos atendimentos.
A solução contemplará ajustes no enumerador de Grau de Parentesco, modificações no modelo de dados para armazenar a descrição textual quando "Outros" for selecionado, bem como alterações no front-end para exibição de um campo adicional de texto livre que será habilitado condicionalmente. Serão realizados testes funcionais e de usabilidade para garantir que os operadores consigam registrar corretamente todos os tipos de relacionamentos durante o processo de cadastro.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Análise do código para identificar todos os arquivos que precisam ser modificados. Inclui mapeamento das dependências entre camadas, planejamento da estratégia de implementação e avaliação de impactos em funcionalidades existentes. | 0:00 | 1:00 | 0:00 | 0:00 | 0:00 | **1:00** |
| Atualização do enumerador | - | Melhoria | Adicionar o novo valor "Outros" ao enumerador GrauParentesco. Verificar e atualizar quaisquer métodos de extensão relacionados ao enumerador. | 0:00 | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Atualização do modelo de dados e criação da migration | - | Melhoria | Adicionar a nova propriedade GrauParentescoOutros à entidade VitimaNoticiado. Atualizar o mapeamento do EntityFramework para incluir o novo campo. Criar e testar a migração do banco de dados para adicionar a nova coluna a tabelas, e verificação de compatibilidade com dados existentes. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Atualização da interface (HTML/CSS) | - | Melhoria | Modificar a interface para adicionar o novo campo de texto livre. Estilizar o campo para manter a consistência visual com o restante do sistema. Garantir que o campo seja responsivo e acessível. Atualizar labels e mensagens de validação. | 0:00 | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Implementação de lógica no JavaScript | - | Melhoria | Adicionar lógica ao arquivo JavaScript para controlar a visibilidade do campo de texto adicional baseado na seleção do dropdown. Implementar validação client-side adequada para o novo campo. Garantir que os dados sejam corretamente enviados ao servidor. Testar o comportamento em diferentes navegadores. | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Atualização dos serviços de back-end | - | Melhoria | Modificar os services, controllers e DTOs/ViewModels relevantes para suportar o novo campo. Incluir validação server-side para o campo adicional. Garantir que os dados sejam corretamente persistidos e recuperados do banco de dados. Atualizar mapeamentos do para incluir o novo campo. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Testes e correções | - | Melhoria | Realizar testes funcionais completos para validar o comportamento da nova funcionalidade. Incluir testes de casos de uso: seleção de opções normais, seleção da opção "Outros", validação de dados, persistência e recuperação de dados. Identificar e corrigir quaisquer bugs encontrados. Realizar testes de regressão para garantir que funcionalidades existentes não foram impactadas. | 0:00 | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 1:00 | 8,33% |
| Implementação (75%) | 9:00 | 75,00% |
| Teste (20%) | 2:00 | 16,67% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **12:00** | **100,00%** |
