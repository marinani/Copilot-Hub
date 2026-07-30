# Cursor Usage Bar

Desenvolvido por **Rafael Miqueletto**.

Mostra na **barra de status** do Cursor o uso do plano (`%`) e o gasto **on-demand/excedente** quando houver.

Não pede senha: usa o token da sessão já logada no Cursor (leitura local do `state.vscdb`).

## Como instalar

Siga o runbook completo:

**[INSTALAR.md](./INSTALAR.md)** — instalação pelo `.vsix`, build local, smoke test, compartilhar no GitHub e troubleshooting.

Resumo rápido:

1. Baixe o `.vsix` (Release) ou gere com `npm install && npm run compile && npx vsce package`
2. Cursor → **Extensions** → `...` → **Install from VSIX...**
3. `Ctrl+Shift+P` → **Developer: Reload Window**
4. Confira a barra inferior: `Cursor 72%` ou `Cursor 100% · +$12.40`

## O que aparece

| Situação | Exemplo |
|----------|---------|
| Uso normal | `Cursor 72%` |
| Aviso (≥ 80%) | `Cursor 88%` (amarelo) |
| Crítico (≥ 95%) | `Cursor 97%` (vermelho) |
| Com excedente | `Cursor 100% · +$12.40` (vermelho) |
| Sem login | `Cursor: login?` |

- **Hover** na barra: detalhes (incluso, limite, on-demand, ciclo).
- **Clique** na barra: atualiza agora.
- Comando: `Cursor Usage Bar: Atualizar agora`.

## Atualização automática

A barra **atualiza sozinha a cada 5 minutos** (300 segundos) por padrão.

Também atualiza:
- ao abrir ou recarregar o Cursor
- ao clicar na barra
- pelo comando `Cursor Usage Bar: Atualizar agora`

Para mudar o intervalo: Settings → `cursorUsageBar.pollIntervalSeconds` (mínimo 60).

## Privacidade

- Token lido só do disco local; não é enviado a terceiros.
- Única rede: `https://api2.cursor.sh` (API de usage da Cursor).
- Token nunca é impresso completo no log.

## Aviso

A API de usage da Cursor **não é oficial/pública**. Pode mudar e a extensão pode precisar de atualização.

## Configurações

| Setting | Default | Descrição |
|---------|---------|-----------|
| `cursorUsageBar.pollIntervalSeconds` | `300` | Intervalo de refresh (mín. 60) |
| `cursorUsageBar.warningPercent` | `80` | Limiar amarelo |
| `cursorUsageBar.criticalPercent` | `95` | Limiar vermelho |
