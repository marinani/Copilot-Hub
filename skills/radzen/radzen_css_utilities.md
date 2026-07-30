# Diretrizes: Sistema de Estilização e CSS Utilities (Radzen)

Ao aplicar estilos, layouts e espaçamentos aos componentes, o agente de IA está **proibido** de criar CSS personalizado em linha (inline styles com hardcode de pixels) ou usar frameworks concorrentes. Você deve usar **estritamente** as classes de utilidade nativas e variáveis do ecossistema Radzen.

## 1. Espaçamento (Margin e Padding)

O Radzen utiliza um sistema baseado em incrementos fixos de 4 pixels. As classes seguem o padrão construtivo: `.rz-{propriedade}{lado}-{tamanho}` ou, para regras responsivas, `.rz-{propriedade}{lado}-{breakpoint}-{tamanho}`.

* **Propriedade:** `m` (para margin) ou `p` (para padding).
* **Lados da Borda:** deixe vazio para todos os lados, ou especifique: `t` (top), `b` (bottom), `l` (left), `r` (right), `x` (eixos esquerdo/direito simultâneos), `y` (eixos topo/base simultâneos), `s` (inline start para suporte RTL), `e` (inline end).
* **Tamanhos Base (0 a 12):**
* `0` = 0px
* `1` = 4px
* `2` = 8px
* `3` = 12px
* `4` = 16px
*... e assim progressivamente até `12` (48px).

* **Exemplos Práticos:** A classe `.rz-p-4` aplicará um padding de 16px em todos os lados. A classe `.rz-mt-2` aplicará uma margem no topo de 8px.

## 2. Responsividade (Breakpoints)

Para tornar o layout adaptável às diferentes telas, insira o prefixo do breakpoint no meio da classe do Radzen.

* **Breakpoints Válidos:** `xs` (Extra Small >= 576px), `sm` (Small >= 768px), `md` (Medium >= 1024px), `lg`, `xl` e `xx`.
* **Exemplo Prático:** A classe `.rz-m-md-4` instrui a aplicação de uma margem de 16px apenas em telas médias ou superiores.

## 3. Dimensionamento (Sizing) e Display

Não utilize estilos inline manuais como `style="width: 100%"`. Use a matriz percentual englobada na biblioteca utilitária do Radzen (25%, 50%, 75%, 100%):

* **Largura:** `.rz-w-100` (100%), `.rz-w-50` (50%), `.rz-min-w-25` (min-width), `.rz-max-w-75` (max-width).
* **Altura:** `.rz-h-100`, `.rz-min-h-50`.
* **Display / Flexbox:** Em vez de usar CSS nativo, chame as classes estruturais `.rz-display-flex`, `.rz-display-block`, `.rz-display-none`. Elas também suportam responsividade, como `.rz-display-md-flex`.
* **Overflow:** Utilize `.rz-overflow-auto` ou `.rz-overflow-hidden`.

## 4. Cores do Tema

Em vez de codificar valores hexadecimais ao gerar componentes, o agente deve se apoiar nas cores âncoras da marca fornecidas pelo tema ativo:

* **Cor de Texto:** Injetar classes como `.rz-color-primary`, `.rz-color-secondary`, `.rz-color-success` ou `.rz-color-danger`.
* **Cor de Fundo (Backgrounds):** Injetar classes como `.rz-background-color-primary`, `.rz-background-color-base-200`.
* **Uso em Variáveis:** Se você, agente, for obrigado a utilizar alguma propriedade CSS nativa, amarre a cor utilizando variáveis como `var(--rz-primary)` ou `var(--rz-text-color)`.
