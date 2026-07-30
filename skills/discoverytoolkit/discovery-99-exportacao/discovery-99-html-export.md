---
applyTo: "discovery/**"
---


# Skill: discovery-99-html-export - Exportação HTML Discovery (MkDocs Material + ICI)

## Objetivo

Gerar site HTML navegável, moderno e institucional a partir da documentação em `discovery/`, usando MkDocs Material com identidade visual do ICI.

**Destaques:**
- Tabs por tipo de artefato (Telas, Fluxos, Dados, EJBs)
- Sidebar com acordeon por módulo — **colapsa módulos não ativos** (`navigation.prune`), sem overflow de scroll
- Cada item/tela exibe no menu o valor do campo **Nome** do documento
- **Pesquisa offline** via botão flutuante 🔍 Buscar (canto inferior direito) com atalho `Ctrl+K`; funciona em `file://` sem servidor HTTP; cobertura completa de titulo, módulo e tipo
- **Zoom de diagramas Mermaid** via botão "🔍 Ampliar" injetado em cada diagrama; modal fullscreen com zoom via roda do mouse e drag
- Busca nativa MkDocs Material (PT-BR) disponível quando acessado via HTTP
- Tema visual ICI (azul #003366, laranja #f47920, cinza claro #f4f5f7, branco)
- Logo institucional do ICI

## Pré-requisitos

```powershell
python -m pip install mkdocs mkdocs-material
```

## Execução

```powershell
cd d:\projetos\Gprev-app
python discovery/scripts/gerar-mkdocs.py
```

O script realiza:
1. Varredura dos `.md` em `discovery/`
2. Geração de `discovery/mkdocs.yml` com acordeon por módulo
3. Build para `discovery/html/` com tema e logo ICI

## Saídas esperadas

- `discovery/html/index.html`
- `discovery/mkdocs.yml`
- `discovery/docs_assets/logo.svg` (ICI)
- `discovery/docs_assets/gprev-theme.css` (cores ICI + estilos zoom Mermaid + estilos busca offline)
- `discovery/docs_assets/mermaid-zoom.js` (botão + modal de zoom para diagramas Mermaid)
- `discovery/docs_assets/search-local.js` (painel de busca offline com `window.SEARCH_DATA`)
- `discovery/mkdocs_docs/docs_assets/search-data.js` (gerado automaticamente no build — **não commitar**)

## Verificação

1. Abrir `discovery/html/index.html` em qualquer browser
2. Conferir tabs no topo (Telas, Fluxos, EJBs, etc.)
3. Sidebar mostra módulos **colapsados**; navegar para uma tela expande apenas o módulo corrente
4. Clicar no botão flutuante **🔍 Buscar** (canto inferior direito) ou pressionar `Ctrl+K`
5. Digitar "Atendimento" — resultados aparecem em tempo real com chips de tipo e módulo
6. Abrir uma página de Fluxo (ex.: `FLUXO-F001`) — verificar botão **🔍 Ampliar** ao lado do diagrama Mermaid
7. Clicar no botão → modal fullscreen; zoom via roda do mouse; drag para mover; `Esc` para fechar
8. Busca nativa do MkDocs Material requer servidor HTTP: `python -m http.server 8000 -d discovery/html`

> **Nota:** `search-data.js` é gerado pelo script no build. Não commitar esse arquivo.
> A busca offline cobre títulos, módulos e tipos; a busca nativa MkDocs Material usa índice completo e requer HTTP.

## Atualização

Sempre que houver novos arquivos `.md`:

```powershell
python discovery/scripts/gerar-mkdocs.py
```
