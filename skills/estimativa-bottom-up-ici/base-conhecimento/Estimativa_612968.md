# Estimativa Bottom-Up: Requisição 612968

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 612968 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 11/3/2026 |

---

## Escopo da Estimativa

Implementar a identificação, armazenamento e consulta do tipo de solicitante (ex: cidadão, vereador, deputado) nas solicitações vindas do SIAC 156, permitindo visualização, filtro e consulta detalhada no sistema.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Salvar o tipo de solicitante | - | Melhoria | Garantir que toda solicitação importada do SIAC 156 grave o tipo de solicitante (ex: cidadão, vereador). Caso não venha preenchido, salvar como “Não informado”. Criar o campo no banco para armazenar o tipo de solicitante e atualizar os registros antigos com valor padrão. | 2:00 | 4:00 | 1:00 | 0:00 | 7:00 | **0:00** |
| Exibir no grid de solicitações, no detalhe da solicitação | - | Melhoria | Mostrar o tipo de solicitante na listagem de solicitações, permitindo visualização rápida pelo usuário e apresentar o tipo de solicitante na tela de detalhe da solicitação.. | 1:00 | 2:00 | 0:45 | 0:00 | 3:45 | **0:00** |
| Consultar dados completos do solicitante | - | Novo | Permitir que o usuário clique no tipo de solicitante e visualize mais informações (nome, telefone, etc.) em uma janela (modal), buscando os dados em tempo real no SIAC 156. | 1:30 | 6:00 | 0:30 | 0:00 | 8:00 | **0:00** |
| Criar filtro por tipo de solicitante | - | Novo | Permitir filtrar as solicitações por tipo de solicitante (ex: ver apenas solicitações de vereadores). | 1:00 | 2:00 | 0:30 | 0:00 | 3:30 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 5:30 | 24,72% |
| Arquitetura (40%) | 14:00 | 62,92% |
| Implementação (75%) | 2:45 | 12,36% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 22:15 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
