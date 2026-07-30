# Slide Decks: Especificação para Criação de Slides em HTML

Fazer slides é um cenário de alta frequência no trabalho de design. Este documento explica como fazer bons slides em HTML — desde a escolha da arquitetura, design de página individual, até o caminho completo de exportação para PDF/PPTX.

**Cobertura de capacidades desta skill**:

- **Versão de apresentação HTML (produto base, sempre obrigatório por padrão)** → Cada página em HTML independente + `assets/deck_index.html` agregador, navegação por teclado no navegador, apresentação em tela cheia
- HTML → Exportação PDF → `scripts/export_deck_pdf.mjs` / `scripts/export_deck_stage_pdf.mjs`
- HTML → Exportação PPTX editável → `references/editable-pptx.md` + `scripts/html2pptx.js` + `scripts/export_deck_pptx.mjs` (requer HTML escrito com 4 restrições rígidas)

> **⚠️ HTML é a base, PDF/PPTX são derivados.** Independentemente do formato final de entrega, **deve-se** primeiro fazer a versão de apresentação HTML agregada (`index.html` + `slides/*.html`), que é a "fonte" do trabalho de slides. PDF/PPTX são snapshots exportados do HTML com um comando.
>
> **Por que HTML primeiro**:
>
> - Melhor para apresentações ao vivo (projetor / compartilhamento de tela direto em tela cheia, navegação por teclado, sem depender de Keynote/PPT)
> - Durante o desenvolvimento, cada página pode ser aberta individualmente com duplo clique para verificação, sem precisar reexecutar a exportação
> - É o único upstream para exportação PDF/PPTX (evita o ciclo vicioso de "exportar, depois descobrir que precisa alterar HTML e exportar novamente")
> - O entregável pode ser "HTML + PDF" ou "HTML + PPTX" em duplicata, o receptor usa o que preferir
>
> 2026-04-22 moxt brochure testado na prática: após fazer 13 páginas HTML + index.html agregador, `export_deck_pdf.mjs` exportou PDF com um comando, zero alterações. A versão HTML em si já é um entregável que pode ser apresentado diretamente no navegador.

---

## 🛑 Antes de Começar, Confirme o Formato de Entrega (Checkpoint Mais Importante)

**Esta decisão vem antes de "arquivo único ou múltiplos arquivos".** 2026-04-20 Projeto期权私董会 testado na prática: **não confirmar o formato de entrega antes de começar = 2-3 horas de retrabalho.**

### Árvore de Decisão (Arquitetura HTML-first)

Todas as entregas partem do mesmo conjunto de páginas HTML agregadas (`index.html` + `slides/*.html`). O formato de entrega só determina **as restrições de escrita do HTML** e **o comando de exportação**:

```
【Sempre padrão · Obrigatório】 Versão de apresentação HTML agregada (index.html + slides/*.html)
   │
   ├── Apenas apresentação no navegador / arquivo HTML local → Já está completo aqui, HTML com máxima liberdade visual
   │
   ├── Também precisa de PDF (impressão / compartilhar / arquivar) → Execute export_deck_pdf.mjs com um comando
   │                                                                    Escrita HTML livre, sem restrições visuais
   │
   └── Também precisa de PPTX editável (colegas vão alterar texto) → Desde a primeira linha do HTML, escreva com as 4 restrições rígidas
                                                                       Execute export_deck_pptx.mjs com um comando
                                                                       Sacrifique gradientes / web component / SVG complexo
```

### Roteiro para Começar (Copie e Use)

> Independentemente de a entrega final ser HTML, PDF ou PPTX, vou primeiro fazer uma versão HTML agregada que pode ser navegada e apresentada no navegador (`index.html` com navegação por teclado) — este é o produto base padrão permanente. A partir disso, pergunto se você quer snapshots adicionais em PDF / PPTX.
>
> Qual formato de exportação você precisa?
>
> - **Apenas HTML** (apresentação/arquivamento) → Liberdade visual total
> - **Também PDF** → Mesmo que acima, mais um comando de exportação
> - **Também PPTX editável** (colegas vão alterar texto no PPT) → Preciso escrever o HTML desde a primeira linha com 4 restrições rígidas, sacrificando algumas capacidades visuais (sem gradientes, sem web component, sem SVG complexo).

### Por que "PPTX exige 4 restrições rígidas desde o início"

A premissa do PPTX editável é que `html2pptx.js` consiga traduzir o DOM elemento por elemento para objetos do PowerPoint. Ele precisa de **4 restrições rígidas**:

1. body fixo em 960pt × 540pt (correspondente a `LAYOUT_WIDE`, 13.333″ × 7.5″, não 1920×1080px)
2. Todo texto deve estar dentro de `<p>`/`<h1>`-`<h6>` (proibido div com texto direto, proibido `<span>` como portador de texto principal)
3. `<p>`/`<h*>` não podem ter background/border/shadow próprios (coloque em div externa)
4. `<div>` não pode usar `background-image` (use tag `<img>`)
5. Não use CSS gradient, não use web component, não use SVG decorativo complexo

**Esta skill tem por padrão alta liberdade visual em HTML** — muitos spans, flex aninhados, SVG complexo, web components (como `<deck-stage>`), gradientes CSS — **quase nenhuma passa naturalmente pelas restrições do html2pptx** (testado na prática: HTML orientado a visual direto no html2pptx, taxa de aprovação < 30%).

### Comparação de Custo das Duas Abordagens Reais (Armadilha Real em 2026-04-20)

| Abordagem                                                    | Método                                                           | Resultado                                                                                                                                                                 | Custo                                                                                                                                           |
| ------------------------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| ❌ **Escrever HTML livre primeiro, remediar PPTX depois**    | Arquivo único deck-stage + muitos SVG/span decorativos           | Para PPTX editável, só restam dois caminhos:<br>A. Escrever centenas de linhas de pptxgenjs com coordenadas hard-coded<br>B. Reescrever 17 páginas HTML no formato Path A | 2-3 horas de retrabalho, e a versão manual tem **custo de manutenção perpétuo** (qualquer alteração no HTML exige sincronização manual no PPTX) |
| ✅ **Escrever desde o primeiro passo com restrições Path A** | Cada página HTML independente + 4 restrições rígidas + 960×540pt | Um comando exporta PPTX 100% editável, e também pode ser apresentado em tela cheia no navegador (Path A HTML é HTML padrão reproduzível no navegador)                     | 5 minutos extras ao escrever HTML pensando "como colocar texto dentro de `<p>`", zero retrabalho                                                |

### E Se For Entrega Mista?

Usuário diz "quero apresentação HTML **e** PPTX editável" — **isso não é misto**, é o requisito PPTX cobrindo o requisito HTML. O HTML escrito no formato Path A já pode ser apresentado em tela cheia no navegador (basta adicionar um `deck_index.html`拼接器). **Sem custo adicional.**

Usuário diz "quero PPTX **e** animação / web component" — **isso é realmente contraditório**. Diga ao usuário: para PPTX editável, é preciso sacrificar essas capacidades visuais. Deixe-o fazer a escolha, não implemente secretamente a solução manual pptxgenjs (que se torna dívida de manutenção perpétua).

### E Se Só Depois Descobrir que Precisa de PPTX (Remediação de Emergência)

Casos raros: o HTML já foi escrito e só então descobre-se que precisa de PPTX. Recomenda-se seguir o **fluxo de fallback** (instruções completas em `references/editable-pptx.md` seção "Fallback: Já há rascunho visual, mas usuário insiste em PPTX editável"):

1. **Primeira opção: exportar PDF** (100% de fidelidade visual, multiplataforma, o receptor pode ver e imprimir) — se a necessidade real do receptor é "apresentação/arquivamento", PDF é o melhor entregável
2. **Segunda opção: IA reescreve uma versão editable HTML baseada no rascunho visual** → exporta editable PPTX — preserva as decisões de design de cor/layout/texto, sacrifica gradientes, web component, SVG complexo etc.
3. **Não recomendado: reconstruir manualmente com pptxgenjs** — posição, fonte, alinhamento tudo ajustado manualmente, custo de manutenção alto, e qualquer alteração futura no HTML exige sincronização manual novamente

Sempre apresente as opções ao usuário e deixe-o decidir. **Nunca comece a escrever pptxgenjs como primeira reação** — esse é o último recurso.

---

## 🛑 Antes da Produção em Lote: Faça 2 Páginas Showcase para Definir a Gramática

**Se o deck tiver ≥ 5 páginas, nunca escreva da página 1 até a última diretamente.** Ordem correta validada na prática pelo moxt brochure 2026-04-22:

1. Selecione **2 tipos de página com maior diferença visual** para fazer showcase (ex: "capa" + "página de emoção/citação", ou "capa" + "página de demonstração de produto")
2. Capture a tela e peça confirmação do usuário sobre a gramática (masthead / fonte / cor / espaçamento / estrutura / proporção chinês-inglês)
3. Se a direção for aprovada, produza em lote as N-2 páginas restantes, cada uma reutilizando a gramática estabelecida
4. Após concluir todas, monte o HTML agregado + derivados PDF / PPTX

**Por quê**: Escrever 13 páginas direto → usuário diz "direção errada" = retrabalho de 13 vezes. Primeiro fazer 2 páginas showcase → direção errada = retrabalho de 2 vezes. Uma vez que a gramática visual é estabelecida, o espaço de decisão para as N páginas seguintes é drasticamente reduzido, restando apenas "como colocar o conteúdo".

**Princípio de seleção das páginas showcase**: Escolha as duas páginas com estruturas visuais mais diferentes. Se estas passarem, as outras intermediárias também passam.

| Tipo de Deck                         | Combinação Recomendada de Showcase                                      |
| ------------------------------------ | ----------------------------------------------------------------------- |
| Brochura B2B / Lançamento de produto | Capa + Página de conteúdo (página de conceito/emoção)                   |
| Lançamento de marca                  | Capa + Página de características do produto                             |
| Relatório de dados                   | Página de visão geral dos dados + Página de conclusão da análise        |
| Material didático/tutorial           | Página de capa de capítulo + Página de ponto de conhecimento específico |

---

## 📐 Template de Gramática para Publicação (Reutilizável, Testado com moxt)

Adequado para brochura B2B / lançamento de produto / decks de relatórios longos. Cada página reutiliza esta estrutura = 13 páginas visualmente consistentes, zero retrabalho.

### Estrutura de Cada Página

```
┌─ masthead (faixa superior + linha) ────────────────────────┐
│  [logo 22-28px] · A Product Brochure                Edição · Data · URL │
├──────────────────────────────────────────┤
│                                          │
│  ── kicker (traço curto verde + rótulo uppercase)   │
│  CAPÍTULO XX · NOME DA SEÇÃO                 │
│                                          │
│  H1 (chinês Noto Serif SC 900)             │
│  Palavras-chave em cor principal da marca   │
│                                          │
│  Subtítulo em inglês (Lora itálico)   │
│  ─────────── Linha divisória ──────────            │
│                                          │
│  [Conteúdo específico: duas colunas 60/40 / grid 2x2 / lista] │
│                                          │
├──────────────────────────────────────────┤
│ nome da seção                     XX / total │
└──────────────────────────────────────────┘
```

### Convenções de Estilo (Copie Diretamente)

- **H1**: Chinês Noto Serif SC 900, tamanho 80-140px dependendo do volume de informação, palavras-chave em cor principal da marca (não colorir o texto inteiro)
- **Subtítulo inglês**: Lora itálico 26-46px, palavras de assinatura da marca (ex: "AI team") em negrito + itálico na cor principal
- **Corpo do texto**: Noto Serif SC 17-21px, line-height 1.75-1.85
- **Destaque accent**: No corpo do texto, use a cor principal em negrito para marcar palavras-chave, no máximo 3 por página (mais que isso perde o efeito de âncora)
- **Fundo**: Base creme quente #FAFAFA + radial-gradient noise muito sutil (`rgba(33,33,33,0.015)`) para aumentar a sensação de papel

### O Protagonista Visual Deve Ser Diferenciado

Se 13 páginas forem todas "texto + screenshot", fica muito monótono. ** alterne o tipo de protagonista visual a cada página**:

| Tipo Visual                                               | Seção Adequada                                            |
| --------------------------------------------------------- | --------------------------------------------------------- |
| Layout de capa (letras grandes + masthead + pilar)        | Página inicial / Capa de capítulo                         |
| Retrato de personagem único (momo gigante etc.)           | Apresentar conceito/personagem único                      |
| Vários personagens juntos / cards de avatar lado a lado   | Equipe / Casos de usuário                                 |
| Cards de timeline em progressão                           | Mostrar "relacionamento de longo prazo", "evolução"       |
| Grafo de conhecimento / diagrama de nós conectados        | Mostrar "colaboração", "fluxo"                            |
| Card de comparação Antes/Depois + seta no meio            | Mostrar "mudança", "diferença"                            |
| Screenshot de UI do produto + moldura de dispositivo      | Demonstração de funcionalidade específica                 |
| Big-quote com aspas grandes (meia página, letras grandes) | Página de emoção / página de problema / página de citação |
| Foto de pessoa real + card de depoimento (2×2 ou 1×4)     | Depoimento de usuário / cenário de uso                    |
| Contracapa com letras grandes + botão oval com URL        | CTA / Final                                               |

---

## ⚠️ Armadilhas Comuns (Resumo Prático do moxt)

### 1. Emoji não Renderiza no Chromium / Playwright

Chromium não vem com fonte de emoji colorida por padrão, então `page.pdf()` ou `page.screenshot()` mostram emoji como quadrado vazio.

**Contramedida**: Use símbolos de texto Unicode (`✦` `✓` `✕` `→` `·` `—`) como substitutos, ou mude diretamente para texto puro ("Email · 23" em vez de "📧 23 emails").

### 2. `export_deck_pdf.mjs` Erro `Cannot find package 'playwright'`

Causa: A resolução de módulos ESM procura `node_modules` a partir do diretório do script. O script está em `~/.claude/skills/huashu-design/scripts/`, onde não há dependências.

**Contramedida**: Copie o script para o diretório do projeto deck (ex: `brochure/build-pdf.mjs`), execute `npm install playwright pdf-lib` na raiz do projeto, depois `node build-pdf.mjs --slides slides --out output/deck.pdf`.

### 3. Google Fonts não Carregou Antes do Screenshot → Chinês Mostra Fonte Padrão do Sistema

Antes de screenshot/PDF do Playwright, aguarde `wait-for-timeout=3500` para o webfont baixar e pintar. Ou coloque a fonte em self-host em `shared/fonts/` para reduzir dependência de rede.

### 4. Desequilíbrio de Densidade de Informação: Página de Conteúdo com Excesso

A primeira versão da página de filosofia do moxt usava 2×2 = 4 parágrafos + 3 credos no rodapé = 7 blocos de conteúdo, apertado e repetitivo. Mudando para 1×3 = 3 parágrafos, a sensação de respiração voltou imediatamente.

**Contramedida**: Cada página deve ter no máximo "1 informação central + 3-4 pontos auxiliares + 1 protagonista visual". Se exceder, divida em nova página. **Menos é mais** — o público vê uma página por 10 segundos, dar a ele 1 ponto de memória é mais fácil de lembrar do que 4.

---

## 🛑 Primeiro Defina a Arquitetura: Arquivo Único ou Múltiplos Arquivos?

**Esta escolha é o primeiro passo ao fazer slides. Se errar, vai bater repetidamente. Leia esta seção inteira antes de começar.**

### Comparação das Duas Arquiteturas

| Dimensão                     | Arquivo Único + `deck_stage.js`                            | **Múltiplos Arquivos + `deck_index.html`拼接器**                                    |
| ---------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Estrutura de código          | Um HTML, todos os slides são `<section>`                   | Cada página HTML independente, `index.html` usa iframe para拼接                     |
| Escopo CSS                   | ❌ Global, estilo de uma página pode afetar todas          | ✅ Isolamento natural, cada iframe tem seu próprio escopo                           |
| Granularidade de verificação | ❌ Precisa de JS goTo para navegar até uma página          | ✅ Arquivo de página única pode ser aberto com duplo clique no navegador            |
| Desenvolvimento paralelo     | ❌ Um arquivo, múltiplos agentes alterando causam conflito | ✅ Múltiplos agentes podem fazer páginas diferentes em paralelo, merge sem conflito |
| Dificuldade de depuração     | ❌ Um erro de CSS quebra o deck inteiro                    | ✅ Erro em uma página afeta apenas ela                                              |
| Interação embutida           | ✅ Compartilhar estado entre páginas é simples             | 🟡 Entre iframes precisa de postMessage                                             |
| Impressão PDF                | ✅ Embutido                                                | ✅ O拼接器 beforeprint percorre iframes                                             |
| Navegação por teclado        | ✅ Embutido                                                | ✅ Embutido no拼接器                                                                |

### Qual Escolher? (Árvore de Decisão)

```
│ Pergunta: Quantas páginas o deck deve ter?
├── ≤10 páginas, precisa de animação in-deck ou interação entre páginas, pitch deck → Arquivo único
└── ≥10 páginas, palestra acadêmica, material didático, deck longo, múltiplos agentes paralelos → Múltiplos arquivos (recomendado)
```

**Padrão: caminho de múltiplos arquivos**. Não é "alternativa", é o **caminho principal para decks longos e colaboração em equipe**. Motivo: cada vantagem da arquitetura de arquivo único (navegação por teclado, impressão, scale) está presente em múltiplos arquivos, enquanto o isolamento de escopo e a verificabilidade dos múltiplos arquivos não podem ser compensados pelo arquivo único.

### Por que Esta Regra é Tão Rígida? (Registro de Acidente Real)

A arquitetura de arquivo único já caiu em quatro armadilhas consecutivas na produção de um deck de palestra de psicologia com IA:

1. **Sobreposição de especificidade CSS**: `.emotion-slide { display: grid }` (especificidade 10) sobrescreveu `deck-stage > section { display: none }` (especificidade 2), fazendo todas as páginas renderizarem simultaneamente sobrepostas.
2. **Regra de slot do Shadow DOM suprimida por CSS externo**: `::slotted(section) { display: none }` não resistiu à sobreposição da regra externa, sections se recusavam a esconder.
3. **Condição de corrida entre localStorage + navegação por hash**: Após refresh, não navegava para a posição do hash, mas parava na posição antiga registrada no localStorage.
4. **Custo de verificação alto**: Precisava de `page.evaluate(d => d.goTo(n))` para capturar uma página, duas vezes mais lento que `goto(file://.../slides/05-X.html)`, e frequentemente dava erro.

Todas as causas raiz são **espaço de nomes global único** — a arquitetura de múltiplos arquivos elimina esses problemas no nível físico.

---

## Caminho A (Padrão): Arquitetura de Múltiplos Arquivos

### Estrutura de Diretórios

```
MeuDeck/
├── index.html              # Copiado de assets/deck_index.html, altere MANIFEST
├── shared/
│   ├── tokens.css          # Design tokens compartilhados (paleta/tamanhos de fonte/chrome comum)
│   └── fonts.html          # <link> para importar Google Fonts (cada página inclui)
└── slides/
    ├── 01-cover.html       # Cada arquivo é um HTML 1920×1080 completo
    ├── 02-agenda.html
    ├── 03-problem.html
    └── ...
```

### Template de Estrutura para Cada Slide

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <title>P05 · Título do Capítulo</title>
    <link
      href="https://fonts.googleapis.com/css2?family=..."
      rel="stylesheet"
    />
    <link rel="stylesheet" href="../shared/tokens.css" />
    <style>
      /* Estilos exclusivos desta página. Qualquer nome de classe não poluirá outras páginas. */
      body { padding: 120px; }
      .minha-coisa { ... }
    </style>
  </head>
  <body>
    <!-- Conteúdo 1920×1080 (width/height do body fixados em tokens.css) -->
    <div class="page-header">...</div>
    <div>...</div>
    <div class="page-footer">...</div>
  </body>
</html>
```

**Restrições principais**:

- `<body>` é a tela de desenho, faça o layout diretamente nele. Não envolva em `<section>` ou outro wrapper.
- `width: 1920px; height: 1080px` é fixado pela regra `body` em `shared/tokens.css`.
- Importe `shared/tokens.css` para tokens de design compartilhados (paleta, tamanhos de fonte, page-header/footer etc.).
- Cada página escreve seu próprio `<link>` de fontes (importar fonts separadamente não é caro e garante que cada página pode ser aberta independentemente).

###拼接器: `deck_index.html`

**Copie diretamente de `assets/deck_index.html`**. Você só precisa alterar uma coisa — o array `window.DECK_MANIFEST`, listando todos os nomes de arquivos de slide e rótulos legíveis em ordem:

```js
window.DECK_MANIFEST = [
  { file: "slides/01-cover.html", label: "Capa" },
  { file: "slides/02-agenda.html", label: "Índice" },
  { file: "slides/03-problem.html", label: "Declaração do Problema" },
  // ...
];
```

O拼接器 já vem com: navegação por teclado (←/→/Home/End/teclas numéricas/P para imprimir), scale + letterbox, contador no canto inferior direito, memória localStorage, navegação por hash, modo de impressão (percorre iframes e gera PDF por página).

### Verificação de Página Única (Esta é a Vantagem Killer da Arquitetura de Múltiplos Arquivos)

Cada slide é um HTML independente. **Ao terminar um slide, abra com duplo clique no navegador**:

```bash
open slides/05-personas.html
```

Screenshot com Playwright também é direto `goto(file://.../slides/05-personas.html)`, sem precisar de JS para navegar, e sem interferência de CSS de outras páginas. Isso torna o fluxo de trabalho "altere um pouco, verifique um pouco" com custo próximo de zero.

### Desenvolvimento Paralelo

Distribua a tarefa de cada slide para agentes diferentes, executando simultaneamente — os arquivos HTML são independentes entre si, sem conflitos no merge. Decks longos usando esta abordagem paralela podem reduzir o tempo de produção para 1/N.

### O que `shared/tokens.css` Deve Conter

Coloque apenas o que é **realmente compartilhado entre páginas**:

- Variáveis CSS (paleta, escala de fontes, escala de espaçamento)
- `body { width: 1920px; height: 1080px; }` para fixar o canvas
- `.page-header` / `.page-footer` — chrome que todas as páginas usam exatamente igual

**Não** coloque classes de layout de página única aqui — isso degradaria de volta ao problema de poluição global da arquitetura de arquivo único.

---

## Caminho B (Deck Pequeno): Arquivo Único + `deck_stage.js`

Adequado para ≤10 páginas, quando precisa compartilhar estado entre páginas (ex: um painel de ajustes React que controla todas as páginas), ou para pitch deck demo que exige extrema compactação.

### Uso Básico

1. Leia o conteúdo de `assets/deck_stage.js`, incorpore no `<script>` do HTML (ou `<script src="deck_stage.js">`)
2. No body, use `<deck-stage>` para envolver os slides
3. 🛑 **A tag script deve vir depois de `</deck-stage>`** (veja restrição rígida abaixo)

```html
<body>
  <deck-stage>
    <section>
      <h1>Slide 1</h1>
    </section>
    <section>
      <h1>Slide 2</h1>
    </section>
  </deck-stage>

  <!-- ✅ Correto: script depois de deck-stage -->
  <script src="deck_stage.js"></script>
</body>
```

### 🛑 Restrição Rígida de Posição do Script (Armadilha Real em 2026-04-20)

**Não coloque `<script src="deck_stage.js">` dentro de `<head>`.** Mesmo que ele defina `customElements` no `<head>`, quando o parser encontra a tag de abertura `<deck-stage>`, o `connectedCallback` é disparado — neste momento, os `<section>` filhos ainda não foram parseados, `_collectSlides()` retorna array vazio, o contador mostra `1 / 0`, e todas as páginas renderizam sobrepostas simultaneamente.

**Três formas corretas de escrever** (escolha uma):

```html
<!-- ✅ Mais recomendado: script depois de </deck-stage> -->
</deck-stage>
<script src="deck_stage.js"></script>

<!-- ✅ Também pode: script no head com defer -->
<head><script src="deck_stage.js" defer></script></head>

<!-- ✅ Também pode: script module tem defer natural -->
<head><script src="deck_stage.js" type="module"></script></head>
```

O `deck_stage.js` já tem defesa de atraso `DOMContentLoaded` embutida, então mesmo com script no head não quebra completamente — mas `defer` ou colocar no final do body ainda é a abordagem mais limpa, evitando depender de branches de defesa.

### ⚠️ Armadilhas de CSS na Arquitetura de Arquivo Único (Leia Obrigatoriamente)

A armadilha mais comum da arquitetura de arquivo único — **a propriedade `display` é roubada pelo estilo de página única**.

Erro comum 1 (escrever `display: flex` diretamente no section):

```css
/* ❌ Especificidade CSS 2, sobrescreve ::slotted(section){display:none} do shadow DOM (também 2) */
deck-stage > section {
  display: flex;            /* Todas as páginas renderizam sobrepostas! */
  flex-direction: column;
  padding: 80px;
  ...
}
```

Erro comum 2 (section com classe de especificidade maior):

```css
.emotion-slide {
  display: grid;
} /* Especificidade: 10, pior ainda */
```

Ambos fazem **todos os slides renderizarem sobrepostos simultaneamente** — o contador pode mostrar `1 / 10` fingindo normalidade, mas visualmente a primeira página cobre a segunda, que cobre a terceira.

### ✅ Starter CSS (Copie Diretamente ao Começar, Sem Armadilhas)

**O `section` em si** só gerencia "visível/invisível"; **layout (flex/grid etc.) escreva em `.active`**:

```css
/* section define apenas estilos genéricos não-display */
deck-stage > section {
  background: var(--paper);
  padding: 80px 120px;
  overflow: hidden;
  position: relative;
  /* ⚠️ Não escreva display aqui! */
}

/* Trava "não ativo = oculto" — dupla segurança de especificidade + peso */
deck-stage > section:not(.active) {
  display: none !important;
}

/* Página ativa escreve o display + layout necessário */
deck-stage > section.active {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Modo de impressão: todas as páginas devem aparecer, sobrescreve :not(.active) */
@media print {
  deck-stage > section {
    display: flex !important;
  }
  deck-stage > section:not(.active) {
    display: flex !important;
  }
}
```

Alternativa: **escreva o flex/grid de página única em um wrapper `<div>` interno**, o section em si é apenas um alternador de `display: block/none`. Esta é a abordagem mais limpa:

```html
<deck-stage>
  <section>
    <div class="slide-content flex-layout">...</div>
  </section>
</deck-stage>
```

### Dimensões Personalizadas

```html
<deck-stage width="1080" height="1920">
  <!-- 9:16 vertical -->
</deck-stage>
```

---

## Rótulos de Slide (Slide Labels)

Deck_stage e deck_index atribuem rótulos a cada página (exibidos no contador). Dê a eles rótulos **mais significativos**:

**Múltiplos arquivos**: No `MANIFEST`, escreva `{ file, label: "04 Declaração do Problema" }`
**Arquivo único**: No section, adicione `<section data-screen-label="04 Problem Statement">`

**Importante: A numeração dos slides começa em 1, não em 0.**

Quando o usuário diz "slide 5", ele se refere ao 5º slide, nunca à posição do array `[4]`. Humanos não falam em 0-indexed.

---

## Notas do Apresentador (Speaker Notes)

**Padrão: não adicionar**, só adicione quando o usuário solicitar explicitamente.

Com speaker notes, você pode reduzir o texto no slide ao mínimo, focando em visuais impactantes — as notes carregam o script completo.

### Formato

**Múltiplos arquivos**: No `<head>` do `index.html`, escreva:

```html
<script type="application/json" id="speaker-notes">
  ["Script do slide 1...", "Script do slide 2...", "..."]
</script>
```

**Arquivo único**: Mesma posição acima.

### Pontos Importantes na Escrita das Notes

- **Completas**: Não é um resumo, é o que realmente será dito
- **Conversacionais**: Como se fala normalmente, não linguagem escrita
- **Correspondentes**: O N-ésimo item do array corresponde ao N-ésimo slide
- **Tamanho**: 200-400 palavras é o ideal
- **Linha emocional**: Marque ênfases, pausas, pontos de destaque

---

## Padrões de Design de Slide

### 1. Estabeleça um Sistema (Obrigatório)

Após explorar o context de design, **primeiro diga verbalmente o sistema que você vai usar**:

```markdown
Sistema do Deck:

- Cor de fundo: no máximo 2 (90% branco + 10% section divider escuro)
- Tipografia: display com Instrument Serif, body com Geist Sans
- Ritmo: section divider com full-bleed colorido + texto branco, slide normal fundo branco
- Imagem: hero slide com foto full-bleed, data slide com gráfico

Vou seguir este sistema. Me diga se há problemas.
```

Confirme com o usuário antes de prosseguir.

### 2. Layouts de Slide Comuns

- **Slide de título**: Fundo sólido + título enorme + subtítulo + autor/data
- **Divisor de seção**: Fundo colorido + número do capítulo + título do capítulo
- **Slide de conteúdo**: Fundo branco + título + 1-3 bullet points
- **Slide de dados**: Título + gráfico/número grande + breve explicação
- **Slide de imagem**: Foto full-bleed + legenda pequena no rodapé
- **Slide de citação**: Espaço em branco + citação enorme + atribuição
- **Duas colunas**: Comparação esquerda/direita (vs / before-after / problem-solution)

Um deck deve usar no máximo 4-5 tipos de layout.

### 3. Escala (Reiterado)

- Texto do corpo mínimo **24px**, ideal 28-36px
- Título **60-120px**
- Texto hero **180-240px**
- Slides são vistos a 10 metros de distância, a fonte precisa ser grande o suficiente

### 4. Ritmo Visual

O deck precisa de **variedade intencional**:

- Ritmo de cor: maior parte fundo branco + ocasional section divider colorido + ocasional segmento escuro
- Ritmo de densidade: algumas páginas com muito texto + algumas com muitas imagens + algumas com citações e espaços em branco
- Ritmo de tamanho de fonte: título normal + ocasional texto hero gigante

**Não faça cada slide parecer igual** — isso é template de PPT, não design.

### 5. Espaço para Respirar (Obrigatório para Páginas Densas em Dados)

**O erro mais comum de iniciantes**: colocar todas as informações possíveis em uma única página.

Densidade de informação ≠ transmissão efetiva de informação. Decks acadêmicos/de apresentação exigem moderação:

- Páginas de lista/matriz: não desenhe N elementos com o mesmo tamanho. Use **hierarquia principal-secundário** — os 5 que serão discutidos hoje são ampliados como protagonistas, os outros 16 são reduzidos como dicas de fundo.
- Páginas com números grandes: o número em si é o protagonista visual. As legendas ao redor não devem ultrapassar 3 linhas, senão o olhar do público fica pulando de um lado para o outro.
- Páginas de citação: a citação e a atribuição devem ter espaçamento entre elas, não grudadas.

Faça a autoavaliação com base em dois critérios: "o dado é o protagonista?" e "o texto está amontoado?". Continue ajustando até que o espaço em branco te deixe um pouco desconfortável.

---

## Imprimir como PDF

**Múltiplos arquivos**: `deck_index.html` já trata o evento `beforeprint`, gerando PDF página por página.

**Arquivo único**: `deck_stage.js` também trata.

Os estilos de impressão já estão prontos, não é necessário escrever CSS `@media print` adicional.

---

## Exportar para PPTX / PDF (Scripts Autônomos)

HTML-first é o cidadão de primeira classe. Mas os usuários frequentemente precisam de entrega em PPTX/PDF. Dois scripts genéricos são fornecidos, **qualquer deck multi-arquivo pode usar**, localizados em `scripts/`:

### `export_deck_pdf.mjs` — Exportar PDF Vetorial (Arquitetura Multi-Arquivo)

```bash
node scripts/export_deck_pdf.mjs --slides <slides-dir> --out deck.pdf
```

**Características**:

- O texto **mantém-se vetorial** (copiável, pesquisável)
- Fidelidade visual 100% (Playwright incorpora Chromium para renderizar e imprimir)
- **Não precisa alterar nenhum caractere do HTML**
- Cada slide usa `page.pdf()` independente, depois mescla com `pdf-lib`

**Dependências**: `npm install playwright pdf-lib`

**Limitação**: PDF não pode mais editar texto — para alterar, volte ao HTML.

### `export_deck_stage_pdf.mjs` — Exclusivo para Arquitetura de Arquivo Único deck-stage ⚠️

**Quando usar**: quando o deck é um único arquivo HTML + web component `<deck-stage>` envolvendo N `<section>` (ou seja, arquitetura Caminho B). Neste caso, a abordagem do `export_deck_pdf.mjs` de "um `page.pdf()` por HTML" não funciona, sendo necessário usar este script dedicado.

```bash
node scripts/export_deck_stage_pdf.mjs --html deck.html --out deck.pdf
```

**Por que não pode reutilizar export_deck_pdf.mjs** (registro de problema real de 2026-04-20):

1. **Shadow DOM vence `!important`**: o CSS shadow do deck-stage tem `::slotted(section) { display: none }` (apenas a seção ativa fica `display: block`). Mesmo usando `@media print { deck-stage > section { display: block !important } }` no light DOM não adianta — após `page.pdf()` acionar a mídia print, o Chromium renderiza apenas a seção ativa, resultando em **apenas 1 página no PDF inteiro** (repetição do slide ativo atual).

2. **Loop goto em cada página ainda produz apenas 1 página**: a solução intuitiva "navegar para cada `#slide-N` e depois `page.pdf({pageRanges:'1'})`" também falha — porque as regras CSS de print fora do shadow DOM como `deck-stage > section { display: block }` são sobrescritas, e a renderização final é sempre a primeira seção da lista (não a página para a qual você navegou). Resultado: 17 iterações produzem 17 páginas P01 de capa.

3. **Elementos absolute vazam para a próxima página**: mesmo que todas as seções sejam renderizadas, se a própria seção tiver `position: static`, seus elementos absolute posicionados como `cover-footer`/`slide-footer` se posicionarão relativos ao initial containing block — quando a seção é forçada a 1080px de altura no print, o footer absolute pode ser empurrado para a próxima página (resultando em PDF com 1 página a mais que o número de seções, sendo essa página extra apenas um footer órfão).

**Estratégia de correção** (já implementada no script):

```js
// Após abrir o HTML, use page.evaluate para extrair as seções do slot deck-stage,
// colocá-las diretamente em uma div comum dentro do body, com style inline garantindo position:relative + tamanho fixo
await page.evaluate(() => {
  const stage = document.querySelector("deck-stage");
  const sections = Array.from(stage.querySelectorAll(":scope > section"));
  document.head.appendChild(
    Object.assign(document.createElement("style"), {
      textContent: `
      @page { size: 1920px 1080px; margin: 0; }
      html, body { margin: 0 !important; padding: 0 !important; }
      deck-stage { display: none !important; }
    `,
    }),
  );
  const container = document.createElement("div");
  sections.forEach((s) => {
    s.style.cssText =
      "width:1920px!important;height:1080px!important;display:block!important;position:relative!important;overflow:hidden!important;page-break-after:always!important;break-after:page!important;background:#F7F4EF;margin:0!important;padding:0!important;";
    container.appendChild(s);
  });
  // Desabilitar quebra de página na última, para evitar página em branco no final
  sections[sections.length - 1].style.pageBreakAfter = "auto";
  sections[sections.length - 1].style.breakAfter = "auto";
  document.body.appendChild(container);
});

await page.pdf({
  width: "1920px",
  height: "1080px",
  printBackground: true,
  preferCSSPageSize: true,
});
```

**Por que isso funciona**:

- Extrai as seções do shadow DOM slot para uma div comum no light DOM — contornando completamente a regra `::slotted(section) { display: none }`
- `position: relative` inline faz com que elementos absolute filhos se posicionem relativos à seção, sem vazar
- `page-break-after: always` faz o navegador renderizar cada seção em uma página independente no print
- `:last-child` sem quebra de página evita página em branco no final

**Ao verificar com `mdls -name kMDItemNumberOfPages`**,注意: o metadata Spotlight do macOS tem cache. Após reescrever o PDF, execute `mdimport file.pdf` para forçar a atualização, caso contrário exibirá o número de páginas antigo. Use `pdfinfo` ou `pdftoppm` para contar o número real de arquivos.

---

### `export_deck_pptx.mjs` — Exportar PPTX Editável

```bash
# Modo único: caixas de texto nativamente editáveis (fontes cairão para fontes do sistema)
node scripts/export_deck_pptx.mjs --slides <dir> --out deck.pptx
```

Como funciona: `html2pptx` lê o computedStyle elemento por elemento e traduz o DOM em objetos PowerPoint (text frame / shape / picture). O texto se torna caixas de texto reais, com duplo clique para editar no PowerPoint.

**Restrições rígidas** (o HTML deve atender, caso contrário a página é pulada; detalhes em `references/editable-pptx.md`):

- Todo texto deve estar dentro de `<p>`/`<h1>`-`<h6>`/`<ul>`/`<ol>` (proibido texto solto em div)
- Tags `<p>`/`<h*>` não podem ter background/border/shadow próprios (colocar na div externa)
- Não usar `::before`/`::after` para inserir texto decorativo (pseudo-elementos não podem ser extraídos)
- Elementos inline (span/em/strong) não podem ter margin
- Não usar CSS gradient (não renderizável)
- Div não usar `background-image` (usar `<img>`)

O script já possui **pré-processador automático** integrado — que envolve automaticamente "texto solto em div folha" em `<p>` (preservando a class). Isso resolve a violação mais comum (texto solto). Mas outras violações (border em p, margin em span, etc.) ainda exigem conformidade na origem do HTML.

**Ressalva sobre fallback de fontes**:

- Playwright usa webfont para medir dimensões da text-box; PowerPoint/Keynote usa fontes nativas para renderizar
- Quando diferentes, pode haver **vazamento ou desalinhamento** — cada página precisa ser verificada visualmente
- Recomenda-se que a máquina de destino tenha as fontes usadas no HTML instaladas, ou use fallback para `system-ui`

**Cenários com prioridade visual não devem usar este caminho** → use `export_deck_pdf.mjs` para gerar PDF. O PDF tem fidelidade visual 100%, é vetorial, multiplataforma, com texto pesquisável — é o verdadeiro destino para decks com prioridade visual, não um "compromisso não editável".

### Torne o HTML Amigável à Exportação Desde o Início

O deck mais estável em termos de desempenho: **escreva o HTML desde o início seguindo as 4 restrições rígidas do editable**. Assim o `export_deck_pptx.mjs` pode passar direto. O custo adicional é pequeno:

```html
<!-- ❌ Ruim -->
<div class="title">Descoberta Principal</div>

<!-- ✅ Bom (envolvido em p, class herdada) -->
<p class="title">Descoberta Principal</p>

<!-- ❌ Ruim (border no p) -->
<p class="stat" style="border-left: 3px solid red;">41%</p>

<!-- ✅ Bom (border na div externa) -->
<div class="stat-wrap" style="border-left: 3px solid red;">
  <p class="stat">41%</p>
</div>
```

### Quando Escolher Qual

| Cenário                                         | Recomendação                                               |
| ----------------------------------------------- | ---------------------------------------------------------- |
| Para organizadores/arquivamento                 | **PDF** (universal, alta fidelidade, texto pesquisável)    |
| Enviar para colaboradores ajustarem texto       | **PPTX editable** (aceitar fallback de fontes)             |
| Apresentação ao vivo, sem alteração de conteúdo | **PDF** (fidelidade vetorial, multiplataforma)             |
| HTML é o meio de apresentação principal         | Reproduzir direto no navegador, exportação é apenas backup |

## Caminho Aprofundado para Exportar como PPTX Editável (Apenas Projetos de Longo Prazo)

Se seu deck terá manutenção de longo prazo, alterações frequentes e colaboração em equipe — recomenda-se **escrever o HTML desde o início seguindo as restrições do html2pptx**, assim o `export_deck_pptx.mjs` pode passar direto. Veja `references/editable-pptx.md` (4 restrições rígidas + template HTML + consulta rápida de erros comuns + fluxo de fallback para rascunhos visuais existentes).

---

## Perguntas Frequentes

**Múltiplos arquivos: a página no iframe não abre / tela branca**
→ Verifique se o caminho `file` no `MANIFEST` está correto relativo ao `index.html`. Use o DevTools do navegador para verificar se o src do iframe pode ser acessado diretamente.

**Múltiplos arquivos: o estilo de uma página conflita com outra**
→ Impossível (isolamento por iframe). Se sentir conflito, é cache — Cmd+Shift+R para refresh forçado.

**Arquivo único: múltiplos slides renderizando sobrepostos**
→ Problema de especificidade CSS. Veja a seção "Armadilhas de CSS na Arquitetura de Arquivo Único" acima.

**Arquivo único: o zoom parece incorreto**
→ Verifique se todos os slides estão diretamente sob `<deck-stage>` como `<section>`. Não pode haver `<div>` intermediária.

**Arquivo único: quer pular para um slide específico**
→ Adicione hash na URL: `index.html#slide-5` para pular para o 5º slide.

**Ambas arquiteturas: texto com posição inconsistente em diferentes telas**
→ Use tamanho fixo (1920×1080) e unidades `px`, não use `vw`/`vh` ou `%`. O zoom é tratado de forma unificada.

---

## Checklist de Verificação (Obrigatório ao Finalizar o Deck)

1. [ ] Abrir `index.html` (ou HTML principal) diretamente no navegador, verificar se a primeira página não tem imagem quebrada, fontes carregadas
2. [ ] Pressionar → para navegar por todas as páginas, sem página em branco, sem desalinhamento de layout
3. [ ] Pressionar P para visualizar impressão, cada página exatamente um A4 (ou 1920×1080) sem corte
4. [ ] Selecionar aleatoriamente 3 páginas, Cmd+Shift+R para refresh forçado, localStorage funcionando normalmente
5. [ ] Captura de tela em lote com Playwright (arquitetura multi-página: percorrer `slides/*.html`; arquitetura arquivo único: usar goTo para alternar), verificação visual manual
6. [ ] Pesquisar por `TODO` / `placeholder` residuais, confirmar que todos foram limpos
