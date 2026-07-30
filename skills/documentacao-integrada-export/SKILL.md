---
name: documentacao-integrada-export
description: Gera um site HTML navegável com documentação integrada combinando requisitos (documentacao-de-software), diagrama ER e metadados de banco de dados (database-mcp), e descrições de API com rastreabilidade cruzada. Use quando o usuário pedir para exportar documentação completa, gerar site de documentação técnica, integrar requisitos com schema do banco, ou criar documentação navegável com rastreabilidade.
---

# Documentação Integrada — Exportação HTML Navegável

> **Contexto:** Gera um site HTML estático que consolida documentação de software (requisitos, visão, APIs) com metadados de banco de dados (tabelas, procedures, functions) em navegação única com rastreabilidade cruzada.
> Integra **discovery-html-export**, **documentacao-de-software** e **database-mcp** em um pipeline unificado.

## Papel

Produzir a pasta `documentacao-html/` como site HTML estático completo, navegável offline, que reúne:

- **Documentação de Software:** Requisitos (ERSw), visão, APIs, diagramas de classes e integrações
- **Metadados de Banco:** Tabelas, colunas, procedures, functions, triggers, relacionamentos
- **Rastreabilidade Cruzada:** Links bidireccionais entre requisitos ↔ tables ↔ procedures ↔ endpoints
- **Diagramas Integrados:** PlantUML (ER, sequência, fluxo) renderizados como SVG inline
- **Índice Navegável:** Seções temáticas com busca full-text, hierarquia de conteúdo

---

## Integração com skills relacionadas

### 1. `documentacao-de-software`

A skill **documentacao-integrada-export** consome artefatos gerados ou atualizados pela skill `documentacao-de-software`:

- Requisitos em `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/req-XXXX-*.md`
- Documentação de API em `documentacao/processo_unificado/artefatos_aprovados/documentacao_api/api-*.md`
- Documentação de visão em `documentacao/processo_unificado/artefatos_aprovados/visao/vis-*.md`
- Diagramas de classes em `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_classes/dcl-*.md`
- Diagramas de integração em `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_integracao_de_sistemas/min-*.md`
- Matriz de risco em `documentacao/matriz-risco-sistema.md`

**Papel da integração:** O site exportado oferece navegação web a esses artefatos, com busca e links cruzados.

### 2. `database-mcp`

A skill integrada consulta o índice e artefatos gerados pelo **database-mcp**:

- Índice de schema: `documentacao/banco_dados/discovery-database.yml`
- Mapa de dados: `documentacao/banco_dados/DADOS-05-MAPA-DADOS.md`
- Status e transições: `documentacao/banco_dados/DADOS-06-STATUS-E-TRANSICOES.md`
- Rotinas (SPs, functions, triggers): `documentacao/banco_dados/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md`
- Diagrama ER: `documentacao/banco_dados/DADOS-01-ER.md`
- Mapa de fluxo-tabelas: `documentacao/banco_dados/DADOS-09-MAPA-FLUXO-TABELAS.md`

**Papel da integração:** Enriquece a navegação com metadados de banco em contexto, editáveis a partir do MCP.

### 3. `discovery-html-export`

A skill **documentacao-integrada-export** estende a arquitetura de **discovery-html-export**:

- **Reutiliza:** pipeline de build com MkDocs, injeção de PlantUML, assets (logo, CSS, JS)
- **Adapta:** nav hierárquico para incluir seções de banco de dados e rastreabilidade
- **Estende:** gerador de índice para incluir metadados de tabelas e procedures
- **Integra:** ambos os tipos de documentação (software + banco) em site único

---

## Pré-requisitos

A skill usa **MkDocs 1.x** (não 2.x) e o tema Material for MkDocs:

```powershell
pip install "mkdocs>=1.5,<2" "mkdocs-material"
```

Verificar:

```powershell
mkdocs --version
```

Além disso, é necessário:

- **Python 3.7+** com bibliotecas padrão
- **PowerShell 5.1+** (Windows)
- Artefatos gerados pela skill `documentacao-de-software` (requisitos, APIs, documentação)
- Artefatos gerados pela skill `database-mcp` (metadados de banco, procedures)

---

## Estrutura de artefatos esperados

```
documentacao/
├── README.md                                    ← TOC raiz (obrigatório)
├── matriz-risco-sistema.md                      ← matriz global de risco
├── banco_dados/
│   ├── discovery-database.yml                   ← índice do MCP
│   ├── DADOS-01-ER.md                           ← diagrama ER (PlantUML)
│   ├── DADOS-05-MAPA-DADOS.md                   ← tabelas e colunas
│   ├── DADOS-06-STATUS-E-TRANSICOES.md          ← status mapeados
│   ├── DADOS-09-MAPA-FLUXO-TABELAS.md           ← relacionamento fluxo-tabela
│   └── DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md ← rotinas do banco
└── processo_unificado/
    └── artefatos_aprovados/
        ├── detalhamento_requisitos/
        │   ├── req-XXXX-nome_do_requisito.md
        │   ├── apf-req-XXXX.md
        │   └── wireframes/
        │       └── req-XXXX-wireframe.png
        ├── documentacao_api/
        │   └── api-nome_da_api.md
        ├── visao/
        │   └── vis-nome_da_visao.md
        ├── diagrama_de_classes/
        │   └── dcl-nome_do_diagrama.md
        ├── diagrama_de_integracao_de_sistemas/
        │   └── min-nome_do_diagrama.md
        ├── diagrama_de_entidades_e_relacionamento/
        │   └── der-nome_do_diagrama.md
        └── dicionario_de_dados/
            └── did-nome_do_dicionario.md
```

---

## Execução

```powershell
cd c:\seu-projeto

# Build padrão com integração completa
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1

# Build com reestruturação de HTML (index. na raiz, demais em /html)
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1 -Restructure

# Build com profile específico do MCP
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1 -DatabaseProfile principal
```

O script realiza automaticamente:

1. **Validação:** verifica presença de artefatos documentacao-de-software e banco_dados
2. **Verificação de dependências:** pip e MkDocs
3. **Cópia de assets:** logo, CSS integrado, JS (lightbox + rastreabilidade)
4. **Leitura do MCP:** consulta índice `discovery-database.yml` e metadados
5. **Geração de índice integrado:** agrupa requisitos + tabelas + procedures em nav hierárquica
6. **Coleta de .md:** documentação de software + banco de dados
7. **Geração de mkdocs.yml:** configuração com navegação cruzada
8. **Geração de SVGs PlantUML:** via `generate-diagrams.py`
9. **Execução de mkdocs build:** constrói HTML estático
10. **Injeção de SVGs:** via `inject-diagrams.py` com linking cruzado
11. **(opcional) Reestruturação:** move HTML exceto index para `documentacao-html/html/`

---

## Saída esperada

### Sem `-Restructure` (padrão)

```
seu-projeto/
├── documentacao/               ← artefatos originais (preservados)
├── documentacao-html/          ← gerado pelo build
│   ├── index.html              ← página de entrada (abrir no navegador)
│   ├── software/               ← seção de requisitos e APIs
│   │   ├── req-0001-login.html
│   │   ├── req-0002-cadastro.html
│   │   ├── api-usuarios.html
│   │   └── ...
│   ├── banco-dados/            ← seção de tabelas e procedures
│   │   ├── tabelas.html
│   │   ├── procedures.html
│   │   ├── functions.html
│   │   └── status-transicoes.html
│   ├── rastreabilidade/        ← seção de linakge cruzado
│   │   ├── req-para-tabelas.html
│   │   ├── endpoint-para-sp.html
│   │   └── matriz-risco-integrada.html
│   ├── assets/
│   │   ├── diagrams/           ← SVGs PlantUML
│   │   ├── wireframes/         ← wireframes de requisitos
│   │   ├── logo.svg
│   │   ├── css/
│   │   │   └── integrated-theme.css
│   │   └── js/
│   │       ├── lightbox.js
│   │       └── traceability-links.js
│   └── search/                 ← índice full-text
└── mkdocs.yml                  ← gerado pelo script
```

### Com `-Restructure`

```
documentacao-html/
├── index.html                  ← sozinho na raiz
├── 404.html
├── html/                       ← todos os demais HTML
│   ├── software/
│   ├── banco-dados/
│   ├── rastreabilidade/
│   └── ...
├── assets/
└── search/
```

---

## Estrutura de navegação (nav)

O site é organizado em **5 seções principais**:

### 1. **Visão Geral**

- Índice integrado (documento principal)
- Glossário
- Convenções

### 2. **Requisitos e Especificações** (software/)

- Documentos de visão (vis-\*.md)
- Requisitos funcionais e não funcionais (req-\*.md)
- Critérios de aceitação (Gherkin)
- APF por requisito
- Wireframes integrados
- Diagrama de classes

### 3. **APIs e Integrações** (api/)

- Documentação de endpoints (api-\*.md)
- Diagramas de sequência
- Contrato de requisição/resposta
- Status HTTP e erros
- Diagrama de integração de sistemas

### 4. **Banco de Dados** (banco-dados/)

- Diagrama ER (DADOS-01-ER.md)
- Mapa de dados (DADOS-05-MAPA-DADOS.md)
- Status e transições (DADOS-06-STATUS-E-TRANSICOES.md)
- Procedures, functions, triggers (DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md)
- Mapa de fluxo-tabelas (DADOS-09-MAPA-FLUXO-TABELAS.md)

### 5. **Rastreabilidade** (rastreabilidade/)

- Matriz de requisitos ↔ tabelas
- Matriz de endpoints ↔ procedures
- Matriz de risco integrada (software + banco)
- Mapa de dependências (requisito → API → SP → tabelas)
- Análise de impacto

---

## Tema visual e assets

O build copia automaticamente `assets/` da skill para `{DocsDir}/assets/`. A estrutura inclui:

```
.github/documentacao-integrada-export/assets/
├── logo.svg                    ← logo corporativo
├── css/
│   ├── base-theme.css          ← base do Material for MkDocs
│   ├── integrated-theme.css    ← extensões para integracao
│   └── traceability.css        ← estilo de links cruzados
├── js/
│   ├── lightbox.js             ← zoom/pan para diagramas
│   └── traceability-links.js   ← highlighting de navegacao cruzada
└── img/
    └── icons/                  ← ícones para seções (requisito, BD, API)
```

### Cores do tema integrado

| Variável CSS        | Valor     | Uso                                      |
| ------------------- | --------- | ---------------------------------------- |
| `--primary-color`   | `#0047ab` | Header, links, títulos                   |
| `--secondary-color` | `#f47920` | Acentos, hover                           |
| `--success-color`   | `#28a745` | Status aprovado, ativo                   |
| `--danger-color`    | `#dc3545` | Status crítico, erro                     |
| `--info-color`      | `#17a2b8` | Informações, métodos HTTP                |
| `--warning-color`   | `#ff7625` | Avisos, status em revisão                |
| `--database-color`  | `#6f42c1` | Elementos de banco (tabelas, procedures) |
| `--bg-light`        | `#f4f5f7` | Fundo da página                          |
| `--text-primary`    | `#333333` | Texto principal                          |

---

## Scripts da skill

| Script                       | Papel                                                           |
| ---------------------------- | --------------------------------------------------------------- |
| `build-integrated-docs.ps1`  | Orquestrador principal — 11 passos                              |
| `generate-index.py`          | Gera índice integrado com requisitos + tabelas + procedures     |
| `generate-database-pages.py` | Gera .md de banco de dados a partir de `discovery-database.yml` |
| `generate-traceability.py`   | Gera matriz de rastreabilidade cruzada                          |
| `generate-diagrams.py`       | Extrai blocos PlantUML e gera SVGs via plantuml.com             |
| `inject-diagrams.py`         | Injeta SVGs nos HTML                                            |

---

## Validações obrigatórias

O script executa validações e encerra com erro se:

- ❌ Pasta `documentacao/` não existe
- ❌ Arquivo `documentacao/README.md` (TOC raiz) não encontrado
- ❌ Nenhum requisito em `detalhamento_requisitos/` (0 arquivos req-\*.md)
- ❌ Nenhum banco de dados: `discovery-database.yml` não existe ou está vazio
- ❌ MkDocs não está instalado e falha ao instalar
- ❌ Python não está disponível no PATH

Se alguma validação falhar, o agente exibe mensagem clara indicando a correção necessária.

---

## Fluxo de trabalho típico

### Cenário 1: Documentação de novo requisito

1. **Documentador** escreve requisito com skill `documentacao-de-software`
   - Cria `req-0001-novo-fluxo.md` com critérios Gherkin, APF, matriz de risco local
   - Referencia tabelas impactadas (ex.: `users`, `workflows`, `logs`)

2. **Documentador** atualiza `documentacao-de-software` SKILL.md se necessário

3. **DBA** documenta tabelas relacionadas com skill `database-mcp`
   - Verifica/atualiza `discovery-database.yml`
   - Documenta procedures, functions impactadas
   - Atualiza `DADOS-05-MAPA-DADOS.md`, `DADOS-06-STATUS-E-TRANSICOES.md`

4. **Exportador** roda `build-integrated-docs.ps1`
   - Site HTML gerado em `documentacao-html/`
   - Rastreabilidade automática detecta: req-0001 → users/workflows → procedure sp_insert_workflow
   - Links cruzados adicionados automaticamente

5. **Revisor** abre `documentacao-html/index.html` no navegador
   - Navega requisito → procedura SQL → tabelas
   - Verifica matriz de risco integrada
   - Valida impactos técnicos

---

## Cenário 2: Geração de documentação de API

1. **Developer/Documentador** cria API com skill `documentacao-de-software`
   - Escreve `api-usuarios-service.md` com endpoints, payloads, validações

2. **Exportador** roda `build-integrated-docs.ps1`
   - Site gera seção de APIs
   - Identifica procedures SQL referenciadas na documentação de API
   - Gera matriz automática: endpoint → procedure → tabelas

3. **Revisor** consulta navegação integrada
   - Visualiza fluxo completo: POST /users → sp_insert_user → tabela users
   - Verifica certificações de acesso (DADOS-06 de status)

---

## Heurística de rastreabilidade automática

O gerador de rastreabilidade usa **matching textual + patterns**:

- **Requisito → Tabela:** busca por `table_name` (ex.: `users`) no corpo do req-\*.md
- **Requisito → Procedure:** busca por `sp_*` (ex.: `sp_insert_user`) no corpo do req-\*.md
- **API → Procedure:** busca patterns de SQL no corpo de `api-*.md`
- **Matriz de risco:** combina riscos de requisito + tabelas/procedures referenciadas
- **Status de transição:** mapa automático de enums mencionados em requisitos para valores de status em DADOS-06

---

## Configuração (config.yaml)

Se preferir customização avançada, crie `config-docs-integradas.yaml` na raiz do projeto:

```yaml
# config-docs-integradas.yaml

docs:
  site_name: "Documentação Integrada - Seu Projeto"
  theme: material
  docs_root: documentacao
  site_root: documentacao-html

  sections:
    visao_geral: true
    requisitos: true
    apis: true
    banco_dados: true
    rastreabilidade: true

  nav_prefix_order:
    - VIS # visão
    - REQ # requisitos
    - API # APIs
    - DADOS # banco de dados
    - DER # diagramas ER
    - MIN # integrações
    - RAS # rastreabilidade

database:
  index_file: "documentacao/banco_dados/discovery-database.yml"
  metadata_dir: "documentacao/banco_dados"

# Configuração de PlantUML
plantuml:
  server: "http://www.plantuml.com/plantuml"
  include_diagrams: true
```

---

## Troubleshooting

| Problema                                           | Solução                                                                                |
| -------------------------------------------------- | -------------------------------------------------------------------------------------- |
| "mkdocs not found"                                 | `pip install "mkdocs>=1.5,<2" mkdocs-material`                                         |
| "discovery-database.yml not found"                 | Execute `database-mcp` SKILL primeiro                                                  |
| "No requirements found in detalhamento_requisitos" | Crie requisitos com skill `documentacao-de-software`                                   |
| "MkDocs 2.x detectado"                             | Desinstale e reinstale: `pip uninstall mkdocs && pip install "mkdocs>=1.5,<2"`         |
| "Python not in PATH"                               | Reinstale Python com "Add Python to PATH" marcado                                      |
| "Navegação não mostra rastreabilidade"             | Verifique se nomes de tabela/procedure estão no documento req-\*.md                    |
| "Wireframes não aparecem"                          | Coloque imagens em `wireframes/` e use `![alt](../wireframes/requisito-wireframe.png)` |

---

## Extensibilidade

A skill foi projetada para ser extensível:

### Adicionar nova seção temática

Edite `generate-index.py` na função `SECAO_DESC`:

```python
SECAO_DESC = {
    "DISC": (...),
    "REQ": (...),
    "API": (...),
    "DADOS": (...),
    "MINHA_SECAO": (
        "Título da Seção",
        "Descrição para leitores.",
        "Contexto/motivação.",
    ),
}
```

### Customizar tema CSS

Edite `assets/css/integrated-theme.css` e rerun build.

### Adicionar novo tipo de diagrama

Atualize `generate-diagrams.py` para reconhecer novos blocos:

```python
# Suporte para novos diagramas (ex.: component, architecture)
DIAGRAM_TYPES = ["plantuml", "mermaid", "component", "architecture"]
```

---

## Limitações conhecidas

- ❌ MkDocs 2.x não é compatível com tema Material (use 1.x)
- ❌ Diagrama ER grande (50+ tabelas) pode levar tempo para renderizar
- ❌ PlantUML via sistema remoto (plantuml.com) requer conexão internet
- ❌ Rastreabilidade é heurística (matching textual) — não é garantida 100%
- ✅ Suporta PostgreSQL, SQL Server (database-mcp)
- ✅ Suporta wireframes em PNG, JPG, SVG via referência

---

## Roadmap

- [ ] Integração com OpenAPI/Swagger para auto-gerar documentação de API
- [ ] Suporte a Mermaid.js nativo (além de PlantUML)
- [ ] Cache de PlantUML local (evitar re-render em cada build)
- [ ] Export para PDF com paginação inteligente
- [ ] Integração com GitHub Pages (deploy automático)
- [ ] Análise de cobertura de requisitos vs. código
