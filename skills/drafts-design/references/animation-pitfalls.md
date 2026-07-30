# Animation Pitfalls: Armadilhas e Regras de Animações HTML

Bugs mais comuns ao fazer animações e como evitá-los. Cada regra vem de um caso real de falha.

Leia isto antes de escrever animações — economiza uma rodada de iteração.

## 1. Layout de Camadas — `position: relative` é Obrigação Padrão

**A armadilha**: Um elemento sentence-wrap envolvia 3 bracket-layers (`position: absolute`). Não foi definido `position: relative` no sentence-wrap, então os brackets absolute usaram `.canvas` como referência, flutuando 200px para fora da tela.

**Regra**:

- Qualquer contêiner que contenha filhos com `position: absolute` **deve** ter `position: relative` explícito
- Mesmo que visualmente não precise de "deslocamento", escreva `position: relative` como âncora do sistema de coordenadas
- Se você está escrevendo `.parent { ... }` e seus filhos têm `.child { position: absolute }`, adicione relative ao parent por instinto

**Verificação rápida**: Para cada `position: absolute`, suba nos ancestrais e garanta que o ancestral positioned mais próximo é o sistema de coordenadas que você _deseja_.

## 2. Armadilha de Caracteres — Não Dependa de Unicode Raro

**A armadilha**: Queria usar `␣` (U+2423 OPEN BOX) para visualizar "token de espaço". Noto Serif SC / Cormorant Garamond não têm esse glifo, renderizando como espaço vazio/quadrado — o público não via nada.

**Regra**:

- **Cada caractere que aparece na animação deve existir na fonte escolhida**
- Lista negra de caracteres raros comuns: `␣ ␀ ␐ ␋ ␨ ↩ ⏎ ⌘ ⌥ ⌃ ⇧ ␦ ␖ ␛`
- Para expressar metacaracteres como "espaço / enter / tab", use **caixas semânticas construídas com CSS**:
  ```html
  <span class="space-key">Space</span>
  ```
  ```css
  .space-key {
    display: inline-flex;
    padding: 4px 14px;
    border: 1.5px solid var(--accent);
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.3em;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  ```
- Emojis também precisam de verificação: alguns emojis fora da fonte Noto Emoji podem cair em quadrados cinza — use `emoji` font-family ou SVG

## 3. Template Grid/Flex Orientado a Dados

**A armadilha**: Código com `const N = 6` tokens, mas CSS fixo `grid-template-columns: 80px repeat(5, 1fr)`. O 6º token não tinha coluna, toda a matriz ficou desalinhada.

**Regra**:

- Quando a contagem vem de um array JS (`TOKENS.length`), o template CSS também deve ser orientado a dados
- Opção A: Use variáveis CSS injetadas do JS
  ```js
  el.style.setProperty("--cols", N);
  ```
  ```css
  .grid {
    grid-template-columns: 80px repeat(var(--cols), 1fr);
  }
  ```
- Opção B: Use `grid-auto-flow: column` para o navegador expandir automaticamente
- **Desative a combinação "número fixo + constante JS"** — se N mudar, o CSS não atualiza junto

## 4. Transição Descontínua — Troca de Cena Deve Ser Contínua

**A armadilha**: Entre zoom1 (13-19s) → zoom2 (19.2-23s), a frase principal já estava oculta. zoom1 fade out (0.6s) + zoom2 fade in (0.6s) + stagger delay (0.2s+) = cerca de 1 segundo de tela em branco. O público achou que a animação tinha travado.

**Regra**:

- Ao alternar cenas consecutivas, fade out e fade in devem **se sobrepor**, não um desaparecer completamente antes do próximo começar

  ```js
  // Ruim:
  if (t >= 19) hideZoom("zoom1"); // 19.0s out
  if (t >= 19.4) showZoom("zoom2"); // 19.4s in → 0.4s de espaço vazio

  // Bom:
  if (t >= 18.6) hideZoom("zoom1"); // Começa fade out 0.4s antes
  if (t >= 18.6) showZoom("zoom2"); // Fade in simultâneo (cross-fade)
  ```

- Ou use um "elemento âncora" (como a frase principal) como conexão visual entre cenas, exibindo-o brevemente durante a transição
- Calcule a duração da transição CSS para evitar que uma transição não terminada dispare a próxima

## 5. Princípio Pure Render — Estado da Animação Deve Ser Buscável (seek)

**A armadilha**: Usou `setTimeout` + `fireOnce(key, fn)` em cadeia para disparar estados de animação. Funcionava na reprodução normal, mas ao fazer gravação quadro a quadro/buscar (seek) para um ponto arbitrário no tempo, os setTimeout anteriores já tinham executado e não podiam "voltar ao passado".

**Regra**:

- A função `render(t)` idealmente deve ser **pure function**: dado t, produz um único estado do DOM
- Se efeitos colaterais são necessários (como alternância de classes), use um conjunto `fired` com reset explícito:
  ```js
  const fired = new Set();
  function fireOnce(key, fn) {
    if (!fired.has(key)) {
      fired.add(key);
      fn();
    }
  }
  function reset() {
    fired.clear(); /* limpa todas as classes .show */
  }
  ```
- Exponha `window.__seek(t)` para Playwright / depuração:
  ```js
  window.__seek = (t) => {
    reset();
    render(t);
  };
  ```
- setTimeout relacionados à animação não devem ultrapassar >1 segundo, senão ao buscar (seek) para trás, a ordem se perde

## 6. Medir Antes da Fonte Carregar = Medir Errado

**A armadilha**: Assim que o DOMContentLoaded disparava, chamava `charRect(idx)` para medir a posição dos brackets. A fonte ainda não tinha carregado — a largura de cada caractere era da fonte fallback, todas as posições erradas. Quando a fonte carregava (~500ms depois), os brackets ainda estavam com `left: Xpx` antigo, permanentemente deslocados.

**Regra**:

- Qualquer código de layout que dependa de medição do DOM (`getBoundingClientRect`, `offsetWidth`) **deve** estar dentro de `document.fonts.ready.then()`
  ```js
  document.fonts.ready.then(() => {
    requestAnimationFrame(() => {
      buildBrackets(...);  // Fonte pronta, medição precisa
      tick();              // Animação começa
    });
  });
  ```
- Um `requestAnimationFrame` extra dá ao navegador um frame para submeter o layout
- Se usar Google Fonts CDN, `<link rel="preconnect">` acelera o carregamento inicial

## 7. Preparação para Gravação — Deixe Gatilhos para Exportação de Vídeo

**A armadilha**: Playwright `recordVideo` padrão 25fps, começa a gravar desde a criação do context. Os primeiros 2 segundos de carregamento da página e fontes são gravados. O vídeo entregue tinha 2 segundos de tela em branco/flash branco no início.

**Regra**:

- Forneça a ferramenta `render-video.js` para processar: warmup navigate → reload reinicia animação → aguarda duração → ffmpeg trim head + converte para H.264 MP4
- **O frame 0** da animação deve ser o estado inicial completo com layout finalizado (não em branco ou carregando)
- Quer 60fps? Use ffmpeg `minterpolate` no pós-processamento, não confie na taxa de quadros do navegador
- Quer GIF? Paleta em dois estágios (`palettegen` + `paletteuse`), para animação de 30s 1080p consegue comprimir para 3MB

Consulte `video-export.md` para obter a forma completa de chamada dos scripts.

## 8. Exportação em Lote — Diretório tmp Deve Incluir PID para Evitar Conflito Concorrente

**A armadilha**: 3 processos `render-video.js` gravando 3 HTMLs em paralelo. Como TMP_DIR usava apenas `Date.now()` para nomear, os 3 processos iniciados no mesmo milissegundo compartilhavam o mesmo diretório tmp. O primeiro processo a terminar limpava o tmp, os outros dois liam o diretório e recebiam `ENOENT`, todos quebravam.

**Regra**:

- Qualquer diretório temporário que possa ser compartilhado por múltiplos processos deve ser nomeado com **PID ou sufixo aleatório**:
  ```js
  const TMP_DIR = path.join(
    DIR,
    ".video-tmp-" + Date.now() + "-" + process.pid,
  );
  ```
- Se realmente quiser paralelizar múltiplos arquivos, use `&` + `wait` do shell em vez de fork em um único script node
- Ao gravar múltiplos HTMLs em lote, abordagem conservadora: **serial** (até 2 pode paralelo, 3+ faça fila)

## 9. Gravação com Barra de Progresso/Botão Repetir — Elementos Chrome Poluem o Vídeo

**A armadilha**: O HTML da animação tinha barra de progresso `.progress`, botão `.replay`, timestamp `.counter` para facilitar a depuração humana. Ao gravar MP4, esses elementos apareciam na parte inferior do vídeo, como se as ferramentas de desenvolvedor tivessem sido capturadas junto.

**Regra**:

- No HTML, elementos "chrome" para humanos (progress bar / replay button / footer / masthead / counter / phase labels) e o conteúdo do vídeo devem ser gerenciados separadamente
- **Convenção de classe** `.no-record`: qualquer elemento com essa classe é automaticamente ocultado pelo script de gravação
- No lado do script (`render-video.js`), CSS padrão é injetado para ocultar classes chrome comuns:
  ```
  .progress .counter .phases .replay .masthead .footer .no-record [data-role="chrome"]
  ```
- Use `addInitScript` do Playwright (é injetado antes de cada navegação, reload também funciona)
- Para ver o HTML original (com chrome), adicione a flag `--keep-chrome`

## 10. Repetição da Animação nos Primeiros Segundos da Gravação — Vazamento de Frame Warmup

**A armadilha**: O fluxo antigo do `render-video.js`: `goto → wait fonts 1.5s → reload → wait duration`. A gravação começava desde a criação do context, a animação já tinha reproduzido um trecho durante o warmup, depois reload reiniciava do 0. O resultado: os primeiros segundos do vídeo eram "meio da animação + transição + animação do 0", sensação de repetição.

**Regra**:

- **Warmup e Record devem usar contexts independentes**:
  - Warmup context (sem opção `recordVideo`): apenas carrega url, espera fontes, depois fecha
  - Record context (com `recordVideo`): começa em estado fresco, animação grava a partir de t=0
- ffmpeg `-ss trim` só corta uma pequena latência de startup do Playwright (~0.3s), **não** pode ser usado para mascarar frames de warmup; a origem deve estar limpa
- Fechar o context de gravação = arquivo webm é escrito no disco, esta é uma restrição do Playwright
- Padrão de código relacionado:

  ```js
  // Fase 1: warmup (descartável)
  const warmupCtx = await browser.newContext({ viewport });
  const warmupPage = await warmupCtx.newPage();
  await warmupPage.goto(url, { waitUntil: "networkidle" });
  await warmupPage.waitForTimeout(1200);
  await warmupCtx.close();

  // Fase 2: record (fresco)
  const recordCtx = await browser.newContext({ viewport, recordVideo });
  const page = await recordCtx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(DURATION * 1000);
  await page.close();
  await recordCtx.close();
  ```

## 11. Não Desenhe "Falso Chrome" na Cena — Player UI Decorativo Colide com Chrome Real

**A armadilha**: A animação usava componente `Stage`, que já tem scrubber + timecode + botão de pausa (pertencem ao chrome `.no-record`, ocultados automaticamente na exportação). Eu também desenhei na parte inferior uma "barra de progresso decorativa estilo revista" com `00:60 ──── CLAUDE-DESIGN / ANATOMY`. **Resultado**: o usuário via duas barras de progresso — uma do controle Stage, outra decorativa que eu desenhei. Colisão visual total, considerado bug. "O que é essa barra de progresso dentro do vídeo?"

**Regra**:

- Stage já fornece: scrubber + timecode + botões pausar/repetir. **Não desenhe dentro da cena** indicadores de progresso, timecode atual, barra de créditos, contador de capítulos — ou colidem com o chrome, ou são filler slop (violam o princípio "earn its place").
- "Sensação de página", "sensação de revista", "barra de créditos no rodapé" — esses **desejos decorativos** são fillers de alta frequência que a IA adiciona automaticamente. Cada um que aparece deve ser questionado: ele realmente transmite informação insubstituível? Ou apenas preenche espaço vazio?
- Se você realmente acredita que uma barra inferior deve existir (ex: o tema da animação é sobre player UI), então ela deve ser **narrativamente necessária** e **visualmente distinta do scrubber do Stage** (posição diferente, forma diferente, tom diferente).

**Teste de pertinência do elemento** (cada elemento desenhado no canvas deve responder):

| Pertence a                                    | Tratamento                                         |
| --------------------------------------------- | -------------------------------------------------- |
| Conteúdo narrativo de uma cena                | OK, mantenha                                       |
| Chrome global (controle/depuração)            | Adicione classe `.no-record`, oculte na exportação |
| **Não pertence a nenhuma cena, nem é chrome** | **Remova**. É um órfão, certamente filler slop     |

**Auto-verificação (3 segundos antes de entregar)**: Tire um print estático e pergunte-se:

- Há algo na cena que "parece UI de player de vídeo" (barra de progresso horizontal, timecode, formato de botão de controle)?
- Se sim, remover prejudica a narrativa? Se não, remova.
- A mesma informação (progresso/tempo/créditos) aparece duas vezes? Junte em um único chrome.

**Contraexemplos**: Desenhar `00:42 ──── PROJECT NAME` no rodapé, contagem de capítulo "CH 03 / 06" no canto inferior direito, número de versão "v0.3.1" na borda — todos são pseudo-chrome filler.

## 12. Espaço em Branco no Início da Gravação + Deslocamento do Ponto Inicial — A Tripla Armadilha `__ready` × tick × lastTick

**Armadilha (A · Espaço em branco inicial)**: Animação de 60s exportada como MP4, os primeiros 2-3 segundos eram página em branco. `ffmpeg --trim=0.3` não cortava.

**Armadilha (B · Deslocamento do ponto inicial, acidente real em 2026-04-20)**: Vídeo de 24s exportado, o usuário percebeu "o vídeo só começa a mostrar o primeiro frame aos 19s". Na verdade, a animação começou a gravar em t=5, gravou até t=24, depois fez loop para t=0, gravou mais 5s até o fim — então os últimos 5 segundos do vídeo eram o verdadeiro início da animação.

**Causa raiz** (ambas as armadilhas compartilham a mesma causa raiz):

Playwright `recordVideo` começa a escrever WebM no momento de `newContext()`, quando Babel/React/fontes ainda estão carregando, totalizando L segundos (2-6s). O script de gravação espera `window.__ready = true` como âncora "a animação começa aqui" — ele e o `time = 0` da animação devem estar estritamente pareados. Dois erros comuns:

| Erro                                                                                          | Sintoma                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__ready` definido em `useEffect` ou durante setup síncrono (antes do primeiro frame do tick) | Script de gravação acha que animação começou, mas WebM ainda está gravando página em branco → **espaço em branco inicial**                                                                  |
| `lastTick = performance.now()` do tick inicializado no **top-level do script**                | O tempo de carregamento L das fontes é contado no `dt` do primeiro frame, `time` pula para L instantaneamente → gravação inteira atrasada em L segundos → **deslocamento do ponto inicial** |

**✅ Template starter tick correto** (animações manuais DEVEM usar este esqueleto):

```js
// ━━━━━━ state ━━━━━━
let time = 0;
let playing = false; // ❗ Não reproduz por padrão, espera fontes ready
let lastTick = null; // ❗ Sentinel — primeiro frame do tick força dt=0 (não use performance.now())
const fired = new Set();

// ━━━━━━ tick ━━━━━━
function tick(now) {
  if (lastTick === null) {
    lastTick = now;
    window.__ready = true; // ✅ Pareamento: "início da gravação" e "animação t=0" no mesmo frame
    render(0); // Renderiza novamente para garantir DOM pronto (fontes já ready)
    requestAnimationFrame(tick);
    return;
  }
  const dt = (now - lastTick) / 1000; // Após o primeiro frame, dt começa a avançar
  lastTick = now;

  if (playing) {
    let t = time + dt;
    if (t >= DURATION) {
      t = window.__recording ? DURATION - 0.001 : 0; // Não faz loop durante gravação, mantém 0.001s para preservar último frame
      if (!window.__recording) fired.clear();
    }
    time = t;
    render(time);
  }
  requestAnimationFrame(tick);
}

// ━━━━━━ boot ━━━━━━
// Não chame rAF imediatamente no top-level — espere fontes carregarem
document.fonts.ready.then(() => {
  render(0); // Desenha a tela inicial primeiro (fontes já carregadas)
  playing = true;
  requestAnimationFrame(tick); // Primeiro tick pareia __ready + t=0
});

// ━━━━━━ Interface seek (para correção defensiva do render-video) ━━━━━━
window.__seek = (t) => {
  fired.clear();
  time = t;
  lastTick = null;
  render(t);
};
```

**Por que este template está correto**:

| Etapa                                          | Por que é necessário                                                                                                  |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `lastTick = null` + `return` no primeiro frame | Evita que os L segundos de "carregamento do script até primeira execução do tick" sejam contados no tempo da animação |
| `playing = false` como padrão                  | Durante carregamento das fontes, mesmo que `tick` execute, não avança `time`, evitando renderização desalinhada       |
| `__ready` definido no primeiro frame do tick   | Script de gravação começa a contar a partir deste momento, e a imagem correspondente é o verdadeiro t=0 da animação   |
| `document.fonts.ready.then(...)` inicia o tick | Evita medição com largura de fonte fallback e salto de fonte no primeiro frame                                        |
| `window.__seek` existe                         | Permite que `render-video.js` corrija ativamente — segunda linha de defesa                                            |

**Defesa correspondente no lado do script de gravação**:

1. `addInitScript` injeta `window.__recording = true` (antes do page goto)
2. `waitForFunction(() => window.__ready === true)`, registra o deslocamento como ffmpeg trim
3. **Extra**: após `__ready`, execute ativamente `page.evaluate(() => window.__seek && window.__seek(0))` para forçar zeragem de possível desvio de time no HTML — esta é a segunda linha de defesa contra HTMLs que não seguem rigorosamente o template starter

**Método de verificação**: Após exportar MP4

```bash
ffmpeg -i video.mp4 -ss 0 -vframes 1 frame-0.png
ffmpeg -i video.mp4 -ss $DURATION-0.1 -vframes 1 frame-end.png
```

O primeiro frame deve ser o estado inicial da animação em t=0 (não no meio, não preto), o último frame deve ser o estado final da animação (não algum momento do segundo loop).

**Implementação de referência**: O componente Stage em `assets/animations.jsx` e `scripts/render-video.js` já seguem este protocolo. HTMLs escritos à mão DEVEM usar o template starter tick — cada linha é uma defesa contra bugs específicos.

## 13. Proibir Loop Durante Gravação — Sinal `window.__recording`

**A armadilha**: O Stage da animação tem `loop=true` por padrão (para facilitar visualização no navegador). `render-video.js` gravava por `duration` segundos e ainda esperava 300ms de buffer antes de parar — esses 300ms faziam o Stage entrar no próximo ciclo. ffmpeg `-t DURATION` ao capturar, os últimos 0.5-1s caíam no próximo loop — o final do vídeo voltava subitamente ao primeiro frame (Scene 1), o usuário achava que era um bug.

**Causa raiz**: Não havia protocolo de handshake "estou gravando" entre o script de gravação e o HTML. O HTML não sabia que estava sendo gravado, continuava no modo de interação do navegador com loop.

**Regra**:

1. **Script de gravação**: Injete `window.__recording = true` no `addInitScript` (antes do page goto):

   ```js
   await recordCtx.addInitScript(() => {
     window.__recording = true;
   });
   ```

2. **Componente Stage**: Reconheça este sinal, force loop=false:

   ```js
   const effectiveLoop =
     typeof window !== "undefined" && window.__recording ? false : loop;
   // ...
   if (next >= duration) return effectiveLoop ? 0 : duration - 0.001;
   //                                                       ↑ Mantém 0.001 para evitar que Sprite com end=duration seja desligado
   ```

3. **FadeOut do Sprite final**: Em cenário de gravação, defina `fadeOut={0}`, senão o final do vídeo vai gradativamente para transparente/escuro — o usuário espera parar no último frame nítido, não em fade out. Em HTML manual, sugere-se que o último Sprite use `fadeOut={0}`.

**Implementação de referência**: O componente Stage em `assets/animations.jsx` e `scripts/render-video.js` já têm o handshake embutido. Stage manual DEVE implementar detecção de `__recording` — senão a gravação certamente cairá nesta armadilha.

**Verificação**: Após exportar MP4, execute `ffmpeg -ss 19.8 -i video.mp4 -frames:v 1 end.png`, verifique se os últimos 0.2 segundos ainda são o último frame esperado, sem mudança abrupta para outra cena.

## 14. Vídeo 60fps Usa Duplicação de Quadros por Padrão — Compatibilidade Ruim do minterpolate

**A armadilha**: `convert-formats.sh` usava `minterpolate=fps=60:mi_mode=mci...` para gerar MP4 60fps, que em algumas versões do macOS QuickTime / Safari não abria (tela preta ou recusa). VLC / Chrome abriam normalmente.

**Causa raiz**: O H.264 elementary stream gerado pelo minterpolate continha campos SEI/SPS que alguns players têm dificuldade de interpretar.

**Regra**:

- Para 60fps padrão, use o filter simples `fps=60` (duplicação de quadros), ampla compatibilidade (QuickTime/Safari/Chrome/VLC)
- Para interpolação de alta qualidade, use a flag `--minterpolate` explicitamente — mas **teste localmente no player de destino** antes de entregar
- O valor do rótulo 60fps é **reconhecimento algorítmico das plataformas de upload** (Bilibili / YouTube marcam 60fps com prioridade de streaming), o ganho real de suavidade percebida para animações CSS é pequeno
- Adicione `-profile:v high -level 4.0` para melhorar a compatibilidade geral do H.264

**`convert-formats.sh` já mudou para modo compatível por padrão**. Se precisar de interpolação de alta qualidade, adicione a flag `--minterpolate`:

```bash
bash convert-formats.sh input.mp4 --minterpolate
```

## 15. Armadilha CORS de `file://` + `.jsx` Externo — Entrega em Arquivo Único Deve Inline o Engine

**A armadilha**: HTML de animação usava `<script type="text/babel" src="animations.jsx"></script>` para carregar engine externo. Ao abrir localmente (protocolo `file://`) → Babel Standalone fazia XHR para buscar `.jsx` → Chrome reportava `Cross origin requests are only supported for protocol schemes: http, https, chrome, chrome-extension...` → página preta, sem reportar `pageerror`, apenas console error — facilmente diagnosticado erroneamente como "animação não disparou".

Iniciar servidor HTTP também não resolvia necessariamente — com proxy global ativo, `localhost` também passava pelo proxy, retornando 502 / falha de conexão.

**Regra**:

- **Entrega em arquivo único (HTML que abre com duplo clique)** → `animations.jsx` deve estar **inline** dentro da tag `<script type="text/babel">...</script>`, não use `src="animations.jsx"`
- **Projeto multi-arquivo (com servidor HTTP)** → pode carregar externamente, mas na entrega especifique claramente o comando `python3 -m http.server 8000`
- Critério de decisão: o que está sendo entregue ao usuário é um "arquivo HTML" ou um "diretório de projeto com servidor"? O primeiro usa inline.
- Componente Stage / animations.jsx frequentemente tem 200+ linhas — colar dentro do bloco `<script>` do HTML é perfeitamente aceitável, não tenha medo do tamanho.

**Verificação mínima**: Dê duplo clique no HTML gerado, **não** abra através de servidor. Se o Stage mostrar o primeiro frame da animação normalmente, está aprovado.

## 16. Contexto de Cor Invertida Entre Cenas — Elementos na Cena Não Devem Ter Cor Hard-coded

**A armadilha**: Em animação com múltiplas cenas, elementos como `ChapterLabel` / `SceneNumber` / `Watermark` que **aparecem em todas as cenas** tinham cor fixa `color: '#1A1A1A'` (texto escuro). Nas primeiras 4 cenas com fundo claro funcionava, mas na 5ª cena com fundo preto o "05" e a marca d'água simplesmente desapareciam — sem erro, sem verificação, informação crítica invisível.

**Regra**:

- **Elementos na cena que são reutilizados em múltiplas cenas** (rótulo de capítulo / número de cena / timecode / marca d'água / barra de créditos) **não devem ter valores de cor hard-coded**
- Use uma das três abordagens:
  1. **Herança `currentColor`**: O elemento escreve apenas `color: currentColor`, o contêiner da cena pai define `color: valor calculado`
  2. **Prop invert**: O componente aceita `<ChapterLabel invert />` para alternar manualmente entre claro/escuro
  3. **Cálculo automático baseado na cor de fundo**: `color: contrast-color(var(--scene-bg))` (nova API CSS 4, ou JS para determinar)
- Antes de entregar, use Playwright para capturar **um frame representativo de cada cena** e verifique visualmente se os "elementos entre cenas" estão todos visíveis

A insidiosidade desta armadilha é que **não há alerta de bug**. Apenas o olho humano ou OCR podem detectar.

## Lista de Verificação Rápida (5 segundos antes de começar)

- [ ] Cada `position: absolute` tem um elemento pai com `position: relative`?
- [ ] Caracteres especiais na animação (`␣` `⌘` `emoji`) existem na fonte?
- [ ] A contagem do template Grid/Flex é consistente com o length dos dados JS?
- [ ] As transições entre cenas têm cross-fade, sem espaço em branco puro >0.3s?
- [ ] O código de medição do DOM está dentro de `document.fonts.ready.then()`?
- [ ] `render(t)` é puro, ou tem mecanismo explícito de reset?
- [ ] O frame 0 é o estado inicial completo, não está em branco?
- [ ] Não há elementos "pseudo-chrome" decorativos na cena (barra de progresso/timecode/barra de créditos colidindo com o scrubber do Stage)?
- [ ] O primeiro frame do tick da animação define `window.__ready = true`? (usando animations.jsx já vem; HTML manual adicionar)
- [ ] Stage detecta `window.__recording` e força loop=false? (HTML manual OBRIGATÓRIO)
- [ ] O `fadeOut` do último Sprite está definido como 0 (para o final do vídeo parar em um frame nítido)?
- [ ] MP4 60fps usa modo de duplicação de quadros por padrão (compatibilidade), interpolação de alta qualidade só com `--minterpolate`?
- [ ] Após exportar, verifica o frame 0 e o último frame para confirmar estado inicial/final da animação?
- [ ] Envolve marca específica (Stripe/Anthropic/Lovart/...): seguiu o "protocolo de ativos de marca" (SKILL.md §1.a cinco passos)? Escreveu `brand-spec.md`?
- [ ] Entrega em arquivo único HTML: `animations.jsx` está inline, não é `src="..."`? (file:// com .jsx externo causa CORS e tela preta)
- [ ] Elementos que aparecem em múltiplas cenas (rótulo de capítulo/marca d'água/número de cena) não têm cor hard-coded? Estão visíveis em todas as cores de fundo das cenas?
