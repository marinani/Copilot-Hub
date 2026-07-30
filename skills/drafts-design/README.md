# Drafts-Design — Skill de Produção Visual com HTML

Skill que posiciona o agente de IA como um **designer especialista** que usa HTML como ferramenta de produção, não como meio de entrega web. Conforme a tarefa, o skill incorpora diferentes especialistas: Animador, UX Designer, Slide Designer, Prototipador.

O fluxo de trabalho padrão é o do **Junior Designer**: mostrar suposições e placeholders antes de executar, iterar com feedback antecipado antes que o retrabalho se torne caro.

## O que é

Skill de produção visual com HTML para cinco categorias de entregáveis: protótipos interativos, slides de apresentação, animações com timeline, exploração de variações de design e infográficos com qualidade de impressão. Quando a demanda for vaga, opera em Modo Fallback como **Consultor de Direção de Design** — seleciona 3 direções diferenciadas entre 5 escolas × 20 filosofias de design e gera demos visuais para o usuário escolher.

Não se destina a web apps de produção, sites com SEO ou sistemas dinâmicos com backend.

## Quando Usar

- Protótipos interativos de alta fidelidade: mockups clicáveis de produto (app iOS/Android, web), onde o usuário pode navegar e sentir o fluxo antes da implementação
- Exploração de variações de design: comparar múltiplas direções lado a lado, ou ajustar parâmetros em tempo real via painel Tweaks
- Slides de apresentação: deck HTML em 1920×1080 navegável no browser, exportável para PDF vetorial ou PPTX com caixas de texto editáveis
- Animações e motion design: produção baseada em timeline (Stage + Sprite), exportável como MP4 25fps/60fps + GIF com paleta otimizada + BGM + SFX
- Infográficos e visualizações: layout com qualidade de revista, tipografia precisa, orientado a dados reais, exportável para PDF/PNG 300dpi
- Consultoria de direção de design: quando o usuário não sabe que estilo quer — o skill recomenda 3 direções com demos visuais gerados em paralelo

## Capacidades

| Capacidade | Entregável | Tempo típico |
|------------|-----------|--------------|
| Protótipo interativo (App / Web) | HTML em arquivo único · bezel real de iPhone · clicável · verificado com Playwright | 10–15 min |
| Slides de apresentação | Deck HTML (navegação no browser) + PPTX editável (caixas de texto preservadas) | 15–25 min |
| Animação em timeline | MP4 (25fps / 60fps com interpolação) + GIF (paleta otimizada) + BGM + SFX | 8–12 min |
| Variações de design | 3+ comparações lado a lado · Tweaks em tempo real · exploração multidimensional | 10 min |
| Infográfico / Visualização | Layout com qualidade de impressão · exportável para PDF/PNG/SVG | 10 min |
| Consultoria de direção de design | 5 escolas × 20 filosofias · 3 direções diferenciadas · demos visuais em paralelo | 5 min |
| Revisão especializada | Gráfico radar em 5 dimensões + Keep/Fix/Quick Wins · lista de correções acionáveis | 3 min |

## Como Funciona

### Princípio #0 — Verificação Factual Antes de Supor (prioridade máxima)

Qualquer afirmação sobre existência, status de lançamento, número de versão ou especificações de produtos/tecnologias **deve ser verificada com `WebSearch` antes de qualquer outra ação**. Nunca afirmar com base no corpus de treinamento.

Origem desta regra: em 2026-04-20, o skill assumiu que o DJI Pocket 4 "ainda não havia sido lançado" — o produto tinha sido lançado 4 dias antes. Resultado: animação conceitual genérica que precisou ser refeita (1–2 horas de retrabalho). Uma pesquisa de 10 segundos evitaria o problema.

**Frases que sinalizam que uma pesquisa é necessária antes de continuar:**

- "eu lembro que X ainda não foi lançado"
- "X atualmente está na versão vN"
- "o produto X talvez não exista"
- "pelo que sei, as especificações de X são..."

### Protocolo de Ativos de Marca (5 etapas obrigatórias)

Quando a tarefa envolve uma marca específica (nome de produto, empresa ou cliente), o skill executa obrigatoriamente:

| Etapa | Ação |
|-------|------|
| 1 · Perguntar | Checklist de 6 tipos de ativos: logo / imagens do produto / screenshots de UI / paleta de cores / fontes / brand guidelines |
| 2 · Buscar canais oficiais | `<brand>.com/brand`, `/press`, `/press-kit` · página do produto · Launch Film oficial |
| 3 · Baixar por tipo de ativo | Logo (SVG inline → avatar de rede social) · imagem do produto (hero page → press kit → frames de vídeo de lançamento) · UI (App Store → frames de demo) |
| 4 · Verificar + extrair | Checar fidelidade do logo · resolução da imagem do produto (≥ 2000px) · atualidade da UI · extrair valores hex dos arquivos reais |
| 5 · Consolidar spec | Escrever `brand-spec.md` com caminhos de todos os ativos e variáveis CSS |

**Classificação de importância dos ativos (ordem decrescente):**

1. Logo — obrigatório para qualquer marca
2. Imagem/render do produto — obrigatório para produtos físicos
3. Screenshots de UI — obrigatório para produtos digitais
4. Valores de cor — auxiliar
5. Fontes — auxiliar

**Por que esta ordem importa:** Os três primeiros itens determinam o reconhecimento da marca. Extrair apenas cores e fontes e usar silhuetas CSS no lugar do produto gera uma "animação tecnológica genérica" — fundo preto + accent laranja — indistinguível entre marcas. Testado com o caso DJI Pocket 4 (2026-04-20): a animação produzida sem logo e sem imagem real do produto não comunicava a marca de nenhuma forma reconhecível.

**Critério de qualidade «5-10-2-8» para imagens (exceto logo):**

> "Nosso princípio é pesquisar 5 rodadas, encontrar 10 materiais, selecionar 2 bons. Cada um precisa ter nota 8/10 ou mais. Melhor ter menos do que incluir qualquer coisa só para cumprir tarefa."

| Dimensão | Critério |
|----------|----------|
| 5 rodadas de busca | Cruzar múltiplos canais; não parar nos 2 primeiros resultados |
| 10 candidatos | Acumular pelo menos 10 opções antes de filtrar |
| Selecionar 2 bons | Dos 10, escolher 2 como materiais finais |
| Cada um nota 8/10+ | Abaixo de 8, usar placeholder honesto ou AI generation baseado na referência oficial |

### Fluxo de Trabalho Junior Designer

Modo de trabalho padrão em todas as tarefas:

1. Antes de começar, enviar lista completa de perguntas de uma vez — não perguntar enquanto já está executando
2. No HTML, escrever `assumptions + placeholders + reasoning comments` antes de qualquer componente real
3. Mostrar ao usuário o mais cedo possível (mesmo que apenas blocos cinzas com labels)
4. Preencher componentes reais → variações → Tweaks, mostrando novamente na metade
5. Antes de entregar, verificar visualmente no browser com Playwright

**Lógica subjacente:** entender errado e corrigir cedo é 100× mais barato que corrigir tarde. Um placeholder honesto é 10× melhor que uma implementação ruim.

**Pontos de verificação obrigatórios** (ao encontrar 🛑, parar, dizer o que foi feito, esperar confirmação antes de continuar):

- 🛑 Checkpoint 1: enviar lista de perguntas → esperar resposta
- 🛑 Checkpoint 2: enunciar as quatro perguntas de posicionamento (papel narrativo / distância do espectador / temperatura visual / estimativa de capacidade) + design system → esperar confirmação
- 🛑 Checkpoint 3: mostrar rascunho inicial com placeholders → esperar feedback
- 🛑 Checkpoint 4: revisão visual final no browser antes de entregar

### Consultor de Direção de Design (Fallback para demandas vagas)

Ativado quando o usuário não tem referência de estilo clara ("faz algo bonito", "não sei que estilo quero", "me ajuda a projetar"). O skill **não insiste em fazer com intuição genérica** — entra neste modo para evitar produzir trabalho sem identidade.

O fluxo percorre 8 fases:

1. Entender a fundo a necessidade (máximo 3 perguntas por vez)
2. Recontextualização consultiva (100–200 palavras reformulando a necessidade essencial)
3. Recomendar 3 filosofias de design diferenciadas, obrigatoriamente de 3 escolas distintas (Arquitetura da Informação / Poética do Movimento / Minimalismo / Vanguarda Experimental / Filosofia Oriental)
4. Exibir galeria de showcases pré-fabricados de `assets/showcases/` (8 cenários × 3 estilos = 24 amostras)
5. Gerar 3 demos visuais — um por direção — usando conteúdo real do usuário
6. Usuário escolhe, mistura ("paleta de A + layout de C") ou pede nova rodada
7. Gerar prompt AI estruturado para a direção escolhida
8. Retornar ao fluxo principal do Junior Designer com design context definido

Biblioteca completa de 20 estilos com DNA de prompt em `references/design-styles.md`.

### Regras Anti-AI Slop

*AI slop* = o "máximo denominador comum visual" do corpus de treinamento. Gradiente roxo, emoji como ícone, card arredondado + borda esquerda accent, SVG desenhando rostos — não são feios em si, mas não carregam nenhuma informação de marca. Usar esses elementos dilui a identidade do usuário em "mais uma página feita por IA".

**O que evitar (e por quê):**

| Elemento | Por que é slop | Quando pode usar |
|----------|---------------|-----------------|
| Gradiente roxo agressivo | Fórmula universal de "aparência tecnológica" em landing pages de SaaS/AI/web3 | A própria marca usa gradiente roxo |
| Emoji como ícone | Compensa falta de profissionalismo com decoração infantil | A própria marca usa (ex: Notion) |
| Card arredondado + borda esquerda accent | Combinação batida da era Material/Tailwind 2020-2024 | Explicitamente no brand spec |
| SVG desenhando imagery (rosto/objeto) | Traços desalinhados, proporções estranhas — invariavelmente | Quase nunca — usar imagem real ou placeholder honesto |
| Silhueta CSS substituindo imagem real do produto | Resultado é "animação tecnológica genérica", qualquer produto físico fica igual | Quase nunca — seguir o Protocolo de Ativos |
| Inter/Roboto/Arial como display | Indistinguível de "página de demo" | Brand spec explicitamente usa essas fontes |
| Neon cyberpunk / fundo `#0D1117` | Cópia da estética dark mode do GitHub | Produto developer tool e a própria marca segue essa direção |

**O que fazer positivamente:**

- `text-wrap: pretty` + CSS Grid + propriedades CSS avançadas: detalhes de tipografia que diferenciam um designer real
- `oklch()` ou cores do brand spec: nunca inventar cores novas — cada cor inventada dilui o reconhecimento da marca
- Imagens: priorizar AI generation, screenshots HTML apenas para tabelas de dados precisas
- Um detalhe feito 120%, os outros 80%: bom gosto não é ser refinado em tudo, é ser refinado no lugar certo

**Critério de julgamento:** a exceção legal para qualquer regra acima é "a própria marca usa". Se o brand spec diz para usar gradiente roxo, usar — deixa de ser slop e passa a ser assinatura da marca.

### Revisão Especializada em 5 Dimensões (opcional)

Ativada quando o usuário pede revisão, avaliação ou quando o agente quer fazer controle de qualidade ativo. Avalia em:

1. **Consistência Filosófica** — o design faz o que prometeu filosoficamente?
2. **Hierarquia Visual** — o olhar do espectador percorre a intenção?
3. **Execução de Detalhes** — os detalhes somam ou subtraem?
4. **Funcionalidade** — interações e estados funcionam conforme esperado?
5. **Inovação** — há algo memorável ou é genérico?

Cada dimensão recebe nota 0–10 + lista de problemas classificados como ⚠️ Fatal / ⚡ Importante / 💡 Otimização. Inclui Quick Wins (top 3 coisas que levam 5 minutos). Ver `references/critique-guide.md`.

## Casos de Uso com Lições Aprendidas

### Caso 1 — Animação de lançamento DJI Pocket 4 (2026-04-20)

Usuário pediu animação de lançamento para o DJI Pocket 4. O agente assumiu, sem pesquisar, que o produto ainda não havia sido lançado e produziu uma animação "conceitual" com silhueta CSS (fundo preto + accent laranja). O produto havia sido lançado 4 dias antes, com Launch Film oficial e renders disponíveis.

**Consequência:** animação sem logo da DJI, sem imagem real do produto, sem reconhecimento de marca. Retrabalho de 1–2 horas.

**Protocolo derivado:** Princípio #0 (verificação factual antes de qualquer ação) + obrigatoriedade de buscar logo e imagem real do produto antes de começar qualquer HTML.

### Caso 2 — Design Lovart: confusão entre cor da marca e cor de demonstração

Ao analisar screenshots do produto Lovart, a cor vermelha do XiCha (marca de demonstração visível nos screenshots) foi confundida com a cor da marca Lovart. O design resultante usava vermelho como cor primária — que não é a cor do Lovart.

**Protocolo derivado:** ao extrair cores de screenshots de UI, distinguir ativamente se há marcas de demonstração presentes. Quando duas cores fortes aparecem juntas em um screenshot, verificar qual pertence ao produto e qual à demonstração.

### Caso 3 — Design Kimi: cor adivinhada errada

O agente assumiu "deve ser laranja" para a marca Kimi baseado em memória. Kimi usa azul `#1783FF`. Retrabalho completo.

**Protocolo derivado:** nunca afirmar cores de marca sem extrair de fonte oficial.

### Caso 4 — Deck "Falando sobre skill" (uso avançado)

Deck de 13 páginas HTML com dois demos cinematográficos de 22 segundos (BGM + SFX) com linguagem visual completamente independente entre si. Cada demo exibe por padrão um dashboard de workflow estático completo — visível a qualquer momento pelo público — e dispara a animação ao clicar, retornando ao dashboard ao finalizar. Dados reais integrados via GitHub API (curva de stars), verificação de specs com WebSearch. Padrões documentados em `references/cinematic-patterns.md`.

## Exportação de Vídeo

A forma de entrega padrão de HTML animado é MP4 com áudio — não apenas imagem. Vídeo sem som é produto semi-acabado.

Pipeline:

1. `scripts/render-video.js` → MP4 sem áudio (intermediário, não é o produto final)
2. `scripts/convert-formats.sh` → MP4 60fps (interpolação) + GIF com paleta otimizada
3. `scripts/add-music.sh` → adiciona BGM (6 músicas pré-fabricadas: tech/ad/educational/tutorial + variantes)
4. SFX a partir de `assets/sfx/<categoria>/*.mp3` (37 efeitos pré-fabricados em 8 categorias)

O sistema duplo BGM + SFX é obrigatório: SFX ocupa alta frequência, BGM ocupa baixa frequência. Entregar apenas BGM é ⅓ do trabalho. Ver `references/audio-design-rules.md` e `references/video-export.md`.

**Marca d'água em animações:** `DRAFTS · DESIGN` é incluída por padrão apenas em animações (HTML → MP4/GIF). Não incluída em slides, infográficos, protótipos ou páginas web. Se o usuário disser "sem marca d'água", respeitar.

## Estrutura de Arquivos

```
drafts-design/
├── SKILL.md                      # Documento principal (para o agente ler)
├── README.md                     # Este arquivo
├── assets/                       # Starter Components
│   ├── animations.jsx            # Stage + Sprite + Easing + interpolate
│   ├── ios_frame.jsx             # Bezel do iPhone 15 Pro (Dynamic Island exata)
│   ├── android_frame.jsx         # Bezel Android
│   ├── macos_window.jsx          # Chrome de janela macOS
│   ├── browser_window.jsx        # URL bar + tab bar
│   ├── deck_stage.js             # Engine de slides HTML (single file)
│   ├── deck_index.html           # Agregador de decks com múltiplos arquivos
│   ├── design_canvas.jsx         # Exibição de variações lado a lado
│   ├── showcases/                # 24 exemplos pré-fabricados (8 cenários × 3 estilos)
│   │   ├── INDEX.md              # Índice dos showcases
│   │   ├── cover/                # Capas de artigo (3 estilos)
│   │   ├── ppt/                  # Páginas PPT de dados (3 estilos)
│   │   ├── infographic/          # Infográficos verticais (3 estilos)
│   │   └── website-*/            # Homepages, SaaS, dev docs, AI nav/writing (3 estilos cada)
│   ├── sfx/                      # 37 efeitos sonoros pré-fabricados
│   │   ├── ui/                   # click, hover, focus, toggle, tap
│   │   ├── keyboard/             # type, enter, delete, space
│   │   ├── transition/           # whoosh, dissolve, slide, swipe
│   │   ├── impact/               # logo-reveal, brand-stamp, drop
│   │   ├── magic/                # sparkle, transform, ai-process
│   │   ├── progress/             # generate-start, loading-tick, complete
│   │   ├── feedback/             # success, error, notification, achievement
│   │   ├── container/            # card-flip, modal-open, stack-collapse
│   │   └── terminal/             # command-execute, cursor-blink, output-appear
│   └── bgm-*.mp3                 # 6 músicas de fundo por cenário
├── references/                   # Subdocumentos para leitura por tarefa
│   ├── workflow.md               # Fluxo de trabalho e templates de perguntas
│   ├── design-styles.md          # Biblioteca de 20 filosofias de design + DNA de prompt
│   ├── design-context.md         # Âncoras de bom gosto (fallback leve)
│   ├── scene-templates.md        # Templates de cena por tipo de saída
│   ├── content-guidelines.md     # Anti-AI slop e diretrizes de conteúdo
│   ├── react-setup.md            # Setup React+Babel + erros comuns
│   ├── slide-decks.md            # Arquitetura HTML-first para slides
│   ├── editable-pptx.md          # 4 restrições rígidas para PPTX editável
│   ├── animations.md             # Referência de animações
│   ├── animation-pitfalls.md     # 14 armadilhas reais de animação
│   ├── animation-best-practices.md # 5 arcos narrativos + Expo easing + linguagem de movimento
│   ├── tweaks-system.md          # Sistema de variações em tempo real
│   ├── critique-guide.md         # Revisão especializada em 5 dimensões
│   ├── verification.md           # Checklist de verificação Playwright
│   ├── video-export.md           # Pipeline completo de exportação de vídeo
│   ├── audio-design-rules.md     # Sistema duplo BGM+SFX, proporções, receitas de cena
│   ├── sfx-library.md            # Catálogo dos 37 SFX pré-fabricados
│   ├── apple-gallery-showcase.md # Técnica Gallery com inclinação 3D + pan lento
│   ├── hero-animation-case-study.md # Gallery Ripple + Multi-Focus (destilado do hero v9)
│   └── cinematic-patterns.md     # Padrões cinematográficos avançados (deck "skill-talk")
├── scripts/                      # Cadeia de ferramentas de exportação
│   ├── render-video.js           # HTML → MP4 sem áudio
│   ├── convert-formats.sh        # MP4 → 60fps + GIF
│   ├── add-music.sh              # MP4 + BGM
│   ├── export_deck_pdf.mjs       # HTML deck multi-arquivo → PDF
│   ├── export_deck_stage_pdf.mjs # HTML deck single-file → PDF
│   ├── export_deck_pptx.mjs      # HTML → PPTX editável
│   ├── html2pptx.js              # Tradutor DOM → objetos PowerPoint
│   └── verify.py                 # Wrapper Playwright para verificação
└── demos/                        # Demonstrações de capacidades (HTML + GIF)
    ├── c1-ios-prototype.*        # Protótipo iOS
    ├── c2-slides-pptx.*          # Slides → PPTX
    ├── c3-motion-design.*        # Motion design engine
    ├── c4-tweaks.*               # Tweaks em tempo real
    ├── c5-infographic.*          # Infográfico
    ├── c6-expert-review.*        # Revisão especializada
    ├── w1-brand-protocol.*       # Protocolo de ativos de marca
    ├── w2-junior-designer.*      # Fluxo Junior Designer
    └── w3-fallback-advisor.*     # Consultor de direção de design
```

## Exemplos de Invocação

**Protótipo iOS clicável:**
> "Crie um protótipo iOS de app Pomodoro com IA, 4 telas principais clicáveis."

**Slides com exportação:**
> "Faça uma apresentação de slides sobre psicologia da IA, recomende 3 direções de estilo para eu escolher."

**Animação de produto:**
> "Transforme essa lógica em uma animação de 60 segundos, exporte MP4 e GIF."

**Consultoria de direção (demanda vaga):**
> "Preciso fazer algo bonito para o lançamento do produto. Não sei que estilo quero."

**Revisão de design:**
> "Faça uma revisão em 5 dimensões deste design."

**Variações de design:**
> "Quero ver 3 variações diferentes de layout para esta landing page."

## Integração com o Repositório

Esta pasta é disponibilizada para o agente no projeto-alvo via symlink, conforme documentado no [README.md raiz](../../../README.md):

```cmd
mklink /D .cursor\skills\design D:\ai-dev-agents\skills\design
```

Isso disponibiliza todos os skills de design (`design-specialist`, `drafts-design` e `ui-ux-pro-max`) para o agente no projeto-alvo.

### Posição no Workflow

O `drafts-design` não faz parte do pipeline ForjaSpec — é um skill complementar de produção visual. Pode ser invocado em qualquer momento do workflow, tipicamente para:

- Prototipar uma feature especificada pelo `especificar` antes da implementação
- Criar material de apresentação a partir de um `plano.md` ou especificação
- Produzir demonstrações visuais de um sistema mapeado pelo `mapear`
- Gerar infográficos a partir de dados produzidos em qualquer etapa do pipeline

### Quando Usar em Conjunto com Outros Skills de Design

| Cenário | Skill recomendado |
|---------|-------------------|
| Avaliar usabilidade de uma interface existente | `design-specialist` |
| Criar personas e mapear objetivos de usuário | `design-specialist` |
| Gerar design system completo com fundamento teórico | `ui-ux-pro-max` |
| Prototipar com alta fidelidade a partir do design system | `drafts-design` |
| Criar material de apresentação ou animação | `drafts-design` |
| Fundamento teórico + exploração de variações visuais | `design-specialist` + `drafts-design` |
| Design system completo + protótipo navegável | `ui-ux-pro-max` + `drafts-design` |

## Limitações

- **PPTX editável em camadas para Figma não é suportado.** O skill produz HTML exportável como imagem ou PPTX com caixas de texto reais, mas não pode ser importado para o Keynote como elementos arrastáveis.
- **Animações no nível do Framer Motion não são possíveis.** 3D com física, simulação de partículas e sistemas de fluidos estão fora do escopo.
- **Design do zero para marca sem contexto resulta em qualidade reduzida.** Criar alta fidelidade sem logo, imagens do produto e cores da marca é sempre o último recurso — o protocolo de ativos existe para evitar esse cenário.
