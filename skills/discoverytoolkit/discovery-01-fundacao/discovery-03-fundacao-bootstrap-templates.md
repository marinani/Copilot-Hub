---
name: discovery-03-fundacao-bootstrap-templates
description: Mantém os templates oficiais de discovery em .github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/ como fonte canônica. Opcionalmente instala cópias em discovery/_template/ para revisão humana. É idempotente. Use quando o usuário pedir para instalar/reinstalar templates de discovery em discovery/_template/, ou quando quiser consultar o local canônico dos templates.
---

# Discovery Bootstrap Templates

## Responsabilidade

Manter os templates oficiais de discovery no repositório canônico:

```
.github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/
```

As skills que precisam dos templates leem **diretamente dos assets** — não dependem de `discovery/_template/`. O diretório `discovery/_template/` é apenas uma cópia opcional, útil para revisão humana.

Esta skill é **idempotente**: executá-la múltiplas vezes não destrói nem sobrescreve arquivos que já foram customizados, a menos que o usuário solicite explicitamente uma restauração.

## Arquivos canônicos (assets da skill)

| Arquivo em assets | Descrição |
|---|---|
| `…/assets/FLUXO-TEMPLATE-LEGADO.md` | Template estrutural para fluxos do legado (seções 1–13 + rótulos de confiança) |
| `…/assets/TELA-TEMPLATE-PRINCIPAL.md` | Template para telas **PRINCIPAL** — tela central do fluxo (**13 seções** completas) |
| `…/assets/TELA-TEMPLATE-AUXILIAR.md` | Template para telas **AUXILIAR** — tela de apoio no fluxo (**9 seções**) |
| `…/assets/TELA-TEMPLATE-SEM-FLUXO.md` | Template para telas **SEM-FLUXO** — autodocumentada, sem fluxo associado (**13 seções**) |

## Arquivos opcionalmente instalados em discovery/_template/

| Origem (assets da skill) | Destino em discovery/ | Ação |
|---|---|---|
| `…/assets/FLUXO-TEMPLATE-LEGADO.md` | `discovery/_template/FLUXO-TEMPLATE-LEGADO.md` | Copiar se ausente; atualizar se o usuário solicitar |
| `…/assets/TELA-TEMPLATE-PRINCIPAL.md` | `discovery/_template/TELA-TEMPLATE-PRINCIPAL.md` | Copiar se ausente; atualizar se o usuário solicitar |
| `…/assets/TELA-TEMPLATE-AUXILIAR.md` | `discovery/_template/TELA-TEMPLATE-AUXILIAR.md` | Copiar se ausente; atualizar se o usuário solicitar |
| `…/assets/TELA-TEMPLATE-SEM-FLUXO.md` | `discovery/_template/TELA-TEMPLATE-SEM-FLUXO.md` | Copiar se ausente; atualizar se o usuário solicitar |
| *(gerado pela skill)* | `discovery/_template/README.md` | Criar se ausente; nunca sobrescrever |

## Fluxo de trabalho

### Passo 1 — Verificar existência de discovery/_template/

Verificar se o diretório `discovery/_template/` existe no workspace.

- Se **não existir**: criar o diretório e prosseguir.
- Se **existir**: verificar os arquivos dentro dele e prosseguir apenas onde necessário.

### Passo 2 — Verificar e instalar FLUXO-TEMPLATE-LEGADO.md

Verificar se `discovery/_template/FLUXO-TEMPLATE-LEGADO.md` existe.

**Se não existir:**

Ler o asset canônico:
```
.github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/FLUXO-TEMPLATE-LEGADO.md
```

Criar `discovery/_template/FLUXO-TEMPLATE-LEGADO.md` com o conteúdo lido acima, sem modificações.

Registrar: `[instalado]`.

**Se já existir:**

Não sobrescrever. Registrar: `[já presente — mantido]`.

Exceção: se o usuário usar a palavra-chave **"restaurar template"** ou **"forçar atualização"**, ler novamente o asset e sobrescrever.

### Passo 2-B — Verificar e instalar templates de TELA

Para cada template de tela abaixo, seguir o mesmo padrão do Passo 2:

| Asset canônico | Destino |
|---|---|
| `…/assets/TELA-TEMPLATE-PRINCIPAL.md` | `discovery/_template/TELA-TEMPLATE-PRINCIPAL.md` |
| `…/assets/TELA-TEMPLATE-AUXILIAR.md` | `discovery/_template/TELA-TEMPLATE-AUXILIAR.md` |
| `…/assets/TELA-TEMPLATE-SEM-FLUXO.md` | `discovery/_template/TELA-TEMPLATE-SEM-FLUXO.md` |

Para cada um: copiar se ausente; não sobrescrever se presente; substituir somente com "restaurar template" ou "forçar atualização". Registrar status individual.

### Passo 3 — Verificar e criar discovery/_template/README.md

Verificar se `discovery/_template/README.md` existe.

**Se não existir:** criar com o conteúdo abaixo (verbatim):

```markdown
# discovery/_template — Templates Oficiais de Discovery

## O que é este diretório

Contém os templates canônicos usados pelas skills de discovery do projeto GPrev.
Os arquivos aqui são instalados automaticamente pela skill `discovery - 03 - fundacao - bootstrap-templates`.

## Regras de uso

1. **Nunca editar diretamente** os arquivos deste diretório para criar fluxos reais.
   - Use sempre a skill `discovery-fluxo-from-template` para gerar novos FLUXOs em `discovery/`.
2. **Para restaurar um template** corrompido ou desatualizado:
   - Execute a skill `discovery - 03 - fundacao - bootstrap-templates` com a instrução "restaurar template".
3. **Para adicionar um novo template**:
   - Adicionar o arquivo canônico em `.github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/`.
   - Adicionar a entrada correspondente na skill `discovery - 03 - fundacao - bootstrap-templates`.
   - Executar a skill para instalar em `discovery/_template/`.

## Templates disponíveis

| Arquivo | Descrição | Skill que usa |
|---|---|---|
| `FLUXO-TEMPLATE-LEGADO.md` | Template estrutural para fluxos do sistema legado GPrev (seções 1–13 + rótulos de confiança) | `discovery-fluxo-from-template`, `discovery-fluxo-from-cf`, `discovery-20-fluxos-gerar` |

## Fonte canônica

**Os templates canônicos ficam em:**
```
.github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/
```

As skills leem os templates **diretamente dos assets** — este diretório é apenas uma cópia para revisão humana.
Nunca edite os arquivos aqui como template permanente. Edições devem ir para o asset em `.github/skill/discoverytoolkit/`.
```

**Se já existir:** não sobrescrever. Registrar: `[já presente — mantido]`.

### Passo 4 — Reportar resultado

Ao final, informar ao usuário:

```
Bootstrap concluído:
- discovery/_template/FLUXO-TEMPLATE-LEGADO.md         → [instalado | já presente — mantido]
- discovery/_template/TELA-TEMPLATE-PRINCIPAL.md       → [instalado | já presente — mantido]
- discovery/_template/TELA-TEMPLATE-AUXILIAR.md        → [instalado | já presente — mantido]
- discovery/_template/TELA-TEMPLATE-SEM-FLUXO.md       → [instalado | já presente — mantido]
- discovery/_template/README.md                        → [instalado | já presente — mantido]
```

Se alguma ação foi necessária, confirmar que o diretório está pronto para uso pela skill `discovery-fluxo-from-template`.

## Regras de idempotência

| Condição | Ação |
|---|---|
| Arquivo não existe | Instalar do asset |
| Arquivo existe, sem flag de força | Manter — não sobrescrever |
| Arquivo existe + "restaurar template" | Sobrescrever com o asset canônico |
| Diretório não existe | Criar antes de instalar arquivos |

## Restrições

- Nunca criar arquivos fora de `discovery/_template/` nesta skill.
- Nunca modificar os assets em `.github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/` durante a instalação.
- Nunca inventar conteúdo — o template instalado deve ser idêntico ao asset canônico.
- Esta skill não registra nada no `DISC-00-INDICE.md` — o diretório `_template/` é infraestrutura, não documento de discovery.
- **As skills de geração de FLUXOs e TELAs leem os templates diretamente dos assets (`SKILL.md` delas aponta para `.github/skill/discoverytoolkit/discovery - 03 - fundacao - bootstrap-templates/assets/`). Esta skill apenas cria cópias de revisão em `discovery/_template/`.**

## Referências adicionais

- Para contexto de arquivos existentes no discovery, ver [references/REFERENCE.md](references/REFERENCE.md)




