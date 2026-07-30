# Estimativa Bottom-Up: Requisição 764899

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | Fabiano da Silva Santos |
| **Sistema** | SIGMU Cidades |
| **Órgão** | SMU |
| **Requisição/Ofício** | 764899 |
| **Identificador SGC** | 2158 |
| **Analista Responsável** | Vinícius Alves |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 29/5/2026 |

---

## Escopo da Estimativa

Implementar uma nova estrutura de gestão de multas integrada ao CAF, contemplando o cadastro centralizado de valores de multa reutilizáveis, configuração de multas fixas e variáveis nos modelos de formulário, utilização de novas etiquetas para composição automática dos documentos e adequação do processo de envio de informações ao CAF. A melhoria também contempla o preenchimento de multas variáveis durante a execução das vistorias, manutenção da compatibilidade com modelos já existentes em produção e aprimoramentos de usabilidade na tela de modelos de formulário por meio da otimização do painel de etiquetas e da funcionalidade de cópia rápida de etiquetas para utilização nos documentos.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Cadastro e gerenciamento de Valores de Multa | - | Novo | Implementar cadastro, edição, exclusão e consulta de valores de multa reutilizáveis, incluindo validações de unicidade, bloqueio de exclusão quando houver utilização em modelos ativos e exibição automática do valor por extenso. | 1:00 | 6:00 | 1:00 | 0:00 | 8:00 | **0:00** |
| Integração de valores de multa nos Modelos de Formulário | - | Melhoria | Implementar nova configuração de multas na integração com o CAF, contemplando seleção de multas cadastradas, suporte a multa variável, nova etiqueta de sistema para multa variável, avisos informativos para utilização de etiquetas e garantia de retrocompatibilidade com modelos já existentes em produção. | 4:00 | 10:00 | 2:00 | 0:00 | 16:00 | **0:00** |
| Preenchimento de multa variável na Execução de Vistoria | - | Melhoria | Implementar preenchimento manual de valor de multa pelo fiscal durante a execução da vistoria, incluindo preenchimento automático do valor por extenso, validações obrigatórias e envio correto das informações ao CAF. | 3:00 | 8:00 | 2:00 | 0:00 | 13:00 | **0:00** |
| Melhorias no painel de Etiquetas | - | Melhoria | Implementar barra de rolagem interna no painel de etiquetas e funcionalidade de cópia automática de etiquetas para a área de transferência com feedback visual ao usuário. | 2:00 | 3:00 | 1:00 | 0:00 | 6:00 | **0:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 10:00 | 23,26% |
| Arquitetura (40%) | 27:00 | 62,79% |
| Implementação (75%) | 6:00 | 13,95% |
| Teste (20%) | 0:00 | 0,00% |
| Cientista de Dados (10%) | 43:00 | 100,00% |
| **TOTAL ESTIMADO** | **0:00** | **100,00%** |
