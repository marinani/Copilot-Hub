---
name: relatorio-desenvolvedor
description: >
  Gera relatório de tarefas e atividades dos desenvolvedores a partir dos lançamentos de horas no Redmine.
  Salva o resultado em arquivo Markdown na pasta relatorios da raiz do workspace.
  Organiza por colaboradores, projetos, tipos de atividade e matriz colaborador x projeto x atividade.
  Inclui horas estimadas quando existirem e KPIs do período.
      Use quando o usuário escrever "relatório dev", "relatório desenvolvedor", "horas do time", "horas lançadas",
      "relatório de atividades" ou variações similares.
---

# RelatorioDev

## Entrada esperada

```
relatório dev
relatório desenvolvedor
horas do time
horas lançadas em março
relatório de atividades do mês
gere relatório da equipe do projeto X
```

Parâmetros que o usuário pode informar na mesma mensagem:

- **Período**: "em março", "de janeiro a março", "no mês passado", "de 01/02 a 28/02"
- **Desenvolvedor(es)**: "do João", "de mim", "da equipe", ou uma lista de nomes/IDs
- **Projeto**: "do projeto ICI-DOC", "do CSDE DevOps"

> **Regra obrigatória:** o relatório é sempre de **um mês específico**.
> Se o mês não for informado pelo usuário, o agente deve obrigatoriamente perguntar via **handoff**:
> "De qual mês você deseja o relatório? (ex.: março/2026)"

---

## Saída obrigatória em arquivo

- Sempre criar a pasta `relatorios/` na raiz do workspace se não existir.
- Sempre criar/atualizar um arquivo com nome:
  - `relatorios/relatorio-dev-{mes}.md`
- Padrão de `{mes}`:
  - usar `yyyy-mm` (ex.: `2026-03`)
- A geração de `.pdf` é **opcional** e não deve ser tratada como obrigatória na skill.
- O documento deve conter:
  1. **Título**
  2. **Período**
  3. **Índice navegável (sumário)**
  4. **Painel executivo**
  5. **Seção 1: Colaboradores**
  6. **Seção 2: Projetos**
  7. **Seção 3: Tipos de atividade**
  8. **Seção 4: Projeto > Tipo > Colaborador (em subtabelas)**
  9. **Seção 5: Projeto X Tipo X Colaborador (Service Desk, em subtabelas)**
  10. **Seção de KPIs e índices de planejamento**
  11. **Seção de estatísticas de planejamento**
  12. **Observações finais**

---

## Regras inegociáveis

- Sem hardcode de tokens ou credenciais — usar apenas `REDMINE_API_KEY` do ambiente.
- Toda interação com o usuário deve acontecer no **chat integrado** (nunca em `input()` de terminal).
- Textos de saída em **pt-BR**.
- Não instalar novas libs sem decisão explícita — usar apenas a stdlib Python.
- O resultado principal deve ser salvo no arquivo `.md` (não apenas no chat).
- A versão `.pdf` pode ser gerada quando solicitado, mas **não é obrigatória por padrão**.
- Todas as seções de resultado devem estar em **tabelas Markdown**.
- As seções hierárquicas devem usar **subtabelas** para melhorar legibilidade.
- O relatório deve conter **gráficos Mermaid** para visão rápida de distribuição de carga.
- Sempre exibir **horas lançadas**, **horas estimadas** (se existir) e **delta** (`lançadas - estimadas`) quando aplicável.
- Sempre exibir o **total de horas** ao final de cada seção e um **total geral**.
- O relatório deve sempre usar **um único mês de referência** informado pelo usuário.
- Quando o mês não estiver explícito na solicitação, é obrigatório abrir **handoff** e aguardar resposta antes de continuar.
- Se nenhum lançamento for encontrado: exibir mensagem clara e encerrar sem erro.
- A API do Redmine aceita no máximo 100 registros por página — **sempre paginar** quando `total_count > limit`.

---

## PASSO 0 — Verificar pré-requisitos

1. Verificar se `REDMINE_API_KEY` está disponível no ambiente.
   - Se ausente: perguntar ao usuário no chat, persistir via `setx` (Windows) e definir na sessão atual.
2. Verificar se Python está disponível no PATH.
3. Garantir que a pasta `relatorios/` exista na raiz do workspace.
4. Ler `.github/config.yaml` para obter `redmine.project_id` (filtro padrão de projeto, se aplicável).

---

## PASSO 1 — Identificar parâmetros do relatório

A partir da mensagem do usuário, extrair:

| Parâmetro    | Padrão quando ausente       |
| ------------ | --------------------------- |
| `from_date`  | obrigatório (mês informado) |
| `to_date`    | obrigatório (mês informado) |
| `user_scope` | `team` (equipe do projeto)  |
| `project_id` | nenhum (todos os projetos)  |

**Regras de inferência de período:**

| Expressão do usuário    | `from_date`        | `to_date`                  |
| ----------------------- | ------------------ | -------------------------- |
| "em março" / "de março" | `YYYY-03-01`       | `YYYY-03-31`               |
| "no mês passado"        | 1º do mês anterior | último dia do mês anterior |
| "neste mês" / "do mês"  | 1º do mês atual    | último dia do mês atual    |
| "de jan a mar"          | `YYYY-01-01`       | `YYYY-03-31`               |
| "de 01/02 a 28/02"      | `YYYY-02-01`       | `YYYY-02-28`               |
| sem menção de período   | **não permitido**  | **não permitido**          |

**Regras de inferência de usuário:**

| Expressão                                         | Comportamento                                        |
| ------------------------------------------------- | ---------------------------------------------------- |
| "de mim" / "minhas" / "meus"                      | usa apenas usuário autenticado                       |
| "do time" / "da equipe" / "de todos" / sem menção | buscar membros via `/projects/{id}/memberships.json` |
| "do [Nome]"                                       | buscar ID via `/users.json?name=Nome`                |

Se o período ou usuário estiver **ambíguo**, perguntar no chat antes de prosseguir (**GATE**).

### GATE obrigatório — mês não informado

Quando o mês não for informado explicitamente na solicitação:

1. Enviar pergunta no chat usando **handoff**:
   - "De qual mês você deseja o relatório? (ex.: março/2026)"
2. Aguardar a resposta do usuário na próxima mensagem.
3. Só então converter para `from_date` e `to_date` e continuar.

---

## PASSO 2 — Buscar dados (lançadas + estimadas)

Executar script Python para buscar e consolidar dados com as regras abaixo:

1. Buscar `time_entries` com paginação.
2. Coletar IDs únicos de issue dos lançamentos.
3. Para cada issue única, buscar `/issues/{id}.json` e capturar `issue.estimated_hours`.
4. Usar cache em memória para não repetir requisição da mesma issue.
5. Em agregações, considerar:
   - `horas_lancadas`: soma de `time_entry.hours`
   - `horas_estimadas`: soma de `estimated_hours` por issue (somar por grupo sem duplicar issue no mesmo grupo)
   - `delta_horas`: `horas_lancadas - horas_estimadas`

Template mínimo esperado do script:

```python
#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
import urllib.parse
import urllib.request
from collections import defaultdict
from typing import Any, Dict, List, Optional

BASE_URL = os.environ.get("REDMINE_URL", "https://redmine.ici.curitiba.org.br")
API_KEY = os.environ.get("REDMINE_API_KEY", "")

if not API_KEY:
    print(json.dumps({"error": "REDMINE_API_KEY_MISSING"}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(2)


def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    url = urllib.parse.urljoin(BASE_URL, path)
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    req = urllib.request.Request(url)
    req.add_header("X-Redmine-API-Key", API_KEY)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all_time_entries(project_id: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"project_id": project_id, "from": from_date, "to": to_date, "limit": 100, "offset": 0}
    all_entries: List[Dict[str, Any]] = []
    while True:
        data = api_get("/time_entries.json", params)
        entries = data.get("time_entries", [])
        all_entries.extend(entries)
        params["offset"] += len(entries)
        if not entries or len(entries) < 100:
            break
    return all_entries


def fetch_issue_estimates(issue_ids: List[int]) -> Dict[int, float]:
    estimates: Dict[int, float] = {}
    for issue_id in issue_ids:
        try:
            issue_data = api_get(f"/issues/{issue_id}.json")
            issue = issue_data.get("issue", {})
            estimate = issue.get("estimated_hours")
            estimates[issue_id] = float(estimate) if estimate is not None else 0.0
        except Exception:
            estimates[issue_id] = 0.0
    return estimates


def md_table(headers: List[str], rows: List[List[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---:" if i > 0 else "---" for i in range(len(headers))]) + "|"]
    out.extend(["| " + " | ".join(r) + " |" for r in rows])
    return "\n".join(out)


def sum_estimates_for_group(issue_ids: set, estimates: Dict[int, float]) -> float:
    return sum(estimates.get(i, 0.0) for i in issue_ids)


def write_report_file(file_path: Path, content: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


# O restante do script deve montar as 4 seções obrigatórias e salvar em:
# relatorios/relatorio-dev-{yyyy-mm}.md
```

Script auxiliar parametrizável recomendado para formatação final do markdown:

- Caminho: `.github/skills/relatorio-desenvolvedor/scripts/gerar_template_relatorio.py`
- Objetivo: receber dados já consolidados (JSON) e renderizar o template final com índice, gráficos e subtabelas.
- Resultado esperado: sempre criar o artefato principal em `.md`.
- Opcional: criar `.pdf` quando houver solicitação explícita do usuário.
- Parâmetros mínimos:
  - `--output`
  - `--period-start`
  - `--period-end`
- Parâmetros opcionais:
  - `--input` (JSON consolidado)
  - `--project`
  - `--generated-at`

Exemplo de uso:

```bash
python .github/skills/relatorio-desenvolvedor/scripts/gerar_template_relatorio.py \
  --input relatorios/dados-2026-03.json \
  --output relatorios/relatorio-dev-2026-03.md \
  --period-start 01/03/2026 \
  --period-end 31/03/2026 \
  --project Todos

# Arquivos gerados:
# - relatorios/relatorio-dev-2026-03.md
```

Além das agregações já existentes, o script deve montar também:

- uma agregação hierárquica da seção 4 com ordenação por:
  1. Projeto
  2. Tipo de atividade
  3. Colaborador
- uma agregação da seção 5 contendo a classificação da demanda em:
  - `Requisição de Service Desk`
  - `Incidente de Service Desk`
  - `Não classificado`

Critério de classificação para a seção de Service Desk:

1. Se a issue possuir tracker, categoria, assunto ou outro campo textual contendo `incidente`, classificar como `Incidente de Service Desk`.
2. Se possuir tracker, categoria, assunto ou outro campo textual contendo `requisição`, `requisicao`, `solicitação` ou `solicitacao`, classificar como `Requisição de Service Desk`.
3. Se não for possível inferir, classificar como `Não classificado`.
4. Para classificar corretamente, o script pode buscar detalhes adicionais da issue via `/issues/{id}.json` e usar cache em memória.

---

## PASSO 3 — Estrutura obrigatória do arquivo Markdown

O arquivo `relatorios/relatorio-dev-{mes}.md` deve seguir exatamente esta ordem de seções:

````markdown
# Relatório de Atividades dos Desenvolvedores

**Período:** DD/MM/YYYY a DD/MM/YYYY
**Projeto:** Nome do projeto (ou "Todos")
**Gerado em:** DD/MM/YYYY HH:mm

## Índice

- [1) Painel Executivo](#1-painel-executivo)
- [2) Carga Total e Distribuições](#2-carga-total-e-distribuições)
- [3) Colaboradores](#3-colaboradores)
- [4) Projetos](#4-projetos)
- [5) Tipos de atividade](#5-tipos-de-atividade)
- [6) Projeto > Tipo > Colaborador (Subtabelas)](#6-projeto--tipo--colaborador-subtabelas)
- [7) Service Desk (Subtabelas)](#7-service-desk-subtabelas)
- [8) KPIs e Índices de Planejamento](#8-kpis-e-índices-de-planejamento)
- [9) Estatísticas para Planejamento](#9-estatísticas-para-planejamento)
- [10) Observações](#10-observações)

## 1) Painel Executivo

| Indicador Chave | Valor |
| --------------- | ----: |
| ...             |   ... |

## 2) Carga Total e Distribuições

### 2.1 Carga total lançada x estimada

```mermaid
xychart-beta
  title "Carga total: lançadas x estimadas"
  x-axis [Lancadas, Estimadas]
  y-axis "Horas"
  bar [..., ...]
```
````

### 2.2 Distribuição de horas por colaborador

```mermaid
---
config:
  xyChart:
    width: 1400
    height: 900
---
xychart-beta horizontal
  title "Distribuição de horas por colaborador"
  x-axis ["Colaborador A", "Colaborador B", "Colaborador C"]
  y-axis "Horas"
  bar [..., ..., ...]
```

> Regra para 2.2: exibir todos os colaboradores no gráfico (sem agregação em `Outros`).
> Sempre usar `xychart-beta horizontal` com altura configurável para evitar corte de labels.
> Altura recomendada: `height = max(700, 28 * quantidade_de_colaboradores + 220)`.

### 2.3 Distribuição por classificação Service Desk

```mermaid
pie showData
  title Distribuição Service Desk por horas
  "Requisição de Service Desk" : ...
  "Incidente de Service Desk" : ...
  "Não classificado" : ...
```

### 2.4 Distribuição de horas por projeto

```mermaid
xychart-beta
  title "Distribuição de horas por projeto"
  x-axis [P1, P2, P3]
  y-axis "Horas"
  bar [..., ..., ...]
```

**Legenda do gráfico 2.4**

| Código | Projeto   | Horas |
| ------ | --------- | ----: |
| P1     | Projeto A |   ... |
| P2     | Projeto B |   ... |
| P3     | Projeto C |   ... |

> Regra para 2.4: usar labels curtos (`P1...Pn`) no eixo para garantir visibilidade.
> Sempre incluir logo abaixo uma legenda em tabela com o mapeamento `Código -> Projeto -> Horas`.
> Em cenário com muitos projetos, pode usar Top N + `Outros`, mantendo o mesmo padrão de legenda.

## 3) Colaboradores

| Colaborador | Horas Lançadas | Horas Estimadas | Delta (L-E) | Atividades com Horas |
| ----------- | -------------: | --------------: | ----------: | -------------------: |
| ...         |            ... |             ... |         ... |                  ... |

## 4) Projetos

| Projeto | Horas Lançadas | Horas Estimadas | Delta (L-E) | Atividades com Horas |
| ------- | -------------: | --------------: | ----------: | -------------------: |
| ...     |            ... |             ... |         ... |                  ... |

## 5) Tipos de atividade

| Tipo de Atividade | Horas Lançadas | Horas Estimadas | Delta (L-E) | Atividades com Horas |
| ----------------- | -------------: | --------------: | ----------: | -------------------: |
| ...               |            ... |             ... |         ... |                  ... |

## 6) Projeto > Tipo > Colaborador (Subtabelas)

### Projeto: <nome>

#### Tipo: <nome>

| Colaborador        | Horas Lançadas | Horas Estimadas | Delta (L-E) | Atividades com Horas |
| ------------------ | -------------: | --------------: | ----------: | -------------------: |
| ...                |            ... |             ... |         ... |                  ... |
| **Subtotal (...)** |        **...** |         **...** |     **...** |              **...** |

## 7) Service Desk (Subtabelas)

### 7.1 Consolidado por classificação

| Classificação Service Desk | Horas Lançadas | Horas Estimadas | Delta (L-E) | Atividades com Horas |  % sobre SD |
| -------------------------- | -------------: | --------------: | ----------: | -------------------: | ----------: |
| ...                        |            ... |             ... |         ... |                  ... |         ... |
| **Total SD**               |        **...** |         **...** |     **...** |              **...** | **100.00%** |

### Projeto: <nome>

#### Tipo: <nome>

| Colaborador        | Classificação Service Desk | Horas Lançadas | Horas Estimadas | Delta (L-E) | Atividades com Horas |
| ------------------ | -------------------------- | -------------: | --------------: | ----------: | -------------------: |
| ...                | ...                        |            ... |             ... |         ... |                  ... |
| **Subtotal (...)** | -                          |        **...** |         **...** |     **...** |              **...** |

## 8) KPIs e Índices de Planejamento

| KPI                                            |       Valor |
| ---------------------------------------------- | ----------: |
| Total de horas lançadas                        |        ...h |
| Total de horas estimadas                       |        ...h |
| Aderência estimativa (%)                       |        ...% |
| Desvio absoluto (\|L-E\|)                      |        ...h |
| Nº colaboradores ativos                        |         ... |
| Nº projetos ativos                             |         ... |
| Nº tipos de atividade                          |         ... |
| Média de horas por colaborador                 |        ...h |
| Colaborador com maior carga                    | Nome (...h) |
| Projeto com maior carga                        | Nome (...h) |
| Índice de concentração da equipe (top1/total)  |        ...% |
| Índice de concentração de projeto (top1/total) |        ...% |
| Índice de participação de Service Desk (%)     |        ...% |

## 9) Estatísticas para Planejamento

| Estatística                        | Fórmula                               | Resultado |
| ---------------------------------- | ------------------------------------- | --------: |
| Capacidade média semanal da equipe | Horas lançadas / semanas do mês       |       ... |
| Carga média por projeto            | Horas lançadas / projetos ativos      |       ... |
| Carga média por lançamento         | Horas lançadas / lançamentos          |       ... |
| Cobertura de estimativas           | Issues com estimativa / issues totais |       ... |
| Variação relativa de esforço       | (L-E) / E                             |       ... |

## 10) Observações

- Observações objetivas sobre ausência de estimativas, qualidade dos dados e recomendações de ação.

```

---

## PASSO 4 — Exibir resumo no chat

Após salvar o arquivo, exibir no chat:

1. Caminho do arquivo `.md` criado (e do `.pdf`, apenas quando gerado).
2. Período consolidado.
3. Total de horas lançadas e estimadas.
4. Top 3 colaboradores por horas lançadas.
5. Top 3 projetos por horas lançadas.
6. Quantidade de linhas classificadas como requisição/incidente na seção de Service Desk.

---

## PASSO 5 — Regras de cálculo de KPI

Calcular e incluir no documento:

- **Total de horas lançadas** = soma de todas as horas dos lançamentos.
- **Total de horas estimadas** = soma das estimativas das issues únicas do escopo.
- **Aderência estimativa (%)** = `(horas_lancadas / horas_estimadas) * 100`, quando `horas_estimadas > 0`.
- **Desvio absoluto (|L-E|)** = `abs(horas_lancadas - horas_estimadas)`.
- **Média por colaborador** = `horas_lancadas / colaboradores_ativos`.
- **Taxa de atividades administrativas (%)** = `(horas_administrativas / horas_lancadas) * 100` quando houver atividade "Administrativa".

KPIs adicionais recomendados (incluir quando possível):

- Percentual de horas de desenvolvimento.
- Concentração top 3 colaboradores (% das horas totais).
- Concentração top 3 projetos (% das horas totais).

---

## PASSO 6 — Tratamento de ausência de estimativas

Quando uma issue não tiver `estimated_hours`:

- Exibir `0.00` na agregação de estimadas.
- Não remover a linha da tabela.
- Incluir observação no final do relatório:
  - "Observação: parte das issues não possui horas estimadas no Redmine."

---

## PASSO 7 — Regras da seção Projeto X Tipo X Colaborador (Service Desk)

- A seção 5 deve ser construída com o mesmo agrupamento base da seção 4, acrescentando a coluna `Classificação Service Desk`.
- A ordenação da seção 5 deve seguir:
  1. Projeto
  2. Tipo de atividade
  3. Classificação Service Desk
  4. Colaborador
- As classificações válidas são somente:
  - `Requisição de Service Desk`
  - `Incidente de Service Desk`
  - `Não classificado`
- A soma de `Horas Estimadas` deve continuar sem duplicar a mesma issue dentro do mesmo agrupamento.

---

## Formatação de saída (arquivo)

- Usar ponto decimal com 2 casas (`123.45`).
- Tabelas sempre com cabeçalho e alinhamento numérico à direita.
- Ordenar tabelas por `Horas Lançadas` decrescente.
- A coluna `Atividades com Horas` representa contagem de atividades distintas com apontamento no agrupamento.
- Evitar texto longo fora de tabela; usar seção de observações curtas no final quando necessário.
- Não criar outros arquivos além de `relatorios/relatorio-dev-{mes}.md` para o mesmo relatório.

---

## Tratamento de erros

| Situação                     | Ação                                                           |
| ---------------------------- | -------------------------------------------------------------- |
| `REDMINE_API_KEY` ausente    | Perguntar no chat e persistir via `setx`                       |
| Nenhum lançamento encontrado | Criar arquivo com cabeçalho + observação de ausência de dados  |
| Projeto não encontrado       | Perguntar nome exato do projeto no chat                        |
| Erro HTTP 403                | Avisar falta de permissão para consultar horas/usuários/issues |
| Erro HTTP 404                | Validar projeto/usuário/issue informado                        |
| Timeout / erro de rede       | Retentar uma vez; se falhar novamente, exibir erro claro       |
```
