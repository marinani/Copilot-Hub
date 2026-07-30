# Base de Conhecimento — Estimativa Bottom-Up

Este diretório armazena o **histórico de estimativas anteriores** realizadas para o Sigesguarda Pro. Serve como base de referência para calibrar novas estimativas e identificar padrões de esforço em demandas similares.

## Objetivo

Manter um repositório central de estimativas passadas para:

- **Aumentar precisão**: usar dados reais de estimativas anteriores como referência
- **Identificar padrões**: reconhecer tipos de tarefa similares (CRUD, integração, relatório, etc.)
- **Reduzir variabilidade**: evitar sub ou superestimação ao comparar com casos semelhantes
- **Documentar aprendizados**: registrar complexidades específicas do sistema e integrações

## Que Arquivos Salvar Aqui

### 1. **Estimativas Realizadas** (Obrigatório)

Salve aqui arquivos markdown (`.md`) com o resultado final de cada estimativa realizada, seguindo o padrão:

**Nomenclatura**: `ESTIMATIVA-DESCRICAO-DATA.md`

**Exemplo**:
- `ESTIMATIVA-Integracao-Sefaz-2026-05.md`
- `ESTIMATIVA-Relatorio-Financeiro-2026-03.md`
- `ESTIMATIVA-Migração-BD-PostgreSQL-2026-02.md`

### 2. **Conteúdo de Cada Arquivo**

Cada arquivo deve incluir:

```markdown
# Estimativa: [Nome da Demanda]

**Data**: DD/MM/YYYY
**Redmine**: #[número] (se houver)
**Status**: [Concluída | Em Andamento | Cancelada]

## Escopo

Breve descrição da solicitação.

## Premissas

- Premissa 1
- Premissa 2
- Premissa 3

## Decomposição de Funcionalidades

| # | Funcionalidade | Tipo | Engenharia (h) | Implementação (h) | Teste (h) | Homolog. (h) | **Total (h)** |
|---|---|---|---|---|---|---|---|
| 1 | [Nome] | Novo/Melhoria | X | Y | Z | W | **Total** |

## Resumo de Horas

- **Engenharia de Requisitos**: X horas (00%)
- **Implementação**: Y horas (00%)
- **Teste**: Z horas (00%)
- **Homologação/Implantação**: W horas (00%)
- **TOTAL**: XXX horas

## Fatores de Complexidade Aplicados

- [Fator]: [Justificativa] → +[%]

## Referências Consultadas

- Estimativa anterior similiar: `ESTIMATIVA-XXX.md`
- Documentação de discovery: TELA-T0XX, FLUXO-F0XX, etc.

## Observações

Anotações adicionais sobre a estimativa, riscos identificados, etc.
```

### 3. **Documentos de Apoio** (Opcional)

Você também pode salvar:

- **Análises técnicas**: detalhes de complexidade descobertos durante a análise
- **Planilhas estruturadas**: versões em Markdown de estimativas em Excel quando necessário
- **Comparações**: análises que comparem estimativas similares para justificar variações

**Exemplo de nomes**:
- `ANALISE-IMPACTO-Integracao-Sefaz.md`
- `COMPARACAO-CRUD-Estimativas.md`

## Estrutura Recomendada

```
base-conhecimento/
├── README.md                           (este arquivo)
├── ESTIMATIVA-Integracao-Sefaz-2026-05.md
├── ESTIMATIVA-Relatorio-Financeiro-2026-03.md
├── ESTIMATIVA-Migração-BD-PostgreSQL-2026-02.md
├── ANALISE-IMPACTO-Autenticacao-JWT.md
└── COMPARACAO-CRUD-Estimativas.md
```

## Como Usar Estes Arquivos

Ao realizar uma nova estimativa, siga este processo:

1. **Leia o escopo** da demanda
2. **Consulte este diretório** procurando por estimativas com escopo similar
3. **Compare funcionalidades** e horas estimadas em casos parecidos
4. **Ajuste** baseado em particularidades da nova demanda
5. **Documente** qual arquivo histórico foi usado como referência
6. **Salve a nova estimativa** aqui ao concluir

## Padrões Calibrados

Conforme novas estimativas forem realizadas, este documento será atualizado com padrões de esforço identificados:

### Atividades Típicas (em revisão)

- **CRUD simples**: [a definir]
- **Integração externa (API REST)**: [a definir]
- **Relatório com filtros**: [a definir]
- **Autenticação/Autorização**: [a definir]
- **Migration de dados**: [a definir]

---

**Última atualização**: Junho de 2026
