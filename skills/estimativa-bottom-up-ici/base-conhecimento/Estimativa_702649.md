# Estimativa Bottom-Up: Requisição 702649

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 702649 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 29/4/2026 |

---

## Escopo da Estimativa

Implementação da geração automática do Relatório Geral de Lote no módulo de Fiscalização, contemplando configuração por assunto SUP, parametrização de intervenções, integração com API Parcelamento Solo para consulta de dados do imóvel, aplicação de regras e filtros de geração, composição automática do PDF no padrão da Prefeitura de Curitiba e anexação do relatório ao mesmo trâmite SUP utilizado pelos documentos SIAC 156, incluindo tratamento de falhas e controle administrativo das configurações.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Configuração de Assunto x Relatório de Lote | RF 001 ao RF 004 | Novo | Disponibilizar tela administrativa para configuração dos assuntos SUP responsáveis pela geração automática do Relatório Geral de Lote, permitindo seleção dos tipos de relatório, parametrização de protocolos, controle de permissões e gerenciamento completo dos vínculos. | 3:00 | 6:00 | 2:00 | 0:00 | 11:00 | **0:00** |
| Parametrização da Intervenção para Geração do Relatório | RF 005 | Melhoria | Permitir configurar nas intervenções do módulo de Fiscalização se o Relatório Geral de Lote deverá ser gerado automaticamente durante o fluxo de geração do protocolo SUP. | 0:30 | 1:00 | 0:15 | 0:00 | 1:45 | **0:00** |
| Integração com API Parcelamento Solo | RF 006 ao RF 011 | Novo | Implementar integração automática com a API Parcelamento Solo para consulta dos dados do imóvel, resolução de lote, aplicação de filtros e montagem das informações utilizadas na geração do relatório. | 5:00 | 14:00 | 4:00 | 0:00 | 23:00 | **0:00** |
| Geração e Anexação Automática do Relatório Geral de Lote | RF 012 ao RF 015 | Novo | Gerar automaticamente o PDF do Relatório Geral de Lote no padrão da Prefeitura, realizar anexação automática ao protocolo SUP e garantir tratamento de falhas sem interromper o fluxo principal da vistoria. | 3:15 | 9:00 | 2:00 | 0:00 | 14:15 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 11:45 | 23,50% |
| Arquitetura (40%) | 30:00 | 60,00% |
| Implementação (75%) | 8:15 | 16,50% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 50:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
