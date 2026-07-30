# Estimativa Bottom-Up: Requisição 541629

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 541629 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 11/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo implementar um módulo de gestão de tamanhos de uniformes no sistema, permitindo cadastrar, editar e inativar tamanhos de forma dinâmica. O campo atualmente utilizado passará a ser alimentado por este novo cadastro, garantindo maior flexibilidade e controle. Será realizada a migração de todos os tamanhos já existentes para o novo módulo, de forma a preservar o histórico e evitar perda de informações. A solução contemplará ajustes no backend, frontend e banco de dados, bem como testes funcionais e de usabilidade.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Definição de regras de negócio | - | Novo | Detalhar permissões, formatos e critérios de inclusão/inativação de tamanhos | 2:00 | 0:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Modelo de dados | - | Novo | Criação/alteração de tabelas e relacionamentos para armazenar tamanhos | 0:00 | 3:00 | 0:00 | 0:00 | 0:00 | **3:00** |
| Planejamento de migração de dados | - | Novo | Estruturar processo de migração dos tamanhos existentes para o novo cadastro | 0:00 | 1:30 | 0:00 | 0:00 | 0:00 | **1:30** |
| CRUD de tamanhos de uniforme | - | Novo | Implementar criação, edição, exclusão e listagem de tamanhos | 0:00 | 0:00 | 10:00 | 0:00 | 0:00 | **10:00** |
| Filtros e ordenação | - | Novo | Implementar filtros e ordenação na listagem | 0:00 | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Inativação lógica | - | Novo | Implementar lógica para marcar tamanhos como inativos sem excluir | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Migração de dados | - | Novo | Executar processo de migração dos tamanhos existentes | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Ajuste no campo existente | - | Novo | Alterar o campo atual da tela de tipo de uniforme para consumir o novo cadastro de tamanhos | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Alteração de referências antigas | - | Novo | Localizar e modificar todos os pontos no sistema que utilizam tamanho no formato antigo para usar o novo cadastro dinâmico | 0:00 | 2:00 | 8:00 | 2:00 | 0:00 | **12:00** |
| Testes unitários | - | Novo | Testes unitários | 0:00 | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |
| Teste de migração | - | Novo | Validar a integridade dos dados migrados | 0:00 | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |
| Teste de interface e usabilidade | - | Novo | Garantir que a interface seja funcional e intuitiva | 0:00 | 0:00 | 0:00 | 1:30 | 0:00 | **1:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:00 | 4,44% |
| Arquitetura (40%) | 6:30 | 14,44% |
| Implementação (75%) | 30:00 | 66,67% |
| Teste (20%) | 6:30 | 14,44% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **45:00** | **100,00%** |
