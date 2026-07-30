# Estimativa Bottom-Up: Requisição 667044

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 667044 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 2/2/2026 |

---

## Escopo da Estimativa

Implementar a anexação opcional de arquivos na Etapa 4 da vistoria, com validação de formatos, preservação do nome original e envio automático e isolado ao SUP apenas nos cenários de criação ou trâmite de processo, sem impacto no fluxo operacional.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Disponibilizar componente de anexação na Etapa 4 | - | Melhoria | Disponibilizar, na Etapa 4 – Protocolo da vistoria, um componente de upload de arquivos alinhado ao padrão visual e funcional já utilizado no cadastro de solicitações, permitindo anexação simples ou múltipla dentro do limite definido. | 2:00 | 8:00 | 1:40 | 0:00 | 11:40 | **0:00** |
| Validar tipos de arquivos permitidos | - | Melhoria | O sistema deve aceitar exclusivamente arquivos nos formatos JPG, JPEG, PDF e TIFF (case-insensitive), rejeitando automaticamente extensões inválidas com feedback claro ao usuário. | 0:10 | 1:00 | 0:10 | 0:00 | 1:20 | **0:00** |
| Realizar envio condicional dos anexos ao SUP | - | Melhoria | Os anexos devem ser enviados automaticamente ao SUP apenas nos cenários de criação de novo processo ou trâmite/juntada de vistoria em processo existente, sempre vinculados à vistoria corrente. | 0:10 | 1:00 | 0:10 | 0:00 | 1:20 | **0:00** |
| Garantir anexação opcional sem bloqueio do fluxo | - | Melhoria | A anexação de arquivos deve ser opcional, não impactando o fluxo da vistoria nem o habilitamento do botão de prosseguir, mesmo na ausência de anexos. | 0:10 | 1:00 | 0:10 | 0:00 | 1:20 | **0:00** |
| Isolar anexos por vistoria | - | Melhoria | O sistema deve garantir o isolamento dos anexos por vistoria, impedindo reutilização entre vistorias distintas e assegurando que apenas os arquivos da vistoria atual sejam enviados ao SUP. | 0:10 | 1:00 | 0:10 | 0:00 | 1:20 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:40 | 15,69% |
| Arquitetura (40%) | 12:00 | 70,59% |
| Implementação (75%) | 2:20 | 13,73% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 17:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
