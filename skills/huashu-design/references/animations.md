# Animações: Engine de Animação em Timeline

Leia isto ao fazer animações/motion design em HTML. Princípios, uso, padrões típicos.

## Padrão Central: Stage + Sprite

Nosso sistema de animação (`assets/animations.jsx`) fornece um engine orientado por timeline:

- **`<Stage>`**: Contêiner de toda a animação, fornece auto-scale (ajuste ao viewport) + scrubber + controles play/pause/loop
- **`<Sprite start end>`**: Fragmento de tempo. Um Sprite só é exibido entre `start` e `end`. Internamente, pode usar o hook `useSprite()` para ler seu progresso local `t` (0→1)
- **`useTime()`**: Lê o tempo global atual (segundos)
- **`Easing.easeInOut` / `Easing.easeOut` / ...**: Funções de easing
- **`interpolate(t, from, to, easing?)`**: Interpola com base em t

Este padrão é inspirado em Remotion/After Effects, mas leve e sem dependências.

## Primeiros Passos

```html
<script type="text/babel" src="animations.jsx"></script>
<script type="text/babel">
  const { Stage, Sprite, useTime, useSprite, Easing, interpolate } =
    window.Animations;

  function Titulo() {
    const { t } = useSprite(); // Progresso local 0→1
    const opacity = interpolate(t, [0, 1], [0, 1], Easing.easeOut);
    const y = interpolate(t, [0, 1], [40, 0], Easing.easeOut);
    return (
      <h1
        style={{
          opacity,
          transform: `translateY(${y}px)`,
          fontSize: 120,
          fontWeight: 900,
        }}
      >
        Olá.
      </h1>
    );
  }

  function Cena() {
    return (
      <Stage duration={10}>
        {" "}
        {/* Animação de 10 segundos */}
        <Sprite start={0} end={3}>
          <Titulo />
        </Sprite>
        <Sprite start={2} end={5}>
          <SubTitulo />
        </Sprite>
        {/* ... */}
      </Stage>
    );
  }

  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<Cena />);
</script>
```

## Padrões de Animação Comuns

### 1. Fade In / Fade Out

```jsx
function FadeIn({ children }) {
  const { t } = useSprite();
  const opacity = interpolate(t, [0, 0.3], [0, 1], Easing.easeOut);
  return <div style={{ opacity }}>{children}</div>;
}
```

**Nota sobre intervalo**: `[0, 0.3]` significa que nos primeiros 30% do tempo do sprite o fade in é concluído, depois mantém opacity=1.

### 2. Slide In

```jsx
function SlideIn({ children, from = "left" }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, 0.4], [0, 1], Easing.easeOut);
  const offset = (1 - progress) * 100;
  const directions = {
    left: `translateX(-${offset}px)`,
    right: `translateX(${offset}px)`,
    top: `translateY(-${offset}px)`,
    bottom: `translateY(${offset}px)`,
  };
  return (
    <div
      style={{
        transform: directions[from],
        opacity: progress,
      }}
    >
      {children}
    </div>
  );
}
```

### 3. Máquina de Escrever (Typewriter)

```jsx
function Typewriter({ text }) {
  const { t } = useSprite();
  const charCount = Math.floor(text.length * Math.min(t * 2, 1));
  return <span>{text.slice(0, charCount)}</span>;
}
```

### 4. Contagem Numérica

```jsx
function CountUp({ from = 0, to = 100, duration = 0.6 }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, duration], [0, 1], Easing.easeOut);
  const value = Math.floor(from + (to - from) * progress);
  return <span>{value.toLocaleString()}</span>;
}
```

### 5. Explicação em Segmentos (Animação Didática Típica)

```jsx
function Cena() {
  return (
    <Stage duration={20}>
      {/* Fase 1: Mostrar o problema */}
      <Sprite start={0} end={4}>
        <Problema />
      </Sprite>

      {/* Fase 2: Mostrar a abordagem */}
      <Sprite start={4} end={10}>
        <Abordagem />
      </Sprite>

      {/* Fase 3: Mostrar o resultado */}
      <Sprite start={10} end={16}>
        <Resultado />
      </Sprite>

      {/* Legenda exibida durante todo o tempo */}
      <Sprite start={0} end={20}>
        <Legenda />
      </Sprite>
    </Stage>
  );
}
```

## Funções de Easing

Curvas de easing pré-definidas:

| Easing             | Característica                             | Usar em                                                        |
| ------------------ | ------------------------------------------ | -------------------------------------------------------------- |
| `linear`           | Velocidade constante                       | Legendas rolantes, animações contínuas                         |
| `easeIn`           | Lento→rápido                               | Saída/desaparecimento                                          |
| `easeOut`          | Rápido→lento                               | Entrada/aparecimento                                           |
| `easeInOut`        | Lento→rápido→lento                         | Mudanças de posição                                            |
| **`expoOut`** ⭐   | **Easing exponencial de saída**            | **Easing principal nível Anthropic** (sensação de peso físico) |
| **`overshoot`** ⭐ | **Ressalto elástico**                      | **Toggle / Botão pop / Ênfase em interação**                   |
| `spring`           | Mola                                       | Feedback de interação, geometria retornando ao lugar           |
| `anticipation`     | Primeiro vai para trás, depois para frente | Ênfase em ação                                                 |

**Easing principal padrão: use `expoOut`** (não `easeOut`) — veja `animation-best-practices.md` §2.
Entrada use `expoOut`, saída use `easeIn`, toggle use `overshoot` — a regra básica das animações nível Anthropic.

## Guia de Ritmo e Duração

### Micro-interações (0.1-0.3s)

- Hover em botão
- Expansão de card
- Aparecimento de Tooltip

### Transições de UI (0.3-0.8s)

- Troca de página
- Aparecimento de modal
- Item adicionado à lista

### Animações Narrativas (2-10s por segmento)

- Uma fase de explicação de conceito
- Revelação de gráfico de dados
- Transição de cena

### Cada segmento de animação narrativa não deve exceder 10 segundos

A atenção humana é limitada. 10 segundos para contar uma coisa, depois passe para a próxima.

## Ordem de Pensamento ao Projetar Animações

### 1. Primeiro o conteúdo/história, depois a animação

**Errado**: Primeiro querer fazer uma animação fancy, depois enfiar conteúdo
**Correto**: Primeiro pensar claramente qual informação transmitir, depois usar meios de animação para servir essa informação

Animação é **sinal**, não **decoração**. Um fade-in enfatiza "isto é importante, olhe aqui" — se tudo tem fade-in, o sinal perde o efeito.

### 2. Escreva a timeline por cenas

```
0:00 - 0:03   Problema aparece (fade in)
0:03 - 0:06   Problema amplia/expande (zoom+pan)
0:06 - 0:09   Solução aparece (slide in from right)
0:09 - 0:12   Explicação da solução (typewriter)
0:12 - 0:15   Demonstração do resultado (counter up + chart reveal)
0:15 - 0:18   Frase de resumo (static, leia por 3s)
0:18 - 0:20   CTA ou fade out
```

Escreva a timeline antes de escrever os componentes.

### 3. Recursos primeiro

Imagens/ícones/fontes a serem usados na animação **prepare antes**. Não pare no meio para buscar materiais — isso interrompe o ritmo.

## Problemas Comuns

**Animação travando**
→ Principalmente layout thrashing. Use `transform` e `opacity`, não mexa em `top`/`left`/`width`/`height`/`margin`. O navegador acelera `transform` pela GPU.

**Animação muito rápida, não dá para ver claramente**
→ Um ser humano leva 100-150ms para ler um caractere, 300-500ms para uma palavra. Se você usa texto para contar histórias, cada frase deve ficar pelo menos 3 segundos.

**Animação muito lenta, público entediado**
→ Mudanças visuais interessantes devem ser densas. Mais de 5 segundos de tela estática fica entediante.

**Múltiplas animações interferindo umas nas outras**
→ Use `will-change: transform` do CSS para avisar o navegador com antecedência que este elemento vai se mover, reduzindo reflow.

**Gravação em vídeo**
→ Use a toolchain própria da skill (um comando gera três formatos): veja `video-export.md`

- `scripts/render-video.js` — HTML → 25fps MP4 (Playwright + ffmpeg)
- `scripts/convert-formats.sh` — 25fps MP4 → 60fps MP4 + GIF otimizado
- Quer renderização de frames mais precisa? Faça render(t) ser uma pure function, veja `animation-pitfalls.md` regra 5

## Integração com Ferramentas de Vídeo

Esta skill produz **animações HTML** (que rodam no navegador). Se o produto final precisa ser material de vídeo:

- **Animações curtas/concept demo**: Use o método aqui (animação HTML) → gravação de tela
- **Vídeos longos/narrativa**: Esta skill foca em animações HTML; vídeos longos usem skills de geração de vídeo por IA ou software profissional de vídeo
- **Motion graphics**: After Effects profissional / Motion Canvas são mais adequados

## Sobre Popmotion e Bibliotecas Similares

Se você realmente precisa de animações físicas (spring, decay, keyframes com temporização precisa) e nosso engine não dá conta, pode usar Popmotion como fallback:

```html
<script src="https://unpkg.com/popmotion@11.0.5/dist/popmotion.min.js"></script>
```

Mas **tente nosso engine primeiro**. 90% dos casos são suficientes.
