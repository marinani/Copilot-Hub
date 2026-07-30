# 🚀 Guia de Inicialização Rápida

## documentacao-integrada-export em 5 minutos

### ✅ Pre-requisitos (1 min)

Certifique-se de ter:

- [x] Python 3.7+ instalado (`python --version`)
- [x] PowerShell 5.1+ (Windows)
- [x] `documentacao/` como pasta na raiz do projeto
- [x] Artefatos da skill `documentacao-de-software` (requisitos)
- [x] Artefatos da skill `database-mcp` (banco de dados)

### 📋 Passo 1: Estruturar a Documentação (1-2 min)

```
seu-projeto/
└── documentacao/
    ├── README.md                          ← Criar se não existir
    ├── banco_dados/
    │   └── discovery-database.yml         ← Gerado por database-mcp
    └── processo_unificado/
        └── artefatos_aprovados/
            ├── detalhamento_requisitos/
            │   ├── req-0001-login.md
            │   └── ...
            ├── documentacao_api/
            │   ├── api-usuarios.md
            │   └── ...
            └── visao/
                └── vis-001-escopo.md
```

**Dica:** Se não tiver artefatos ainda, crie um mínimo com skill `documentacao-de-software` antes.

### 🔨 Passo 2: Executar o Build (1 min)

```powershell
# Navegue até a raiz do seu projeto
cd c:\seu-projeto

# Execute o script
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1
```

**Primeira execução pode levar 1-2 minutos** (instalação de dependências pip).

### 🌐 Passo 3: Abrir o Site (30 seg)

```powershell
# Abrir no navegador padrão
start "documentacao-html\index.html"
```

Ou copie/cole no navegador:

```
file:///C:/seu-projeto/documentacao-html/index.html
```

### ✨ Resultado esperado

```
✅ Documentação integrada gerada com sucesso!

📁 Localização da documentação:
   C:\seu-projeto\documentacao-html

🌐 Para visualizar, abra no navegador:
   file:///C:/seu-projeto/documentacao-html/index.html

✅ Resumo do build:
   ✓ Índice integrado gerado
   ✓ Matrizes de rastreabilidade criadas
   ✓ Diagramas PlantUML processados
   ✓ Site HTML estático em documentacao-html
   ✓ Navegação full-text ativa
```

---

## 🎯 Próximos Passos

### 1. Personalizar Logo e Cor

Edite o arquivo:

```
.github/documentacao-integrada-export/assets/logo.svg
.github/documentacao-integrada-export/assets/css/integrated-theme.css
```

Rode build novamente.

### 2. Adicionar Mais Requisitos

Crie arquivos em:

```
documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/
```

Padrão de nome:

```
req-0002-cadastro-usuario.md
req-0003-autenticacao-oauth.md
```

Use a skill `documentacao-de-software` para garantir estrutura correta.

### 3. Documentar o Banco

Execute a skill `database-mcp`:

```powershell
# A skill database-mcp irá gerar:
# - discovery-database.yml
# - DADOS-01-ER.md
# - DADOS-05-MAPA-DADOS.md
# - DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md
```

### 4. Explorar Rastreabilidade

Após o build, abra:

```
documentacao-html/rastreabilidade/
```

Navegue por:

- **01-requisitos-tabelas.md** — Quais tabelas cada requisito toca
- **02-apis-procedures.md** — Quais procedures cada endpoint chama
- **04-matriz-risco-integrada.md** — Consolidação de riscos

---

## 🐛 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| ❌ "mkdocs: command not found" | `pip install "mkdocs>=1.5,<2" mkdocs-material` |
| ❌ "discovery-database.yml not found" | Execute `database-mcp` skill antes |
| ❌ "No requirements found" | Crie `req-*.md` em `detalhamento_requisitos/` |
| ❌ "Connection refused" (PlantUML) | Verifique conexão internet; serve usa plantuml.com |
| ⚠️  Build muito lento | Diagramas ER grandes levam tempo; normal |

---

## 📚 Documentação Completa

Para detalhes avançados, consulte:

- [SKILL.md](./SKILL.md) — Documentação completa
- [README.md](./README.md) — Guia de referência
- [config-docs-integradas.yaml.example](./config-docs-integradas.yaml.example) — Customizações

---

## 🎓 Exemplo Completo

### 1. Criar um Requisito

Arquivo: `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/req-0001-login.md`

```markdown
# REQ-0001: Autenticação de Usuário

## Objetivo

Permitir que usuários façam login na plataforma usando e-mail e senha.

## Descrição

Quando um usuário acessa a página de login (`/login`), ele preenche e-mail
e senha, e clica em "Entrar". O sistema valida as credenciais consultando
a tabela `users` via função `sp_authenticate_user`.

## Critérios de Aceitação

```gherkin
Cenário: Login com sucesso
  Dado que o usuário tem credenciais válidas
  Quando preenche e-mail e senha
  E clica em "Entrar"
  Então é redirecionado para a dashboard
```

## Impactos Técnicos

- **Tabelas:** `users`, `sessions`, `login_history`
- **Procedures:** `sp_authenticate_user`, `sp_log_login`
- **Endpoints:** `POST /auth/login`
```

### 2. Executar Build

```powershell
.\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1
```

### 3. Visualizar Resultado

Abra `documentacao-html/index.html` e navegue:

```
Home
├── Requisitos
│   └── REQ-0001: Autenticação de Usuário
│       └── Tabelas Referenciadas: users, sessions, login_history
└── Rastreabilidade
    └── Matriz: Requisitos ↔ Tabelas
        └── REQ-0001 → [users, sessions, login_history]
```

TODO: Links automáticos para documentação de tabelas.

---

## 💡 Dicas Profissionais

1. **Rode o build após cada mudança em requisitos**
   ```powershell
   .\.github\documentacao-integrada-export\scripts\build-integrated-docs.ps1
   ```

2. **Use git para versionamento**
   ```bash
   git add documentacao/
   git commit -m "docs: novo requisito de login"
   ```

3. **Revise a rastreabilidade regularmente**
   - Confirme que todos os requisitos têm referência a tabelas/procedures
   - Valide a matriz de risco integrada

4. **Customizar CSS para se alinhar com brand**
   - Edite `assets/css/integrated-theme.css`
   - Use variáveis CSS para cores

---

## 🆘 Suporte

Dúvidas? Consulte a documentação completa:

- [SKILL.md](./SKILL.md)
- [README.md](./README.md)

Ou verifique as skills relacionadas:

- [documentacao-de-software](../.github/documentacao-de-software/SKILL.md)
- [database-mcp](../.github/database-mcp/SKILL.md)
- [discovery-html-export](../.github/discovery-html-export/SKILL.md)

---

**Parabéns!** 🎉 Você tem uma documentação integrada, navegável e rastreável!
