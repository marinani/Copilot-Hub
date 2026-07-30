# Animation Best Practices · Sintaxe de Motion Design Positivo

> Baseado na análise aprofundada de três animações oficiais da Anthropic (Claude Design / Claude Code Desktop / Claude for Word),
> destilando as regras de design de animação de "nível Anthropic".
>
> Use junto com `animation-pitfalls.md` (lista de armadilhas) — este arquivo é o que **deve ser feito**,
> pitfalls é o que **não deve ser feito**, são ortogonais, leia ambos.
>
> **Declaração de restrição**: este arquivo contém apenas **lógica de movimento e estilo de expressão**,
> **sem introduzir valores de cores de marca específicos**.
> Decisões de cor seguem o §1.a Protocolo de Ativos Principais (extraído do brand spec) ou o "Consultor de Direção de Design"
> (esquemas de cores das 20 filosofias). Este reference discute **"como se move"**, não **"qual cor"**.

---

## §0 · Quem Você É · Identidade e Bom Gosto

> Antes de ler qualquer regra técnica a seguir, leia esta seção. As regras **emergem da identidade** —
> não o contrário.

### §0.1 Âncora de Identidade

**Você é um motion designer que estudou os arquivos de movimento da Anthropic / Apple / Pentagram / Field.io.**

Ao fazer animação, você não está ajustando CSS transition — você está **simulando um mundo físico** com elementos digitais,
fazendo o subconsciente do espectador acreditar que "isto é um objeto com peso, inércia e que pode transbordar".

Você não faz animação estilo PowerPoint. Você não faz animação "fade in fade out". A animação que você faz **faz as pessoas acreditarem que a tela é um espaço onde se pode colocar a mão**.

### §0.2 Crenças Centrais (3)

1. **Animação é física, não é curva de animação**
   `linear` é digital, `expoOut` é objeto. Você acredita que os pixels na tela merecem ser tratados como "objetos".
   Cada escolha de easing é uma resposta à pergunta física "este elemento tem quanto peso? Qual o coeficiente de atrito?"

2. **Distribuição do tempo é mais importante que o formato da curva**
   Lento-Rápido-Boom-Parada é sua respiração. **Animação de ritmo uniforme é demonstração técnica; animação com ritmo é narrativa.**
   Desacelerar no momento certo — é mais importante que usar o easing certo no momento errado.

3. **Dar espaço ao espectador é mais difícil que exibir técnica**
   Pausar 0,5s antes de um resultado-chave é **técnica**, não concessão. **Dar tempo de reação ao cérebro humano é a mais alta qualidade de um animador.**
   Por padrão, a IA fará uma animação sem pausas, com densidade máxima de informação — isso é amador. O que você precisa fazer é conter-se.

### §0.3 Padrão de Bom Gosto · O que é Belo

Seu critério para "bom" e "excelente" é o seguinte. Cada item tem um **método de identificação** — ao ver uma animação candidata,
use estas perguntas para julgar se ela atinge o padrão, em vez de conferir mecanicamente 14 regras.

| Dimensão da Beleza           | Método de Identificação (reação do espectador)                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sensação de peso físico**  | Ao final da animação, o elemento "**pousa**" com firmeza — não "**para**" ali. O subconsciente do espectador sente "isto tem peso"             |
| **Espaço para o espectador** | Há uma pausa perceptível (≥300ms) antes da informação-chave aparecer — o espectador tem tempo de "**ver**" antes de continuar                  |
| **Espaço em branco**         | O final é uma parada brusca + pausa, não um fade to black. O último quadro é nítido, firme, com sensação de decisão                            |
| **Moderação**                | A peça inteira tem apenas um momento "120% refinado", os outros 80% são na medida certa — **exibir técnica em toda parte é sinal de barateza** |
| **Toque**                    | Curvas (não retas), irregulares (não o ritmo mecânico de setInterval), com sensação de respiração                                              |
| **Respeito**                 | Mostrar o processo de ajuste, mostrar a correção de bugs — **não esconder o trabalho, não dar "mágica"**. IA é colaboradora, não mágica        |

### §0.4 Autoverificação · Método da Primeira Reação do Espectador

Ao terminar uma animação, **qual é a primeira reação do espectador ao assisti-la?** — Esta é a única métrica que você deve otimizar.

| Reação do Espectador                                  | Classificação | Diagnóstico                                                  |
| ----------------------------------------------------- | ------------- | ------------------------------------------------------------ |
| "Parece bem fluido"                                   | bom           | Adequado mas sem personalidade, você está fazendo PowerPoint |
| "Esta animação é muito suave"                         | bom+          | A técnica está correta, mas não impressiona                  |
| "Esta coisa realmente parece que **flutuou da mesa**" | excelente     | Você alcançou a sensação de peso físico                      |
| "Não parece que foi feita por IA"                     | excelente+    | Você atingiu o nível da Anthropic                            |
| "Quero **printar** e postar"                          | excelente++   | Você fez o espectador querer compartilhar ativamente         |

**A diferença entre excelente e bom não está na correção técnica, mas no julgamento de bom gosto**. Técnica correta + bom gosto = excelente.
Técnica correta + bom gosto vazio = bom. Técnica errada = nem começou.

### §0.5 Relação entre Identidade e Regras

As regras técnicas §1-§8 abaixo são **meios de execução** desta identidade em cenários específicos — não são uma lista de regras independentes.

- Ao encontrar um cenário não coberto pelas regras → volte ao §0, julgue com a **identidade**, não adivinhe
- Ao encontrar conflito entre regras → volte ao §0, julgue com o **padrão de bom gosto** qual é mais importante
- Se quiser quebrar uma regra → primeiro responda: "Fazer isso atende a qual item de beleza do §0.3?" Se conseguir responder, quebre. Se não conseguir, não quebre.

Certo. Continue lendo.

---

## Visão Geral · Animação é Física em Três Camadas

A raiz do aspecto barato da maioria das animações geradas por IA é — **elas se comportam como "números", não como "objetos"**.
Objetos do mundo real têm massa, inércia, elasticidade, transbordam. A raiz da "sensação premium" dos três vídeos da Anthropic
está em dar aos elementos digitais um conjunto de **regras de movimento do mundo físico**.

Este conjunto tem 3 níveis:

1. **Camada de Ritmo Narrativo**: Distribuição temporal Lento-Rápido-Boom-Parada
2. **Camada de Curvas de Movimento**: Expo Out / Overshoot / Spring, rejeite linear
3. **Camada de Linguagem de Expressão**: Mostrar o processo, curva do mouse, contração do Logo

---

## 1. Ritmo Narrativo · Estrutura de 5 Estágios Lento-Rápido-Boom-Parada

Os três vídeos da Anthropic seguem invariavelmente esta estrutura:

| Estágio           | Proporção | Ritmo  | Função                                            |
| ----------------- | --------- | ------ | ------------------------------------------------- |
| **S1 Gatilho**    | ~15%      | Lento  | Dá tempo de reação humana, estabelece realismo    |
| **S2 Geração**    | ~15%      | Médio  | Ponto de impacto visual aparece                   |
| **S3 Processo**   | ~40%      | Rápido | Mostra controlabilidade / densidade / detalhes    |
| **S4 Explosão**   | ~20%      | Boom   | Zoom out / 3D pop-out / painéis múltiplos emergem |
| **S5 Fechamento** | ~10%      | Quieto | Logo da marca + parada brusca                     |

**Mapeamento de duração específica** (para animação de 15 segundos):
S1 Gatilho 2s · S2 Geração 2s · S3 Processo 6s · S4 Explosão 3s · S5 Fechamento 2s

**O que é proibido**:

- ❌ Ritmo uniforme (mesma densidade de informação por segundo) — cansa o espectador
- ❌ Alta densidade contínua — sem pico, sem ponto de memória
- ❌ Finalização com fade out (desvanecer para transparente) — deve **parar bruscamente**

**Autoverificação**: Desenhe 5 thumbnails no papel, cada um representando o clímax de um estágio. Se as 5 imagens não diferirem muito, o ritmo não foi construído.

---

## 2. Filosofia de Easing · Rejeite linear, Abrace a Física

Todos os efeitos nos três vídeos da Anthropic usam curvas Bezier com "sensação de amortecimento". O cubic easeOut padrão
(`1-(1-t)³`) **não é agudo o suficiente** — a partida não é rápida o bastante, a parada não é estável o bastante.

### Três Easing Centrais (já inclusos em animations.jsx)

```js
// 1. Expo Out · Partida rápida, frenagem suave (mais usado, easing padrão principal)
// Correspondente CSS: cubic-bezier(0.16, 1, 0.3, 1)
Easing.expoOut(t); // = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)

// 2. Overshoot · Com elasticidade para toggle/ botão pop-out
// Correspondente CSS: cubic-bezier(0.34, 1.56, 0.64, 1)
Easing.overshoot(t);

// 3. Spring físico · Geometria se ajustando, aterrissagem natural
Easing.spring(t);
```

### Mapeamento de Uso

| Cenário                                                                                    | Qual Easing Usar                             |
| ------------------------------------------------------------------------------------------ | -------------------------------------------- |
| Card rise-in / painel de entrada / Terminal fade / focus overlay                           | **`expoOut`** (easing principal, mais usado) |
| Alternância de toggle / botão pop-out / interação de destaque                              | `overshoot`                                  |
| Preview de geometria se ajustando / aterrissagem física / elementos de UI com elasticidade | `spring`                                     |
| Movimento contínuo (ex.: interpolação de trajetória do mouse)                              | `easeInOut` (preserva simetria)              |

### Insight Contraintuitivo

A maioria das animações de vídeos promocionais de produtos é **rápida e dura demais**. `linear` faz elementos digitais parecerem máquinas, `easeOut` é a nota básica,
`expoOut` é a raiz técnica da "sensação premium" — ela dá aos elementos digitais uma **sensação de peso do mundo físico**.

---

## 3. Linguagem de Movimento · 8 Princípios Comuns

### 3.1 Fundo não usa preto ou branco puro

Nenhum dos três vídeos da Anthropic usa `#FFFFFF` ou `#000000` como cor de fundo principal. **Neutros com temperatura de cor** (quentes ou frios) têm sensação material de "papel / tela / mesa", enfraquecendo a sensação de máquina.

**Decisão de valores de cor específicos** segue o §1.a Protocolo de Ativos Principais (extraído do brand spec) ou o "Consultor de Direção de Design" (esquemas de fundo das 20 filosofias). Este reference não fornece valores de cor específicos — isso é **decisão de marca**, não regra de movimento.

### 3.2 Easing nunca é linear

Veja §2.

### 3.3 Narrativa Lento-Rápido-Boom-Parada

Veja §1.

### 3.4 Mostrar o "Processo" em vez de "Resultado Mágico"

- Claude Design mostra ajuste de parâmetros, arrastar slider (não gera resultado perfeito com um clique)
- Claude Code mostra erro de código + correção pela IA (não sucesso na primeira tentativa)
- Claude for Word mostra o processo de edição Redline (vermelho deletado, verde adicionado) em vez de dar o rascunho final diretamente

**Subtexto comum**: o produto é **colaborador, engenheiro de par, editor sênior** — não um mágico de um clique.
Isso ataca precisamente a dor dos usuários profissionais quanto a "controlabilidade" e "autenticidade".

**Anti AI slop**: a IA por padrão fará animações de "sucesso mágico com um clique" (gerar → resultado perfeito),
este é o denominador comum. **Fazer o oposto** — mostrar o processo, mostrar ajustes, mostrar bugs e correções —
é a fonte de identidade da marca.

### 3.5 Trajetória do Mouse Desenhada Artificialmente (Arco + Perlin Noise)

O movimento real do mouse humano não é uma linha reta, é "aceleração inicial → arco → desaceleração com correção → clique".
A trajetória do mouse interpolada diretamente em linha reta pela IA **tem rejeição subconsciente**.

```js
// Interpolação de curva Bezier quadrática (início → ponto de controle → fim)
function bezierQuadratic(p0, p1, p2, t) {
  const x = (1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0];
  const y = (1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1];
  return [x, y];
}

// Caminho: início → ponto médio desviado → fim (fazendo arco)
const path = [
  [100, 100],
  [targetX - 200, targetY + 80],
  [targetX, targetY],
];

// Depois sobreponha Perlin Noise muito pequeno (±2px) para criar "mão trêmula"
const jitterX = (simpleNoise(t * 10) - 0.5) * 4;
const jitterY = (simpleNoise(t * 10 + 100) - 0.5) * 4;
```

### 3.6 "Contração por Transformação" do Logo (Morph)

A aparição do Logo nos três vídeos da Anthropic **nunca é um simples fade-in**, é **a transformação a partir do elemento visual anterior**.

**Padrão comum**: nos últimos 1-2 segundos, fazer Morph / Rotate / Converge, fazendo toda a narrativa "colapsar" no ponto da marca.

**Implementação de baixo custo** (sem morph real):
Faça o elemento visual anterior "colapsar" em um bloco de cor (scale → 0.1, translate para o centro),
então o bloco de cor "expande" para formar a wordmark. A transição usa 150ms de corte rápido + motion blur
(`filter: blur(6px)` → `0`).

```js
<Sprite start={13} end={14}>
  {/* Colapso: elemento anterior scale 0.1, opacity mantido, filter blur aumenta */}
  const scale = interpolate(t, [0, 0.5], [1, 0.1], Easing.expoOut);
  const blur = interpolate(t, [0, 0.5], [0, 6]);
</Sprite>
<Sprite start={13.5} end={15}>
  {/* Expansão: Logo do centro do bloco scale 0.1 → 1, blur 6 → 0 */}
  const scale = interpolate(t, [0, 0.6], [0.1, 1], Easing.overshoot);
  const blur = interpolate(t, [0, 0.6], [6, 0]);
</Sprite>
```

### 3.7 Fonte Dupla: Serifada + Não Serifada

- **Marca / Narração**: Serifada (com "sensação acadêmica / de publicação / de bom gosto")
- **UI / Código / Dados**: Não serifada + monoespaçada

**Usar uma única fonte é errado**. Serifada dá "bom gosto", não serifada dá "função".

A escolha específica da fonte segue o brand spec (pilha Display / Body / Mono do brand-spec.md) ou as 20 filosofias do Consultor de Direção de Design. Este reference não fornece fontes específicas — isso é **decisão de marca**.

### 3.8 Troca de Foco = Fundo Atenuado + Primeiro Plano Nitidificado + Flash de Guia

A troca de foco **não é apenas reduzir opacity**. A receita completa é:

```js
// Combinação de filtros para elementos fora de foco
tile.style.filter = `
  brightness(${1 - 0.5 * focusIntensity})
  saturate(${1 - 0.3 * focusIntensity})
  blur(${focusIntensity * 4}px)        // ← Crucial: adicionar blur para realmente "recuar"
`;
tile.style.opacity = 0.4 + 0.6 * (1 - focusIntensity);

// Após o foco, fazer um Flash highlight de 150ms na posição de foco para guiar o olhar de volta
focusOverlay.animate(
  [
    { background: "rgba(255,255,255,0.3)" },
    { background: "rgba(255,255,255,0)" },
  ],
  { duration: 150, easing: "ease-out" },
);
```

**Por que blur é obrigatório**: apenas com opacity + brightness, os elementos fora de foco ainda estão "nítidos",
visualmente não há efeito de "recuar para o fundo". blur(4-8px) faz os elementos fora de foco realmente recuarem uma camada de profundidade.

---

## 4. Técnicas Específicas de Movimento (Trechos de Código Prontos para Uso)

### 4.1 FLIP / Transição de Elemento Compartilhado

Botão "expandindo" em campo de entrada, **não** é botão desaparecendo + novo painel aparecendo. O núcleo é **o mesmo elemento DOM** fazendo transição entre dois estados, não dois elementos fazendo cross-fade.

```jsx
// Usando Framer Motion layoutId
<motion.div layoutId="design-button">Design</motion.div>
// ↓ Após clique, mesmo layoutId
<motion.div layoutId="design-button">
  <input placeholder="Descreva seu design..." />
</motion.div>
```

Implementação nativa: https://aerotwist.com/blog/flip-your-animations/

### 4.2 Expansão "Respiratória" (width → height)

A expansão de um painel **não é puxar width e height simultaneamente**, mas sim:

- Primeiros 40% do tempo: apenas width (mantendo height pequeno)
- Últimos 60% do tempo: width mantido, expande height

Isso simula a sensação física de "primeiro desenrolar, depois preencher".

```js
const widthT = interpolate(t, [0, 0.4], [0, 1], Easing.expoOut);
const heightT = interpolate(t, [0.3, 1], [0, 1], Easing.expoOut);
style.width = `${widthT * targetW}px`;
style.height = `${heightT * targetH}px`;
```

### 4.3 Staggered Fade-up (30ms de intervalo)

Linhas de tabela, colunas de cards, itens de lista ao entrar, **cada elemento atrasa 30ms**, `translateY` de 10px volta a 0.

```js
rows.forEach((row, i) => {
  const localT = Math.max(0, t - i * 0.03); // 30ms stagger
  row.style.opacity = interpolate(localT, [0, 0.3], [0, 1], Easing.expoOut);
  row.style.transform = `translateY(${interpolate(
    localT,
    [0, 0.3],
    [10, 0],
    Easing.expoOut,
  )}px)`;
});
```

### 4.4 Respiração Não Linear · Pausa de 0,5s Antes do Resultado-Chave

A execução da máquina é rápida e contínua, mas **pausar 0,5s antes do resultado-chave aparecer** dá tempo ao cérebro do espectador para reagir.

```jsx
// Cenário típico: IA termina de gerar → pausa 0,5s → resultado aparece
<Sprite start={8} end={8.5}>
  {/* Pausa de 0,5s — nada se move, o espectador foca no estado de carregamento */}
  <LoadingState />
</Sprite>
<Sprite start={8.5} end={10}>
  <ResultAppear />
</Sprite>
```

**Contraexemplo**: IA termina de gerar e imediatamente faz transição suave para o resultado — o espectador não tem tempo de reação, a informação se perde.

### 4.5 Chunk Reveal · Simulando Token Streaming

A geração de texto por IA **não deve usar `setInterval` para caracteres individuais** (como legendas de filmes antigos), mas sim **chunk reveal**
— aparecem 2-5 caracteres por vez, com intervalo irregular, simulando a saída real de token streaming.

```js
// Dividir em chunks em vez de caracteres
const chunks = text.split(/(\s+|,\s*|\.\s*|;\s*)/); // Dividir por palavra + pontuação
let i = 0;
function reveal() {
  if (i >= chunks.length) return;
  element.textContent += chunks[i++];
  const delay = 40 + Math.random() * 80; // Irregular 40-120ms
  setTimeout(reveal, delay);
}
reveal();
```

### 4.6 Antecipação → Ação → Follow-through

3 dos 12 Princípios da Disney. A Anthropic os usa de forma explícita:

- **Antecipação**: antes do movimento começar, há um pequeno movimento reverso (botão encolhe ligeiramente antes de saltar)
- **Ação**: o movimento principal em si
- **Follow-through**: resquício após o movimento terminar (card dá um leve bounce ao pousar)

```js
// Três estágios completos da entrada de um card
const anticip = interpolate(t, [0, 0.2], [1, 0.95], Easing.easeIn); // Antecipação
const action = interpolate(t, [0.2, 0.7], [0.95, 1.05], Easing.expoOut); // Ação
const settle = interpolate(t, [0.7, 1], [1.05, 1], Easing.spring); // Estabilização
// scale final = produto dos 3 estágios ou aplicação segmentada
```

**Contraexemplo**: animação com apenas Ação, sem Antecipação + Follow-through, parece "animação de PowerPoint".

### 4.7 Perspectiva 3D + translateZ em Camadas

Para obter a aparência de "inclinação 3D + cards flutuantes", adicione perspective ao contêiner e diferentes translateZ aos elementos individuais:

```css
.stage-wrap {
  perspective: 2400px;
  perspective-origin: 50% 30%; /* Olhar ligeiramente de cima */
}
.card-grid {
  transform-style: preserve-3d;
  transform: rotateX(8deg) rotateY(-4deg); /* Proporção áurea */
}
.card:nth-child(3n) {
  transform: translateZ(30px);
}
.card:nth-child(5n) {
  transform: translateZ(-20px);
}
.card:nth-child(7n) {
  transform: translateZ(60px);
}
```

**Por que rotateX 8° / rotateY -4° é a proporção áurea**:

- Maior que 10° → distorção excessiva do elemento, parece "caindo"
- Menor que 5° → parece "cisalhamento" em vez de "perspectiva"
- A proporção assimétrica 8° × -4° simula o ângulo natural de "câmera no canto superior esquerdo da mesa olhando para baixo"

### 4.8 Pan Diagonal · Movendo XY Simultaneamente

O movimento da câmera não é puramente vertical ou horizontal, mas sim **movendo XY simultaneamente** simulando deslocamento diagonal:

```js
const panX = Math.sin(flowT * 0.22) * 40;
const panY = Math.sin(flowT * 0.35) * 30;
stage.style.transform = `
  translate(-50%, -50%)
  rotateX(8deg) rotateY(-4deg)
  translate3d(${panX}px, ${panY}px, 0)
`;
```

**Crucial**: as frequências de X e Y são diferentes (0.22 vs 0.35), evitando a regularização do ciclo de Lissajous.

---

## 5. Receitas de Cena (Três Templates Narrativos)

Os três vídeos do material de referência correspondem a três personalidades de produto. **Escolha a que melhor se adequa ao seu produto**, não misture.

### Receita A · Estilo Dramático Apple Keynote (tipo Claude Design)

**Adequado para**: lançamento de grande versão, animação hero, impacto visual prioritário
**Ritmo**: Lento-Rápido-Boom-Parada com arco forte
**Easing**: `expoOut` do início ao fim + pouca quantidade de `overshoot`
**Densidade de SFX**: alta (~0.4/s), tom do SFX ajustado à escala do BGM
**BGM**: IDM / techno minimalista, frio + preciso
**Fechamento**: zoom out abrupto → drop → transformação do Logo → nota única etérea → parada brusca

### Receita B · Estilo Ferramenta em Plano Sequência (tipo Claude Code)

**Adequado para**: ferramentas de desenvolvedor, apps de produtividade, cenários de fluxo
**Ritmo**: fluxo estável contínuo, sem picos evidentes
**Easing**: `spring` físico + `expoOut`
**Densidade de SFX**: **0** (puramente BGM conduz o ritmo de edição)
**BGM**: Lo-fi Hip-hop / Boom-bap, 85-90 BPM
**Técnica central**: ações-chave de UI sincronizadas com os transient kick/snare do BGM — **"o ritmo musical é o efeito sonoro da interação"**

### Receita C · Estilo Narrativo de Produtividade de Escritório (tipo Claude for Word)

**Adequado para**: software empresarial, documentos/planilhas/calendários, profissionalismo prioritário
**Ritmo**: múltiplas cenas com corte seco + Dolly In/Out
**Easing**: `overshoot` (toggle) + `expoOut` (painéis)
**Densidade de SFX**: média (~0.3/s), principalmente clique de UI
**BGM**: Instrumental Jazz, tom menor, BPM 90-95
**Destaque central**: uma cena deve ter obrigatoriamente o "ponto alto do vídeo inteiro" — 3D pop-out / flutuar para fora do plano

---

## 6. Contraexemplos · Assim é AI Slop

| Antipadrão                                      | Por que está errado                                                | Fazendo certo                                     |
| ----------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| `transition: all 0.3s ease`                     | `ease` é parente de linear, todos os elementos na mesma velocidade | Use `expoOut` + stagger por elemento              |
| Todas as entradas são `opacity 0→1`             | Sem direção de movimento                                           | Combine com `translateY 10→0` + Antecipação       |
| Logo com fade-in                                | Sem sensação de fechamento narrativo                               | Morph / Converge / Colapso-expansão               |
| Mouse em linha reta                             | Sensação subconsciente de máquina                                  | Arco Bezier + Perlin Noise                        |
| Digitação caractere por caractere (setInterval) | Parece legenda de filme antigo                                     | Chunk Reveal, intervalo aleatório                 |
| Resultado-chave sem pausa                       | Espectador sem tempo de reação                                     | Pausa de 0,5s antes do resultado                  |
| Troca de foco só altera opacity                 | Elementos fora de foco ainda nítidos                               | opacity + brightness + **blur**                   |
| Fundo preto puro / branco puro                  | Sensação cyber / cansaço por reflexo                               | Neutro com temperatura de cor (seguir brand spec) |
| Todas as animações na mesma velocidade          | Sem ritmo                                                          | Lento-Rápido-Boom-Parada                          |
| Finalização com Fade out                        | Sem sensação de decisão                                            | Parada brusca (segurar o último quadro)           |

---

## 7. Checklist de Autoverificação (60 segundos antes de entregar a animação)

- [ ] A estrutura narrativa é Lento-Rápido-Boom-Parada, não ritmo uniforme?
- [ ] O easing padrão é `expoOut`, não `easeOut` ou `linear`?
- [ ] Toggle / botão pop-out usou `overshoot`?
- [ ] Cards / listas de entrada têm 30ms de stagger?
- [ ] Há pausa de 0,5s antes do resultado-chave?
- [ ] A digitação usa Chunk Reveal, não setInterval caractere por caractere?
- [ ] A troca de foco adicionou blur (não apenas opacity)?
- [ ] O Logo é transformação (Morph), não fade-in?
- [ ] A cor de fundo não é preto/branco puro (com temperatura de cor)?
- [ ] O texto tem hierarquia de serifada + não serifada?
- [ ] O final é parada brusca, não fade out?
- [ ] (Se houver mouse) A trajetória do mouse é em arco, não em linha reta?
- [ ] A densidade de SFX corresponde à personalidade do produto (ver Receita A/B/C)?
- [ ] BGM e SFX têm diferença de 6-8dB de loudness? (ver `audio-design-rules.md`)

---

## 8. Relação com Outros References

| reference                   | Posicionamento                    | Relação                                             |
| --------------------------- | --------------------------------- | --------------------------------------------------- |
| `animation-pitfalls.md`     | Prevenção técnica (16 itens)      | **"Não fazer assim"** · O oposto deste arquivo      |
| `animations.md`             | Uso do motor Stage/Sprite         | Base de **como escrever** animações                 |
| `audio-design-rules.md`     | Regras de áudio de via dupla      | Regras de **áudio para animação**                   |
| `sfx-library.md`            | Lista de 37 SFX                   | **Biblioteca de materiais** de efeitos sonoros      |
| `apple-gallery-showcase.md` | Estilo de exibição Apple Gallery  | Especialização de um estilo específico de movimento |
| **Este arquivo**            | Sintaxe de motion design positivo | **"Fazer assim"**                                   |

**Ordem de chamada**:

1. Primeiro veja o workflow do SKILL.md, Etapa 3, as quatro perguntas de posicionamento (determinam papel narrativo e temperatura visual)
2. Após definir a direção, leia este arquivo para determinar a **linguagem de movimento** (Receita A/B/C)
3. Ao escrever código, consulte `animations.md` e `animation-pitfalls.md`
4. Ao exportar vídeo, siga `audio-design-rules.md` + `sfx-library.md`

---

## Apêndice · Fontes de Material deste Arquivo

- Análise de animações oficiais da Anthropic: `参考动画/BEST-PRACTICES.md` no diretório do projeto Huashu
- Análise de áudio da Anthropic: mesmo diretório `AUDIO-BEST-PRACTICES.md`
- 3 vídeos de referência: `ref-{1,2,3}.mp4` + respectivos `gemini-ref-*.md` / `audio-ref-*.md`
- **Filtro rigoroso**: este reference não inclui nenhum valor de cor de marca específico, nome de fonte ou nome de produto.
  Decisões de cor/fonte seguem o §1.a Protocolo de Ativos Principais ou as 20 filosofias de design.
