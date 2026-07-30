# Documentação Integrada — README

Esta é a skill **documentacao-integrada-export**, que integra três skills do Copilot para gerar um site de documentação HTML navegável e unificado.

## 🎯 Objetivo

Gerar um site HTML estático (`documentacao-html/`) que consolida:

- **Documentação de Software** (requisitos, visão, APIs) — gerada pela skill **documentacao-de-software**
- **Metadados de Banco de Dados** (tabelas, procedures, functions) — extraídos do MCP **database-mcp**
- **Rastreabilidade Cruzada** — matrizes automáticas de Requisito ↔ Tabela, API ↔ Procedure, etc.

Tudo em um único site com navegação integrada, busca full-text e diagramas PlantUML renderizados.

## 📋 Pré-requisitos

1. **Python 3.7+** com pip
2. **PowerShell 5.1+** (Windows)
3. **MkDocs 1.5+** (instalado automaticamente durante o build)
4. Projeto estruturado com:
   - Pasta `documentacao/` na raiz
   - Artefatos de `documentacao-de-software` (requisitos, APIs, diagramas)
   - Artefatos de `database-mcp` (índice `discovery-database.yml`)

## 🚀 Uso Rápido

```powershell
# Navegue até a raiz do seu projeto
cd c:\seu-projeto

# Execute o script de build
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1

# Abra o site gerado
start "documentacao-html\index.html"
```

## 📦 Arquivos da Skill

```
.github/documentacao-integrada-export/
├── SKILL.md                           ← Documentação completa
├── README.md                          ← Este arquivo
├── scripts/
│   ├── build-integrated-docs.ps1      ← Orquestrador principal (PowerShell)
│   ├── generate-integrated-index.py   ← Gera índice combinado
│   ├── generate-traceability.py       ← Gera matrizes de rastreabilidade
│   ├── generate-diagrams.py           ← Processa diagramas PlantUML*
│   └── inject-diagrams.py             ← Injeta SVGs nos HTML*
└── assets/
    ├── css/
    │   ├── base-theme.css
    │   ├── integrated-theme.css       ← Tema integrado
    │   └── traceability.css           ← Estilos de rastreabilidade
    ├── js/
    │   ├── lightbox.js                ← Zoom para diagramas
    │   └── traceability-links.js      ← Highlighting de navegação cruzada
    └── logo.svg

*Scripts herdados de discovery-html-export
```

## 🔄 Fluxo de Trabalho

### 1. Documentar Requisitos (skill: documentacao-de-software)

```bash
# Criar novo requisito
documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/
└── req-0001-login-usuario.md
```

### 2. Manter Banco de Dados (skill: database-mcp)

```bash
# Atualizar metadados
documentacao/banco_dados/
├── discovery-database.yml          ← Índice automático
├── DADOS-01-ER.md                  ← Diagrama ER
├── DADOS-05-MAPA-DADOS.md          ← Tabelas
└── DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md
```

### 3. Gerar Documentação Integrada (esta skill)

```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1

# Resultado:
# documentacao-html/
# ├── index.html                    ← Abrir no navegador
# ├── software/
# │   ├── req-0001-login-usuario.html
# │   └── ...
# ├── banco-dados/
# │   ├── tabelas.html
# │   └── procedures.html
# └── rastreabilidade/
#     └── matriz-rastreabilidade.html
```

## ⚙️ Opções de Execução

### Build padrão (sem reorganização)

```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1
```

Saída: todos os `.html` na raiz de `documentacao-html/`

### Build com reorganização

```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1 -Restructure
```

Saída: `index.html` na raiz, demais HTML em `documentacao-html/html/`

### Build com profile específico do MCP

```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1 -DatabaseProfile principal
```

(Útil se houver múltiplas conexões de banco configuradas)

## 🔗 Como Funciona a Rastreabilidade

### Detecção Automática

O script `generate-traceability.py` usa **matching textual** para encontrar:

- **Requisito → Tabela:** Busca por `table_name` no corpo do req-*.md
- **Requisito → Procedure:** Busca por `sp_*` ou `proc_*` no texto
- **API → Procedure:** Busca em documentação de endpoint

### Exemplo

```markdown
# REQ-0001: Autenticação de Usuário

...conteúdo...

Quando o usuário faz login, a tabela `users` é consultada
e a função `sp_authenticate_user` é executada.

```

Isso gera automaticamente:

```
REQ-0001 → [users]
REQ-0001 → [sp_authenticate_user]
```

E essas referências aparecem como **links navegáveis** no site.

## 📊 Seções do Site Gerado

### 1. Home (index.html)
- Visão geral e índice integrado
- Links para todas as seções

### 2. Requisitos e Especificações
- Documentos de visão
- Requisitos funcionais e não funcionais
- Wireframes integrados
- Critérios de aceitação (Gherkin)

### 3. APIs e Integrações
- Documentação de endpoints
- Diagramas de sequência
- Contrato request/response

### 4. Banco de Dados
- Diagrama ER
- Mapa de tabelas
- Mapa de status e transições
- Procedures, functions, triggers

### 5. Rastreabilidade
- Matriz: Requisitos ↔ Tabelas
- Matriz: APIs ↔ Procedures
- Matriz de risco integrada
- Análise de impacto

## 🎨 Personalização

### Mudar Logo

Edite o arquivo:

```
.github/documentacao-integrada-export/assets/logo.svg
```

Na próxima build, o logo será copiado automaticamente.

### Customizar Cores

Edite o arquivo:

```
.github/documentacao-integrada-export/assets/css/integrated-theme.css
```

Variáveis disponíveis:

```css
--primary-color: #0047ab;
--secondary-color: #f47920;
--database-color: #6f42c1;
--success-color: #28a745;
--danger-color: #dc3545;
```

## 📋 Checklist Pré-Build

Antes de executar o build, verifique:

- [ ] Pasta `documentacao/` existe
- [ ] `documentacao/README.md` (TOC raiz) existe
- [ ] Pelo menos 1 arquivo `req-*.md` em `detalhamento_requisitos/`
- [ ] Arquivo `discovery-database.yml` existe em `banco_dados/`
- [ ] Python está instalado e acessível
- [ ] MkDocs pode ser instalado (conexão pip funcionando)

## 🆘 Troubleshooting

### "mkdocs not found"

```powershell
pip install "mkdocs>=1.5,<2" mkdocs-material
```

### "discovery-database.yml not found"

Execute a skill `database-mcp` primeiro para gerar o índice de banco de dados.

### "No requirements found"

Crie requisitos na pasta:

```
documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/
```

Com nome: `req-XXXX-nome_do_requisito.md`

### Build lento

- Diagramas PlantUML grande (50+ tabelas) levam tempo
- Se usar servidor remoto (plantuml.com), pode depender de latência
- Para offline, considere usar PlantUML local

### Diagrama ER não renderiza

- Verifique se `DADOS-01-ER.md` existe
- Confirme sintaxe PlantUML válida
- Verifique conexão internet (se usar plantuml.com)

## 🔮 Roadmap

- [ ] Cache local de PlantUML (evitar re-renders)
- [ ] Integração com OpenAPI/Swagger
- [ ] Suporte a Mermaid.js nativo
- [ ] Export para PDF
- [ ] Deploy automático via GitHub Pages
- [ ] Análise de cobertura de requisitos vs. código

## 📞 Suporte

Para problemas ou sugestões, consulte:

1. [SKILL.md](./SKILL.md) — Documentação completa da skill
2. [documentacao-de-software SKILL](../.github/documentacao-de-software/SKILL.md)
3. [database-mcp SKILL](../.github/database-mcp/SKILL.md)
4. [discovery-html-export SKILL](../.github/discovery-html-export/SKILL.md)

---

**Última atualização:** DD/MM/AAAA
**Versão da Skill:** 1.0.0
