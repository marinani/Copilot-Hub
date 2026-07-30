# Estimativa Bottom-Up: Requisição 439184

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 439184 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 19/3/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo alterar a funcionalidade de cadastro/edição de funcionário permitindo que os campos "Classe", "Referência" e "Status" não sejam mais atualizados automaticamente via Meta4. Permitindo a partir de então atualização manual via sistema.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Desvincular os campos "Classe" e "Status" do job de atualização de servidores | - | Melhoria | Alterar o job de atualização de servidores para passar a não atualizar os campos "Classe" e "Status" do servidor de forma automática. | 0:00 | 0:00 | 1:30 | 0:30 | 0:00 | **2:00** |
| Liberar os campos "Classe", "Referência" e "Status" para alteração | - | Melhoria | Na tela de cadastro/edição do funcionário, liberar os campos "Classe", "Referência" e "Status" para edição. | 0:00 | 0:00 | 2:00 | 0:30 | 0:00 | **2:30** |
| Incluir nível de proteção nos campos "Classe", "Referência" e "Status" | - | Melhoria | Incluir condição nos campos "Classe", "Referência" e "Status" em que só serão liberados se o usuário autenticado estiver em um dos grupos do Segurança "Administradores", "Apoio Técnico Administrativo (Assistência)". | 0:00 | 0:00 | 1:30 | 0:30 | 0:00 | **2:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 5:00 | 76,92% |
| Teste (20%) | 1:30 | 23,08% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **6:30** | **100,00%** |
