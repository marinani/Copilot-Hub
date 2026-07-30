# Runbook — Instalar e usar no Cursor

Guia passo a passo para colocar a **Cursor Usage Bar** rodando no Cursor Desktop (Windows, macOS ou Linux).

---

## Pré-requisitos

- [ ] Cursor instalado e aberto
- [ ] Conta Cursor **já logada** (Settings → Account / ícone de perfil)
- [ ] Arquivo `.vsix` **ou** este repositório clonado (para gerar o pacote)

Não é necessário digitar senha na extensão. Ela usa a sessão local do Cursor.

---

## Opção A — Instalar pelo `.vsix` (recomendado para quem só quer usar)

### 1. Obter o arquivo

- Baixe `cursor-usage-bar-*.vsix` do **Release** do repositório, **ou**
- Peça o arquivo a quem gerou o pacote, **ou**
- Gere localmente (veja [Opção B](#opção-b--gerar-o-vsix-a-partir-do-código)).

### 2. Instalar no Cursor

1. Abra o Cursor.
2. Vá em **Extensions** (ícone de blocos na barra lateral, ou `Ctrl+Shift+X`).
3. Clique no menu `...` (canto superior direito do painel de Extensions).
4. Escolha **Install from VSIX...**.
5. Selecione o arquivo `cursor-usage-bar-0.1.1.vsix` (ou versão mais nova).
6. Aguarde a mensagem de sucesso.

### 3. Ativar / recarregar

1. `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`).
2. Digite e execute: **Developer: Reload Window**.

### 4. Conferir se funcionou

Na **barra inferior** (status bar), à direita, deve aparecer algo como:

| Esperado | Significado |
|----------|-------------|
| `Cursor 72%` | Uso do plano no ciclo atual |
| `Cursor 100% · +$12.40` | Plano esgotado + gasto on-demand |
| `Cursor: login?` | Cursor sem sessão — faça login e clique na barra |

- Passe o mouse sobre o item para ver o tooltip (detalhes: ciclo, %, overage).
- Clique no item para forçar atualização.
- A barra **atualiza sozinha a cada 5 minutos** (configurável em `cursorUsageBar.pollIntervalSeconds`, mín. 60).

### 5. Comandos úteis

`Ctrl+Shift+P` e busque:

| Comando | Função |
|---------|--------|
| `Cursor Usage Bar: Atualizar agora` | Refresh manual |
| `Cursor Usage Bar: Abrir log` | Diagnóstico (sem exibir o token completo) |

---

## Opção B — Gerar o `.vsix` a partir do código

Use se você clonou o repo e quer empacotar / instalar você mesmo.

### 1. Requisitos de build

- Node.js 18+ (`node -v`)
- npm (`npm -v`)

### 2. Build e pacote

No PowerShell ou terminal:

```powershell
cd d:\projetos\cursor-usage-bar
npm install
npm run compile
npx vsce package
```

Saída esperada: arquivo na raiz, por exemplo:

`cursor-usage-bar-0.1.1.vsix`

### 3. Instalar o pacote gerado

```powershell
cursor --install-extension .\cursor-usage-bar-0.1.1.vsix
```

Se o CLI `cursor` não existir no PATH, use a Opção A (Install from VSIX pela UI).

Depois: **Developer: Reload Window**.

### 4. (Opcional) Smoke test sem abrir a UI

Valida token local + API:

```powershell
cd d:\projetos\cursor-usage-bar
npm run compile
node -e "const { getAccessToken } = require('./out/auth'); const { fetchPeriodUsage } = require('./out/usage-api'); const { buildPresentation } = require('./out/format'); (async () => { const t = await getAccessToken(); const u = await fetchPeriodUsage(t); console.log(buildPresentation(u, { warningPercent: 80, criticalPercent: 95, updatedAt: new Date() }).text); })().catch(e => { console.error(e.message); process.exit(1); });"
```

Exemplo de saída OK: `Cursor 100% · +$106.58`

---

## Compartilhar com outras pessoas

1. Faça push deste repositório no GitHub.
2. Em **Releases** → **Create a new release**:
   - Tag: `v0.1.1`
   - Anexe o arquivo `cursor-usage-bar-0.1.1.vsix`
3. No README / Release notes, cole o link deste runbook e diga:

> Baixe o `.vsix` → Extensions → `...` → Install from VSIX → Reload Window.

Cada pessoa verá o uso da **própria** conta logada no Cursor dela.

---

## Troubleshooting

| Sintoma | O que fazer |
|---------|-------------|
| `Cursor: login?` | Faça login no Cursor; clique na barra para refresh |
| `Cursor: —` | Abra o log (`Cursor Usage Bar: Abrir log`) e veja o erro |
| Nada na status bar | Confirme que a extensão está **Enabled** em Extensions; Reload Window |
| Erro de API / 401 | Token expirado — relogue no Cursor e atualize |
| Extensão não instala | Use Cursor Desktop (não só o CLI); arquivo `.vsix` íntegro |

Arquivo de estado lido (somente leitura):

| SO | Caminho |
|----|---------|
| Windows | `%APPDATA%\Cursor\User\globalStorage\state.vscdb` |
| macOS | `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` |
| Linux | `~/.config/Cursor/User/globalStorage/state.vscdb` |

---

## Configurações (opcional)

`Ctrl+,` → busque `Cursor Usage Bar`:

| Setting | Default | Descrição |
|---------|---------|-----------|
| `cursorUsageBar.pollIntervalSeconds` | `300` | Intervalo de refresh (mín. 60) |
| `cursorUsageBar.warningPercent` | `80` | Fica amarelo a partir deste % |
| `cursorUsageBar.criticalPercent` | `95` | Fica vermelho a partir deste % |

---

## Aviso de segurança / API

- A extensão **não pede senha**.
- Só fala com `https://api2.cursor.sh`.
- A API de usage da Cursor **não é oficial**; pode mudar e exigir atualização da extensão.
