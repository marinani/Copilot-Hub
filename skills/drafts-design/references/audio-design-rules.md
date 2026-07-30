# Regras de Design de Áudio · drafts-design

> Todas as receitas de aplicação de áudio para demos de animação. Use em conjunto com `sfx-library.md` (inventário de ativos).
> Forjado na prática: iterações hero v1-v9 do lançamento drafts-design · Decomposição aprofundada de três vídeos oficiais da Anthropic · Mais de 8000 comparações A/B

---

## Princípio Central · Sistema de Duas Trilhas de Áudio (Regra de Ferro)

O áudio da animação **deve ser projetado em duas camadas independentes**, não apenas uma:

| Camada                      | Função                       | Escala de Tempo         | Relação com o Visual                        | Faixa de Frequência                 |
| --------------------------- | ---------------------------- | ----------------------- | ------------------------------------------- | ----------------------------------- |
| **SFX (camada de batida)**  | Marca cada batida visual     | 0.2-2 segundos curta    | **Sincronia forte** (alinhamento de quadro) | **Altas frequências 800Hz+**        |
| **BGM (base de atmosfera)** | Base emocional, campo sonoro | Contínuo 20-60 segundos | Sincronia fraca (nível de parágrafo)        | **Médias/baixas frequências <4kHz** |

**Animações com apenas BGM são deficientes** — o público percebe subconscientemente que "a imagem está se movendo mas não há resposta sonora", e é aí que reside a sensação de baixa qualidade.

---

## Padrão Ouro · Proporção Áurea

Estes valores são **parâmetros de engenharia concretos** obtidos da medição de três vídeos oficiais da Anthropic + comparação com nossa versão v9 final. Basta aplicar diretamente:

### Volume

- **Volume BGM**: `0.40-0.50` (relativo à escala máxima 1.0)
- **Volume SFX**: `1.00`
- **Diferença de loudness**: BGM **-6 a -8 dB abaixo** do pico SFX (não é pelo volume absoluto do SFX que se destaca, mas pela diferença de loudness)
- **Parâmetro amix**: `normalize=0` (nunca usar normalize=1, pois achata a faixa dinâmica)

### Isolamento de Faixa de Frequência (Otimização Prioritária P1)

O segredo da Anthropic não é "SFX com volume alto", mas **separação por faixa de frequência**:

```bash
[bgm_raw]lowpass=f=4000[bgm]      # BGM limitado a <4kHz (médias/baixas frequências)
[sfx_raw]highpass=f=800[sfx]      # SFX elevado para 800Hz+ (médias/altas frequências)
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]
```

Por quê: O ouvido humano é mais sensível à faixa de 2-5kHz (a chamada "faixa de presença"). Se o SFX estiver nessa faixa e o BGM cobrir toda a faixa de frequência, **o SFX será mascarado pelas altas frequências do BGM**. Usar highpass para elevar o SFX + lowpass para reduzir o BGM faz com que ambos ocupem seu próprio espaço no espectro, melhorando diretamente a clareza do SFX.

### Fade

- BGM in: `afade=in:st=0:d=0.3` (0.3s, evita corte brusco)
- BGM out: `afade=out:st=N-1.5:d=1.5` (1.5s cauda longa, sensação de conclusão)
- SFX tem envelope próprio, não precisa de fade adicional

---

## Regras de Design de Cue SFX

### Densidade (Quantos SFX a cada 10 segundos)

A densidade de SFX medida nos três vídeos da Anthropic tem três níveis:

| Vídeo                | SFX a cada 10s | Personalidade do Produto                 | Cenário                                         |
| -------------------- | -------------- | ---------------------------------------- | ----------------------------------------------- |
| Artifacts (ref-1)    | **~9/10s**     | Funcionalidades densas, muita informação | Demonstração de ferramenta complexa             |
| Code Desktop (ref-2) | **0**          | Puramente atmosférico, meditativo        | Estado de foco em ferramenta de desenvolvimento |
| Word (ref-3)         | **~4/10s**     | Equilibrado, ritmo de escritório         | Ferramenta de produtividade                     |

**Heurística**:

- Produto com personalidade calma/focada → densidade SFX baixa (0-3/10s), BGM como principal
- Produto com personalidade vibrante/muita informação → densidade SFX alta (6-9/10s), SFX conduz o ritmo
- **Não preencha cada batida visual** — espaço em branco é mais sofisticado que densidade. **Remover 30-50% dos cues torna os restantes mais dramáticos**.

### Prioridade de Seleção de Cue

Nem toda batida visual precisa de SFX. Selecione por esta prioridade:

**P0 Obrigatório** (omitir causa estranheza):

- Digitação (terminal/input)
- Clique/seleção (momento de decisão do usuário)
- Mudança de foco (transferência do protagonista visual)
- Logo reveal (encerramento da marca)

**P1 Recomendado**:

- Entrada/saída de elemento (modal / card)
- Feedback de conclusão/sucesso
- Início/fim de geração por IA
- Transição importante (mudança de cena)

**P2 Opcional** (excesso causa confusão):

- hover / focus-in
- tick de progresso
- ambient decorativo

### Precisão de Alinhamento de Timestamp

- **Alinhamento no mesmo quadro** (erro 0ms): clique/mudança de foco/logo no ponto final
- **1-2 quadros antes** (-33ms): whoosh rápido (dá expectativa psicológica ao espectador)
- **1-2 quadros depois** (+33ms): objeto caindo/impacto (física realista)

---

## Árvore de Decisão para Seleção de BGM

O skill drafts-design vem com 6 músicas BGM (`assets/bgm-*.mp3`):

```
Qual é a personalidade da animação?
├─ Lançamento de produto / demonstração técnica → bgm-tech.mp3 (minimal synth + piano)
├─ Tutorial explicativo / uso de ferramenta → bgm-tutorial.mp3 (warm, instructional)
├─ Educacional / explicação de conceito → bgm-educational.mp3 (curious, thoughtful)
├─ Marketing / divulgação de marca → bgm-ad.mp3 (upbeat, promotional)
└─ Variação do mesmo estilo → bgm-*-alt.mp3 (versões alternativas)
```

### Cenários sem BGM (vale a pena considerar)

Referência: Anthropic Code Desktop (ref-2): **0 SFX + BGM Lo-fi puro** também pode ser sofisticado.

**Quando escolher sem BGM**:

- Duração da animação <10s (BGM não se estabelece)
- Personalidade do produto é "foco/meditação"
- A cena já tem som ambiente/narração
- Densidade de SFX muito alta (evitar sobrecarga auditiva)

---

## Receitas de Cenário (Prontas para Uso)

### Receita A · Hero de lançamento de produto (mesmo estilo do drafts-design v9)

```
Duração: 25 segundos
BGM: bgm-tech.mp3 · 45% · Faixa <4kHz
Densidade SFX: ~6/10s

cue:
  Digitação no terminal → type × 4 (intervalo 0.6s)
  Enter              → enter
  Cartões convergindo → card × 4 (escalonado 0.2s)
  Seleção            → click
  Ripple             → whoosh
  4 mudanças de foco → focus × 4
  Logo               → thud (1.5s)

Volume: BGM 0.45 / SFX 1.0 · amix normalize=0
```

### Receita B · Demonstração de funcionalidade de ferramenta (referência Anthropic Code Desktop)

```
Duração: 30-45 segundos
BGM: bgm-tutorial.mp3 · 50%
Densidade SFX: 0-2/10s (muito baixa)

Estratégia: Deixar BGM + narração conduzirem, SFX apenas em **momentos decisivos** (salvar arquivo/conclusão de comando)
```

### Receita C · Demonstração de geração por IA

```
Duração: 15-20 segundos
BGM: bgm-tech.mp3 ou sem BGM
Densidade SFX: ~8/10s (alta densidade)

cue:
  Input do usuário → type + enter
  IA começa a processar → magic/ai-process (loop 1.2s)
  Geração concluída → feedback/complete-done
  Resultado apresentado → magic/sparkle

Destaque: ai-process pode fazer loop 2-3 vezes durante todo o processo de geração
```

### Receita D · Plano-sequência puramente atmosférico (referência Artifacts)

```
Duração: 10-15 segundos
BGM: nenhum
SFX: 3-5 cues cuidadosamente projetados, usados individualmente

Estratégia: Cada SFX é o protagonista, sem o problema de BGM "embaçar tudo".
Adequado para: Câmera lenta de produto único, exibição em close-up
```

---

## Templates de Composição ffmpeg

### Template 1 · SFX único sobreposto ao vídeo

```bash
ffmpeg -y -i video.mp4 -itsoffset 2.5 -i sfx.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### Template 2 · Composição de múltiplos SFX na linha do tempo (alinhados por tempo de cue)

```bash
ffmpeg -y \
  -i sfx-type.mp3 -i sfx-enter.mp3 -i sfx-click.mp3 -i sfx-thud.mp3 \
  -filter_complex "\
[0:a]adelay=1100|1100[a0];\
[1:a]adelay=3200|3200[a1];\
[2:a]adelay=7000|7000[a2];\
[3:a]adelay=21800|21800[a3];\
[a0][a1][a2][a3]amix=inputs=4:duration=longest:normalize=0[mixed]" \
  -map "[mixed]" -t 25 sfx-track.mp3
```

**Parâmetros-chave**:

- `adelay=N|N`: primeiro é o delay do canal esquerdo (ms), depois o direito, escrever duas vezes para garantir alinhamento estéreo
- `normalize=0`: preserva faixa dinâmica, crucial!
- `-t 25`: corta para a duração especificada

### Template 3 · Vídeo + trilha SFX + BGM (com isolamento de faixa de frequência)

```bash
ffmpeg -y -i video.mp4 -i sfx-track.mp3 -i bgm.mp3 \
  -filter_complex "\
[2:a]atrim=0:25,afade=in:st=0:d=0.3,afade=out:st=23.5:d=1.5,\
     lowpass=f=4000,volume=0.45[bgm];\
[1:a]highpass=f=800,volume=1.0[sfx];\
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k final.mp4
```

---

## Consulta Rápida de Modos de Falha

| Sintoma                                     | Causa Raiz                               | Correção                                                            |
| ------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------------- |
| SFX inaudível                               | Altas frequências do BGM mascaram        | Adicionar `lowpass=f=4000` no BGM + `highpass=f=800` no SFX         |
| SFX muito alto/estridente                   | Volume absoluto do SFX muito alto        | Reduzir volume SFX para 0.7, reduzir BGM para 0.3, manter diferença |
| Conflito de ritmo entre BGM e SFX           | BGM errado (música com batida forte)     | Trocar para BGM ambient / minimal synth                             |
| BGM corta abruptamente no final da animação | Sem fade out                             | `afade=out:st=N-1.5:d=1.5`                                          |
| SFX sobrepostos e embaralhados              | Cues muito densos + cada SFX muito longo | Manter SFX com duração <0.5s, intervalo entre cues ≥ 0.2s           |
| MP4 do WeChat sem áudio                     | WeChat às vezes muta auto-play           | Não se preocupe, o usuário ouvirá ao clicar; GIF não tem som mesmo  |

---

## Integração com o Visual (Avançado)

### Timbre do SFX deve combinar com o estilo visual

- Visual quente/bege/papel → SFX com timbre **amadeirado/suave** (Morse, paper snap, soft click)
- Visual frio/alta tecnologia → SFX com timbre **metálico/digital** (beep, pulse, glitch)
- Visual desenhado à mão/infantil → SFX com timbre **cartunesco/exagerado** (boing, pop, zap)

Nosso atual `apple-gallery-showcase.md` com fundo bege quente → combina com `keyboard/type.mp3` (mechanical) + `container/card-snap.mp3` (soft) + `impact/logo-reveal-v2.mp3` (cinematic bass)

### SFX pode guiar o ritmo visual

Técnica avançada: **projete a linha do tempo SFX primeiro, depois ajuste a animação visual para alinhar com o SFX** (não o contrário).
Porque cada cue SFX é um "tick de relógio", a animação visual se adaptando ao ritmo do SFX fica muito estável — o contrário, SFX tentando acompanhar o visual, frequentemente resulta em ±1 quadro de diferença que causa estranheza.

---

## Lista de Verificação de Qualidade (Auto-inspeção Pré-publicação)

- [ ] Diferença de loudness: pico SFX - pico BGM = -6 a -8 dB?
- [ ] Faixa de frequência: BGM lowpass 4kHz + SFX highpass 800Hz?
- [ ] amix normalize=0 (preserva faixa dinâmica)?
- [ ] BGM fade-in 0.3s + fade-out 1.5s?
- [ ] Quantidade de SFX adequada (densidade conforme personalidade do cenário)?
- [ ] Cada SFX alinhado no mesmo quadro da batida visual (dentro de ±1 quadro)?
- [ ] Duração do som de Logo reveal suficiente (recomendado 1.5s)?
- [ ] Ouvir sem BGM: o SFX sozinho tem ritmo suficiente?
- [ ] Ouvir sem SFX: o BGM sozinho tem variação emocional?

Qualquer uma das duas camadas ouvida isoladamente deve ser coerente. Se só soar bem quando sobrepostas, o trabalho não está bem feito.

---

## Referências

- Inventário de ativos SFX: `sfx-library.md`
- Referência de estilo visual: `apple-gallery-showcase.md`
- Análise aprofundada de áudio dos três vídeos da Anthropic: `/Users/alchain/Documents/writing/01-wechat-articles/projects/2026.04-drafts-design-release/reference-animations/AUDIO-BEST-PRACTICES.md`
- Caso prático drafts-design v9: `/Users/alchain/Documents/writing/01-wechat-articles/projects/2026.04-drafts-design-release/assets/hero-animation-v9-final.mp4`
