# Cinematic Patterns · Best Practice para Workflow Demo

> 5 padrões-chave para evoluir de "animação PPT" para "cinematográfica nível lançamento".
> Destilado de dois cinematic demos do deck "Falando sobre skill" de 2026-04 (workflow Nuwa + workflow Darwin), comprovadamente reproduzíveis.

---

## 0 · O Que Este Documento Resolve

Quando você precisa fazer uma "animação de demonstração de workflow" (cenário típico: workflow de skill, onboarding de produto, fluxo de chamada de API, execução de tarefa de agente), há duas abordagens comuns:

| Paradigma                 | Aparência                                                                             | Consequência                                                                                    |
| ------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Animação PPT** (ruim)   | step 1 fade in → step 2 fade in → step 3 fade in, 4 boxes na mesma tela               | Espectador sente "é só um PPT com efeito fade", sem wow moment                                  |
| **Cinematográfica** (boa) | baseada em cenas, uma coisa de cada vez, transições com dissolve / focus pull / morph | Espectador sente "isto é um trecho de lançamento de produto", vai querer printar e compartilhar |

A raiz da diferença **não é a técnica de animação**, é o **paradigma narrativo**. Este documento explica como evoluir do primeiro para o segundo.

---

## 1 · Cinco Padrões Centrais

### Padrão A · Estrutura de Duas Camadas: Dashboard + Cinematic Overlay

**Problema**: cinematic puro por padrão é tela preta + um botão ▶. Se o usuário chegar nesta página e não clicar, não vê nada.

**Solução**:

```
ESTADO DEFAULT (sempre visível): dashboard de workflow estático completo
  └── Espectador vê de relance como este skill / workflow funciona

GATILHO ▶ (overlay sobrepõe): cinematic de 22 segundos
  └── Ao terminar, fade automático de volta ao DEFAULT

```

**Pontos de implementação**:

- `.dash` default visible, `.cinema` default `opacity: 0; pointer-events: none`
- `.play-cta` é um pequeno botão dourado no canto inferior direito (não um grande overlay central)
- Clique → `cinema.classList.add('show')` + `dash.classList.add('hide')`
- Use `requestAnimationFrame` para executar uma vez (não em loop), ao finalizar `endCinematic()` reverte o estado

**Antipadrão**: default = grande overlay ▶ central cobrindo tudo, página fica em branco antes do clique.

---

### Padrão B · Baseado em Cenas, NÃO em Etapas

**Problema**: dividir a animação em "step 1 mostrar → step 2 mostrar → ..." é pensamento PPT.

**Solução**: dividir em 5 cenas, cada cena é um **enquadramento independente**, tela cheia focando apenas uma coisa:

| Tipo de Cena          | Responsabilidade                                                | Duração |
| --------------------- | --------------------------------------------------------------- | ------- |
| 1 · Invocação         | Gatilho de entrada do usuário (typewriter no terminal)          | 3-4s    |
| 2 · Processamento     | Visualização do workflow central (linguagem visual única)       | 5-6s    |
| 3 · Resultado/Insight | Produto-chave destilado (visualização)                          | 4-5s    |
| 4 · Saída             | Exibição do produto real (arquivo / diff / número)              | 3-4s    |
| 5 · Hero Reveal       | Momento hero de fechamento (letras grandes + proposta de valor) | 4-5s    |

**Duração total ≈ 22 segundos** — este é o comprimento ideal testado:

- Menos de 18s: o PM ainda não entrou no estado antes de terminar
- Mais de 25s: perde a paciência
- 22s é o suficiente para "enganchar → desenvolver → fechar → deixar impressão"

**Pontos de implementação**:

- `T = { DURATION: 22.0, s1_in: [0, 0.7], s2_in: [3.8, 4.6], ... }` timeline global
- Único `requestAnimationFrame(render)` executa todos os cálculos de opacity / transform de todas as cenas
- Não use cadeias de setTimeout (fáceis de quebrar, difíceis de depurar)
- Easing obrigatório: `expoOut` / `easeOut` / cubic-bezier, **proibido linear**

---

### Padrão C · A Linguagem Visual de Cada Demo Deve Ser Independente

**Problema**: após fazer o primeiro cinematic, ao fazer o segundo, por preguiça reutiliza o mesmo template (mesmo orbit + pentagon + typewriter + hero letras grandes), só trocando o texto.

**Consequência**: o espectador descobre que os dois skills "são idênticos", equivalendo a dizer "estes dois skills não têm diferença".

**Solução**: a metáfora central de cada workflow é diferente, portanto a linguagem visual deve ser diferente.

**Estudo de caso comparativo**:

| Dimensão         | Nuwa (Destilador de Pessoa)                           | Darwin (Otimizador de skill)                                    |
| ---------------- | ----------------------------------------------------- | --------------------------------------------------------------- |
| Metáfora central | Coletar → Destilar → Escrever                         | Ciclar → Avaliar → Catraca                                      |
| Movimento visual | Flutuação / Radiação / Pentágono                      | Ciclo / Ascensão / Comparação                                   |
| Cena 2           | 3D Orbit · 8 arquivos flutuando em elipse perspectiva | Spin Loop · token percorre 5 voltas em anel de 6 nós            |
| Cena 3           | Pentágono · 5 tokens irradiando do centro             | v1 vs v5 · diff lado a lado (versão vermelha vs versão dourada) |
| Cena 4           | SKILL.md typewriter                                   | Hill-Climb · curva desenhada em tela cheia                      |
| Cena 5 hero      | "21 minutos" serif itálico letras grandes             | Engrenagem giratória ⚙ + tag dourada "KEPT +1.1"                |

**Critério de avaliação**: tampe o texto, olhe apenas o visual, consegue distinguir qual demo é qual? Se não consegue, é preguiça.

---

### Padrão D · Use Materiais Reais Gerados por IA, Não Emoji ou SVG Desenhado à Mão

**Problema**: 3D orbit / gallery precisa de fragmentos de material flutuando, emoji (📚🎤) é feio e sem marca, lombada de livro desenhada em SVG nunca parece um livro real.

**Solução**: use `[autor]-gpt-image` para gerar uma imagem grande em grid 4×2 (8 itens relacionados ao tema · fundo branco · 60px de breathing space · estilo unificado), use `extract_grid.py --mode bbox` para recortar em 8 PNGs transparentes independentes.

**Pontos-chave do Prompt** (padrões detalhados de prompt veja a skill `[autor]-gpt-image`):

- Ancoragem de IP ("estética de arquivo Caltech dos anos 1960" / "tratamento consistente estilo Hearthstone")
- Fundo branco (fácil para recorte; fundo cinza tem boa atmosfera mas recorte de fundo transparente é difícil)
- 4×2, não 5×5 (evita bug de compressão na última linha)
- Persona finishing ("Você é um curador da Wired magazine preparando uma foto de exposição")

**Antipadrão**: usar emoji como ícone, usar silhueta CSS no lugar de imagem de produto.

---

### Padrão E · Sistema de Via Dupla: BGM + SFX

**Problema**: apenas animação sem som, o espectador subconscientemente sente "isto parece um demo pobre".

**Solução**: BGM de longa duração + 11 cues de SFX.

**Receita de SFX universal** (aplicável a workflow demo):

| Momento        | SFX         | Cena de Gatilho                                                           |
| -------------- | ----------- | ------------------------------------------------------------------------- |
| 0,10s          | whoosh      | Terminal subindo de baixo                                                 |
| 3,0s           | enter       | Typewriter concluído, pressiona enter                                     |
| 4,0s           | slide-in    | Elementos da cena 2 entrando                                              |
| 5-9s × 5 vezes | sparkle     | Marcos do processo-chave (cada geração / cada token / cada ponto de dado) |
| 14s            | click       | Transição para cena de saída                                              |
| 17,8s          | logo-reveal | Momento hero reveal                                                       |
| typewriter     | type        | Dispara a cada 2 caracteres (densidade não muito alta)                    |

**Isolamento de frequência**: BGM volume 0,32 (ruído de fundo de baixa frequência), SFX volume 0,55 (punch médio-alta frequência), sparkle 0,7 (para se destacar), logo-reveal 0,85 (momento hero mais forte).

**Controle do usuário**:

- Deve ter ▶ overlay de início (limitação de autoplay do navegador)
- Pequeno botão mute no canto superior direito (usuário pode silenciar a qualquer momento)
- Não fazer "ao chegar nesta página, toca forçadamente"

---

## 2 · Pontos de Design do Dashboard Estático

O Dashboard é a Camada 1 da estrutura de duas camadas. O PM pode entender este skill mesmo sem clicar em ▶.

**Layout**: grid de 3 colunas (ou 1 grande + 2 pequenas), cada painel resolve uma pergunta:

| Tipo de Painel                   | Resolve Qual Pergunta                 | Exemplo                                                                   |
| -------------------------------- | ------------------------------------- | ------------------------------------------------------------------------- |
| **Pipeline / Diagrama de Fluxo** | "Qual é o workflow deste skill?"      | Pipeline de 4 estágios Nuwa · Loop de autoresearch Darwin                 |
| **Snapshot / Estado**            | "Como são os dados reais gerados?"    | Snapshot de rubrica de 8 dimensões Darwin                                 |
| **Trajetória / Evolução**        | "Como muda após múltiplas execuções?" | Curva hill-climb de 5 gerações Darwin                                     |
| **Exemplos / Galeria**           | "O que já foi produzido?"             | Galeria de 21 personas Nuwa                                               |
| **Strip · Exemplo I/O**          | "O que entra → o que sai"             | Strip de exemplo Nuwa: `› nuwa destilar feynman → feynman.skill (21 min)` |

**Restrições-chave**:

- Densidade de informação suficiente (cada painel deve carregar informação diferenciada)
- Mas não pode entupir de dados (cada número deve ter significado)
- Esquema de cores consistente com o cinematic (mesma família de cores, para transição suave)

---

## 3 · Ferramentas de Depuração e Desenvolvimento

Qualquer animação longa deve vir com três ferramentas de desenvolvimento, senão a depuração explode.

### Ferramenta 1 · `?seek=N` Congela no N-ésimo Segundo

```js
const seek = parseFloat(params.get("seek"));
if (!isNaN(seek)) {
  started = true;
  muted = true;
  frozenT = seek; // render() usa este t em vez de elapsed
  cinema.classList.add("show");
  dash.classList.add("hide");
}

// Em render():
let t = frozenT !== null ? frozenT : elapsed % T.DURATION;
```

Uso: `http://.../slide.html?seek=12` vê diretamente a imagem do 12º segundo, sem esperar a reprodução.

### Ferramenta 2 · `?autoplay=1` Pula o Overlay ▶

Facilita captura automática de tela com Playwright, também útil para forçar início ao incorporar em iframe.

### Ferramenta 3 · Botão REPLAY Manual

Pequeno botão no canto superior direito, usuário/depurador pode repetir quantas vezes quiser. CSS:

```css
.replay {
  position: absolute;
  top: 18px;
  right: 18px;
  background: rgba(212, 165, 116, 0.1);
  border: 1px solid rgba(212, 165, 116, 0.3);
  color: #d4a574;
  font-family: monospace;
  font-size: 10px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  padding: 6px 12px;
  border-radius: 1px;
  cursor: pointer;
  backdrop-filter: blur(6px);
  z-index: 6;
}
```

---

## 4 · Armadilhas de Incorporação em iframe (se o cinematic estiver embutido em um deck)

### Armadilha 1 · Zona de clique do pai intercepta botões dentro do iframe

Se o deck index.html adicionou "zonas de clique transparentes de 22vw esquerda/direita para virar página", elas **cobrirão o botão ▶ play dentro do iframe** — o clique do usuário no botão é engolido como "próxima página".

**Correção**: a zona de clique adiciona `top: 12vh; bottom: 25vh`, dando 25% no topo e na base sem interceptação, permitindo que o ▶ central e o ▶ no canto inferior direito dentro do iframe sejam clicáveis.

### Armadilha 2 · iframe rouba foco, eventos de teclado perdidos

Após o usuário clicar no iframe, o foco está dentro do iframe, os eventos de teclado ←/→ da janela pai não são recebidos.

**Correção**:

```js
iframe.addEventListener('load', () => {
  // Injetar retransmissor de teclado
  const doc = iframe.contentDocument;
  doc.addEventListener('keydown', (e) => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: e.key, ... }));
  });
  // Após clique, trazer foco de volta para a janela pai
  doc.addEventListener('click', () => setTimeout(() => window.focus(), 0));
});
```

### Armadilha 3 · Diferenças de comportamento file:// vs https://

O cinematic testado localmente com file:// pode quebrar após implantação, porque:

- Em file://, iframe contentDocument tem mesma origem
- Em https://, também tem mesma origem (se mesmo host), mas a restrição de autoplay de áudio é mais rigorosa

**Correção**:

- Antes de implantar, use `python3 -m http.server` para iniciar um servidor HTTP local e testar
- BGM deve aguardar o clique do usuário em ▶ para `bgm.play()`, não tocar imediatamente no page-load

---

## 5 · Tabela Rápida de Antipadrões

| ❌ Antipadrão                                              | ✅ Padrão Correto                                                                |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Default = tela preta ▶ overlay                             | Default = dashboard estático, ▶ é auxiliar                                       |
| 4 steps lado a lado na mesma tela com fade in              | 5 cenas em tela cheia, cada uma focando uma coisa                                |
| Reutilizar template trocando texto para demos diferentes   | Cada demo com linguagem visual independente (tampe o texto e consiga distinguir) |
| Emoji / SVG desenhado à mão como material                  | Imagem grande gpt-image-2 + extract_grid para recorte                            |
| Sem BGM sem SFX                                            | Sistema de via dupla BGM + 11 SFX cues                                           |
| Usar cadeia de setTimeout para agendar                     | requestAnimationFrame + objeto de timeline global T                              |
| Animação linear                                            | Expo / cubic-bezier easing                                                       |
| Sem ferramentas de desenvolvimento                         | `?seek=N` + `?autoplay=1` + botão REPLAY                                         |
| Botão dentro do iframe engolido pela zona de clique do pai | Zona de clique adiciona margem top/bottom para dar espaço aos botões             |

---

## 6 · Orçamento de Tempo

Seguindo estes padrões, um cinematic demo completo (incluindo dashboard):

| Tarefa                                                          | Tempo                                                    |
| --------------------------------------------------------------- | -------------------------------------------------------- |
| Projetar narrativa de 5 cenas + linguagem visual                | 30 minutos (deve ser criterioso, decide a independência) |
| Layout estático do Dashboard + conteúdo                         | 1 hora                                                   |
| Implementação das 5 cenas Cinematic                             | 1,5 hora                                                 |
| Ajuste de timing dos Audio cues + botão replay                  | 30 minutos                                               |
| Verificação de captura de tela Playwright para 5 momentos-chave | 15 minutos                                               |
| **Total de um demo**                                            | **3-4 horas**                                            |

O segundo demo reutiliza o framework mas **a linguagem visual deve ser independente**, tempo aproximado de 2-3 horas.
