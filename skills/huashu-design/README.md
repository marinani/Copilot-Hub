<sub>🌐 <a href="README.en.md">English</a> · <b>Português (BR)</b></sub>

<div align="center">

# Huashu Design

> _「Digitar. Enter. Um design pronto para entrega.」_
> _"Type. Hit enter. A finished design lands in your lap."_

[![License](https://img.shields.io/badge/License-Personal%20Use%20Only-orange.svg)](LICENSE)
[![Agent-Agnostic](https://img.shields.io/badge/Agent-Agnostic-blueviolet)](https://skills.sh)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**Digite uma frase no seu agent e receba um design pronto para entrega.**

<br>

Em 3 a 30 minutos, você pode shipar uma **animação de lançamento de produto**, um protótipo de App clicável, uma apresentação PPT editável, um infográfico com qualidade de impressão.

Não é daquele nível "até que o AI fez bonito" — parece que foi feito por uma equipe de design de grande empresa. Dê ao skill seus ativos de marca (logo, paleta de cores, screenshots de UI), e ele entenderá a identidade da sua marca; não dê nada, e os 20 vocabulários de design embutidos já garantem que não saia AI slop.

**Cada animação que você vê neste README foi feita pelo próprio huashu-design.** Não é Figma, não é After Effects — é uma frase de prompt + o skill rodando. Precisa de um vídeo de lançamento para o próximo produto? Agora você também consegue.

```
npx skills add alchaincyf/huashu-design
```

Funciona em qualquer agent — Claude Code, Cursor, Codex, OpenClaw, Hermes.

[Ver efeitos](#demo-galeria) · [Instalação](#instalação) · [O que faz](#o-que-faz) · [Mecanismos principais](#mecanismos-principais) · [Relação com Claude Design](#relação-com-claude-design)

</div>

---

<p align="center">
  <img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/hero-animation-v10-en.gif" alt="huashu-design Hero · Digitar → Escolher direção → Galeria se expande → Foco → Marca aparece" width="100%">
</p>

<p align="center"><sub>
  ▲ 25 seg · Terminal → 4 direções → Gallery ripple → 4 Focos → Brand reveal<br>
  👉 <a href="https://www.huasheng.ai/huashu-design-hero/">Acesse a versão HTML interativa com efeitos sonoros</a> ·
  <a href="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/hero-animation-v10-en.mp4">Baixar MP4 (com BGM+SFX · 10MB)</a>
</sub></p>

---

## Instalação

```bash
npx skills add alchaincyf/huashu-design
```

Depois, é só falar diretamente no Claude Code:

```
「Faça uma apresentação de slides sobre psicologia da IA, recomende 3 direções de estilo para eu escolher」
「Crie um protótipo iOS de Pomodoro com IA, 4 telas principais realmente clicáveis」
「Transforme essa lógica em uma animação de 60 segundos, exporte MP4 e GIF」
「Faça uma revisão em 5 dimensões deste design」
```

Sem botões, sem painéis, sem plugins do Figma.

---

## Star History

<p align="center">
  <a href="https://star-history.com/#alchaincyf/huashu-design&Date">
    <img src="https://api.star-history.com/svg?repos=alchaincyf/huashu-design&type=Date" alt="huashu-design Star History" width="80%">
  </a>
</p>

---

## O que faz

| Capacidade                           | Entregável                                                                          | Tempo típico |
| ------------------------------------ | ----------------------------------------------------------------------------------- | ------------ |
| Protótipo interativo (App / Web)     | HTML em arquivo único · Bezel real de iPhone · Clicável · Verificado com Playwright | 10–15 min    |
| Slides de apresentação               | Deck HTML (apresentação no navegador) + PPTX editável (caixas de texto preservadas) | 15–25 min    |
| Animação em linha do tempo           | MP4 (25fps / 60fps com interpolação) + GIF (paleta otimizada) + BGM                 | 8–12 min     |
| Variações de design                  | 3+ comparações lado a lado · Tweaks em tempo real · Exploração multidimensional     | 10 min       |
| Infográfico / Visualização           | Layout com qualidade de impressão · Exportável para PDF/PNG/SVG                     | 10 min       |
| Consultoria de direção de design     | 5 escolas × 20 filosofias de design · Recomenda 3 direções · Gera Demos em paralelo | 5 min        |
| Revisão especializada em 5 dimensões | Gráfico radar + Keep/Fix/Quick Wins · Lista de correções acionáveis                 | 3 min        |

---

## Demo Galeria

### Consultoria de Direção de Design

Fallback para quando a demanda é vaga: de 5 escolas × 20 filosofias de design, escolhe 3 direções diferenciadas e gera 3 Demos em paralelo para você escolher.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/w3-fallback-advisor.gif" width="100%"></p>

### Protótipo iOS App

Corpo exato do iPhone 15 Pro (Dynamic Island / barra de status / Home Indicator) · Navegação entre múltiplas telas orientada a estado · Imagens reais do Wikimedia/Met/Unsplash · Teste de clique automático com Playwright.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/c1-ios-prototype.gif" width="100%"></p>

### Motion Design Engine

Modelo de segmentos de tempo Stage + Sprite · Quatro APIs — `useTime` / `useSprite` / `interpolate` / `Easing` — cobrindo todas as necessidades de animação · Um comando exporta MP4 / GIF / 60fps com interpolação / vídeo finalizado com BGM.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/c3-motion-design.gif" width="100%"></p>

### HTML Slides → PPTX Editável

Deck HTML para apresentação no navegador · `html2pptx.js` lê o computedStyle do DOM e traduz elemento por elemento em objetos PowerPoint · O resultado são **caixas de texto reais**, clicáveis duas vezes para editar no PowerPoint.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/c2-slides-pptx.gif" width="100%"></p>

### Tweaks · Alternância de Variações em Tempo Real

Esquema de cores / tipografia / densidade de informação parametrizados · Painel lateral para alternar · Front-end puro + `localStorage` para persistência · Não perde as configurações ao atualizar.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/c4-tweaks.gif" width="100%"></p>

### Infográfico / Visualização de Dados

Layout com qualidade de revista · Colunas precisas com CSS Grid · Detalhes tipográficos com `text-wrap: pretty` · Orientado a dados reais · Exportável para PDF vetorial / PNG 300dpi / SVG.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/c5-infographic.gif" width="100%"></p>

### Revisão Especializada em 5 Dimensões

Consistência filosófica · Hierarquia visual · Execução de detalhes · Funcionalidade · Inovação — cada uma de 0 a 10 · Visualização em gráfico radar · Gera lista de Keep / Fix / Quick Wins.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/c6-expert-review.gif" width="100%"></p>

### Fluxo de Trabalho Junior Designer

Não sai fazendo tudo de uma vez: primeiro escreve assumptions + placeholders + reasoning, mostra pra você o mais cedo possível, depois itera. Entender errado e corrigir cedo é 100x mais barato do que corrigir tarde.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/w2-junior-designer.gif" width="100%"></p>

### Protocolo de Ativos de Marca — 5 Etapas Obrigatórias

Quando envolve uma marca específica, é executado obrigatoriamente: Perguntar → Buscar → Baixar (3 rotas de fallback) → grep nos valores de cor → Escrever `brand-spec.md`.

<p align="center"><img src="https://github.com/alchaincyf/huashu-design/releases/download/v2.0/w1-brand-protocol.gif" width="100%"></p>

---

## Showcase · Casos Reais

### 「Falando sobre skill」 · Deck de apresentação PM after-party

> **Live demo · [https://skill-huasheng.vercel.app](https://skill-huasheng.vercel.app)**

13 páginas em HTML deck, **todas feitas com huashu-design**:

- Sistema visual serifado minimalista em fundo preto (cover / about / hook / what / why / closing)
- 2 demos cinematográficos de 22 segundos com BGM + SFX (Nuwa skill workflow + Darwin skill workflow), cada um com **linguagem visual completamente independente**:
  - **Nuwa**: Órbita de conhecimento 3D + Síntese Pentagon + typewriter do SKILL.md + hero reveal de 「21 minutos」
  - **Darwin**: Autoresearch loop spin + diff lado a lado v1/v5 + curva Hill-Climb em tela cheia + Ratchet gear lock
- Cada cinematic exibe por padrão um **dashboard de workflow estático completo** (o público vê como o skill funciona a qualquer momento), só dispara a animação ao clicar ▶, e ao finalizar faz fade de volta ao dashboard
- Incorpora a animação hero de 25 segundos do huasheng.ai (fallback localizado do iframe)
- Dados reais: 14.495 stargazers — curva real (via gh API) + specs reais do DeepSeek V4 (verificadas com WebSearch)
- Assets de IA reais: usou `huashu-gpt-image` para gerar grid 4×2, `extract_grid.py` para recortar 8 PNGs transparentes individuais, criando flutuação em órbita 3D

**Páginas recomendadas para referência**:

- `/slides/slide-04b-nuwa-flow.html` · Arquitetura de duas camadas: dashboard estático + overlay cinematográfico
- `/slides/slide-06b-darwin-flow.html` · Caso de contraste com linguagem visual completamente independente
- `/slides/slide-03b-deepseek-cover.html` · Página de comparação entre AI slop e a perspectiva de um designer real

Padrões cinematográficos detalhados em `references/cinematic-patterns.md`.

---

## Mecanismos Principais

### Protocolo de Ativos de Marca

A regra mais rigorosa do skill. Quando envolve uma marca específica (Stripe, Linear, Anthropic, sua própria empresa, etc.), executa obrigatoriamente 5 etapas:

| Etapa                                | Ação                                                                                       | Objetivo                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| 1 · Perguntar                        | O usuário tem brand guidelines?                                                            | Respeitar recursos existentes                                              |
| 2 · Buscar página oficial da marca   | `<brand>.com/brand` · `brand.<brand>.com` · `<brand>.com/press`                            | Capturar valores de cor oficiais                                           |
| 3 · Baixar assets                    | Arquivo SVG → HTML completo do site → Extrair cor de screenshot do produto                 | 3 rotas de fallback; se a anterior falhar, executa a próxima imediatamente |
| 4 · grep para extrair valores de cor | Capturar todos os `#xxxxxx` dos assets, ordenar por frequência, filtrar preto/branco/cinza | **Nunca adivinhar cor de marca pela memória**                              |
| 5 · Consolidar spec                  | Escrever `brand-spec.md` + variáveis CSS, todo HTML referencia `var(--brand-*)`            | Se não consolidar, esquece                                                 |

Teste A/B (v1 vs v2, cada um rodando em 6 agents): **a variância de estabilidade da v2 é 5x menor que a da v1**. Estabilidade da estabilidade — este é o verdadeiro fosso do skill.

### Consultoria de Direção de Design (Fallback)

Acionada quando a demanda do usuário é vaga demais para começar:

- Não insiste em fazer com intuição genérica — entra no modo Fallback
- De 5 escolas × 20 filosofias de design, recomenda 3 direções diferenciadas **que devem vir de escolas diferentes**
- Cada direção vem com obra representativa, palavras-chave de identidade, designer representativo
- Gera 3 Demos visuais em paralelo para o usuário escolher
- Após a escolha, entra no fluxo principal Junior Designer

### Fluxo de Trabalho Junior Designer

Modo de trabalho padrão, presente em todas as tarefas:

- Antes de começar, envia a lista de perguntas de uma vez para o usuário, espera todas serem respondidas antes de agir
- No HTML, primeiro escreve assumptions + placeholders + reasoning comments
- Mostra para o usuário o mais cedo possível (mesmo que sejam apenas blocos cinzas)
- Preenchimento do conteúdo real → variations → Tweaks — cada uma dessas três etapas mostra novamente
- Antes de entregar, faz uma revisão visual no navegador com Playwright

### Regras Anti-AI Slop

Evita o máximo divisor comum visual que entrega AI na cara (gradiente roxo / ícones emoji / cantos arredondados com borda esquerda accent / desenhar rostos com SVG / usar Inter como display). Usa `text-wrap: pretty` + CSS Grid + serif display cuidadosamente selecionados e cores oklch.

---

## Relação com Claude Design

Eu admito abertamente: a filosofia do Protocolo de Ativos de Marca foi roubada dos prompts que vazaram do Claude Design. Aquele prompt enfatiza repetidamente que **bom design de alta fidelidade não começa do zero, mas cresce a partir do contexto de design existente**. Esse princípio é a linha divisória entre um trabalho nota 65 e um nota 90.

Diferenças de posicionamento:

|                     | Claude Design                          | huashu-design                                         |
| ------------------- | -------------------------------------- | ----------------------------------------------------- |
| Forma               | Produto web (usa-se no navegador)      | Skill (usa-se no Claude Code)                         |
| Cota                | Cota de assinatura                     | Consumo de API · agent em paralelo sem limite de cota |
| Entregável          | Dentro da tela + exportável para Figma | HTML / MP4 / GIF / PPTX editável / PDF                |
| Modo de operação    | GUI (clicar, arrastar, modificar)      | Conversa (falar, esperar o agent terminar)            |
| Animações complexas | Limitadas                              | Stage + Sprite timeline · Exportação 60fps            |
| Multi-agent         | Exclusivo Claude.ai                    | Qualquer agent compatível com skill                   |

Claude Design é uma **ferramenta gráfica melhor**, huashu-design é **fazer a camada de ferramenta gráfica desaparecer**. Dois caminhos, públicos diferentes.

---

## Limitações

- **Não suporta PPTX editável em camadas para Figma**. Produz HTML, que pode ser capturado em screenshot, gravação de tela ou exportado como imagem, mas não pode ser arrastado para o Keynote para alterar posição de texto.
- **Animações complexas no nível do Framer Motion não são possíveis**. 3D, simulação física, sistemas de partículas estão além do escopo do skill.
- **Design do zero para uma marca completamente em branco cai para 60–65 pontos**. Criar alta fidelidade do nada é sempre último recurso.

Este é um skill nota 80, não um produto nota 100. Para quem não quer abrir uma interface gráfica, um skill nota 80 é mais útil que um produto nota 100.

---

## Estrutura do Repositório

```
huashu-design/
├── SKILL.md                 # Documento principal (para o agent ler)
├── README.md                # Este arquivo (para o usuário ler)
├── assets/                  # Starter Components
│   ├── animations.jsx       # Stage + Sprite + Easing + interpolate
│   ├── ios_frame.jsx        # Bezel do iPhone 15 Pro
│   ├── android_frame.jsx
│   ├── macos_window.jsx
│   ├── browser_window.jsx
│   ├── deck_stage.js        # Engine de slides HTML
│   ├── deck_index.html      # Concatenador de decks com múltiplos arquivos
│   ├── design_canvas.jsx    # Exibição de variações lado a lado
│   ├── showcases/           # 24 exemplos pré-fabricados (8 cenários × 3 estilos)
│   └── bgm-*.mp3            # 6 músicas de fundo por cenário
├── references/              # Subdocumentos para leitura aprofundada por tarefa
│   ├── animation-pitfalls.md
│   ├── design-styles.md     # Biblioteca detalhada de 20 filosofias de design
│   ├── slide-decks.md
│   ├── editable-pptx.md
│   ├── critique-guide.md
│   ├── video-export.md
│   └── ...
├── scripts/                 # Cadeia de ferramentas de exportação
│   ├── render-video.js      # HTML → MP4
│   ├── convert-formats.sh   # MP4 → 60fps + GIF
│   ├── add-music.sh         # MP4 + BGM
│   ├── export_deck_pdf.mjs
│   ├── export_deck_pptx.mjs
│   ├── html2pptx.js
│   └── verify.py
└── demos/                   # 9 demonstrações de capacidades (c*/w*), versões CN/EN em GIF/MP4/HTML + hero v10
```

---

## Origem

No dia em que a Anthropic lançou o Claude Design, eu fiquei jogando até as 4 da manhã. Dias depois, percebi que nunca mais o tinha aberto — não porque ele não seja bom — ele é o produto mais maduro deste segmento atualmente — é que eu prefiro deixar o agent trabalhar para mim no terminal do que abrir qualquer interface gráfica.

Então pedi ao agent para decompor o próprio Claude Design (incluindo os prompts de sistema que circulam na comunidade, o protocolo de ativos de marca, o mecanismo de componentes), destilar em uma spec estruturada, e então escrever como skill e instalar no meu próprio Claude Code.

Agradeço à Anthropic por escrever os prompts do Claude Design de forma tão clara. Esse tipo de criação secundária baseada na inspiração de outros produtos é a nova forma da cultura open source na era da IA.

---

## Licença · Autorização de Uso

**Uso pessoal gratuito e livre** — para estudar, pesquisar, criar, fazer coisas para si mesmo, escrever artigos, fazer projetos paralelos, publicar em redes sociais ou blogs — use à vontade, sem necessidade de avisar.

**Uso comercial empresarial proibido** — qualquer empresa, equipe ou organização com fins lucrativos que queira integrar este skill em produtos, serviços externos ou trabalhos entregues a clientes **precisa primeiro contatar o Huasheng para obter autorização**. Inclui, mas não se limita a:

- Utilizar o skill como parte da cadeia de ferramentas interna da empresa
- Utilizar os resultados do skill como principal meio de criação para entregas externas
- Desenvolver produtos comerciais baseados em derivações do skill
- Utilizar em projetos contratados por clientes

**Contato para autorização comercial** encontra-se nas plataformas sociais abaixo.

---

## Connect · Huasheng (Huashu)

Huasheng é um AI Native Coder, desenvolvedor independente e criador de conteúdo sobre IA. Principais obras:小猫补光灯 (AppStore Top 1 em pagos), 《一本书玩转 DeepSeek》, Nuwa .skill (GitHub 12000+ stars). Mais de 300 mil seguidores em todas as plataformas.

| Plataforma              | Conta        | Link                                                              |
| ----------------------- | ------------ | ----------------------------------------------------------------- |
| X / Twitter             | @AlchainHust | https://x.com/AlchainHust                                         |
| WeChat (公众号)         | 花叔         | Busque por「花叔」no WeChat                                       |
| Bilibili                | 花叔         | https://space.bilibili.com/14097567                               |
| YouTube                 | 花叔         | https://www.youtube.com/@Alchain                                  |
| Xiaohongshu             | 花叔         | https://www.xiaohongshu.com/user/profile/5abc6f17e8ac2b109179dfdf |
| Site oficial            | huasheng.ai  | https://www.huasheng.ai/                                          |
| Página do desenvolvedor | bookai.top   | https://bookai.top                                                |

Autorização comercial, consultoria de parcerias, encomendas de conteúdo → envie mensagem privada para Huasheng em qualquer uma das plataformas acima.
