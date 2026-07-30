# Estimativa Bottom-Up: Requisição 597982

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 597982 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 9/10/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo entregar um relatório de escala de horas realizadas no formato “croqui”, semelhante ao sistema anterior, disponível em Excel (com cores e legendas) e em PDF colorido com o cabeçalho oficial e espaço para assinatura da chefia imediata.
A implementação contemplará a consolidação automática das horas realizadas combinando a escala normal e as escalas extraordinárias, gerando uma visão diária por funcionário (matriz funcionário x dias) com marcações padronizadas e aplicação de cores/legendas.
Será criado um novo endpoint de serviço para produzir o dataset do croqui, um gerador de Excel com layout e cores conforme o padrão solicitado, e uma View Razor específica para o PDF integrando o cabeçalho oficial e a área de assinatura. A tela atual de relatórios receberá um botão/opção para emissão do croqui em Excel e PDF.
Testes funcionais validarão a consolidação das horas e a aderência do layout às regras acordadas.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Levantamento de pontos de impacto, definição de estratégia. | 0:00 | 2:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Ajustes no repositório/DTO | - | Melhoria | Revisar para garantir dataset diário com marcações de horas realizadas incluindo extras/afastamentos/faltas; criar/ajustar DTO específico para o croqui. | 0:00 | 0:00 | 6:00 | 0:00 | 0:00 | **6:00** |
| Serviço e ViewModel do relatório | - | Melhoria | Implementar IEscalaService (GerarRelatorioEscalaCroquiRealizadas) que consolida o dataset diário para o layout; mapear para um ViewModel enxuto (funcionário, matrícula, regime, colunas por dia, totais/legendárias). | 0:00 | 0:00 | 6:00 | 0:00 | 0:00 | **6:00** |
| Geração do Excel | - | Melhoria | Implementar gerador Excel com: colunas de dias, faixas de grupo, aplicação de cores/legendas, totais e blocos explicativos de legenda ao final. | 0:00 | 0:00 | 8:00 | 0:00 | 0:00 | **8:00** |
| Geração do PDF | - | Melhoria | Nova View Razor “croqui” (colorida), cabeçalho oficial e área de assinatura, rodapé e metadados. | 0:00 | 0:00 | 8:00 | 0:00 | 0:00 | **8:00** |
| Endpoints/Controller + UI | - | Melhoria | Novos endpoints (/RelatorioEscala/GerarRelatorioCroquiExcel e /RelatorioEscala/GerarRelatorioCroquiPDF), botões na tela de filtro e pequenos ajustes no JS para disparar Excel/PDF conforme seleção. | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Testes e correções | - | Melhoria | Validação com dados reais, conferência de totais/cores/legendas, ajustes de performance e revisão geral. | 0:00 | 0:00 | 0:00 | 3:00 | 0:00 | **3:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 2:00 | 5,56% |
| Implementação (75%) | 31:00 | 86,11% |
| Teste (20%) | 3:00 | 8,33% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **36:00** | **100,00%** |
