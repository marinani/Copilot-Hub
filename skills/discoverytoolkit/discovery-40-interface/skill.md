---
name: discovery-40-interface
description: Roteador de skills do grupo discovery-40-interface. Executa catalogação e documentação de telas de UI. DEVE ser executado ANTES do grupo discovery-20-fluxos — os fluxos industriais consomem os TELA-[0-9]*.md gerados aqui.
---

# Skill Router — discovery-40-interface

> **Posição na sequência:** Passo 3 — após `discovery-10-banco`, antes de `discovery-20-fluxos`.
> Os fluxos industriais lêem os `TELA-[0-9]*.md` para preencher Seção 2 (Quem usa), Seção 11 (Integrações) e Seção 14.3 (Rastreabilidade).

## Skills disponíveis

| Skill                       | Descrição resumida                                                              |
|-----------------------------|---------------------------------------------------------------------------------|
| discovery-14-telas-catalogo | Varre o legado e gera/atualiza `TELA-CATALOGO.md` com numeração sequencial      |
| discovery-14-Telas          | Documenta UMA tela por invocação; lê `TELA-CATALOGO.md` para identificar o ID  |

## Fluxo recomendado

Execute **nesta ordem**:

1. **Catálogo** — gera o índice mestre de telas com status:
   ```
   @discovery-40-interface catalogar telas
   ```
   Saída: `TELA-CATALOGO.md`

2. **Documentação individual** — documente uma tela por vez via CLI:
   ```
   @discovery-40-interface documentar TELA-001
   @discovery-40-interface documentar CadastroContribuinte
   ```
   Saída: `TELA-{NNN}-{PascalCase}.md` por tela

## Saídas que alimentam os Fluxos

- `TELA-[0-9]*.md` — telas individuais (`TELA-001-NomeTela.md`, etc.)
- `TELA-CATALOGO.md` — índice geral de telas
- `DISC-02-PERFIS-PERMISSOES.md` — perfis de acesso

---

> Consulte cada skill individual para detalhes de uso, parâmetros e restrições.
