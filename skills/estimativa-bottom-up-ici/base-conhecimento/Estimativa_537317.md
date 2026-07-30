# Estimativa Bottom-Up: Requisição 537317

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 537317 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 11/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo aprimorar o módulo de ocorrência do Sigesguarda Pro, especificamente na funcionalidade de reserva de imagens de câmeras corporais (bodycams). A melhoria prevê que, ao selecionar a opção de “Reservar Imagem”, será obrigatório o preenchimento dos números das bodycams relacionadas à ocorrência, garantindo a correta identificação dos equipamentos.
Adicionalmente, será implementado um novo campo para que o guarda municipal registre o intervalo de tempo (lapso temporal) das imagens a serem preservadas, informando hora inicial e final no formato definido pelo sistema.
Quando a opção de reserva de imagem for acionada, o sistema enviará automaticamente um e-mail de alerta ao setor responsável, contendo informações como número da ocorrência, número(s) das bodycams, intervalo de tempo indicado e demais dados relevantes para a execução da tarefa. O endereço de e-mail de destino será definido em conjunto com o GM responsável e deverá ser parametrizável no sistema.
Essa melhoria visa padronizar e agilizar o processo de solicitação de reserva de imagens, reduzir falhas de comunicação e assegurar que todas as informações necessárias cheguem de forma clara e imediata ao setor encarregado da preservação dos registros.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Definição do email | - | Novo | Validação de regras de obrigatoriedade, formatação do intervalo de tempo e levantamento com GM Wanderson para definir o e-mail de destino e dados obrigatórios no alerta. | 1:00 | 0:00 | 0:00 | 0:00 | 0:00 | **1:00** |
| Revisão do fluxo | - | Novo | Revisão do fluxo atual de reserva de imagem | 1:00 | 0:00 | 0:00 | 0:00 | 0:00 | **1:00** |
| Modelo de dados | - | Novo | Ajuste no modelo de dados para incluir campos de intervalo | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Ajuste de obrigatóriedade dos campos | - | Novo | Ajuste no backend para validar obrigatoriedade dos números das bodycams | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Validação de dados no frontend | - | Novo | Validação obrigatória no frontend | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Alteração na controller | - | Novo | Ajustes no controller para processar e validar dados | 0:00 | 0:00 | 1:00 | 0:00 | 0:00 | **1:00** |
| Envio de email | - | Novo | Implementação do envio de e-mail com template contendo os dados definidos | 0:00 | 0:00 | 3:00 | 0:00 | 0:00 | **3:00** |
| Teste de fluxo completo | - | Novo | Teste funcional do fluxo completo | 0:00 | 0:00 | 0:00 | 1:00 | 0:00 | **1:00** |
| Validação do envio/recebimento de emal | - | Novo | Validação de envio e recebimento do e-mail | 0:00 | 0:00 | 0:00 | 0:30 | 0:00 | **0:30** |
| Teste dos campos obrigatórios | - | Novo | Teste de campos obrigatórios e formato de horário | 0:00 | 0:00 | 0:00 | 0:30 | 0:00 | **0:30** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:00 | 18,18% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 7:00 | 63,64% |
| Teste (20%) | 2:00 | 18,18% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **11:00** | **100,00%** |
