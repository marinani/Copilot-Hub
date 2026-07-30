# Estimativa Bottom-Up: Requisição 596632

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 596632 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 9/10/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo disponibilizar a emissão da Identidade Funcional para os agentes da SETRAN no Sigesguarda Pro, replicando o padrão visual adotado na identidade funcional da Guarda Municipal, com as adequações solicitadas (título “SUPERINTENDÊNCIA DE TRÂNSITO”, borda em verde claro, marcas d’água “SETRAN”, caixa de assinatura “DIRETOR DA SETRAN” e substituição do brasão pela versão oficial de Curitiba).
A implementação desta melhoria é fundamental para atender a necessidade do cliente de padronizar e oficializar a identidade funcional da SETRAN, mantendo a mesma experiência de emissão já consolidada na GM e garantindo a segregação de responsabilidades entre os órgãos.
A solução contemplará a criação de novos templates de arte (imagens de fundo) para a carteirinha da SETRAN, a parametrização da impressão para selecionar automaticamente o template por órgão (GM x SETRAN), além da validação de acesso baseada em grupos do segurança, com a criação de um grupo especial para a SETRAN. Serão realizados testes funcionais para assegurar que a emissão permaneça consistente, com controle de acesso garantindo que apenas os responsáveis da GM emitam documentos da GM e apenas os responsáveis da SETRAN emitam documentos da SETRAN, preservando o fluxo atual de impressão e usabilidade.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Levantamento de pontos de impacto, definição de estratégia. | 0:00 | 1:00 | 0:00 | 0:00 | 0:00 | **1:00** |
| Criação da arte (layout SETRAN) | - | Melhoria | Produção do fundo frente/verso com título, borda verde, marcas d’água “SETRAN”, caixa de assinatura “DIRETOR DA SETRAN” e brasão oficial. | 0:00 | 0:00 | 6:00 | 0:00 | 0:00 | **6:00** |
| Implementação da lógica JavaScript | - | Melhoria | Ajustar construção do HTML na impressão para escolher automaticamente a arte por órgão. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Atualização dos serviços de backend | - | Melhoria | Retornar dados do documento de acordo com o orgão do funcionário de forma automática. | 0:00 | 0:00 | 4:00 | 0:00 | 0:00 | **4:00** |
| Controle de acesso | - | Melhoria | Criar grupo especial para a SETRAN e validar grupos no backend. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Testes e correções | - | Melhoria | Separação GM e SETRAN, impressão, permissões e revisão visual com arte aprovada | 0:00 | 0:00 | 0:00 | 2:00 | 0:00 | **2:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 1:00 | 5,88% |
| Implementação (75%) | 14:00 | 82,35% |
| Teste (20%) | 2:00 | 11,76% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **17:00** | **100,00%** |
