---
name: discovery-notebooklm-export
description: Gera (ou regenera) a pasta discovery/notebooklm/ em modo concatenado para NotebookLM. Saida em 5 arquivos tematicos (fundacao, banco, telas, endpoints, fluxos) + indice + manifesto, com copia integral do conteudo-fonte e sem alterar arquivos fora de discovery/notebooklm/.
---

# Discovery - Exportacao Concatenada para NotebookLM

## Objetivo

Gerar um pacote otimizado para upload no NotebookLM com **poucos arquivos grandes**.
O processo deve:

- Concatenar por tema.
- Manter conteudo na integra (sem resumo).
- Preservar rastreabilidade por arquivo de origem.
- Escrever apenas em `discovery/notebooklm/`.

## Escopo e restricoes

- Nao alterar, mover, renomear ou apagar nada fora de `discovery/notebooklm/`.
- Nao sobrescrever historico fora da pasta de destino.
- Nao reescrever conteudo tecnico: apenas agrupar e concatenar.
- Nao introduzir acoplamento por projeto (sem prefixo fixo como `156-` e sem caminho absoluto hardcoded).

## Parametros

| Parametro | Tipo | Default | Descricao |
|---|---|---|---|
| `diretorio_saida` | string | `discovery/notebooklm` | Pasta de saida obrigatoria dentro de `discovery/` |
| `nome_sistema` | string | `Sistema Discovery` | Usado em cabecalhos informativos |
| `sobrescrever_no_destino` | bool | `true` | Permite atualizar apenas arquivos dentro do destino |
| `incluir_manifesto` | bool | `true` | Gera manifesto de rastreabilidade |

## Fontes de entrada

Ler arquivos na raiz de `discovery/` com os padroes:

- `DISC-*.md`
- `DADOS-*.md`
- `TELA-CATALOGO.md`
- `TELA-[0-9]*.md`
- `DISC-05-ENDPOINTS.md`
- `FLUXO-*.md`
- `INT-*.md`
- `SNAP-ARQUITETURA-CONSOLIDADA-*.md` e `SNAP-CONSISTENCIA-CRUZADA-*.md` (opcionais para fundamento)

Excluir:

- `arquivos-legado.txt`
- `arquivos-workspace.txt`
- arquivos temporarios e snapshots de export (`SNAP-NOTEBOOKLM-*`)
- qualquer arquivo dentro de `_historico/` e `_template/`

## Saidas obrigatorias

Gerar em `discovery/notebooklm/`:

1. `00-indice.md`
2. `01-fundacao.md`
3. `02-banco.md`
4. `03-telas.md`
5. `04-endpoints.md`
6. `05-fluxos.md`
7. `99-manifesto.md` (se `incluir_manifesto = true`)

## Regras de concatenacao

- Cada arquivo de saida deve ter blocos separados por:

```markdown
---
## ORIGEM: <nome-do-arquivo-fonte>
---
```

- Copiar cada fonte integralmente (sem cortes e sem sintese).
- Ordem estavel:
  - Catalogos primeiro.
  - Depois arquivos numerados/codificados em ordem crescente.
  - Depois anexos complementares.

## Mapeamento tema -> fontes

- `01-fundacao.md`
  - `DISC-01-*`, `DISC-02-*`, `DISC-03-*`, `DISC-97-*`, `DISC-98-*`, `DISC-99-*`
  - snapshots consolidados opcionais (`SNAP-ARQUITETURA-CONSOLIDADA-*`, `SNAP-CONSISTENCIA-CRUZADA-*`)

- `02-banco.md`
  - `DADOS-*.md`

- `03-telas.md`
  - `TELA-CATALOGO.md`
  - `TELA-[0-9]*.md`

- `04-endpoints.md`
  - `EJB-CATALOGO.md`
  - `EJB-[0-9]*.md` (Session Beans / EJBs do sistema)
  - se existir: `DISC-05-ENDPOINTS.md` ou qualquer `DISC-*` focado em endpoints

- `05-fluxos.md`
  - `FLUXO-*.md`
  - `INT-*.md` ao final (se existir)

## Conteudo de 00-indice.md

O indice deve vir primeiro e conter:

- Objetivo do pacote para NotebookLM.
- Ordem recomendada de upload:
  1. `00-indice.md`
  2. `01-fundacao.md`
  3. `02-banco.md`
  4. `03-telas.md`
  5. `04-endpoints.md`
  6. `05-fluxos.md`
  7. `99-manifesto.md`
- Tabela com tema, arquivo de destino e lista de fontes.
- Contagem de fontes por tema.
- Regras de inclusao/exclusao usadas na exportacao.

## Conteudo de 99-manifesto.md

Manifesto tecnico com:

- Data/hora de geracao.
- Diretorio de origem e destino.
- Lista completa de arquivos de origem usados em cada arquivo concatenado.
- Contagem total de fontes incluidas e ignoradas.
- Confirmacao textual: "Nada fora de discovery/notebooklm foi alterado nesta execucao".

## Checklist de validacao

1. Confirmar que os 6 ou 7 arquivos esperados foram criados em `discovery/notebooklm/`.
2. Confirmar que cada bloco concatenado possui marcador de origem.
3. Validar amostra de conteudo integral em cada tema (sem sintese).
4. Verificar ausencia de alteracoes fora da pasta de destino.
5. Verificar que nao ha referencia hardcoded a projeto especifico.

## Prompt de execucao

```text
Execute a exportacao NotebookLM no modo concatenado por tema.

Parametros:
{
  "diretorio_saida": "discovery/notebooklm",
  "nome_sistema": "Sistema Discovery",
  "sobrescrever_no_destino": true,
  "incluir_manifesto": true
}

Regras:
- Nao alterar nada fora de discovery/notebooklm.
- Copiar conteudo integral por tema com separador de origem.
- Gerar 00-indice, 01-fundacao, 02-banco, 03-telas, 04-endpoints, 05-fluxos e 99-manifesto.
```
