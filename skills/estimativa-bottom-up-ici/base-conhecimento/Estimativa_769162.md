# Estimativa Bottom-Up: Requisição 769162

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 769162 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 2/6/2026 |

---

## Escopo da Estimativa

Implementar na tela de cadastro de solicitações do módulo Fiscalização a seleção de Subdivisão vinculada à Intervenção escolhida pelo usuário, permitindo o preenchimento automático das informações de Assunto e Subdivisão da solicitação. A funcionalidade será disponibilizada exclusivamente para organizações com integração SIAC156 ativa, utilizando os cadastros já existentes e mantendo compatibilidade com os processos atuais de criação de solicitações.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Exibição da Subdivisão conforme integração SIAC156 e Consulta e carregamento de subdivisões por intervenção | - | Novo | Implementar exibição condicional do campo Subdivisão na tela de cadastro de solicitação do módulo Fiscalização para organizações com integração SIAC156 ativa, permitindo seleção opcional da subdivisão vinculada à intervenção escolhida e Implementar consulta dinâmica das subdivisões vinculadas à intervenção selecionada, incluindo atualização automática do conteúdo do campo, limpeza da seleção ao alterar a intervenção e utilização dos campos já existentes na entidade de solicitação sem necessidade de alterações estruturais. | 1:00 | 3:30 | 0:30 | 0:00 | 5:00 | **0:00** |
| Persistência automática de Assunto e Subdivisão | - | Melhoria | Implementar preenchimento automático dos campos Assunto e Subdivisão da solicitação a partir da subdivisão selecionada, gravando as informações derivadas no momento do cadastro da solicitação. | 0:20 | 0:30 | 0:10 | 0:00 | 1:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 1:20 | 22,22% |
| Arquitetura (40%) | 4:00 | 66,67% |
| Implementação (75%) | 0:40 | 11,11% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 6:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
