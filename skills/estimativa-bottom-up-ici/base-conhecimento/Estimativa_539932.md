# Estimativa Bottom-Up: Requisição 539932

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 539932 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 7/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo adequar o módulo de cadastro de funcionários do Sigesguarda Pro às exigências estabelecidas pelo Plano de Carreira instituído pela Lei nº 16.203/2023, com alterações introduzidas pela Lei nº 16.541/2025. A melhoria prevê a inclusão dos campos “Padrão” e “Nível” na ficha funcional, permitindo o correto enquadramento dos servidores conforme os critérios legais vigentes.
Os campos serão implementados como listas suspensas (select), com valores predefinidos em algarismos romanos, evitando inconsistências e erros de digitação. Além disso, os campos já existentes “Classe” e “Referência” também serão ajustados para o mesmo formato de seleção controlada, garantindo padronização e maior confiabilidade dos dados registrados.
Essa melhoria visa assegurar a conformidade do sistema com a legislação atual, aprimorar a gestão de informações funcionais e proporcionar maior eficiência na atualização e consulta dos dados dos servidores públicos cadastrados.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Criação dos novos campos e alteração dos existentes na interface | - | Novo | Criação dos campos Padrão e Nível, e alteração dos campos existentes Classe e Referência. | 0:00 | 0:00 | 3:00 | 1:00 | 0:00 | **4:00** |
| Alterar back-end da aplicação | - | Novo | Alteração do back-end para aplicação para permitir salvar os novos campos e alterar o tipo dos que foram modificados. | 0:00 | 0:00 | 3:00 | 1:00 | 0:00 | **4:00** |
| Alterar banco de dados | - | Novo | Alteração do banco de dados para inserir os novos campos e adequar os campos existentes ao novo padrão | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 8:00 | 80,00% |
| Teste (20%) | 2:00 | 20,00% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **10:00** | **100,00%** |
