# Content Guidelines: Anti-AI Slop, Diretrizes de Conteúdo, Normas de Escala

A armadilha mais fácil de cair no design com IA. Esta é uma lista do **que NÃO fazer**, mais importante que o "que fazer" — porque AI slop é o padrão; se você não evitar ativamente, ele acontece.

## Lista Negra Completa de AI Slop

### Armadilhas Visuais

**❌ Gradientes de fundo agressivos**

- Gradiente fullscreen roxo → rosa → azul (a marca registrada de páginas geradas por IA)
- Rainbow gradient em qualquer direção
- Mesh gradient preenchendo o fundo
- ✅ Se for usar gradiente: sutil, monocromático, com intenção pontual (ex: hover de botão)

**❌ Card com borda arredondada + borda esquerda colorida**

```css
/* Esta é a assinatura típica de card com "gosto de IA" */
.card {
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  padding: 16px;
}
```

Esse tipo de card é onipresente em Dashboards gerados por IA. Quer destacar? Use formas mais elegantes: contraste de cor de fundo, contraste de peso/tamanho de fonte, linha divisória simples, ou simplesmente não use card.

**❌ Emoji como decoração**
A menos que a marca use emoji (como Notion, Slack), não coloque emoji na UI. **Especialmente não**:

- 🚀 ⚡️ ✨ 🎯 💡 antes de títulos
- ✅ em listas de features
- → em botões CTA (seta sozinha OK, seta emoji não)

Sem ícones, use bibliotecas de verdade (Lucide/Heroicons/Phosphor), ou use placeholder.

**❌ Desenhar imagens com SVG**
Não tente desenhar com SVG: pessoas, cenas, dispositivos, objetos, arte abstrata. Imagens SVG feitas por IA têm cara de IA — parecem amadoras e baratas. **Um retângulo cinza com o texto "Espaço para ilustração 1200×800" é 100x melhor que uma ilustração SVG malfeita**.

Os únicos cenários onde SVG é aceitável:

- Ícones de verdade (nível 16×16 a 32×32)
- Formas geométricas como elementos decorativos
- Gráficos de data viz

**❌ Iconografia em excesso**
Nem todo título/feature/seção precisa de ícone. O uso exagerado de ícones faz a interface parecer um brinquedo. Menos é mais.

**❌ "Data slop"**
Estatísticas inventadas para decorar:

- "10.000+ clientes satisfeitos" (você nem sabe se é verdade)
- "99,9% de uptime" (sem dados reais, não escreva)
- "Metric cards" decorativos compostos de ícone + número + texto
- Dados falsos em tabelas mock enfeitados excessivamente

Se não tiver dados reais, deixe placeholder ou peça ao usuário.

**❌ "Quote slop"**
Depoimentos de usuários inventados, citações de famosos para decorar a página. Deixe placeholder e peça citações reais ao usuário.

### Armadilhas de Tipografia

**❌ Evite estas fontes batidas**:

- Inter (padrão de páginas geradas por IA)
- Roboto
- Arial / Helvetica
- System font stack puro
- Fraunces (IA descobriu e já saturou)
- Space Grotesk (a favorita recente da IA)

**✅ Use pares display+body com personalidade**. Inspirações:

- Serifada display + sem serifa body (estilo editorial)
- Mono display + sans body (estilo técnico)
- Display pesada + body leve (contraste)
- Fonte variável para animação de peso no hero

Recursos de fontes:

- Opções interessantes e menos conhecidas do Google Fonts (Instrument Serif, Cormorant, Bricolage Grotesque, JetBrains Mono)
- Sites de fontes open source (fontes irmãs da Fraunces, Adobe Fonts)
- Não invente nomes de fontes

### Armadilhas de Cor

**❌ Inventar cores do nada**
Não projete um conjunto completo de cores que você não conhece. Geralmente fica dissonante.

**✅ Estratégia**:

1. Tem cor da marca → use a cor da marca, para tokens faltantes use interpolação oklch
2. Não tem cor da marca mas tem referência → extraia cores do screenshot do produto de referência
3. Partindo do zero total → escolha um sistema de cores conhecido (Radix Colors / paleta padrão Tailwind / marca Anthropic), não crie do zero

**Usar oklch para definir cores** é a abordagem mais moderna:

```css
:root {
  --primary: oklch(0.65 0.18 25); /* terracota quente */
  --primary-light: oklch(0.85 0.08 25); /* tom claro do mesmo matiz */
  --primary-dark: oklch(0.45 0.2 25); /* tom escuro do mesmo matiz */
}
```

oklch garante que ao ajustar o brilho, o matiz não se desvia — melhor que hsl.

**❌ Inverter cores aleatoriamente para modo noturno**
Não é simplesmente inverter as cores. Um bom dark mode requer reajuste de saturação, contraste e cor de destaque. Se não quiser fazer dark mode, não faça.

### Armadilhas de Layout

**❌ Bento grid excessivamente usado**
Toda landing page gerada por IA quer fazer bento. A menos que sua estrutura de informação realmente se beneficie do bento, use outro layout.

**❌ Grande hero + 3 colunas de features + depoimentos + CTA**
Este template de landing page está saturado. Se quiser inovar, inove de verdade.

**❌ Todos os cards do grid iguais**
Cards assimétricos, de tamanhos diferentes, alguns com imagem outros só texto, alguns ocupando mais colunas — isso sim parece trabalho de designer de verdade.

## Diretrizes de Conteúdo

### 1. Não adicione conteúdo de enchimento (filler)

Cada elemento precisa **merecer seu lugar**. Espaço vazio é um problema de design, resolva com **composição** (contraste, ritmo, espaçamento), **não** preenchendo com conteúdo.

**Perguntas para identificar filler**:

- Se eu remover este conteúdo, o design fica pior? Se a resposta for "não", remova.
- Este elemento resolve qual problema real? Se for "deixar a página menos vazia", remova.
- Esta estatística/citação/feature tem dados reais? Se não, não invente.

"Mil 'nãos' para cada 'sim'."

### 2. Pergunte antes de adicionar material

Acha que adicionar mais um parágrafo/página/seção vai melhorar? Pergunte ao usuário primeiro, não adicione por conta própria.

Motivos:

- O usuário conhece o público dele melhor que você
- Adicionar conteúdo tem custo, o usuário pode não querer
- Adicionar conteúdo por conta própria viola a relação de "junior designer reportando ao manager"

### 3. Crie um sistema com antecedência

Depois de explorar o design context, **verbalize primeiro o sistema que vai usar** e peça confirmação do usuário:

```markdown
Meu sistema de design:

- Cores: #1A1A1A texto principal + #F0EEE6 fundo + #D97757 destaque (da sua marca)
- Tipografia: Instrument Serif para display + Geist Sans para body
- Ritmo: título de seção com fundo colorido full-bleed + texto branco; seção normal com fundo branco
- Imagens: hero com foto full-bleed, seção de features com placeholder até você fornecer
- Máximo de 2 cores de fundo para evitar poluição visual

Confirme esta direção e eu começo.
```

Aguarde a confirmação do usuário antes de começar. Este check-in evita "descobrir no meio que a direção está errada".

## Normas de Escala

### Slides (1920×1080)

- Texto do corpo mínimo **24px**, ideal 28-36px
- Título 60-120px
- Título de seção 80-160px
- Hero headline pode usar 180-240px
- Nunca use <24px em slides

### Documentos para Impressão

- Texto do corpo mínimo **10pt** (≈13,3px), ideal 11-12pt
- Título 18-36pt
- Legenda 8-9pt

### Web e Mobile

- Texto do corpo mínimo **14px** (para idosos usar 16px)
- Texto do corpo em mobile **16px** (evita zoom automático do iOS)
- Alvo de toque (elementos clicáveis) mínimo **44×44px**
- Altura de linha 1,5-1,7 (chinês 1,7-1,8)

### Contraste

- Texto do corpo vs fundo **pelo menos 4,5:1** (WCAG AA)
- Texto grande vs fundo **pelo menos 3:1**
- Use a ferramenta de acessibilidade do Chrome DevTools para verificar

## CSS Poderoso

**Recursos CSS avançados** são grandes aliados do designer. Use sem medo:

### Tipografia

```css
/* Quebra de linha natural em títulos, evita palavra isolada na última linha */
h1,
h2,
h3 {
  text-wrap: balance;
}

/* Quebra de linha elegante em parágrafos, evita viúvas e órfãs */
p {
  text-wrap: pretty;
}

/* Poderoso para tipografia chinesa: controle de pontuação */
p {
  text-spacing-trim: space-all;
  hanging-punctuation: first;
}
```

### Layout

```css
/* CSS Grid + áreas nomeadas = legibilidade máxima */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
}

/* Subgrid para alinhar conteúdo de cards */
.card {
  display: grid;
  grid-template-rows: subgrid;
}
```

### Efeitos Visuais

```css
/* Scrollbar com estilo */
* {
  scrollbar-width: thin;
  scrollbar-color: #666 transparent;
}

/* Efeito vidro (usar com moderação) */
.glass {
  backdrop-filter: blur(20px) saturate(150%);
  background: color-mix(in oklch, white 70%, transparent);
}

/* View transitions API para transições suaves entre páginas */
@view-transition {
  navigation: auto;
}
```

### Interação

```css
/* Seletor :has() facilita estilos condicionais */
.card:has(img) { padding-top: 0; } /* card com imagem não tem padding no topo */

/* Container queries para componentes realmente responsivos */
@container (min-width: 500px) { ... }

/* Nova função color-mix */
.button:hover {
  background: color-mix(in oklch, var(--primary) 85%, black);
}
```

## Consulta Rápida de Decisão: Quando Estiver em Dúvida

- Quer adicionar um gradiente? → Provavelmente não adicione
- Quer adicionar um emoji? → Não adicione
- Quer dar borda arredondada + borda esquerda colorida no card? → Não faça, use outra forma
- Quer desenhar uma ilustração hero com SVG? → Não desenhe, use placeholder
- Quer adicionar uma citação decorativa? → Primeiro pergunte se o usuário tem citação real
- Quer adicionar uma fileira de features com ícones? → Primeiro pergunte se precisa de ícones, talvez não
- Usar Inter? → Troque por algo com mais personalidade
- Usar gradiente roxo? → Troque por uma paleta com fundamento

**Quando você pensa "vou adicionar isso porque fica mais bonito" — isso geralmente é sinal de AI slop**. Comece com a versão mais simples, e só adicione quando o usuário pedir.
