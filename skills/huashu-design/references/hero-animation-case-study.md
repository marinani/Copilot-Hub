# Gallery Ripple + Multi-Focus · Filosofia de Orquestração de Cena

> Uma **estrutura de orquestração visual reutilizável** destilada da animação hero huashu-design v9 (25 segundos, 8 cenas).
> Não é uma linha de produção de animação, mas sim **em que cenário essa orquestração é "correta"**.
> Referência prática: [demos/hero-animation-v9.mp4](../demos/hero-animation-v9.mp4) · [https://www.huasheng.ai/huashu-design-hero/](https://www.huasheng.ai/huashu-design-hero/)

## Resumo em Uma Frase

> **Quando você tem 20+ materiais visuais homogêneos e a cena precisa "expressar escala e profundidade", priorize esta orquestração Gallery Ripple + Multi-Focus em vez de empilhar layouts.**

Animação de funcionalidades SaaS genéricas, lançamento de produto, promoção de skill, exibição de portfólio — contanto que a quantidade de material seja suficiente e o estilo seja consistente, esta estrutura quase sempre produz bons resultados.

---

## O que Esta Técnica Realmente Expressa

Não é "exibir materiais" — é contar uma narrativa através de **duas mudanças de ritmo**:

**Primeiro movimento · Ripple (abertura, ~1,5s)**: 48 cards se espalham do centro para as bordas, o espectador é impactado pela "quantidade" — "nossa, esta coisa tem tantas saídas".

**Segundo movimento · Multi-Focus (~8s, 4 ciclos)**: enquanto a câmera faz pan lento, 4 vezes o fundo é dim + desaturated, e um card específico é ampliado para o centro da tela — o espectador muda do "impacto da quantidade" para a "contemplação da qualidade", cada vez com ritmo estável de 1,7s.

**Estrutura narrativa central**: **Escala (Ripple) → Contemplação (Focus × 4) → Fade out (Walloff)**. Esses três movimentos juntos expressam "Amplitude × Profundidade" — não é apenas "consegue fazer muito", mas "cada um merece ser observado".

Compare com contraexemplos:

| Abordagem                                           | Percepção do Espectador                                                                                                     |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 48 cards estáticos (sem Ripple)                     | Bonito mas sem narrativa, parece um grid screenshot                                                                         |
| Um por um em corte rápido (sem contexto de Gallery) | Parece slideshow, perde a "sensação de escala"                                                                              |
| Apenas Ripple sem Focus                             | Impacta mas não faz ninguém lembrar de nenhum card específico                                                               |
| **Ripple + Focus × 4 (esta receita)**               | **Primeiro impressiona pela quantidade, depois contempla a qualidade, finalmente fade out calmo — arco emocional completo** |

---

## Pré-condições (Todas Obrigatórias)

Esta orquestração **não é universal**, as 4 condições abaixo são indispensáveis:

1. **Quantidade de material ≥ 20, de preferência 30+**
   Menos de 20 fará o Ripple parecer "vazio" — só com 48 células todas se movendo é que há sensação de densidade. A v9 usou 48 células × 32 imagens (preenchimento cíclico).

2. **Estilo visual do material consistente**
   Todos previews de slide 16:9 / todos screenshots de app / todos designs de capa — proporção, tom, layout devem parecer "um conjunto". Misturar faz a Gallery parecer uma área de transferência.

3. **Material ainda tem informação legível quando ampliado individualmente**
   Focus amplia um card para 960px de largura. Se a imagem original ficar borrada ou com informação escassa quando ampliada, este movimento do Focus estará perdido. Validação reversa: consegue escolher 4 entre 48 como "as mais representativas"? Se não consegue, a qualidade do material não é uniforme.

4. **A cena em si é landscape ou quadrada, não vertical**
   A inclinação 3D da Gallery (`rotateX(14deg) rotateY(-10deg)`) precisa de sensação de extensão horizontal. Tela vertical faz o efeito de inclinação parecer estreito e estranho.

**Caminhos alternativos quando faltam condições**:

| Falta o quê          | Degenera para                                                      |
| -------------------- | ------------------------------------------------------------------ |
| Material < 20        | Use "3-5 cards lado a lado estáticos + focus individual"           |
| Estilo inconsistente | Use "capa + 3 capítulos de imagem grande" estilo keynote           |
| Informação escassa   | Use "dashboard data-driven" ou "frases de efeito + letras grandes" |
| Cenário vertical     | Use "vertical scroll + sticky cards"                               |

---

## Receita Técnica (Parâmetros Reais da v9)

### Estrutura de 4 Camadas

```
viewport (1920×1080, perspective: 2400px)
  └─ canvas (4320×2520, overflow grande) → 3D tilt + pan
      └─ grid 8×6 = 48 cards (gap 40px, padding 60px)
          └─ img (16:9, border-radius 9px)
      └─ focus-overlay (absolute center, z-index 40)
          └─ img (corresponde ao slide selecionado)
```

**Crucial**: o canvas é 2,25x maior que o viewport, assim o pan tem a sensação de "espiar um mundo maior".

### Abertura Ripple (algoritmo de delay por distância)

```js
// Tempo de entrada de cada card = distância do centro × 0,8s de delay
const col = i % 8,
  row = Math.floor(i / 8);
const dc = col - 3.5,
  dr = row - 2.5; // Offset até o centro
const dist = Math.hypot(dc, dr);
const maxDist = Math.hypot(3.5, 2.5);
const delay = (dist / maxDist) * 0.8; // 0 → 0,8s
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
const opacity = expoOut(Math.min(1, localT));
```

**Parâmetros centrais**:

- Duração total 1,7s (`T.s3_ripple: [8.3, 10.0]`)
- Delay máximo 0,8s (centro sai primeiro, cantos por último)
- Duração de entrada de cada card 0,7s
- Easing: `expoOut` (sensação de explosão, não suave)

**Simultaneamente**: canvas scale de 1,25 → 0,94 (zoom out para revelar) — sensação de recuo sincronizada com a aparição.

### Multi-Focus (4 vezes, ritmo)

```js
T.focuses = [
  { start: 11.0, end: 12.7, idx: 2 }, // 1,7s
  { start: 13.3, end: 15.0, idx: 3 }, // 1,7s
  { start: 15.6, end: 17.3, idx: 10 }, // 1,7s
  { start: 17.9, end: 19.6, idx: 16 }, // 1,7s
];
```

**Padrão rítmico**: cada focus 1,7s, intervalo de 0,6s de respiro. Total 8s (11,0–19,6s).

**Internamente em cada focus**:

- Rampa de entrada: 0,4s (`expoOut`)
- Hold: meio 0,9s (`focusIntensity = 1`)
- Rampa de saída: 0,4s (`easeOut`)

**Mudança de fundo (isto é crucial)**:

```js
if (focusIntensity > 0) {
  const dimOp = entryOp * (1 - 0.6 * focusIntensity); // escurecer para 40%
  const brt = 1 - 0.32 * focusIntensity; // brightness 68%
  const sat = 1 - 0.35 * focusIntensity; // saturate 65%
  card.style.filter = `brightness(${brt}) saturate(${sat})`;
}
```

**Não é apenas opacity — simultaneamente desaturate + darken**. Isso faz as cores do overlay de foreground "saltarem", em vez de apenas "ficarem um pouco mais claras".

**Animação de tamanho do Focus overlay**:

- De 400×225 (entrada) → 960×540 (estado hold)
- Periferia com 3 camadas de shadow + outline ring de 3px na cor accent, criando "sensação de estar emoldurado"

### Pan (movimento contínuo evita que o estático fique entediante)

```js
const panT = Math.max(0, t - 8.6);
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;
```

- Onda senoidal + drift linear em duas camadas — não é ciclo puro, cada momento tem posição diferente
- Frequências X/Y diferentes (0,12 vs 0,09) evitam que o olho perceba "ciclo regular"
- Clamp em ±900/500px para evitar sair da borda

**Por que não usar pan puramente linear**: com pan linear o espectador "prevê" onde estará no próximo segundo; seno + drift faz cada segundo ser novo, sob inclinação 3D produz uma "micro sensação de navio" (do tipo bom), a atenção é mantida.

---

## 5 Padrões Reutilizáveis (Destilados da Iteração v6→v9)

### 1. **expoOut como easing principal, não cubicOut**

`easeOut = 1 - (1-t)³` (suave) vs `expoOut = 1 - 2^(-10t)` (explosão seguida de convergência rápida).

**Motivo da escolha**: os primeiros 30% do expoOut atingem 90% rapidamente, mais parecido com amortecimento físico, adequado à intuição de "coisa pesada caindo". Particularmente adequado para:

- Entrada de cards (sensação de peso)
- Propagação Ripple (onda de choque)
- Flutuação da Marca (sensação de estabilização)

**Quando ainda usar cubicOut**: rampa de saída de focus, micro movimentos simétricos.

### 2. **Fundo com textura de papel + accent laranja terracota (linhagem Anthropic)**

```css
--bg: #f7f4ee; /* Papel quente */
--ink: #1d1d1f; /* Quase preto */
--accent: #d97757; /* Laranja terracota */
--hairline: #e4ded2; /* Linha quente */
```

**Por quê**: fundo quente após compressão GIF ainda tem "sensação de respiração", diferente do branco puro que parece "sensação de tela". Laranja terracota como único accent percorre terminal prompt, dir-card selecionado, cursor, hífen da marca, focus ring — todos os pontos de ancoragem visual são conectados por esta única cor.

**Lição da v5**: adicionou noise overlay para simular "textura de papel", mas a compressão de quadros GIF destruiu tudo (cada quadro é diferente). Na v6 mudou para "apenas cor de fundo + shadow quente", mantendo 90% da sensação de papel, reduzindo o tamanho do GIF em 60%.

### 3. **Duas faixas de Shadow para simular profundidade, sem 3D real**

```css
.gallery-card.depth-near {
  box-shadow:
    0 32px 80px -22px rgba(60, 40, 20, 0.22),
    ...;
}
.gallery-card.depth-far {
  box-shadow:
    0 14px 40px -16px rgba(60, 40, 20, 0.1),
    ...;
}
```

Use algoritmo determinístico `sin(i × 1.7) + cos(i × 0.73)` para atribuir a cada card uma das três faixas de shadow (near/mid/far) — **visualmente tem sensação de "empilhamento 3D", mas o transform de cada quadro é completamente invariável, consumo de GPU = 0**.

**Custo do 3D real**: cada card com `translateZ` individual, a GPU calcula 48 transforms + shadow blur a cada quadro. A v4 tentou, e a gravação com Playwright já tinha dificuldade a 25fps. As duas faixas de shadow da v6 têm diferença visual <5%, mas custo 10x menor.

### 4. **Variação de peso da fonte (font-variation-settings) é mais cinematográfica que variação de tamanho**

```js
const wght = 100 + (700 - 100) * morphP; // 100 → 700 em 0,9s
wordmark.style.fontVariationSettings = `"wght" ${wght.toFixed(0)}`;
```

A wordmark da marca faz gradiente de Thin → Bold em 0,9s, com ajuste fino de letter-spacing (-0,045 → -0,048em).

**Por que é melhor que aumentar/diminuir tamanho**:

- Aumentar/diminuir tamanho o espectador já viu demais, expectativa cristalizada
- Variação de peso é "sensação de preenchimento interno", como um balão sendo inflado, não "sendo empurrado para perto"
- Variable fonts são uma característica popularizada apenas a partir de 2020+, o espectador subconscientemente sente "moderno"

**Limitação**: deve usar fontes que suportam variable font (Inter/Roboto Flex/Recursive etc.). Fontes estáticas comuns só podem imitar (alternar entre alguns pesos fixos causa saltos).

### 5. **Corner Brand — Assinatura Contínua de Baixa Intensidade**

No estágio da Gallery, no canto superior esquerdo, há um pequeno identificador `HUASHU · DESIGN`, com 16% de opacity, tamanho 12px, espaçamento largo.

**Por que adicionar isto**:

- Após a explosão Ripple, o espectador tende a "perder o foco" e não lembrar o que está vendo; a marcação leve no canto superior esquerdo ajuda a ancorar
- Mais sofisticado que um logo grande em tela cheia — quem trabalha com marca sabe que assinatura de marca não precisa gritar
- Ao ser compartilhado como GIF, ainda deixa um sinal de pertencimento

**Regra**: aparece apenas no meio (quando a tela está ocupada), desliga na abertura (não obstrui o terminal), desliga no fechamento (o brand reveal é o protagonista).

---

## Contraexemplos: Quando Não Usar Esta Orquestração

**❌ Demonstração de produto (precisa mostrar funcionalidades)**: Gallery faz cada card passar rapidamente, o espectador não memoriza nenhuma funcionalidade. Use "foco em tela única + anotação tooltip".

**❌ Conteúdo orientado a dados**: o espectador precisa ler números, o ritmo rápido da Gallery não dá tempo de leitura. Use "gráfico de dados + revelação item por item".

**❌ Narrativa de história**: Gallery é estrutura "paralela", história precisa de "causa e efeito". Use alternância de capítulos keynote.

**❌ Material de apenas 3-5 cards**: densidade Ripple insuficiente, parece "remendo". Use "disposição estática + destaque card por card".

**❌ Tela vertical (9:16)**: 3D tilt precisa de extensão horizontal, tela vertical faz a inclinação parecer "torta" em vez de "aberta".

---

## Como Julgar se Sua Tarefa se Adequa a Esta Orquestração

Verificação rápida em três etapas:

**Etapa 1 · Quantidade de material**: conte quantos materiais visuais semelhantes você tem. < 15 → pare; 15-25 → complete; 25+ → use diretamente.

**Etapa 2 · Teste de consistência**: coloque 4 materiais aleatórios lado a lado, eles parecem "um conjunto"? Se não → primeiro uniformize o estilo, depois faça, ou mude de plano.

**Etapa 3 · Correspondência narrativa**: O que você quer expressar é "Amplitude × Profundidade" (quantidade × qualidade)? Ou é "fluxo" / "funcionalidade" / "história"? Se não for o primeiro, não force.

Se as três etapas forem "sim", bifurque diretamente o HTML da v6, altere o array `SLIDE_FILES` e a linha do tempo para reutilizar. Altere a paleta com `--bg / --accent / --ink`, troque a pele sem trocar os ossos.

---

## References Relacionados

- Fluxo técnico completo: [references/animations.md](animations.md) · [references/animation-best-practices.md](animation-best-practices.md)
- Pipeline de exportação de animação: [references/video-export.md](video-export.md)
- Configuração de áudio (BGM + SFX via dupla): [references/audio-design-rules.md](audio-design-rules.md)
- Referência横向 do estilo Apple Gallery: [references/apple-gallery-showcase.md](apple-gallery-showcase.md)
- HTML fonte (v6 + versão integrada de áudio): `www.huasheng.ai/huashu-design-hero/index.html`
