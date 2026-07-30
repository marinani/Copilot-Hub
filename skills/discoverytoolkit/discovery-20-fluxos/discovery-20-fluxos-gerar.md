---
name: discovery-20-fluxos-gerar
description: Gera ou refina a documentação completa de um único fluxo a partir do catálogo DISC-03. Lê o fluxo candidato selecionado, documenta um fluxo por invocação e atualiza o status no catálogo.
---

# Skill — discovery-20-fluxos-gerar

**Propósito:** documentar **um fluxo por invocação**, lendo primeiro `DISC-03-CATALOGO-DE-FLUXOS.md` e atualizando o status do CF correspondente.

---

## 1. Pré-requisito

`DISC-03-CATALOGO-DE-FLUXOS.md` deve existir e conter o CF alvo.

Se não existir, orientar explicitamente:

```text
Execute antes a skill discovery-20-fluxos-catalago.
```

---

## 2. Entrada esperada

Receber um identificador do fluxo:

- `CF-001`
- nome do fluxo
- ou `F001` quando já houver associação definida

Ler o catálogo e localizar:

- nome operacional
- origem (`AUTO-BANCO` / `MANUAL-CHAT`)
- confiança
- evidências disponíveis
- prioridade
- status atual

Atualizar o status para `em andamento` antes de começar.

---

## 3. Fontes obrigatórias para documentar

### 3.1 Artefatos de discovery

1. `discovery/DISC-03-CATALOGO-DE-FLUXOS.md` — ficha do CF com tabelas, status e lacunas
2. `discovery/DADOS-05-MAPA-DADOS.md` — colunas, tipos, FKs e comentários das tabelas
3. `discovery/DADOS-06-STATUS-E-TRANSICOES.md` — ciclos de vida e transições de status
4. `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` — functions e procedures relevantes
5. Banco via MCP `postgres-gprev` — consultar dados reais quando necessário

### 3.2 Telas relacionadas — leitura OBRIGATÓRIA

**Regra:** ler todos os arquivos `discovery/TELA-[0-9]*.md` listados na ficha do CF no catálogo.
Se um TELA-NNN estiver listado no CF, **não é opcional** — deve ser lido.

De cada arquivo de tela, extrair obrigatoriamente:

| Campo do arquivo TELA | O que alimenta no documento do fluxo |
|---|---|
| `Java associado` (cabeçalho) | Bean/Action Seam responsável → seção de Integrações e diagrama de sequência |
| **Seção 1 — Objetivo e contexto** | Quando a tela entra no fluxo; pré/pós-condições do passo; navegação de entrada e saída |
| **Seção 2 — Atores e perfis** | Seção "Quem usa o fluxo" (perfis, permissões, restrições de acesso) |
| **Seção 3 — Campos e validações** | Campos obrigatórios, regras de preenchimento, dados de entrada para cenários de teste |
| **Seção 4 — Regras de negócio (RN)** | Regras de negócio do fluxo com referência de origem no código; alimenta a matriz de rastreabilidade |
| **Seção 5 — Fluxo de navegação** | Transições entre telas, ações AJAX, modais de confirmação → diagrama de atividade e de estados |

> **Atenção:** as telas frequentemente revelam regras de negócio invisíveis no banco — parâmetros de sistema, validações de integridade, enums de status, flags de permissão. Tratar as RNs das telas com o mesmo peso das RNs de banco.

Se uma tela listada no CF ainda não foi documentada (status `pendente` no TELA-CATALOGO), registrar como **lacuna de evidência** na seção correspondente do fluxo.

---

## 4. Template obrigatório do fluxo

Gerar `discovery/FLUXO-Fxxx-<slug>.md` com o template industrial já adotado, mas com os reforços abaixo obrigatórios:

### 4.1 Campos adicionais no cabeçalho

- **Origem do fluxo:** `AUTO-BANCO` ou `MANUAL-CHAT`
- **Confiança do mapeamento:** `alta`, `media`, `baixa`, `validada pelo usuário`
- **Validação humana:** quem confirmou e quando, se aplicável
- **Lacunas de evidência:** resumo do que ainda falta confirmar

### 4.2 UML / diagramas obrigatórios

- **Diagrama de atividade** — obrigatório
- **Diagrama de sequência** — obrigatório quando há interação entre tela, serviço, SP ou integração
- **Diagrama de estados** — obrigatório quando houver status

Preferir Mermaid no documento Markdown.

### 4.3 Plano de testes obrigatório

Adicionar seção de `Plano de testes` contendo:

| ID | Cenário | Pré-condição | Dados de teste | Resultado esperado | Evidência |
|---|---|---|---|---|---|

Incluir:

- caso feliz
- variações
- erros e exceções
- integrações
- regressão mínima

### 4.4 Matriz de rastreabilidade obrigatória

Incluir tabela ligando:

`Regra de negócio -> Cenário BDD -> Caso de teste -> Evidência -> Artefato técnico`

---

## 5. Conclusão

Ao concluir:

1. salvar o `FLUXO-Fxxx-<slug>.md`
2. atualizar o status do CF no catálogo para `documentado`
3. registrar pendências reais, sem inventar cobertura

---

## 6. Checklist

- [ ] CF localizado no DISC-03
- [ ] Status marcado como `em andamento`
- [ ] DADOS-05, DADOS-06, DADOS-10 lidos
- [ ] Banco consultado quando necessário (MCP postgres-gprev)
- [ ] Todas as telas listadas no CF lidas (TELA-NNN)
- [ ] Atores e perfis extraídos das telas (Seção 2)
- [ ] Regras de negócio das telas incorporadas ao fluxo (Seção 4)
- [ ] Diagrama de atividade gerado a partir das navegações das telas (Seção 5)
- [ ] Diagrama de sequência gerado com beans/actions identificados
- [ ] Diagrama de estados gerado (quando houver status)
- [ ] Plano de testes gerado com dados reais dos campos (Seção 3)
- [ ] Matriz de rastreabilidade com origem nas RNs das telas
- [ ] Lacunas registradas para telas pendentes não documentadas
- [ ] Documento do fluxo salvo
- [ ] Status marcado como `documentado`
