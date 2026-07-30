# Exportação de PPTX Editável: Restrições Rígidas de HTML + Decisão de Tamanho + Erros Comuns

Este documento descreve o caminho de **usar `scripts/html2pptx.js` + `pptxgenjs` para traduzir HTML elemento por elemento em caixas de texto verdadeiramente editáveis do PowerPoint**, que é o único caminho suportado pelo `export_deck_pptx.mjs`.

> **Pré-requisito central**: para seguir este caminho, o HTML deve ser escrito desde a primeira linha seguindo as 4 restrições abaixo. **Não é "escrever e depois converter"** — a correção posterior acarreta 2-3 horas de retrabalho (testado na prática no projeto 期权私董会 em 2026-04-20).
>
> Cenários com prioridade de liberdade visual (animações / web components / gradientes CSS / SVG complexos) devem seguir o caminho PDF (`export_deck_pdf.mjs` / `export_deck_stage_pdf.mjs`), **não** espere que a exportação PPTX consiga aliar fidelidade visual e editabilidade — esta é uma limitação física do próprio formato de arquivo PPTX (veja "Por que as 4 restrições não são bugs, mas sim limitações físicas" no final).

---

## Tamanho da Tela: Use 960×540pt (LAYOUT_WIDE)

A unidade do PPTX é **inch** (polegada física), não px. Princípio de decisão: o tamanho do computedStyle do body deve **corresponder ao tamanho em inch do presentation layout** (±0,1", verificado por `validateDimensions` do `html2pptx.js`).

### Comparação dos 3 Tamanhos Candidatos

| HTML body           | Tamanho físico     | Layout PPT correspondente   | Quando escolher                                                             |
| ------------------- | ------------------ | --------------------------- | --------------------------------------------------------------------------- |
| **`960pt × 540pt`** | **13,333″ × 7,5″** | **pptxgenjs `LAYOUT_WIDE`** | ✅ **Recomendação padrão** (padrão 16:9 do PowerPoint moderno)              |
| `720pt × 405pt`     | 10″ × 5,625″       | Personalizado               | Apenas quando o usuário especificar template "PowerPoint Widescreen antigo" |
| `1920px × 1080px`   | 20″ × 11,25″       | Personalizado               | ❌ Tamanho não padrão, fontes parecem anormalmente pequenas após projeção   |

**Não pense no tamanho do HTML como resolução.** PPTX é um documento vetorial, o tamanho do body determina o **tamanho físico**, não a nitidez. Um body超大 (20″×11,25″) não deixa o texto mais nítido — apenas faz o tamanho da fonte em pt parecer menor relativo à tela, ficando pior na projeção/impressão.

### Três Formas Equivalentes de Escrever o body

```css
body {
  width: 960pt;
  height: 540pt;
} /* Mais claro, recomendado */
body {
  width: 1280px;
  height: 720px;
} /* Equivalente, hábito em px */
body {
  width: 13.333in;
  height: 7.5in;
} /* Equivalente, intuição em polegadas */
```

Código pptxgenjs correspondente:

```js
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 × 7.5 inch, sem necessidade de personalização
```

---

## 4 Restrições Rígidas (Violação Resulta em Erro Direto)

O `html2pptx.js` traduz o DOM do HTML elemento por elemento em objetos do PowerPoint. As restrições de formato do PowerPoint são projetadas no HTML = as 4 regras abaixo.

### Regra 1: Não pode escrever texto diretamente na DIV — deve usar `<p>` ou `<h1>`-`<h6>` para envolver

```html
<!-- ❌ Errado: texto diretamente na div -->
<div class="title">Receita Q3 cresceu 23%</div>

<!-- ✅ Correto: texto dentro de <p> ou <h1>-<h6> -->
<div class="title"><h1>Receita Q3 cresceu 23%</h1></div>
<div class="body"><p>Novos usuários são o principal motor</p></div>
```

**Por quê**: o texto do PowerPoint deve existir em um text frame, e o text frame corresponde a elementos de nível de parágrafo do HTML (p/h\*/li). Um `<div>` sem texto não tem um contêiner de texto correspondente no PPTX.

**Também não pode usar `<span>` para texto principal** — span é um elemento inline, não pode ser alinhado independentemente como uma caixa de texto. Span só pode ser **colocado dentro de p/h\*** para estilos locais (negrito, mudança de cor).

### Regra 2: Não suporta gradientes CSS — usar apenas cores sólidas

```css
/* ❌ Errado */
background: linear-gradient(to right, #ff6b6b, #4ecdc4);

/* ✅ Correto: cor sólida */
background: #ff6b6b;

/* ✅ Se precisar de listras multicoloridas, usar flex com filhos de cor sólida */
.stripe-bar {
  display: flex;
}
.stripe-bar div {
  flex: 1;
}
.red {
  background: #ff6b6b;
}
.teal {
  background: #4ecdc4;
}
```

**Por quê**: o shape fill do PowerPoint suporta apenas solid/gradient-fill, mas o `fill: { color: ... }` do pptxgenjs mapeia apenas solid. O gradiente nativo do PowerPoint exigiria outra estrutura, atualmente não suportada pela ferramenta.

### Regra 3: Background/borda/sombra apenas na DIV, não nas tags de texto

```html
<!-- ❌ Errado: <p> com cor de fundo -->
<p style="background: #FFD700; border-radius: 4px;">Conteúdo importante</p>

<!-- ✅ Correto: div externa com background/borda, <p> apenas texto -->
<div style="background: #FFD700; border-radius: 4px; padding: 8pt 12pt;">
  <p>Conteúdo importante</p>
</div>
```

**Por quê**: no PowerPoint, shape (quadrado/retângulo arredondado) e text frame são dois objetos. O `<p>` do HTML é traduzido apenas como text frame, background/borda/sombra pertencem ao shape — devem ser escritos na **div que envolve o texto**.

### Regra 4: DIV não pode usar `background-image` — usar tag `<img>`

```html
<!-- ❌ Errado -->
<div style="background-image: url('chart.png')"></div>

<!-- ✅ Correto -->
<img
  src="chart.png"
  style="position: absolute; left: 50%; top: 20%; width: 300pt; height: 200pt;"
/>
```

**Por quê**: o `html2pptx.js` extrai caminhos de imagem apenas do elemento `<img>`, não解析 URLs de `background-image` do CSS.

---

## Esqueleto do Template HTML (Caminho A)

Cada slide é um arquivo HTML independente, com escopos isolados entre si (evitando poluição CSS de deck de arquivo único).

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        width: 960pt;
        height: 540pt; /* ⚠️ Corresponder a LAYOUT_WIDE */
        font-family:
          system-ui,
          -apple-system,
          "PingFang SC",
          sans-serif;
        background: #fefef9; /* Cor sólida, sem gradiente */
        overflow: hidden;
      }
      /* DIV responsável por layout/background/borda */
      .card {
        position: absolute;
        background: #1a4a8a; /* Background na DIV */
        border-radius: 4pt;
        padding: 12pt 16pt;
      }
      /* Tags de texto apenas para estilo de fonte, sem background/borda */
      .card h2 {
        font-size: 24pt;
        color: #ffffff;
        font-weight: 700;
      }
      .card p {
        font-size: 14pt;
        color: rgba(255, 255, 255, 0.85);
      }
    </style>
  </head>
  <body>
    <!-- Área de título: div externa para posicionamento, tags de texto internas -->
    <div style="position: absolute; top: 40pt; left: 60pt; right: 60pt;">
      <h1 style="font-size: 36pt; color: #1A1A1A; font-weight: 700;">
        Título use frase afirmativa, não palavra-chave
      </h1>
      <p style="font-size: 16pt; color: #555555; margin-top: 10pt;">
        Subtítulo com explicação complementar
      </p>
    </div>

    <!-- Cartão de conteúdo: div responsável pelo background, h2/p responsáveis pelo texto -->
    <div
      class="card"
      style="top: 130pt; left: 60pt; width: 240pt; height: 160pt;"
    >
      <h2>Ponto Um</h2>
      <p>Texto explicativo breve</p>
    </div>

    <!-- Lista: usar ul/li, sem símbolo • manual -->
    <div style="position: absolute; top: 320pt; left: 60pt; width: 540pt;">
      <ul
        style="font-size: 16pt; color: #1A1A1A; padding-left: 24pt; list-style: disc;"
      >
        <li>Primeiro ponto</li>
        <li>Segundo ponto</li>
        <li>Terceiro ponto</li>
      </ul>
    </div>

    <!-- Ilustração: usar tag <img>, não background-image -->
    <img
      src="illustration.png"
      style="position: absolute; right: 60pt; top: 110pt; width: 320pt; height: 240pt;"
    />
  </body>
</html>
```

---

## Consulta Rápida de Erros Comuns

| Mensagem de erro                                      | Causa                                                               | Método de correção                                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `DIV element contains unwrapped text "XXX"`           | div com texto solto                                                 | Envolver o texto em `<p>` ou `<h1>`-`<h6>`                                               |
| `CSS gradients are not supported`                     | Usou linear/radial-gradient                                         | Mudar para cor sólida, ou usar flex com filhos segmentados                               |
| `Text element <p> has background`                     | Tag `<p>` com cor de fundo                                          | Colocar `<div>` externa para background, `<p>` apenas texto                              |
| `Background images on DIV elements are not supported` | div com background-image                                            | Mudar para tag `<img>`                                                                   |
| `HTML content overflows body by Xpt vertically`       | Conteúdo ultrapassa 540pt                                           | Reduzir conteúdo ou diminuir fonte, ou `overflow: hidden` para truncar                   |
| `HTML dimensions don't match presentation layout`     | Tamanho do body não corresponde ao pres layout                      | body usar `960pt × 540pt` com `LAYOUT_WIDE`; ou defineLayout com tamanho personalizado   |
| `Text box "XXX" ends too close to bottom edge`        | `<p>` com fonte grande muito próximo da borda inferior (< 0,5 inch) | Mover para cima, deixar margem inferior suficiente; parte inferior do PPT já é encoberta |

---

## Fluxo de Trabalho Básico (3 Passos para Gerar PPTX)

### Passo 1: Escrever cada página HTML independente seguindo as restrições

```
MeuDeck/
├── slides/
│   ├── 01-capa.html       # Cada arquivo é um HTML completo 960×540pt
│   ├── 02-agenda.html
│   └── ...
└── illustration/           # Todas as imagens referenciadas por <img>
    ├── chart1.png
    └── ...
```

### Passo 2: Escrever build.js chamando `html2pptx.js`

```js
const pptxgen = require("pptxgenjs");
const html2pptx = require("../scripts/html2pptx.js"); // Script desta skill

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 × 7.5 inch, correspondendo ao HTML 960×540pt

  const slides = ["01-capa.html", "02-agenda.html", "03-conteudo.html"];
  for (const file of slides) {
    await html2pptx(`./slides/${file}`, pres);
  }

  await pres.writeFile({ fileName: "deck.pptx" });
})();
```

### Passo 3: Abrir e Verificar

- Abrir o PPTX exportado no PowerPoint/Keynote
- Clicar duas vezes em qualquer texto — deve ser editável diretamente (se for imagem, a regra 1 foi violada)
- Verificar overflow: cada página deve estar dentro dos limites do body, sem cortes

---

## Este Caminho vs. Outras Opções (Quando Escolher o Quê)

| Necessidade                                                                                                  | Escolher                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Colegas vão alterar texto no PPTX / Enviar para não-técnicos continuarem editando                            | **Este caminho** (editável, requer HTML escrito desde o início com as 4 restrições)                                      |
| Apenas para apresentação / arquivamento, sem mais alterações                                                 | `export_deck_pdf.mjs` (múltiplos arquivos) ou `export_deck_stage_pdf.mjs` (arquivo único deck-stage), gerar PDF vetorial |
| Prioridade de liberdade visual (animações, web component, gradientes CSS, SVG complexo), aceita não editável | **PDF** (igual acima) — PDF é fiel e multiplataforma, mais adequado que "PPTX imagem"                                    |

**Nunca force html2pptx em HTML escrito com liberdade visual** — a taxa de aprovação de HTML visual-driven no html2pptx é < 30%, e a adaptação página por página restante é mais lenta que reescrever. Nestes cenários, deve-se gerar PDF, não forçar PPTX.

---

## Fallback: Quando já existe um rascunho visual, mas o usuário insiste em PPTX editável

Ocasionalmente surge este cenário: você/usuário já escreveu um HTML visualmente rico (com gradientes, web components, SVG complexos), que seria mais adequado para PDF, mas o usuário diz claramente "não, precisa ser PPTX editável".

**Não force `html2pptx` esperando que passe** — a taxa de aprovação de HTML visual-driven no html2pptx é < 30%, os outros 70% gerarão erros ou distorções. O fallback correto é:

### Passo 1 · Comunique as Limitações (Transparência)

Uma frase para dizer ao usuário três coisas:

> "Seu HTML atual usa [listar especificamente: gradientes / web component / SVG complexo / ...], a conversão direta para editable PPTX vai falhar. Tenho duas opções:
>
> - A. **Gerar PDF** (recomendado) — mantém 100% da qualidade visual, o destinatário pode ver e imprimir, mas não pode alterar texto
> - B. **Reescrever uma versão editable HTML com base no rascunho visual** (mantendo as decisões de design de cor/layout/texto, mas reorganizando a estrutura HTML conforme as 4 restrições rígidas, **sacrificando** gradientes, web components, SVG complexos, etc.) → depois exportar editable PPTX
>
> Qual você prefere?"

Não minimize a opção B — informe claramente **o que será perdido**. Deixe o usuário fazer a escolha.

### Passo 2 · Se o Usuário Escolher B: IA Reescreve Ativamente, sem Exigir que o Usuário Escreva

A doutrina aqui é: **o usuário dá a intenção de design, você é responsável por traduzir para uma implementação compatível**. Não é fazer o usuário aprender as 4 restrições rígidas e reescrever sozinho.

Princípios a seguir ao reescrever:

- **Manter**: sistema de cores (primária/secundária/neutra), hierarquia de informação (título/subtítulo/corpo/nota), texto principal, esqueleto do layout (superior/médio/inferior / divisão esquerda-direita / grid), ritmo da página
- **Degradar**: gradiente CSS → cor sólida ou flex segmentado, web component → HTML de nível de parágrafo, SVG complexo → `<img>` simplificado ou geometria de cor sólida, sombras → remover ou reduzir ao mínimo, fontes personalizadas → alinhar com fontes do sistema
- **Reescrever**: texto solto → envolver em `<p>` / `<h*>`, `background-image` → tag `<img>`, background/borda em `<p>` → div externa

### Passo 3 · Produzir Lista de Comparação (Entrega Transparente)

Após a reescrita, forneça ao usuário uma comparação before/after, para que ele saiba quais detalhes visuais foram simplificados:

```
Design original → Ajuste na versão editável
- Gradiente roxo na área do título → Fundo sólido na cor primária #5B3DE8
- Sombra nos cartões de dados → Removida (substituída por borda de 2pt para distinguir)
- Gráfico de linha SVG complexo → Simplificado para <img> PNG (gerado a partir de screenshot do HTML)
- Efeito de animação web component no Hero → Frame estático inicial (web component não pode ser traduzido)
```

### Passo 4 · Exportar & Entregar em Formato Duplo

- Versão HTML `editable` → Executar `scripts/export_deck_pptx.mjs` para gerar PPTX editável
- **Recomenda-se manter também** o rascunho visual original → Executar `scripts/export_deck_pdf.mjs` para gerar PDF de alta fidelidade
- Entregar em formato duplo ao usuário: PDF do rascunho visual + PPTX editável, cada um com sua função

### Quando Recusar Diretamente a Opção B

Em alguns cenários, o custo da reescrita é muito alto, e deve-se aconselhar o usuário a desistir do PPTX editável:

- O valor central do HTML são animações ou interatividade (após reescrita, restaria apenas o frame estático inicial, perda de informação > 50%)
- Número de páginas > 30, custo de reescrita excede 2 horas
- O design visual depende profundamente de SVG preciso / filter personalizado (após reescrita, quase não se relaciona com a imagem original)

Neste caso, diga ao usuário: "O custo de reescrita deste deck é muito alto, recomendo gerar PDF em vez de PPTX. Se o destinatário realmente precisar do formato pptx, aceite que o visual ficará bastante simplificado — prefere mudar para PDF?"

---

## Por que as 4 Restrições Não São Bugs, Mas Sim Limitações Físicas

Estas 4 restrições não são preguiça do autor do `html2pptx.js` — são **limitações do próprio formato de arquivo PowerPoint (OOXML)** projetadas no HTML:

- No PPTX, o texto deve estar em um text frame (`<a:txBody>`), correspondendo a elementos HTML de nível de parágrafo
- No PPTX, shape e text frame são dois objetos separados, não é possível desenhar background e escrever texto no mesmo elemento simultaneamente
- O shape fill do PPTX tem suporte limitado a gradientes (apenas certos gradientes predefinidos, não suporta gradientes CSS com ângulos arbitrários)
- O objeto picture do PPTX deve referenciar um arquivo de imagem real, não uma propriedade CSS

Entendendo isso, **não espere que a ferramenta fique mais inteligente** — é a escrita do HTML que deve se adaptar ao formato PPTX, não o contrário.
