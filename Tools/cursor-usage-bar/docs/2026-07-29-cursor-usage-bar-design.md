# Cursor Usage Bar — Design

Data: 2026-07-29  
Status: aguardando revisão

## Objetivo

Extensão local para o Cursor (compatível VS Code) que mostra na **status bar**:

- percentual de uso do plano incluso no ciclo atual
- gasto **on-demand / excedente** quando existir

Sem pedir senha: usa o token da sessão já logada no Cursor.

## Fora de escopo (v1)

- Painel/webview detalhado
- Publicação no VS Code Marketplace
- Integração com chat do Agent
- Admin API de time / comparação entre membros
- Alterar ou gravar o token no `state.vscdb`

## Localização do projeto

Repositório independente em `d:\projetos\cursor-usage-bar` (fora do Argos).

## Distribuição

1. Empacotar `.vsix` com `vsce package`
2. Publicar no GitHub (código + Release com o `.vsix`)
3. Instalação: Cursor → Extensions → `...` → **Install from VSIX...**

## Arquitetura

```
┌─────────────────┐     lê token      ┌──────────────────┐
│  state.vscdb    │ ───────────────► │  auth.ts         │
│  (Cursor local) │                  └────────┬─────────┘
└─────────────────┘                           │
                                              ▼
┌─────────────────┐     Bearer JWT    ┌──────────────────┐
│  Status Bar UI  │ ◄──────────────── │  usage-api.ts    │
│  + tooltip      │                   │  api2.cursor.sh  │
└─────────────────┘                   └──────────────────┘
```

### Módulos

| Arquivo | Responsabilidade |
|---------|------------------|
| `src/auth.ts` | Localiza `state.vscdb` (Win/macOS/Linux) e lê `cursorAuth/accessToken` (somente leitura) |
| `src/usage-api.ts` | `POST /aiserver.v1.DashboardService/GetCurrentPeriodUsage` |
| `src/format.ts` | Formata texto da barra e tooltip (%, USD) |
| `src/status-bar.ts` | Cria/atualiza `StatusBarItem`, cores, clique = refresh |
| `src/extension.ts` | Ativa extensão, timer de poll, comandos |

## Auth

- Caminhos do `state.vscdb`:
  - Windows: `%APPDATA%\Cursor\User\globalStorage\state.vscdb`
  - macOS: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
  - Linux: `~/.config/Cursor/User/globalStorage/state.vscdb`
- Chave: `cursorAuth/accessToken`
- Leitura via `better-sqlite3` ou `sql.js` (fallback), **read-only**
- Token só em memória; nunca logado em Output Channel em texto completo
- Se ausente: status bar `Cursor: login?` + mensagem pedindo login no Cursor

## API de usage

- Base: `https://api2.cursor.sh`
- Endpoint: `POST /aiserver.v1.DashboardService/GetCurrentPeriodUsage`
- Headers: `Authorization: Bearer <token>`, `Connect-Protocol-Version: 1`, `Content-Type: application/json`
- Body: `{}`
- Valores monetários em **centavos** (dividir por 100)

Campos usados:

- `planUsage.totalPercentUsed` — % na barra
- `planUsage.includedSpend`, `planUsage.limit`, `planUsage.remaining` — tooltip
- `spendLimitUsage.individualUsed` / `totalSpend` — overage quando > 0
- `billingCycleStart` / `billingCycleEnd` — tooltip

Fallback (se Connect RPC falhar): tentar `GET /auth/usage` e exibir requests restantes no formato Enterprise, sem overage em $.

## UI da status bar

| Estado | Texto | Cor |
|--------|-------|-----|
| Uso normal (&lt; 80%) | `Cursor 72%` | default |
| Aviso (80–94%) | `Cursor 88%` | amarelo |
| Crítico (≥ 95%) | `Cursor 97%` | vermelho |
| Com overage | `Cursor 100% · +$12.40` | vermelho |
| Erro / sem login | `Cursor: —` ou `Cursor: login?` | default |

Tooltip (hover):

- % usado e gasto incluso / limite
- On-demand (se houver)
- Período de cobrança
- Última atualização

Clique: refresh imediato.

## Configurações (`package.json` contributes.configuration)

| Chave | Default | Descrição |
|-------|---------|-----------|
| `cursorUsageBar.pollIntervalSeconds` | `300` | Intervalo (mín. 60) |
| `cursorUsageBar.warningPercent` | `80` | Limiar amarelo |
| `cursorUsageBar.criticalPercent` | `95` | Limiar vermelho |

## Comandos

- `cursorUsageBar.refresh` — atualizar agora
- `cursorUsageBar.showOutput` — abrir log de diagnóstico (sem token)

## Segurança

- Sem senha, sem settings de credencial
- Rede apenas para `api2.cursor.sh`
- Código aberto no GitHub para auditoria
- README deixa claro: API não oficial; pode quebrar se a Cursor mudar o endpoint

## Empacotamento

- `package.json` com `engines.vscode` compatível com Cursor
- `publisher` + `name` únicos (ex.: `rmiqueletto.cursor-usage-bar`)
- Script `npm run package` → gera `.vsix`
- README com passos de instalação em PT-BR

## Critérios de sucesso

1. Com Cursor logado, a barra mostra `%` do plano sem pedir senha
2. Com gasto on-demand > 0, aparece `+$X.XX` na barra
3. Outra pessoa instala pelo `.vsix` do Release e vê o uso da **própria** conta logada
4. Sem token/login, mensagem clara — sem crash
