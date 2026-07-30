---
name: uc-generator
description: >
  Gera documentos de User Case (UC) a partir de transcrições de reuniões ou documentos escritos,
  seguindo o padrão SDD do projeto. Use esta skill sempre que o usuário mencionar:
  "criar UC", "gerar user case", "documentar reunião", "higienizar transcrição",
  "gerar UC a partir de", "documentar levantamento".
  A skill conduz 5 fases obrigatórias em sequência: higienização → classificação de tópicos →
  confirmação do usuário → salvamento do documento higienizado → geração e salvamento da UC.
  Não pule fases. Sempre aguarde a resposta do usuário antes de avançar para a próxima fase.
---

# UC Generator — Gerador de User Cases (SDD)

Skill para gerar documentos de **User Case (UC)** a partir de:

- **Transcrição de reunião** (texto bruto, com ruídos, falas informais, assuntos paralelos)
- **Documento escrito** (já estruturado, mas pode precisar de lapidação)

Conduza **obrigatoriamente** as 5 fases abaixo, em ordem, aguardando resposta do usuário quando indicado.

---

## Antes de começar

Leia o contexto do sistema em `AGENTS.md` (raiz do repositório). Esse arquivo descreve os módulos, domínios de negócio, glossário e **destino canônico de salvamento** — use para distinguir o que é relevante para documentação UC versus ruído de reunião.

Se o arquivo não existir ou estiver em branco, prossiga com bom senso e pergunte ao usuário sobre o módulo/contexto quando necessário.

### Destino de salvamento

Antes das Fases 4 e 5, determine onde salvar cada artefato:

| Artefato                       | Destino padrão (`AGENTS.md`) |
| ------------------------------ | ---------------------------- |
| Documento higienizado (Fase 4) | `refinamentos/`              |
| User Case (Fase 5)             | `UC/`                        |

Ordem de resolução do destino:

1. Leia `AGENTS.md` e use os caminhos definidos em **"Fonte canônica para escrita de User Cases (UC)"**.
2. Se o usuário indicar outro caminho na conversa, use o caminho informado pelo usuário.
3. Se **não** houver destino definido no `AGENTS.md` **nem** informado pelo usuário, **pare e pergunte** onde salvar antes de gravar qualquer arquivo. Aguarde a resposta antes de prosseguir.
4. **Nunca** salve em caminhos genéricos de sandbox (ex.: `/mnt/user-data/outputs/`).

Após salvar, informe no chat os caminhos completos dos arquivos criados.

---

## FASE 1 — Higienização

**Objetivo:** Transformar o texto bruto em um documento limpo e coerente.

### Se a fonte for **transcrição de reunião**:

Aplique as seguintes transformações:

1. **Remover ruídos:** risadas, "ééé", "hmmm", "né", repetições, palavras de preenchimento
2. **Normalizar falas:** manter a essência do que foi dito, em português formal
3. **Identificar participantes:** se houver labels como "Fulano:" ou "P1:", preserve-os de forma consistente
4. **Organizar cronologicamente:** respeitar a ordem temporal da conversa
5. **Separar assuntos:** inserir marcadores `### [Assunto identificado]` sempre que o tema mudar
6. **Não interpretar ainda:** nesta fase apenas limpe — não resuma nem tire conclusões

### Se a fonte for **documento escrito**:

1. **Corrigir ortografia e gramática**
2. **Padronizar formatação** (títulos, listas, tabelas)
3. **Remover redundâncias** óbvias
4. **Não alterar conteúdo** — apenas lapide a forma

### Saída da Fase 1

Apresente o documento higienizado **no chat** com o cabeçalho:

```
## 📄 Documento Higienizado
*Fonte: [Transcrição de reunião / Documento escrito] — [data se disponível]*
```

Depois do documento, avance **automaticamente** para a Fase 2.

---

## FASE 2 — Classificação de Conteúdo

**Objetivo:** Identificar e listar todos os tópicos encontrados no documento higienizado, classificando sua relevância para documentação de UC.

### Como classificar

Use o contexto de `AGENTS.md` para julgar relevância. Classifique cada tópico em:

| Categoria         | Descrição                                                             |
| ----------------- | --------------------------------------------------------------------- |
| ✅ **Funcional**  | Comportamento do sistema, fluxo de tela, regra de negócio, integração |
| ⚙️ **Técnico**    | Decisão de arquitetura, tecnologia, infraestrutura                    |
| 🔄 **Processo**   | Fluxo de trabalho, etapas operacionais, responsáveis                  |
| 💬 **Contextual** | Histórico, motivação, referência a sistemas legados                   |
| 🚫 **Ruído**      | Assuntos paralelos, piadas, logística de reunião, off-topic           |

### Saída da Fase 2

Liste os tópicos numerados, com título curto, categoria e breve descrição do que foi abordado:

```
## 🗂️ Tópicos Identificados

| # | Tópico | Categoria | Resumo |
|---|--------|-----------|--------|
| 1 | Nome do tópico | ✅ Funcional | O que foi discutido em 1-2 linhas |
| 2 | ... | 🚫 Ruído | ... |
```

Depois da tabela, avance **automaticamente** para a Fase 3.

---

## FASE 3 — Solicitar o que Documentar

**Objetivo:** Apresentar os tópicos ao usuário e perguntar o que deve ser descartado antes de gerar a UC.

### Como apresentar

Após a tabela da Fase 2, pergunte ao usuário quais tópicos devem ser **descartados** da UC:

- Liste cada tópico identificado no formato: `#N — [Nome do tópico]`
- Inclua sempre a opção: `Nenhum — manter todos os tópicos`
- Use a ferramenta `AskQuestion` (multi_select) quando disponível; caso contrário, apresente a lista numerada no chat e aguarde resposta

**Aguarde a resposta do usuário antes de prosseguir.**

Quando o usuário responder:

- Se selecionou "Nenhum — manter todos os tópicos": use todos os tópicos classificados como não-ruído
- Se selecionou tópicos para descartar: remova-os da lista de trabalho
- Confirme no chat: `"✅ Tópicos retidos para a UC: [lista]. Gerando documentos..."`

Então avance para as Fases 4 e 5.

---

## FASE 4 — Salvar Documento Higienizado

**Objetivo:** Persistir o documento limpo da Fase 1 (íntegro, sem descartes — este é o registro histórico).

### Destino

Salve em `refinamentos/` conforme **"Fonte canônica para escrita de User Cases (UC)"** em `AGENTS.md`.

Se o destino ainda não estiver definido, **pare e pergunte ao usuário** antes de gravar.

### Nome do arquivo

Use o padrão: `higienizado-[slug-do-assunto]-[YYYYMMDD].md`

Exemplos:

- `refinamentos/higienizado-reuniao-atendimento-solicitacoes-20240315.md`
- `refinamentos/higienizado-levantamento-tramitacao-20240320.md`

Se não houver data disponível, use a data atual.

### Cabeçalho do arquivo

```markdown
# Documento Higienizado — [Título do assunto]

**Fonte original:** [Transcrição de reunião / Documento escrito]
**Data da fonte:** [data ou "não informada"]
**Gerado em:** [data atual]
**Tópicos identificados:** [N tópicos]
**Tópicos descartados na UC:** [lista dos descartados, ou "nenhum"]

---

[conteúdo higienizado completo aqui]
```

Informe no chat o caminho completo do arquivo salvo.

---

## FASE 5 — Gerar e Salvar a UC

**Objetivo:** Criar o documento de User Case preenchido com base nos tópicos retidos.

### Destino

Salve em `UC/` conforme **"Fonte canônica para escrita de User Cases (UC)"** em `AGENTS.md`.

Se o destino ainda não estiver definido, **pare e pergunte ao usuário** antes de gravar.

Antes de atribuir numeração, liste os arquivos `UC-*.md` existentes em `UC/` para evitar duplicidade.

### Template

Leia o template em `assets/TEMPLATE-UC.md` e preencha cada seção:

**Cabeçalho:**

- `UC-XXX`: use o próximo número sequencial disponível em `UC/` ou pergunte ao usuário se já existe uma numeração
- `Módulo`: infira do contexto ou deixe `(a definir)`
- `Fonte`: preencha com tipo e data da reunião/documento

**Seção 1 — Contexto de Negócio:**

- Sintetize o objetivo do que foi discutido em linguagem To-Be (o que o sistema deve fazer)
- Sem menção ao legado

**Seção 2 — Regras de Negócio:**

- Extraia afirmações do tipo "o sistema deve...", "sempre que...", "não é permitido..."
- Numere como `RN-001-01`, `RN-001-02`, etc.

**Seção 3 — Estrutura UX e Navegação:**

- Preencha apenas o que foi mencionado; deixe em branco o que não há informação
- Jornada do usuário: extraia sequências de ações/resultados mencionados
- Telas: liste telas ou módulos citados
- Campos: liste campos discutidos com tipo e obrigatoriedade quando mencionados

**Seção 4 — Critérios de Aceite Macro:**

- Derive critérios objetivos a partir das regras e fluxos identificados
- Formato: "Dado que... quando... então..."

**Seção 5 — Rastreabilidade:**

- UCs relacionados: preencha se mencionados; caso contrário, deixe vazio
- Módulos impactados: use o contexto de `AGENTS.md`

**Seção 6 — Dúvidas e Checklist:**

- Liste pontos não resolvidos na reunião, ambiguidades ou pendências identificadas

### Nome do arquivo UC

Use o padrão: `UC-[numero]-[slug-do-assunto].md`

Exemplos:

- `UC/UC-001-atendimento-nova-solicitacao.md`
- `UC/UC-042-tramitacao-redistribuicao.md`

Informe no chat os caminhos completos dos arquivos salvos (higienizado + UC).

---

## Fluxo resumido

```
INPUT (transcrição ou documento)
        ↓
[FASE 1] Higienizar → exibir no chat
        ↓
[FASE 2] Classificar tópicos → exibir tabela
        ↓
[FASE 3] Perguntar o que descartar → aguardar usuário
        ↓ (resposta do usuário)
[PRÉ-FASE 4/5] Confirmar destinos (higienizado → refinamentos/; UC → UC/; senão, perguntar)
        ↓
[FASE 4] Salvar higienizado íntegro em refinamentos/
[FASE 5] Gerar UC com tópicos retidos em UC/
```

---

## Regras gerais

- **Nunca pule fases.** A higienização sempre precede a classificação.
- **Nunca invente informação.** Se algo não foi mencionado, deixe o campo do template como `(a definir)` ou em branco.
- **Preserve a intenção.** Ao higienizar, não altere o sentido do que foi dito — apenas a forma.
- **Ruído não vai para a UC.** Tópicos 🚫 nunca devem alimentar o documento final, mesmo que o usuário não os descarte manualmente.
- **Documento higienizado é íntegro.** Salve o documento completo, independente dos descartes da UC.
- **Nomenclatura UC, não UC.** O documento segue o template, mas o termo é sempre "User Case" ou "UC".
- **Destinos obrigatórios.** Documento higienizado em `refinamentos/`; User Case em `UC/` — conforme `AGENTS.md`. Se não houver destino definido, pergunte ao usuário antes de gravar.
- **Precedência.** Em conflito entre esta skill e `AGENTS.md`, prevalece `AGENTS.md`.
