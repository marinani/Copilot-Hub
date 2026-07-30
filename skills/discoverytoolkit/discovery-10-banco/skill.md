---
name: discovery-10-banco
description: Roteador de skills do grupo discovery-10-banco. Agrupa as skills de banco de dados do discovery: snapshot de schema, mapeamento de status/enums, documentação de rotinas/SPs e deep-dive em SPs críticas. Execute em pipeline: snapshot → status-mapa → rotinas → sp-aprofundar. Quando o usuário pedir para "executar o banco" ou "executar o discovery banco", execute as quatro skills na sequência abaixo.
---

# discovery-10-banco — Roteador de Skills

Este grupo reúne as skills de banco de dados do discovery:

- discovery-10-banco-snapshot.md
- discovery-11-banco-status-mapa.md
- discovery-12-banco-rotinas.md
- discovery-13-banco-sp-aprofundar.md

## Execução automática em sequência

Quando o usuário pedir para **executar o banco** ou **executar o discovery banco**, execute as skills nesta ordem, uma após a outra, sem pular etapas:

### Passo 1 — Snapshot
Leia e execute integralmente as instruções de `discovery-10-banco-snapshot.md`.
Aguarde a geração do snapshot do schema antes de prosseguir.

### Passo 2 — Status e Enums
Leia e execute integralmente as instruções de `discovery-11-banco-status-mapa.md`.
Aguarde o mapeamento de status e enums antes de prosseguir.

### Passo 3 — Rotinas e SPs
Leia e execute integralmente as instruções de `discovery-12-banco-rotinas.md`.
Aguarde a documentação de rotinas e SPs antes de prosseguir.

### Passo 4 — Deep-dive em SPs críticas
Leia e execute integralmente as instruções de `discovery-13-banco-sp-aprofundar.md`.
Confirme ao usuário a conclusão de cada etapa.

## Como usar manualmente

Você pode executar cada etapa isoladamente ou todas em sequência conforme a necessidade do projeto.
