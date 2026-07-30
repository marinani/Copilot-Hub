# Estimativa Bottom-Up: Requisição 507237_v2

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 507237 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 2/6/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo a parametrização dos campos "Volta ao Estoque" e "Quantidade". Para que estes campos sejam exibidos de forma personalizada de acordo com o tipo de equipamento e com isso evitar redudância.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Criar campo para parametrizar a opção de "Volta ao estoque" (Interface) | - | Novo | Na tela de Tipo de Equipamento criar um novo botão Sim/Não chamado "Volta ao estoque". Onde o usuário poderá informar se para o tipo de equipamento selecionado deverá possuir a opção de voltar ao estoque em caso de devolução | 0:00 | 0:00 | 1:00 | 0:30 | 0:00 | **1:30** |
| Criar campo para parametrizar a opção de "Volta ao estoque" (Back-end) | - | Novo | Alterar o back-end da aplicação para permitir que o novo campo seja salvo. | 0:00 | 0:00 | 2:30 | 0:30 | 0:00 | **3:00** |
| Alterar a modal de devolução da cautela (Interface) | - | Novo | Alterar a modal de devolução da cautela para permitir que o campo "Volta ao estoque" seja exibido de acordo com o valor do parâmetro escolhido pelo usuário. | 0:00 | 0:00 | 1:30 | 0:30 | 0:00 | **2:00** |
| Alterar a modal de devolução da cautela (Back-end) | - | Novo | Alterar o back-end da aplicação para passar a informar o novo dado parametrizado. | 0:00 | 0:00 | 2:30 | 0:30 | 0:00 | **3:00** |
| Alterar banco de dados | - | Novo | Alterar o modelo de dados para permitir salvar o novo campo de parametrização "Volta ao estoque". | 0:00 | 0:00 | 1:00 | 0:30 | 0:00 | **1:30** |
| Criar campo para parametrizar a opção de "Quantidade" por tipo de equipamento. (Interface) | - | Novo | Na tela de Tipo de Equipamento criar um novo botão Sim/Não chamado "Permitir quantidade". Onde o usuário poderá informar se para o tipo de equipamento selecionado deverá possuir a opção de informar a quantidade no momento do cadastro do equipamento. | 0:00 | 0:00 | 1:00 | 0:30 | 0:00 | **1:30** |
| Criar campo para parametrizar a opção de "Quantidade" por tipo de equipamento. (Back-end) | - | Novo | Alterar o back-end da aplicação para permitir que o novo campo seja salvo. | 0:00 | 0:00 | 2:30 | 0:30 | 0:00 | **3:00** |
| Alterar a tela de cadastro e de edição do equipamento (Interface) | - | Novo | Alterar a tela de cadastro e de edição do equipamento para permitir que o campo "Quantidade" seja exibido de acordo com o valor do parâmetro escolhido pelo usuário. | 0:00 | 0:00 | 1:30 | 0:30 | 0:00 | **2:00** |
| Alterar a tela de cadastro e de edição do equipamento (Back-end) | - | Novo | Alterar o back-end da aplicação para passar a informar o novo dado parametrizado. | 0:00 | 0:00 | 2:30 | 0:30 | 0:00 | **3:00** |
| Alterar banco de dados | - | Novo | Alterar o modelo de dados para permitir salvar o novo campo de parametrização "Permitir quantidade". | 0:00 | 0:00 | 1:00 | 0:30 | 0:00 | **1:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 17:00 | 77,27% |
| Teste (20%) | 5:00 | 22,73% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **22:00** | **100,00%** |
