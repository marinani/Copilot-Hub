# 📑 Índice da Skill documentacao-integrada-export

## 📚 Estrutura de Documentação

Esta skill está organizada em **6 níveis de detalhe**, do mais rápido ao mais completo:

### 1️⃣ **GETTING_STARTED.md** (5 min)
   - ⚡ Inicialização em 5 minutos
   - ✅ Checklist pré-requisitos
   - 🐛 Troubleshooting rápido
   - **👉 Comece aqui**

### 2️⃣ **README.md** (10 min)
   - 🎯 Objetivo e propósito
   - 📋 Pré-requisitos detalhados
   - 🚀 Uso rápido (without deep dive)
   - ⚙️ Opções de execução
   - 🔗 Como funciona rastreabilidade
   - 🎨 Personalização (logo, cores)

### 3️⃣ **SKILL.md** (30 min) — Documentação Completa
   - 🏠 Visão geral completa
   - 🔗 Integração detalhada com 3 skills
   - 📦 Pré-requisitos técnicos
   - 📂 Estrutura esperada de artefatos
   - ⚙️ Execução com todos os parâmetros
   - 📊 Saídas esperadas (estrutura HTML)
   - 🗺️ Navegação do site (5 seções)
   - 🎨 Tema visual e cores
   - 📜 Scripts disponíveis (6 tipos)
   - ✅ Validações obrigatórias
   - 🔄 Fluxos de trabalho (2 cenários)
   - 🧠 Heurística de rastreabilidade
   - ⚙️ Configuração avançada (config.yaml)
   - 🔧 Troubleshooting completo
   - 🚀 Extensibilidade
   - ⚠️ Limitações conhecidas
   - 🗓️ Roadmap

### 4️⃣ **INTEGRATION.md** (15 min)
   - 📊 Compatibilidade com skills relacionadas
   - 🔄 Fluxo de dados entre as 3 skills
   - 📋 Checklist de uso integrado
   - ⏱️ Ciclo de atualização recomendado
   - ⚙️ Dependências entre skills
   - 🎯 3 casos de uso integrados
   - 🚀 Fluxo de entrega (4 phases)
   - 🔐 Princípios de integração

### 5️⃣ **config-docs-integradas.yaml.example** (5 min)
   - ⚙️ Template de configuração personalizada
   - 🎨 Customização de site
   - 🗂️ Ordenação de navegação
   - 🗄️ Configuração de banco de dados
   - 🔗 Rastreabilidade automática
   - 📊 Diagramas PlantUML
   - 🎨 Tema visual

### 6️⃣ **SKILL.md** (referência)
   - 📖 Documentação completa de referência
   - 📋 Tudo sobre a skill em um arquivo

---

## 📂 Estrutura de Arquivos da Skill

```
.github/documentacao-integrada-export/
│
├── 📖 DOCUMENTAÇÃO (leia na ordem abaixo)
│   ├── GETTING_STARTED.md           ← COMECE AQUI
│   ├── README.md                    ← Depois aqui
│   ├── SKILL.md                     ← Referência completa
│   ├── INTEGRATION.md               ← Integração com outras skills
│   └── INDEX.md                     ← Este arquivo
│
├── 📜 CONFIGURAÇÃO
│   └── config-docs-integradas.yaml.example
│
├── 🛠️ SCRIPTS (PowerShell + Python)
│   ├── build-integrated-docs.ps1    ← ORQUESTRADOR PRINCIPAL
│   ├── generate-integrated-index.py ← Gera índice combined
│   ├── generate-traceability.py     ← Gera matrizes
│   ├── generate-diagrams.py         ← Processa PlantUML (herdado)
│   └── inject-diagrams.py           ← Injeta SVGs (herdado)
│
└── 🎨 ASSETS (Logo, CSS, JS)
    ├── logo.svg
    ├── css/
    │   ├── base-theme.css
    │   ├── integrated-theme.css     ← TEMA CUSTOMIZADO
    │   └── traceability.css
    └── js/
        ├── lightbox.js
        └── traceability-links.js
```

---

## 🎯 Mapa de Uso

### Para iniciantes:
1. [GETTING_STARTED.md](./GETTING_STARTED.md) (5 min)
2. Execute `build-integrated-docs.ps1`
3. Abra `documentacao-html/index.html`

### Para desenvolvedores:
1. [README.md](./README.md) (10 min)
2. [SKILL.md](./SKILL.md) (referência)
3. Customize `config-docs-integradas.yaml`
4. Personalize `assets/css/integrated-theme.css`

### Para integradores:
1. [INTEGRATION.md](./INTEGRATION.md) (15 min)
2. Entenda fluxos com skills relacionadas
3. Configure ciclo de atualização
4. Implemente em pipeline CI/CD

### Para contribuidores:
1. [SKILL.md](./SKILL.md) — Arquitetura completa
2. Estude `generate-integrated-index.py` e `generate-traceability.py`
3. Estude `build-integrated-docs.ps1` (orquestração)
4. Submeta melhorias!

---

## 🔗 Documentação das Skills Relacionadas

Se precisar dos detalhes das skills integradas:

| Skill | Arquivo | Propósito |
|-------|---------|----------|
| `documentacao-de-software` | [SKILL.md](../.github/documentacao-de-software/SKILL.md) | Requisitos, APIs, visão |
| `database-mcp` | [SKILL.md](../.github/database-mcp/SKILL.md) | Tabelas, procedures, índice |
| `discovery-html-export` | [SKILL.md](../.github/discovery-html-export/SKILL.md) | MkDocs, PlantUML, navegação |

---

## 🚀 Comandos Rápidos

### Build padrão:
```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1
```

### Build com reestruturação HTML:
```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1 -Restructure
```

### Abrir documentação gerada:
```powershell
start "documentacao-html\index.html"
```

---

## ✅ Checklist de Implementação

- [ ] Li [GETTING_STARTED.md](./GETTING_STARTED.md)
- [ ] Tenho `documentacao/` estruturada
- [ ] Tenho artefatos de `documentacao-de-software`
- [ ] Tenho `discovery-database.yml` de `database-mcp`
- [ ] Python 3.7+ instalado
- [ ] Executei `build-integrated-docs.ps1`
- [ ] Abri `documentacao-html/index.html`
- [ ] Validei rastreabilidade em `documentacao-html/rastreabilidade/`
- [ ] Customizel logo e cores (opcional)
- [ ] Integrei em pipeline CI/CD (opcional)

---

## 📞 Precisa de Ajuda?

### Problema básico?
→ Veja [GETTING_STARTED.md](./GETTING_STARTED.md) ou seção de Troubleshooting no [README.md](./README.md)

### Dúvida técnica?
→ Consulte [SKILL.md](./SKILL.md) (documentação completa)

### Integração complexa?
→ Estude [INTEGRATION.md](./INTEGRATION.md)

### Erro específico?
→ Busque no [SKILL.md](./SKILL.md) seção "Troubleshooting"

---

## 🗺️ Estrutura do Site Gerado (documentacao-html/)

```
documentacao-html/
├── index.html                           ← Página de entrada
├── software/                            ← Seção de requisitos/APIs
│   ├── vis-001-escopo.html
│   ├── req-0001-login.html
│   └── api-usuarios.html
├── banco-dados/                         ← Seção de metadados BD
│   ├── tabelas.html
│   ├── procedures.html
│   ├── functions.html
│   └── status-transicoes.html
├── rastreabilidade/                     ← Seção de linking cruzado
│   ├── 01-requisitos-tabelas.html
│   ├── 02-apis-procedures.html
│   ├── 03-procedures-tabelas.html
│   ├── 04-matriz-risco-integrada.html
│   └── 05-analise-impacto.html
├── assets/                              ← Recursos estáticos
│   ├── diagrams/                        ← SVGs PlantUML
│   ├── wireframes/
│   ├── logo.svg
│   ├── css/
│   │   ├── base.css
│   │   ├── integrated-theme.css
│   │   └── traceability.css
│   └── js/
│       ├── lightbox.js
│       └── traceability-links.js
└── search/                              ← Índice full-text
    ├── search_index.json
    └── ...
```

---

## 🎓 Exemplos Úteis

### Quanto tempo leva?
- Inicialização: 5 minutos
- Estudo completo: 30 minutos
- Build: 1-2 minutos (primeira vez), 30-60 seg (builds seguintes)
- Customização: 10-20 minutos

### Quanto espaço consome?
- Skill `documentacao-integrada-export`: ~5MB
- Site gerado (`documentacao-html/`): 20-50MB (depende da quantidade de documentação)

### Qual é a curva de aprendizado?
- Básico: 5 minutos
- Avançado: 30 minutos
- Expert: 2 horas

---

## 📈 Próximos Passos Recomendados

1. **Hoje:** Leia [GETTING_STARTED.md](./GETTING_STARTED.md) e execute primeiro build
2. **Semana 1:** Crie 3-5 requisitos com `documentacao-de-software`
3. **Semana 2:** Documente banco com `database-mcp`
4. **Semana 3:** Integre em pipeline CI/CD
5. **Mês 1:** Customize tema, adicione mais documentação

---

**Bem-vindo ao futuro da documentação integrada!** 🚀
