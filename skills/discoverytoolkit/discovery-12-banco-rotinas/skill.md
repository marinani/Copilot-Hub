---
name: discovery-12-banco-rotinas
updated: 2026-03-23

description: |
  Documenta stored procedures, functions, triggers e jobs do sistema com fichas em linguagem natural, explicando o que cada rotina faz, onde é usada no código legado e sugerindo relação com telas e fluxos. Gera dicionário de dados completo (tabelas, campos, tipos, comentários) e permite navegação cruzada entre tabelas, SPs e telas.
---

# Discovery DB Rotinas — Skill Ajustada

## Responsabilidade

- Gerar dicionário de dados: listar todas as tabelas do schema, com campos, tipos e comentários.
- Para cada SP/function/trigger:
  - Explicar em linguagem natural o que faz.
  - Buscar onde é usada no código legado (Java/EJB/etc), listando arquivos e trechos relevantes.
  - Sugerir chamada da skill de tela correspondente, se aplicável.
- Permitir navegação cruzada entre tabelas, SPs e telas.

## Fluxo de trabalho

1. Ler discovery-project.yml para engine, schema, caminhos e stack.
2. Extrair estrutura do banco (tabelas, campos, tipos, comentários).
3. Para cada rotina:
   - Extrair código.
   - Explicar em linguagem natural.
   - Buscar uso no código legado.
   - Relacionar com telas/fluxos.
4. Gerar/atualizar arquivos:
   - discovery/DADOS-05-MAPA-DADOS.md (dicionário de dados)
   - discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md (fichas de rotinas)

## Observações
- Sempre rotular evidências e pendências.
- Integrar com skills de tela e fluxo para rastreabilidade de negócio.
