# Apple Gallery Showcase · Estilo de Animação de Parede de Galeria

> Inspiração: vídeo hero do site Claude Design + exibição estilo "parede de trabalhos" das páginas de produto da Apple
> Origem prática: lançamento hero v5 do huashu-design
> Cenário de aplicação: **animação hero de lançamento de produto, demonstração de capacidade de skill, exibição de portfólio** — qualquer cenário que precise exibir simultaneamente "múltiplas saídas de alta qualidade" e guiar a atenção do espectador

---

## Julgamento de Gatilho: Quando Usar Este Estilo

**Adequado**:

- Tem 10 ou mais saídas reais para exibir na mesma tela (PPT, App, página web, infográfico)
- O público é profissional (desenvolvedores, designers, gerentes de produto), sensível a "qualidade"
- Deseja transmitir uma atmosfera de "contenção, estilo exposição, sofisticação, sensação de espaço"
- Precisa de foco e visão global simultaneamente (ver detalhes sem perder o todo)

**Inadequado**:

- Foco em produto único (use o template hero de produto do frontend-design)
- Animação emocional / com forte narrativa (use o template narrativo de linha do tempo)
- Tela pequena / vertical (a perspectiva inclinada fica borrada em telas pequenas)

---

## Token Visual Central

```css
:root {
  /* Paleta de galeria clara */
  --bg: #f5f5f7; /* Fundo da tela principal — cinza Apple */
  --bg-warm: #faf9f5; /* Variação bege quente */
  --ink: #1d1d1f; /* Cor principal do texto */
  --ink-80: #3a3a3d;
  --ink-60: #545458;
  --muted: #86868b; /* Texto secundário */
  --dim: #c7c7cc;
  --hairline: #e5e5ea; /* Borda de 1px do card */
  --accent: #d97757; /* Laranja terracota — Claude brand */
  --accent-deep: #b85d3d;

  --serif-cn: "Noto Serif SC", "Songti SC", Georgia, serif;
  --serif-en: "Source Serif 4", "Tiempos Headline", Georgia, serif;
  --sans: "Inter", -apple-system, "PingFang SC", system-ui;
  --mono: "JetBrains Mono", "SF Mono", ui-monospace;
}
```

**Princípios-chave**:

1. **Nunca use fundo preto puro**. Fundo preto faz os trabalhos parecerem filme, não "resultados de trabalho que podem ser adotados"
2. **Laranja terracota é o único acento de matiz**, todo o resto é escala de cinza + branco
3. **Pilha de três fontes** (serif EN + serif CN + sans + mono) cria atmosfera de "publicação" em vez de "produto de internet"

---

## Padrões Centrais de Layout

### 1. Card Flutuante (unidade básica de todo o estilo)

```css
.gallery-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 6px; /* Padding interno é a "moldura do quadro" */
  border: 1px solid var(--hairline);
  box-shadow:
    0 20px 60px -20px rgba(29, 29, 31, 0.12),
    /* Sombra principal, suave e longa */ 0 6px 18px -6px rgba(29, 29, 31, 0.06); /* Segunda camada de luz próxima, criando sensação de flutuação */
  aspect-ratio: 16 / 9; /* Proporção uniforme de slide */
  overflow: hidden;
}
.gallery-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 9px; /* Ligeiramente menor que o raio do card, aninhamento visual */
}
```

**Contraexemplo**: não faça azulejos colados (sem padding, sem border, sem shadow) — isso é expressão de densidade de infográfico, não exposição.

### 2. Parede de Trabalhos Inclinada em 3D

```css
.gallery-viewport {
  position: absolute;
  inset: 0;
  overflow: hidden;
  perspective: 2400px; /* Perspectiva mais profunda, inclinação não exagerada */
  perspective-origin: 50% 45%;
}
.gallery-canvas {
  width: 4320px; /* Canvas = 2,25× viewport */
  height: 2520px; /* Espaço para pan */
  transform-origin: center center;
  transform: perspective(2400px) rotateX(14deg) /* Inclinar para trás */
    rotateY(-10deg) /* Girar para a esquerda */ rotateZ(-2deg); /* Leve inclinação, removendo o excesso de regularidade */
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 40px;
  padding: 60px;
}
```

**Sweet spot dos parâmetros**:

- rotateX: 10-15deg (mais que isso parece painel VIP de festa)
- rotateY: ±8-12deg (sensação de simetria esquerda-direita)
- rotateZ: ±2-3deg (toque humano de "não foi a máquina que colocou")
- perspective: 2000-2800px (menos que 2000 causa olho de peixe, mais que 3000 se aproxima de projeção ortográfica)

### 3. Convergência dos Quatro Cantos 2×2 (cenário selecionado)

```css
.grid22 {
  display: grid;
  grid-template-columns: repeat(2, 800px);
  gap: 56px 64px;
  align-items: start;
}
```

Cada card desliza do canto correspondente (tl/tr/bl/br) em direção ao centro + fade in. Vetor `cornerEntry` correspondente:

```js
const cornerEntry = {
  tl: { dx: -700, dy: -500 },
  tr: { dx: 700, dy: -500 },
  bl: { dx: -700, dy: 500 },
  br: { dx: 700, dy: 500 },
};
```

---

## Cinco Modos de Animação Central

### Modo A · Convergência dos Quatro Cantos (0,8-1,2s)

4 elementos deslizam dos quatro cantos do viewport, com escala 0,85→1,0, usando ease-out. Adequado para abertura que "mostra múltiplas direções de escolha".

```js
const inP = easeOut(clampLerp(t, start, end));
card.style.transform = `translate3d(${(1 - inP) * ce.dx}px, ${(1 - inP) * ce.dy}px, 0) scale(${0.85 + 0.15 * inP})`;
card.style.opacity = inP;
```

### Modo B · Selecionado Amplia + Outros Deslizam para Fora (0,8s)

O card selecionado amplia 1,0→1,28, os outros cards fazem fade out + blur + flutuam de volta aos cantos:

```js
// Selecionado
card.style.transform = `translate3d(${cellDx * outP}px, ${cellDy * outP}px, 0) scale(${1 + 0.28 * easeOut(zoomP)})`;
// Não selecionado
card.style.opacity = 1 - outP;
card.style.filter = `blur(${outP * 1.5}px)`;
```

**Crucial**: os não selecionados devem ter blur, não apenas fade. O blur simula profundidade de campo, visualmente "empurrando" o selecionado para frente.

### Modo C · Onda Ripple (1,7s)

Do centro para fora, com delay baseado na distância, cada card aparece sequencialmente com fade-in + escala de 1,25x para 0,94x ("zoom out da câmera"):

```js
const col = i % COLS,
  row = Math.floor(i / COLS);
const dc = col - (COLS - 1) / 2,
  dr = row - (ROWS - 1) / 2;
const dist = Math.sqrt(dc * dc + dr * dr);
const delay = (dist / maxDist) * 0.8;
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
card.style.opacity = easeOut(Math.min(1, localT));

// Simultaneamente, escala geral 1,25→0,94
const galleryScale = 1.25 - 0.31 * easeOut(rippleProgress);
```

### Modo D · Pan Senoidal (Deriva Contínua)

Usa combinação de onda senoidal + deriva linear, evitando a sensação de ciclo "com início e fim" do marquee:

```js
const panX = Math.sin(panT * 0.12) * 220 - panT * 8; // Deriva horizontal para esquerda
const panY = Math.cos(panT * 0.09) * 120 - panT * 5; // Deriva vertical para cima
const clampedX = Math.max(-900, Math.min(900, panX)); // Evitar bordas expostas
```

**Parâmetros**:

- Período senoidal `0,09-0,15 rad/s` (lento, cerca de 30-50 segundos por oscilação)
- Deriva linear `5-8 px/s` (mais lento que a piscada do espectador)
- Amplitude `120-220 px` (grande o suficiente para sentir, pequena o suficiente para não causar tontura)

### Modo E · Focus Overlay (Troca de Foco)

**Design crucial**: o focus overlay é um **elemento plano** (não inclinado), flutuando sobre o canvas inclinado. O slide selecionado escala da posição do tile (cerca de 400×225) para o centro da tela (960×540), o canvas de fundo não muda de inclinação mas **escurece para 45%**:

```js
// Focus overlay (plano, centralizado)
focusOverlay.style.width = startW + (endW - startW) * focusIntensity + "px";
focusOverlay.style.height = startH + (endH - startH) * focusIntensity + "px";
focusOverlay.style.opacity = focusIntensity;

// Cards de fundo escurecem, mas ainda visíveis (crucial! não mascarar 100%)
card.style.opacity = entryOp * (1 - 0.55 * focusIntensity); // 1 → 0.45
card.style.filter = `brightness(${1 - 0.3 * focusIntensity})`;
```

**Regra de ferro da nitidez**:

- O `<img>` do Focus overlay deve ter `src` direto para a imagem original, **não reutilizar a miniatura comprimida da galeria**
- Pré-carregue todas as imagens originais em um array `new Image()[]` com antecedência
- O próprio overlay tem `width/height` calculados por frame, o navegador reamostra a imagem original a cada frame

---

## Arquitetura da Linha do Tempo (Esqueleto Reutilizável)

```js
const T = {
  DURATION: 25.0,
  s1_in: [0.0, 0.8],
  s1_type: [1.0, 3.2],
  s1_out: [3.5, 4.0],
  s2_in: [3.9, 5.1],
  s2_hold: [5.1, 7.0],
  s2_out: [7.0, 7.8],
  s3_hold: [7.8, 8.3],
  s3_ripple: [8.3, 10.0],
  panStart: 8.6,
  focuses: [
    { start: 11.0, end: 12.7, idx: 2 },
    { start: 13.3, end: 15.0, idx: 3 },
    { start: 15.6, end: 17.3, idx: 10 },
    { start: 17.9, end: 19.6, idx: 16 },
  ],
  s4_walloff: [21.1, 21.8],
  s4_in: [21.8, 22.7],
  s4_hold: [23.7, 25.0],
};

// Easing central
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const easeInOut = (t) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
function lerp(time, start, end, fromV, toV, easing) {
  if (time <= start) return fromV;
  if (time >= end) return toV;
  let p = (time - start) / (end - start);
  if (easing) p = easing(p);
  return fromV + (toV - fromV) * p;
}

// Função única render(t) lê timestamp e escreve todos os elementos
function render(t) {
  /* ... */
}
requestAnimationFrame(function tick(now) {
  const t = ((now - startMs) / 1000) % T.DURATION;
  render(t);
  requestAnimationFrame(tick);
});
```

**Essência da arquitetura**: **todo o estado é derivado do timestamp t**, sem máquina de estados, sem setTimeout. Assim:

- Reproduzir para qualquer momento `window.__setTime(12.3)` salta instantaneamente (útil para captura quadro a quadro com playwright)
- Loop naturalmente sem emendas (t mod DURATION)
- Ao depurar, é possível congelar qualquer quadro

---

## Detalhes de Qualidade (Fáceis de Ignorar, Mas Fatais)

### 1. Textura SVG noise

Fundos claros temem mais "serem muito lisos". Sobreponha um fractalNoise muito fraco:

```html
<style>
  .stage::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.078  0 0 0 0 0.078  0 0 0 0 0.074  0 0 0 0.035 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
    opacity: 0.5;
    pointer-events: none;
    z-index: 30;
  }
</style>
```

Não parece diferente visualmente, mas ao remover, percebe-se a diferença.

### 2. Identidade da Marca no Canto

```html
<div class="corner-brand">
  <div class="mark"></div>
  <div>HUASHU · DESIGN</div>
</div>
```

```css
.corner-brand {
  position: absolute;
  top: 48px;
  left: 72px;
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
}
```

Exibido apenas na cena da parede de trabalhos, fade in/out. Como etiqueta de museu.

### 3. Wordmark de Fechamento da Marca

```css
.brand-wordmark {
  font-family: var(--sans);
  font-size: 148px;
  font-weight: 700;
  letter-spacing: -0.045em; /* Espaçamento negativo é crucial, torna as letras compactas como um logotipo */
}
.brand-wordmark .accent {
  color: var(--accent);
  font-weight: 500; /* Caractere de acento ligeiramente mais fino, contraste visual */
}
```

`letter-spacing: -0.045em` é a prática padrão de letras grandes nas páginas de produto da Apple.

---

## Modos Comuns de Falha

| Sintoma                       | Causa                                                   | Solução                                                       |
| ----------------------------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| Parece template de PPT        | Card sem shadow / hairline                              | Adicione duas camadas de box-shadow + 1px border              |
| Sensação de inclinação barata | Usou apenas rotateY sem rotateZ                         | Adicione ±2-3deg rotateZ para quebrar a simetria              |
| Pan parece "travado"          | Usou setTimeout ou loop de CSS keyframes                | Use rAF + funções contínuas sin/cos                           |
| Foco com texto ilegível       | Reutilizou imagem de baixa resolução do tile da galeria | Overlay independente + src direto da imagem original          |
| Fundo muito vazio             | Cor sólida `#F5F5F7`                                    | Sobreponha SVG fractalNoise com 0.5 opacity                   |
| Fonte muito "internet"        | Apenas Inter                                            | Adicione Serif (um para CN e um para EN) + mono, pilha tripla |

---

## Referências

- Amostra de implementação completa: `/Users/alchain/Documents/写作/01-公众号写作/项目/2026.04-huashu-design发布/配图/hero-animation-v5.html`
- Inspiração original: vídeo hero claude.ai/design
- Estética de referência: Páginas de produto Apple, coleção de shots Dribbble

Ao encontrar uma demanda de animação que precise "exibir múltiplas saídas de alta qualidade", copie diretamente o esqueleto deste arquivo, troque o conteúdo + ajuste o timing.
