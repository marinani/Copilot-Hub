# Design Context: Partindo do Contexto Existente

**Esta é a coisa mais importante deste skill.**

Um bom design hi-fi sempre surge a partir de um design context existente. **Fazer hi-fi do zero é o último recurso e certamente produzirá um trabalho genérico**. Portanto, no início de cada tarefa de design, pergunte: há algo que possa servir de referência?

## O que é Design Context

Por ordem de prioridade (da maior para a menor):

### 1. Design System / UI Kit do Usuário

A biblioteca de componentes, tokens de cor, especificações tipográficas e sistema de ícones já existentes no produto do usuário. **A situação ideal**.

### 2. Codebase do Usuário

Se o usuário forneceu o código-fonte, ele contém implementações reais de componentes. Leia esses arquivos:

- `theme.ts` / `colors.ts` / `tokens.css` / `_variables.scss`
- Componentes específicos (Button.tsx, Card.tsx)
- Scaffold de layout (App.tsx, MainLayout.tsx)
- Stylesheets globais

**Leia o código e copie os valores exatos**: hex codes, escala de espaçamento, font stack, border radius. Não redesenhe de memória.

### 3. Produto Publicado do Usuário

Se o usuário tem um produto online mas não forneceu o código, use Playwright ou peça screenshots.

```bash
# Capturar screenshot de uma URL pública com Playwright
npx playwright screenshot https://example.com screenshot.png --viewport-size=1920,1080
```

Isso permite que você veja o vocabulário visual real.

### 4. Guia de Marca / Logo / Materiais Existentes

O usuário pode ter: arquivos de logo, especificações de cores da marca, materiais de marketing, templates de apresentação. Tudo isso é contexto.

### 5. Referências de Concorrentes

Se o usuário disser "como o site XX" — peça a URL ou screenshot. **Não** confie na sua vaga lembrança dos dados de treinamento.

### 6. Design Systems Conhecidos (fallback)

Se nada disso existir, use design systems consagrados como base:

- Apple HIG
- Material Design 3
- Radix Colors (paletas de cor)
- shadcn/ui (componentes)
- Paleta padrão do Tailwind

Avise claramente ao usuário o que você está usando, deixando claro que é um ponto de partida, não a versão final.

## Fluxo para Obter Contexto

### Passo 1: Pergunte ao Usuário

Lista de perguntas obrigatórias no início da tarefa (do [`workflow.md`](workflow.md)):

```markdown
1. Você tem design system/UI kit/biblioteca de componentes prontos? Onde?
2. Tem guia de marca, especificação de cores/tipografia?
3. Pode me fornecer screenshots ou URL do produto existente?
4. Tem codebase que eu possa ler?
```

### Passo 2: Quando o Usuário Disser "Não", Ajude-o a Encontrar

Não desista de imediato. Tente:

```markdown
Deixe-me ver se há pistas:

- Seus projetos anteriores têm designs relacionados?
- O site de marketing da empresa usa quais cores/tipografia?
- Qual o estilo do Logo do seu produto? Pode me enviar uma imagem?
- Existe algum produto que você admira e que possa servir de referência?
```

### Passo 3: Leia Todo o Contexto Encontrável

Se o usuário forneceu o caminho do codebase, leia:

1. **Liste a estrutura de arquivos primeiro**: procure arquivos relacionados a style/theme/component
2. **Leia os arquivos de theme/token**: extraia os valores hex/px específicos
3. **Leia 2-3 componentes representativos**: veja o vocabulário visual (hover state, shadow, border, padding, padrão de nós)
4. **Leia o stylesheet global**: reset básico, carregamento de fontes
5. **Se houver link Figma/screenshot**: olhe a imagem, mas **confie mais no código**

**Importante**: **Não** olhe superficialmente e trabalhe de memória. Você só realmente extraiu o contexto quando tiver 30+ valores específicos.

### Passo 4: Verbalize o Sistema que Vai Usar

Depois de analisar o contexto, diga ao usuário qual sistema você vai usar:

```markdown
Com base no seu codebase e screenshots do produto, o design system que extraí:

**Cores**

- Primary: #C27558 (do tokens.css)
- Background: #FDF9F0
- Text: #1A1A1A
- Muted: #6B6B6B

**Tipografia**

- Display: Instrument Serif (do @font-face no global.css)
- Body: Geist Sans
- Mono: JetBrains Mono

**Espaçamento** (da sua escala)

- 4, 8, 12, 16, 24, 32, 48, 64

**Padrão de Sombras**

- `0 1px 2px rgba(0,0,0,0.04)` (card sutil)
- `0 10px 40px rgba(0,0,0,0.1)` (modal elevado)

**Border-radius**

- Componentes pequenos 4px, cards 12px, botões 8px

**Vocabulário de Componentes**

- Button: filled primary, outlined secondary, ghost tertiary, todos com border-radius 8px
- Card: fundo branco, sombra sutil, sem borda

Vou começar com base neste sistema. Confirma que está ok?
```

Aguarde a confirmação do usuário antes de começar.

## Fazendo Design do Zero (Fallback sem Contexto)

**Aviso importante**: A qualidade do resultado nesta situação será significativamente inferior. Deixe isso claro para o usuário.

```markdown
Você não tem design context, então só posso trabalhar com base no bom senso geral.
O resultado será "visualmente ok, mas sem originalidade".
Você prefere continuar assim, ou primeiro buscar alguns materiais de referência?
```

Se o usuário insistir, siga esta ordem de decisões:

### 1. Escolha uma Direção Estética

Não entregue um resultado genérico. Escolha uma direção clara:

- brutalmente minimalista
- editorial/revista
- brutalista/cru
- orgânico/natural
- luxuoso/refinado
- lúdico/infantil
- retrô-futurista
- suave/pastel

Informe ao usuário qual você escolheu.

### 2. Escolha um Design System Conhecido como Estrutura

- Use Radix Colors para paletas (https://www.radix-ui.com/colors)
- Use shadcn/ui para vocabulário de componentes (https://ui.shadcn.com)
- Use a escala de espaçamento do Tailwind (múltiplos de 4)

### 3. Escolha Pares de Fontes com Personalidade

Não use Inter/Roboto. Combinações sugeridas (gratuitas do Google Fonts):

- Instrument Serif + Geist Sans
- Cormorant Garamond + Inter Tight
- Bricolage Grotesque + Söhne (pago)
- Fraunces + Work Sans (atenção: Fraunces já está saturada pelo uso em IA)
- JetBrains Mono + Geist Sans (estilo técnico)

### 4. Cada Decisão Crítica com Justificativa

Não escolha em silêncio. Escreva nos comentários do HTML:

```html
<!--
Design decisions:
- Primary color: warm terracotta (oklch 0.65 0.18 25) — adequado à direção "editorial"
- Display: Instrument Serif para sensação humanista e literária
- Body: Geist Sans para contraste de limpeza
- Sem gradientes — compromisso com o minimalismo, sem AI slop
- Espaçamento: base 8px, proporção áurea (8/13/21/34)
-->
```

## Estratégia de Import (quando o usuário fornece codebase)

Se o usuário disser "importe este codebase como referência":

### Pequeno (<50 arquivos)

Leia todos, internalize o contexto.

### Médio (50-500 arquivos)

Foco em:

- `src/components/` ou `components/`
- Todos os arquivos relacionados a styles/tokens/theme
- 2-3 componentes de página completa representativos (Home.tsx, Dashboard.tsx)

### Grande (>500 arquivos)

Peça ao usuário para indicar o foco:

- "Vou fazer a página de configurações" → leia os arquivos de configurações existentes
- "Vou criar uma nova feature" → leia o shell geral + a referência mais próxima
- Não busque abrangência, busque precisão

## Trabalhando com Figma / Arquivos de Design

Se o usuário forneceu um link do Figma:

- **Não** espere conseguir "converter Figma para HTML" diretamente — isso requer ferramentas adicionais
- Links do Figma geralmente não são acessíveis publicamente
- Peça ao usuário: exporte como **screenshot** e envie para você + informe os valores específicos de cor/espaçamento

Se recebeu apenas screenshot do Figma, avise ao usuário:

- Consigo ver o visual, mas não consigo extrair valores precisos
- Os números críticos (hex, px) por favor me informe, ou exporte como código (o Figma suporta)

## Lembrete Final

**A qualidade máxima de um projeto de design é determinada pela qualidade do contexto que você obtém.**

Gastar 10 minutos coletando contexto vale mais do que gastar 1 hora desenhando hi-fi do zero.

**Quando não houver contexto, priorize pedir ao usuário, em vez de forçar a barra.**
