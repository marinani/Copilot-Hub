# Estimativa Bottom-Up: Requisição 691669

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 691669 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 11/3/2026 |

---

## Escopo da Estimativa

A estimativa contempla a implementação de um relatório de solicitações que retornaram do SIAC 156, permitindo ao usuário filtrar, visualizar e exportar solicitações que retornaram ao SIGMU após recusa do cidadão ou avaliador (motivos 2 e 4). A solução inclui: Criação de filtros de pesquisa avançados Listagem paginada das solicitações retornadas Visualização de detalhes da solicitação Exportação de relatórios em PDF e Excel Processamento assíncrono via RabbitMQ Registro de auditoria Melhorias visuais para identificação de solicitações retornadas no sistema. O objetivo é fornecer visibilidade gerencial e operacional sobre recusas de solicitações provenientes do SIAC, permitindo análise de padrões e melhoria dos processos de atendimento.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Relatório de Solicitações Retornadas do SIAC | - | Novo | Implementar tela de relatório que permita filtrar solicitações que retornaram do SIAC 156 por múltiplos critérios como período, regional, intervenção, motivo de retorno, status da solicitação, protocolo e indicação fiscal. A funcionalidade deve validar filtros obrigatórios, aplicar regras de negócio e executar consultas otimizadas no banco retornando apenas solicitações com MotivoSIAC 2 e 4. | 2:00 | 8:00 | 1:00 | 0:00 | 11:00 | **0:00** |
| Listagem Paginada e Navegação para Solicitações | - | Novo | Implementar grid paginada para visualização das solicitações retornadas do SIAC contendo informações como protocolo SIAC, data de retorno, regional, intervenção, motivo de retorno, descrição do motivo e status da solicitação. A listagem deve permitir ordenação, paginação e abertura da solicitação em nova aba conforme lógica de roteamento baseada no status. | 2:00 | 8:00 | 0:45 | 0:00 | 10:45 | **0:00** |
| Exportação de Relatório em PDF | - | Novo | Implementar geração de relatório em PDF contendo as solicitações retornadas do SIAC conforme filtros aplicados, incluindo cabeçalho com logo institucional, data de geração, usuário solicitante e filtros utilizados. O relatório deve apresentar tabela paginada com dados das solicitações e totalizadores por motivo de retorno e regional. | 1:30 | 6:00 | 0:30 | 0:00 | 8:00 | **0:00** |
| Exportação de Relatório em Excel | - | Novo | Implementar geração de relatório em formato Excel contendo todas as solicitações retornadas do SIAC conforme filtros aplicados. A planilha deve conter dados completos das solicitações, incluindo protocolo, datas, regional, intervenção, motivo de retorno, descrição do motivo e status da solicitação, permitindo posterior análise e manipulação dos dados. | 1:30 | 6:00 | 0:30 | 0:00 | 8:00 | **0:00** |
| Processamento Assíncrono de Relatórios | - | Novo | Implementar processamento assíncrono para geração de relatórios utilizando RabbitMQ e MassTransit, garantindo que a geração de arquivos seja executada em background. O processo deve publicar mensagens na fila, processar a geração do relatório via consumer e disponibilizar o arquivo para download após conclusão, notificando o usuário através da central de relatórios. | 1:00 | 4:00 | 0:30 | 0:00 | 5:30 | **0:00** |
| Melhorias de Interface e Visualização de Solicitações Retornadas | - | Melhoria | Implementar melhorias visuais nos grids principais do sistema para destacar solicitações retornadas do SIAC, incluindo ícone indicativo, tooltip informativo e destaque visual da linha. Também deve ser exibida na página de detalhes da solicitação a descrição do motivo de retorno informada pelo cidadão ou avaliador. | 0:30 | 2:00 | 0:15 | 0:00 | 2:45 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 8:30 | 18,48% |
| Arquitetura (40%) | 34:00 | 73,91% |
| Implementação (75%) | 3:30 | 7,61% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 46:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
