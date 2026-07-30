# Estimativa Bottom-Up: Requisição 638542

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 638542 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 29/1/2026 |

---

## Escopo da Estimativa

Implementação de um sistema de notificação em tempo real para despacho de ocorrências, incluindo: criação de serviço para consulta dinâmica de ocorrências pendentes por setor, desenvolvimento de SignalR Hub para comunicação bidirecional, integração com fluxo de despacho existente, construção de interface visual com toast notifications no topo da tela com efeito intermitente, implementação de cliente JavaScript para gerenciamento de notificações e sincronização de estado, integração de áudio para alertas sonoros, testes de integração e concorrência para validar múltiplos usuários simultâneos, e documentação completa do sistema.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|
| Análise e Planejamento | - | Novo | Analisar fluxo de despacho existente, definir queries de pendências, arquitetura de estado, documentar casos de uso. | 3:00 | 0:00 | 0:00 | 0:00 | **3:00** |
| Criar Interface IOcorrenciaPendenteService | - | Novo | Definir contrato do serviço, DTO, validações | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Implementar OcorrenciaPendenteService | - | Novo | Lógica de query para pendências, otimização de BD, testes de performance | 0:00 | 2:30 | 0:00 | 0:00 | **2:30** |
| Criar SignalR Hub | - | Novo | Gerenciar conexões, autenticação, grupos por setor, métodos de listener, tratamento de erros | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Integrar com DespachoService | - | Novo | Injetar dependências, chamar serviço de pendências, enviar notificações atualizadas ao grupo | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Integrar com RegistroAtendimentoService | - | Novo | Chamar notificação ao registrar despacho inicial | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Criar Frontend - Container e Toast | - | Novo | HTML/CSS do container fixo no topo, componente toast reutilizável, animations (slide + piscante) | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Implementar JavaScript Cliente - Conexão | - | Novo | Conectar ao Hub, handle de reconexão, logs | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Implementar JavaScript Cliente - Listeners | - | Novo | Implementar todos os listeners (OcorrenciasPendentes, TodasOcorrenciasResolvidas, etc), sincronização de estado | 0:00 | 2:30 | 0:00 | 0:00 | **2:30** |
| Implementar JavaScript Cliente - Gerenciamento de Notificações | - | Novo | Map de notificações, adicionar/remover dinamicamente, evitar duplicatas, show/hide do container | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Sistema de Áudio | - | Novo | Integrar sound library (Howler.js ou Web Audio API), permitir mute, testar em navegadores | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Registrar Dependências em Startup | - | Novo | Injetar IOcorrenciaPendenteService, verificar CORS, validar configurações SignalR | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Testes Unitários - Backend | - | Novo | Testar OcorrenciaPendenteService com diferentes cenários, testes de BD | 0:00 | 0:00 | 3:00 | 0:00 | **3:00** |
| Testes Integração - SignalR | - | Novo | Testar conexão/desconexão, múltiplos usuarios, envio de mensagens, grupos | 0:00 | 0:00 | 4:00 | 0:00 | **4:00** |
| Testes E2E - Fluxo Completo | - | Novo | Testar: conectar, receber pendências, despachar, atualizar, remover, desconectar | 0:00 | 0:00 | 3:00 | 0:00 | **3:00** |
| Testes de Concorrência | - | Novo | Testar múltiplos usuarios despachando simultâneamente, race conditions, ordem de mensagens | 0:00 | 0:00 | 2:30 | 0:00 | **2:30** |
| Debugging e Ajustes de Performance | - | Novo | Investigar lentidão de queries, otimizar conexões SignalR, verificar memory leaks | 0:00 | 0:00 | 3:00 | 0:00 | **3:00** |
| Refinamentos de UX | - | Novo | Ajustar timing de animations, cores, posicionamento, responsividade mobile | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Documentação | - | Novo | Documentar serviço, Hub, cliente JavaScript, guia de configuração, exemplos de uso | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 3:00 | 6,90% |
| Implementação (75%) | 25:00 | 57,47% |
| Teste (20%) | 15:30 | 35,63% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **43:30** | **100,00%** |
