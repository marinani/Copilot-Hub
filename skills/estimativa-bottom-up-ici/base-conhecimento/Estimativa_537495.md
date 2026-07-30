# Estimativa Bottom-Up: Requisição 537495

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 537495 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 8/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo incluir um botão de sincronização manual dos dados cadastrais na tela de funcionários, semelhante ao já existente na tela de afastamentos, com extensão do fluxo para os funcionários da SETRAN. O botão permitirá a atualização manual de dados como setor e lotação oriundos do Meta4 e da api onde constam os dados de funcionários da SETRAN, funcionando como contingência ao serviço automático já existente. O controle de acesso seguirá as permissões já implementadas no sistema, garantindo a segregação entre os grupos GM e SETRAN, com acesso total apenas a administradores.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Sincronização manual de dados cadastrais (GM) | - | Novo | Incluir botão “Sincronizar Meta4” na tela de dados cadastrais do funcionário da GM, com atualização manual de dados do Meta4. | 0:00 | 0:00 | 2:00 | 1:00 | 0:00 | **3:00** |
| Sincronização manual de dados cadastrais (SETRAN) | - | Novo | Incluir botão “Sincronizar API” também na tela dos funcionários da SETRAN, com comportamento idêntico ao da GM. | 0:00 | 0:00 | 2:00 | 1:00 | 0:00 | **3:00** |
| Integração com a API da SETRAN | - | Novo | Integração do sistema com API que armazena os dados de funcionários da SETRAN. | 0:00 | 0:00 | 6:00 | 0:00 | 0:00 | **6:00** |
| Extensão do serviço automático de sincronização para funcionários da SETRAN | - | Novo | Reaproveitar lógica de sincronização automática dos dados cadastrais e afastamentos para também atender os funcionários da SETRAN. | 0:00 | 0:00 | 6:00 | 1:00 | 0:00 | **7:00** |
| Controle de acesso para os botões e dados sincronizados (GM, SETRAN e administradores) | - | Novo | Garantir segregação de acesso aos botões e dados de acordo com o grupo do usuário (GM, SETRAN ou administrador). | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Integração com serviço existente de sincronização | - | Novo | Reutilizar o serviço já existente de sincronização Meta4, adaptando apenas os pontos necessários para novo contexto. | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Validação geral do fluxo (manual + automático) após implementação | - | Novo | Testar comportamento do botão manual e do serviço automático tanto para GM quanto para SETRAN, verificando controle de acesso e atualização de dados. | 0:00 | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 20:00 | 83,33% |
| Teste (20%) | 4:00 | 16,67% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **24:00** | **100,00%** |
