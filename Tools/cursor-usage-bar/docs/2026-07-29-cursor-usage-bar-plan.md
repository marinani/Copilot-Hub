# Cursor Usage Bar — Implementation Plan

> **For agentic workers:** implementar task-by-task. Steps usam checkbox.

**Goal:** Extensão Cursor/VS Code que mostra na status bar o % do plano + overage on-demand, usando o token local.

**Architecture:** `auth.ts` lê `state.vscdb`; `usage-api.ts` chama Connect RPC; `format.ts` + `status-bar.ts` renderizam; `extension.ts` orquestra poll/comandos.

**Tech Stack:** TypeScript, VS Code Extension API, sql.js, vsce

---

### Task 1: Scaffold do projeto
- [x] package.json, tsconfig, .gitignore, README

### Task 2: Auth + API + Format
- [x] src/auth.ts, usage-api.ts, format.ts (+ testes unitários de format se possível)

### Task 3: Status bar + activation
- [x] src/status-bar.ts, extension.ts

### Task 4: Empacotar VSIX
- [x] npm install, compile, vsce package
