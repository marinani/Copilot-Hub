# Verification: Fluxo de Verificação de Saída

Alguns ambientes nativos de design-agent (como Claude.ai Artifacts) têm um `fork_verifier_agent` embutido que usa subagent com iframe para capturar screenshots. Na maioria dos ambientes de agente (Claude Code / Codex / Cursor / Trae / etc.) esse recurso não existe — use Playwright manualmente para cobrir os mesmos cenários de verificação.

## Lista de Verificação

Sempre que produzir um HTML, siga esta lista:

### 1. Verificação de Renderização no Navegador (obrigatório)

O mais básico: **o HTML abre?** No Windows:

```bash
start chrome "c:/caminho/para/seu/design.html"
```

Ou use Playwright para capturar screenshot (próxima seção).

### 2. Verificação de Erros no Console

O problema mais comum em arquivos HTML é erro de JS causando tela branca. Execute com Playwright:

```bash
python ~/.claude/skills/claude-design/scripts/verify.py caminho/para/design.html
```

Este script:

1. Abre o HTML com headless chromium
2. Salva screenshot no diretório do projeto
3. Captura erros do console
4. Reporta o status

Veja detalhes em `scripts/verify.py`.

### 3. Verificação em Múltiplos Viewports

Se for design responsivo, capture em vários viewports:

```bash
python verify.py design.html --viewports 1920x1080,1440x900,768x1024,375x667
```

### 4. Verificação de Interação

Tweaks, animações, alternância de botões — o screenshot estático padrão não mostra isso. **Sugira que o usuário abra no navegador e clique em tudo**, ou use gravação de tela com Playwright:

```python
page.video.record('interacao.mp4')
```

### 5. Verificação Slide a Slide

Para HTML do tipo Deck, capture slide por slide:

```bash
python verify.py deck.html --slides 10  # captura os 10 primeiros slides
```

Gera `deck-slide-01.png`, `deck-slide-02.png`... para visualização rápida.

## Configuração do Playwright

Primeiro uso requer:

```bash
# Se ainda não instalou
npm install -g playwright
npx playwright install chromium

# Ou versão Python
pip install playwright
playwright install chromium
```

Se o usuário já tiver Playwright instalado globalmente, use diretamente.

## Boas Práticas de Screenshot

### Capturar página completa

```python
page.screenshot(path='completo.png', full_page=True)
```

### Capturar viewport

```python
page.screenshot(path='viewport.png')  # padrão: apenas área visível
```

### Capturar elemento específico

```python
element = page.query_selector('.hero-section')
element.screenshot(path='hero.png')
```

### Screenshot em alta resolução

```python
page = browser.new_page(device_scale_factor=2)  # retina
```

### Aguardar animações antes de capturar

```python
page.wait_for_timeout(2000)  # espera 2 segundos para animações estabilizarem
page.screenshot(...)
```

## Enviando Screenshots para o Usuário

### Abrir screenshot local diretamente

```bash
start screenshot.png
```

O usuário verá no Preview / Figma / VSCode / navegador.

### Upload para compartilhar link

Se precisar mostrar para colaboradores remotos (ex: Slack/Feishu/WeChat), peça ao usuário para usar sua ferramenta de upload ou MCP:

```bash
python ~/Documents/escrita/ferramentas/upload_imagem.py screenshot.png
```

Retorna um link permanente do ImgBB, que pode ser colado em qualquer lugar.

## Quando a Verificação Falha

### Página em Branco

Com certeza há erro no console. Verifique primeiro:

1. Se o integrity hash da script tag React+Babel está correto (veja `react-setup.md`)
2. Se há conflito de nome com `const styles = {...}`
3. Se componentes entre arquivos foram exportados para `window`
4. Erro de sintaxe JSX (babel.min.js não reporta erro; troque para babel.js versão não minificada)

### Animação Travando

- Grave um trecho com a aba Performance do Chrome DevTools
- Procure por layout thrashing (reflow frequente)
- Priorize `transform` e `opacity` para animações (aceleradas por GPU)

### Fonte Incorreta

- Verifique se a URL do `@font-face` está acessível
- Verifique as fontes de fallback
- Fontes chinesas carregam devagar: mostre fallback primeiro, troque após carregamento

### Layout Desalinhado

- Verifique se `box-sizing: border-box` está aplicado globalmente
- Verifique o reset `* { margin: 0; padding: 0 }`
- No Chrome DevTools, ative gridlines para ver o layout real

## Verificação = o Segundo Olhar do Designer

**Sempre revise você mesmo**. Ao escrever código com IA, frequentemente aparecem:

- Coisas que parecem certas mas têm bugs de interação
- Screenshot estático bom, mas ao scrollar desalinha
- Tela larga bonita, mas tela estreita quebra
- Modo escuro esquecido de testar
- Após alternar Tweaks, alguns componentes não respondem

**1 minuto de verificação no final pode economizar 1 hora de retrabalho**.

## Comandos Comuns de Verificação

```bash
# Básico: abrir + screenshot + capturar erros
python verify.py design.html

# Múltiplos viewports
python verify.py design.html --viewports 1920x1080,375x667

# Múltiplos slides
python verify.py deck.html --slides 10

# Saída para diretório específico
python verify.py design.html --output ./screenshots/

# headless=false, abre navegador real para você ver
python verify.py design.html --show
```
