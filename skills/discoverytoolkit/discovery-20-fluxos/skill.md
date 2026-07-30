---
name: discovery-20-fluxos
description: Roteador de skills do grupo discovery-20-fluxos. Permite executar qualquer uma das funções do grupo (catálogo, fluxo industrial) individualmente ou todas em sequência. PRÉ-REQUISITO: discovery-40-interface (Telas) deve estar executado — os fluxos industriais lêem TELA-[0-9]*.md para preencher perfis, integrações e rastreabilidade. Quando o usuário pedir para "executar os fluxos" ou "executar o discovery fluxos", execute as skills na sequência abaixo.
---

# Skill Router — discovery-20-fluxos

> **Posição na sequência:** Passo 4 — após `discovery-40-interface` (Telas).
> Os fluxos industriais lêem os `TELA-[0-9]*.md` para preencher:
> - Seção 2 (Quem usa) — perfis identificados nas telas
> - Seção 11 (Integrações) — controllers e endpoints das telas
> - Seção 14.3 (Rastreabilidade) — artefatos de tela como referência
> - Diagrama de sequência 5.1 — Interface de entrada vem da tela correspondente

## Skills disponíveis

| Skill                                 | Descrição resumida                                                      |
|---------------------------------------|------------------------------------------------------------------------|
| discovery-20-fluxos-catalago          | Gera o catálogo de fluxos candidatos e pergunta no chat por fluxos faltantes |
| discovery-fluxo-from-cf               | [DEPRECATED] Gera rascunho básico de fluxo a partir de um CF           |
| discovery-20-fluxos-gerar             | Documenta um fluxo por invocação a partir do catálogo consolidado      |

## Execução automática em sequência

Quando o usuário pedir para **executar os fluxos** ou **executar o discovery fluxos**, execute as skills nesta ordem, uma após a outra, sem pular etapas:

### Passo 1 — Catálogo de Fluxos
Leia e execute integralmente as instruções de `discovery-20-fluxos-catalago.md`.
Aguarde a geração de `DISC-03-CATALOGO-DE-FLUXOS.md` e `SNAP-CATALOGO-FLUXOS-VALIDACAO.md` antes de prosseguir.

### Passo 2 — Fluxo Industrial
Leia e execute integralmente as instruções de `discovery-20-fluxos-gerar.md`.
Gere/refine o `FLUXO-Fxxx-<slug>.md` completo, snapshot e atualize o DISC-00.
Confirme ao usuário a conclusão de cada etapa.

> **Lembrete:** Os fluxos industriais lêem `TELA-[0-9]*.md` gerados pelo grupo `discovery-40-interface`. Certifique-se de que as telas já foram executadas antes de iniciar este pipeline.

## Pipeline sugerido

1. **Catálogo de fluxos**: Gera DISC-03-CATALOGO-DE-FLUXOS.md e SNAP-CATALOGO-FLUXOS-VALIDACAO.md
2. **Fluxo industrial**: Gera/refina FLUXO-Fxxx-<slug>.md completo, snapshot e atualiza DISC-00
   - Lê TELA-[0-9]*.md do grupo `discovery-40-interface` para preenchimento das seções de interface

## Como usar manualmente

- Para rodar uma função específica, chame pelo nome da skill desejada.
- Para rodar o pipeline completo, use a instrução: **"executar os fluxos"**.

---

> Consulte cada skill individual para detalhes de uso, parâmetros e restrições.
