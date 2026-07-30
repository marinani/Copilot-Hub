# Estimativa Bottom-Up: Requisição 537306

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 537306 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 8/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo incluir a etapa “Encaminhar Ocorrência” no fluxo de geração de ocorrências, tornando obrigatório o direcionamento inicial da ocorrência a um setor. A funcionalidade permitirá registrar o encaminhamento, restringir o acesso por setor e status, além de possibilitar o reencaminhamento da ocorrência até sua alocação correta, garantindo rastreabilidade e controle do processo.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|
| Entendimento e formalização do fluxo proposto | - | Novo | Entendimento e formalização do fluxo proposto | 3:00 | 0:00 | 0:00 | 0:00 | **3:00** |
| Mapeamento de regras de negócio e validações | - | Novo | Mapeamento de regras de negócio e validações obrigatórias (encaminhamento obrigatório, fluxo alternativo para despacho direto) | 3:00 | 0:00 | 0:00 | 0:00 | **3:00** |
| Definição do controle de acesso | - | Novo | Definição dos critérios de controle de acesso por setor/status e regras para reencaminhamento | 2:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Análise de impacto | - | Novo | Avaliação do impacto no fluxo de geração de ocorrências e telas existentes (Gerar, Visualizar, Monitoramento) | 2:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Modelagem da estrutura | - | Novo | Modelagem da entidade de encaminhamento | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Atualização do controle de acesso | - | Novo | Atualização de controle de permissões e filtros de visualização no mapa/lista | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Alteração do botão de "Gerar Ocorrência" | - | Novo | Alteração no botão “Gerar Ocorrência” para “Gerar Ocorrência e Encaminhar” com abertura de modal | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Criação da modal de seleção | - | Novo | Criação do modal de seleção de setor de despacho (listando apenas os setores de despacho cadastrados) | 0:00 | 5:00 | 0:00 | 0:00 | **5:00** |
| Salvar encaminhamento | - | Novo | Implementação do salvamento do encaminhamento (data/hora, setor, usuário) | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Atualização do histórico | - | Novo | Atualização do histórico de alterações da ocorrência com registro do encaminhamento | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Incluir opção de reencaminhar | - | Novo | Adição da nova opção “Reencaminhar” no menu “Opções” da visualização da ocorrência, com reutilização do modal de seleção | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Implementação das regras de acesso | - | Novo | Implementação das regras de acesso ao mapa e lista conforme o setor do usuário e status da ocorrência | 0:00 | 5:00 | 0:00 | 0:00 | **5:00** |
| Teste de encaminhamento | - | Novo | Testes manuais do novo fluxo de geração com encaminhamento obrigatório | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |
| Teste de reencaminhamento | - | Novo | Testes do reencaminhamento e múltiplos registros | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |
| Teste do histórico | - | Novo | Verificação do histórico da ocorrência e validação dos registros de data/hora/setor | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |
| Teste de controle de acesso | - | Novo | Testes de controle de acesso no mapa/lista por setor e status | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |
| Testes regressivos | - | Novo | Testes regressivos nas funcionalidades de despacho e geração direta de OC | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 10:00 | 20,83% |
| Implementação (75%) | 31:00 | 64,58% |
| Teste (20%) | 7:00 | 14,58% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **48:00** | **100,00%** |
