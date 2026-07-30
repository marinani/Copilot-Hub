# Integração com Skills Relacionadas

## 📚 Compatibilidade

A skill **documentacao-integrada-export** foi projetada para trabalhar em harmonia com:

| Skill | Versão | Função | Dependência |
|-------|--------|--------|------------|
| `documentacao-de-software` | 1.0+ | Gera requisitos, APIs, visão | ✅ Recomendado |
| `database-mcp` | 1.0+ | Fornece metadados de banco | ✅ Recomendado |
| `discovery-html-export` | 1.0+ | Fornece pipeline MkDocs | ✅ Necessário (herança) |

---

## 🔗 Como as Skills se Integram

### Fluxo de Dados

```
documentacao-de-software SKILL
    ↓ gera artefatos
documentacao/processo_unificado/artefatos_aprovados/
    ├── detalhamento_requisitos/req-XXXX-*.md
    ├── documentacao_api/api-*.md
    └── visao/vis-*.md

database-mcp MCP SERVER
    ↓ gera índice e metadados
documentacao/banco_dados/
    ├── discovery-database.yml
    ├── DADOS-01-ER.md
    ├── DADOS-05-MAPA-DADOS.md
    └── DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md

documentacao-integrada-export SKILL
    ↓ consome e integra
build-integrated-docs.ps1
    ↓ orquestra
discovery-html-export (herança)
    ├── MkDocs build
    ├── PlantUML rendering
    └── HTML injection
    ↓ gera site
documentacao-html/
    ├── index.html
    ├── software/
    ├── banco-dados/
    ├── rastreabilidade/
    └── assets/
```

---

## 📋 Checklist de Uso Integrado

### Antes

- [ ] Skill `documentacao-de-software` está instalada
- [ ] Skill `database-mcp` está instalada
- [ ] Skill `discovery-html-export` está disponível
- [ ] Python 3.7+
- [ ] PowerShell 5.1+

### Durante

- [ ] Criar requisitos com `documentacao-de-software`
- [ ] Documenter banco com `database-mcp`
- [ ] Executar `build-integrated-docs.ps1`

### Depois

- [ ] Visualizar `documentacao-html/index.html`
- [ ] Validar rastreabilidade em `rastreabilidade/`
- [ ] Revisar diagramas (ER, sequência, fluxo)

---

## 🔄 Ciclo de Atualização Recomendado

1. **Developer** cria/atualiza requisito com `documentacao-de-software`
2. **DBA** atualiza banco com `database-mcp` (procedures, tabelas)
3. **Documentador** executa `build-integrated-docs.ps1`
4. **Revisor** abre `documentacao-html/index.html` e valida rastreabilidade
5. **Commit** de documentação atualizada no git

---

## ⚙️ Dependências Entre Skills

### `documentacao-integrada-export` depende de:

#### 1. `documentacao-de-software`
- Para estrutura de arquivo
- Para padrões de prefixo (req-, api-, vis-)
- Para critérios de aceitação em Gherkin
- Para matrizes de risco locais

#### 2. `database-mcp`
- Para índice `discovery-database.yml`
- Para metadados de tabelas/procedures
- Para diagramas ER
- Para documentação de rotinas

#### 3. `discovery-html-export`
- Para pipeline MkDocs
- Para gerador de diagramas PlantUML
- Para injetor de SVGs
- Para assets (logo, CSS, JS lightbox)

---

## 🎯 Casos de Uso Integrados

### Caso 1: Novo Requisito com Impacto em Banco

```
1. Developer cria req-0005-relatório-vendas.md
   └─ Referencia: tabela `vendas`, procedure `sp_get_vendas`

2. database-mcp DETECTA procedura e tabela
   ├─ Documenta em DADOS-05-MAPA-DADOS.md
   └─ Adiciona a DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md

3. documentacao-integrada-export INTEGRA
   ├─ Lê req-0005
   ├─ Lê discovery-database.yml atualizado
   ├─ GENERA matriz: REQ-0005 → [vendas] → [sp_get_vendas]
   └─ Cria links automáticos no site
```

### Caso 2: Temas Multiusuário

```
Usuário 1: Requirements Writer (documentacao-de-software)
   └─ Cria requisitos

Usuário 2: DBA (database-mcp)
   └─ Documenta tabelas/procedures

Usuário 3: Tech Writer (documentacao-integrada-export)
   └─ Gera site integrado

Result: Documentação unificada sem conflitos!
```

### Caso 3: Auditoria e Conformidade

```
documentacao-integrada-export
├─ Matriz de Risco Integrada
│  ├─ Requisitos com risco alto
│  ├─ Tabelas sensíveis (LGPD, PCI)
│  └─ Procedures críticas
│
└─ Análise de Impacto
   ├─ Quais requisitos tocam dados sensíveis
   └─ Quais procedures acessam esses dados
```

---

## 🚀 Fluxo de Entrega

```
PHASE 1: Discovery & Planning
├── Tech Writer usa documentacao-de-software
│   └─ Cria visão, requisitos, APIs
└── DBA usa database-mcp
    └─ Documenta tabelas, procedures, triggers

PHASE 2: Integration & Synthesis
└── Tech Lead usa documentacao-integrada-export
    ├─ build-integrated-docs.ps1
    └─ Revisa rastreabilidade

PHASE 3: Review & Approval
├── Stakeholders: abre documentacao-html/index.html
├── Validam requisitos vs. banco
└── Aprovam rastreabilidade

PHASE 4: Deployment
├── Commit documentacao no git
├── Deploy site via GitHub Pages (futuro)
└── Distribuir "Read-Only" link
```

---

## 🔐 Princípios de Integração

1. **Unidirecionais:** As skills não se modificam mutuamente
   - `documentacao-integrada-export` **lê** artefatos
   - Não sobrescreve `documentacao-de-software` ou `database-mcp`

2. **Independentes:** Cada skill pode rodar isoladamente
   - `documentacao-de-software` sem database-mcp
   - `database-mcp` sem `documentacao-de-software`
   - `documentacao-integrada-export` roda melhor COM ambas

3. **Versionadas:** Cada artefato tem versão (SemVer)
   - Histórico de mudanças rastrevel
   - Validação de compatibilidade entre versões

4. **Auditáveis:** Tudo é documentado
   - Quem mudou o quê
   - Por que (histórico de mudanças)
   - Quando (timestamp)

---

## 📞 Suporte

Para problemas de integração:

1. **Verifique documentação de cada skill**
   - [documentacao-de-software SKILL.md](../.github/documentacao-de-software/SKILL.md)
   - [database-mcp SKILL.md](../.github/database-mcp/SKILL.md)
   - [discovery-html-export SKILL.md](../.github/discovery-html-export/SKILL.md)

2. **Valide pré-requisitos**
   - Artefatos estão no local correto?
   - Nomes de arquivo seguem padrão?
   - discovery-database.yml existe e é válido?

3. **Teste skills isoladamente**
   - Teste `documentacao-de-software` criando um req-*
   - Teste `database-mcp` gerando índice
   - Depois teste `documentacao-integrada-export`

---

## 📈 Roadmap Futuro

- [ ] Integração com GitHub API (pull request checks)
- [ ] Deploy automático para GitHub Pages
- [ ] Integração com Azure DevOps (wiki sync)
- [ ] Export para Confluence
- [ ] Análise de cobertura de requisitos vs. código
- [ ] Webhooks para rebuild automático

---

**Integração Perfeita = Documentação consistida, navegável, rastreável!** ✨
