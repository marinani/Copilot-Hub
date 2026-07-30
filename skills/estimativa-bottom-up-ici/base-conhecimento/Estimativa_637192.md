# Estimativa Bottom-Up: Requisição 637192

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 637192 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 4/12/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo incluir as armas habilitadas de cada Guarda Municipal (GM) nos relatórios de funcionários do Sigesguarda Pro, tanto no formato PDF quanto no formato Excel (CSV).
A implementação desta melhoria é fundamental para atender a necessidade do cliente de visualizar, de forma consolidada, quais armas cada funcionário está habilitado a portar, informação atualmente cadastrada na aba "Porte de Arma" do cadastro de funcionários.
A solução contemplará a modificação do ViewModel de relatório para incluir os campos de armas habilitadas, adaptação da query de busca no método FiltroRelatorio para carregar os dados de ArmasPorteDeArma associados a cada funcionário, alteração da exportação CSV para adicionar colunas individuais para cada tipo de arma (Carabina, Dispositivo Elétrico Incapacitante, Espingarda, Fuzil, CTT .40, Pistola e Revólver) conforme solicitado pelo cliente, e modificação da View Razor do PDF para exibir a lista de armas habilitadas de cada funcionário.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Análise e planejamento | - | Melhoria | Mapear arquivos envolvidos, entender estrutura de dados ArmasPorteDeArma, verificar relacionamento com Funcionário e analisar impacto nas consultas existentes. | 0:00 | 0:30 | 0:00 | 0:00 | 0:00 | **0:30** |
| Atualização da ViewModel | - | Melhoria | Adicionar propriedades para as armas habilitadas (uma para lista consolidada e uma para cada tipo de arma individual) no RegistroFuncionarioRelatorioViewModel. | 0:00 | 0:00 | 0:30 | 0:00 | 0:00 | **0:30** |
| Atualização do Serviço | - | Melhoria | Modificar método FiltroRelatorio no FuncionarioService.cs para incluir Include da entidade ArmasPorteDeArma e mapear os valores para o ViewModel. | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Atualização da exportação Excel/CSV | - | Melhoria | Modificar método ExportarArquivoCSV para adicionar colunas separadas para cada tipo de arma (Sim/Não): Carabina, DEI, Espingarda, Fuzil, CTT .40, Pistola, Revólver | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Atualização do relatório PDF | - | Melhoria | Adicionar seção na View ImprimirRelatorioFuncionario.cshtml para exibir as armas habilitadas de cada funcionário. | 0:00 | 0:00 | 1:30 | 0:00 | 0:00 | **1:30** |
| Testes e validações | - | Melhoria | Testar a exportação CSV com diferentes cenários (funcionários com/sem armas), validar layout do PDF, verificar performance da consulta com Include adicional. | 0:00 | 0:00 | 0:00 | 1:30 | 0:00 | **1:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 0:00 | 0,00% |
| Arquitetura (40%) | 0:30 | 8,33% |
| Implementação (75%) | 4:00 | 66,67% |
| Teste (20%) | 1:30 | 25,00% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **6:00** | **100,00%** |
