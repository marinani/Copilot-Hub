# SFX Library · drafts-design

> Todos gerados pela ElevenLabs Sound Generation API, qualidade de áudio nível keynote Apple.
> Biblioteca de ativos SFX de nível profissional, cobrindo todos os cenários de animação/demonstração/demo de produto do [autor].

**Localização dos ativos**: `assets/sfx/<categoria>/<nome>.mp3`
**Total**: 37 SFX (30 gerados em lote + 7 preservados do v7b)
**Modelo de geração**: ElevenLabs Sound Generation API (prompt_influence 0.4)
**Qualidade de áudio**: 44.1kHz MP3, clareza nível keynote Apple, sem reverberação extra

---

## Estrutura de Diretórios

```
assets/sfx/
├── keyboard/      type, type-fast, delete-key, space-tap, enter
├── ui/            click, click-soft, focus, hover-subtle, tap-finger, toggle-on
├── transition/    whoosh, whoosh-fast, swipe-horizontal, slide-in, dissolve
├── container/     card-snap, card-flip, stack-collapse, modal-open
├── feedback/      success-chime, error-tone, notification-pop, achievement
├── progress/      loading-tick, complete-done, generate-start
├── impact/        logo-reveal, logo-reveal-v2, brand-stamp, drop-thud
├── magic/         sparkle, ai-process, transform
└── terminal/      command-execute, output-appear, cursor-blink
```

---

## Índice Rápido

### ⌨️ Keyboard (Digitação)

| Arquivo                       | Duração | Uso                                                            | Pontos-chave do Prompt                              |
| ----------------------------- | ------- | -------------------------------------------------------------- | --------------------------------------------------- |
| `sfx/keyboard/type.mp3`       | 0.5s    | Toque de tecla única (mechanical keyboard single key)          | mechanical keyboard single key press                |
| `sfx/keyboard/type-fast.mp3`  | 1.5s    | Digitação rápida contínua (demonstração de inserção de prompt) | fast continuous typing rhythm, apple magic keyboard |
| `sfx/keyboard/delete-key.mp3` | 0.5s    | Backspace (apagar)                                             | single backspace key, low pitched thud              |
| `sfx/keyboard/space-tap.mp3`  | 0.5s    | Toque leve na barra de espaço                                  | soft spacebar tap, wide flat                        |
| `sfx/keyboard/enter.mp3`      | 0.5s    | Confirmação com Enter (preservado do v7b)                      | enter key press, crisp tactile                      |

### 🎯 UI (Interação de Interface)

| Arquivo                   | Duração | Uso                                          | Pontos-chave do Prompt                   |
| ------------------------- | ------- | -------------------------------------------- | ---------------------------------------- |
| `sfx/ui/click.mp3`        | 0.5s    | Clique UI padrão (preservado do v7b)         | crisp modern interface click             |
| `sfx/ui/click-soft.mp3`   | 0.5s    | Clique UI suave (botão secundário/link)      | soft gentle button click, mid pitched    |
| `sfx/ui/focus.mp3`        | 0.5s    | Foco/seleção de elemento (preservado do v7b) | subtle focus tone, element highlight     |
| `sfx/ui/hover-subtle.mp3` | 0.5s    | Dica de hover (feedback de microssegundos)   | barely audible tick, air whisper         |
| `sfx/ui/tap-finger.mp3`   | 0.5s    | Toque mobile (interface iOS)                 | finger tap on touchscreen, muted thud    |
| `sfx/ui/toggle-on.mp3`    | 0.5s    | Ativar interruptor                           | ios toggle switch flip, satisfying click |

### 🌊 Transition (Transição)

| Arquivo                               | Duração | Uso                                                      | Pontos-chave do Prompt            |
| ------------------------------------- | ------- | -------------------------------------------------------- | --------------------------------- |
| `sfx/transition/whoosh.mp3`           | 0.5s    | Whoosh padrão (preservado do v7b)                        | air whoosh transition             |
| `sfx/transition/whoosh-fast.mp3`      | 0.6s    | Whoosh rápido (título que aparece, troca de aba)         | quick fast air whoosh, cinematic  |
| `sfx/transition/swipe-horizontal.mp3` | 0.7s    | Deslize horizontal (carrossel, troca de tab)             | smooth left-to-right air movement |
| `sfx/transition/slide-in.mp3`         | 0.6s    | Elemento deslizando para dentro (painel lateral, gaveta) | smooth soft whoosh with arrival   |
| `sfx/transition/dissolve.mp3`         | 0.8s    | Dissolução suave (fade out/in de imagem)                 | soft dissolve, airy shimmer       |

### 🃏 Container (Cartão/Container)

| Arquivo                            | Duração | Uso                                                | Pontos-chave do Prompt                |
| ---------------------------------- | ------- | -------------------------------------------------- | ------------------------------------- |
| `sfx/container/card-snap.mp3`      | 0.5s    | Cartão encaixando/posicionando (preservado do v7b) | card snap into place                  |
| `sfx/container/card-flip.mp3`      | 0.7s    | Virar cartão (troca frente/verso)                  | playing card flip, crisp snap         |
| `sfx/container/stack-collapse.mp3` | 0.8s    | Pilha se fechando (agregação de lista)             | cards stacking, paper taps collapsing |
| `sfx/container/modal-open.mp3`     | 0.6s    | Abertura de modal                                  | modal popping open, whoosh + thud     |

### 🔔 Feedback (Notificação/Feedback)

| Arquivo                             | Duração | Uso                                                           | Pontos-chave do Prompt                 |
| ----------------------------------- | ------- | ------------------------------------------------------------- | -------------------------------------- |
| `sfx/feedback/success-chime.mp3`    | 1.0s    | Indicador de sucesso (pagamento concluído, tarefa finalizada) | two ascending bell tones, ios-style    |
| `sfx/feedback/error-tone.mp3`       | 0.7s    | Indicador de erro (aviso, falha)                              | descending two-note warning, soft      |
| `sfx/feedback/notification-pop.mp3` | 0.6s    | Pop-up de mensagem (toast, notificação)                       | notification bloop, ios message alert  |
| `sfx/feedback/achievement.mp3`      | 1.5s    | Conquista alcançada (marco, medalha)                          | triumphant rising arpeggio, game-style |

### ⏳ Progress (Progresso/Estado)

| Arquivo                           | Duração | Uso                                                         | Pontos-chave do Prompt              |
| --------------------------------- | ------- | ----------------------------------------------------------- | ----------------------------------- |
| `sfx/progress/loading-tick.mp3`   | 0.5s    | Temporizador de carregamento (batida de barra de progresso) | soft short pulse, minimal ambient   |
| `sfx/progress/complete-done.mp3`  | 0.8s    | Confirmação de conclusão (etapa concluída)                  | two ascending satisfying tones      |
| `sfx/progress/generate-start.mp3` | 0.8s    | IA começando a gerar                                        | soft rising shimmer, magical whoosh |

### 💥 Impact (Marca/Impacto)

| Arquivo                         | Duração | Uso                                          | Pontos-chave do Prompt               |
| ------------------------------- | ------- | -------------------------------------------- | ------------------------------------ |
| `sfx/impact/logo-reveal.mp3`    | 0.7s    | Impacto de Logo (preservado do v7b)          | logo reveal thud                     |
| `sfx/impact/logo-reveal-v2.mp3` | 1.5s    | Impacto de Logo mais longo (cinematográfico) | cinematic bass hit with shimmer tail |
| `sfx/impact/brand-stamp.mp3`    | 1.0s    | Batida de carimbo (certificação, selo)       | rubber stamp thud, paper contact     |
| `sfx/impact/drop-thud.mp3`      | 0.7s    | Objeto caindo (inserção, colocação)          | heavy thud, wood surface contact     |

### ✨ Magic (Transformação por IA)

| Arquivo                    | Duração | Uso                                            | Pontos-chave do Prompt                  |
| -------------------------- | ------- | ---------------------------------------------- | --------------------------------------- |
| `sfx/magic/sparkle.mp3`    | 0.8s    | Brilho mágico (destaque de IA, surpresa)       | bright twinkling stars, fairy dust      |
| `sfx/magic/ai-process.mp3` | 1.2s    | Som de processamento de IA (estado "pensando") | modulating digital hum with shimmer     |
| `sfx/magic/transform.mp3`  | 1.0s    | Transição de transformação (efeito morph)      | rising shimmer whoosh with sparkle tail |

### 💻 Terminal (Linha de Comando)

| Arquivo                            | Duração | Uso                 | Pontos-chave do Prompt                  |
| ---------------------------------- | ------- | ------------------- | --------------------------------------- |
| `sfx/terminal/command-execute.mp3` | 0.5s    | Execução de comando | crisp digital beep with tick, hacker ui |
| `sfx/terminal/output-appear.mp3`   | 0.6s    | Saída aparecendo    | rapid digital ticks, retro printout     |
| `sfx/terminal/cursor-blink.mp3`    | 0.5s    | Cursor piscando     | subtle soft digital pulse, rhythmic     |

---

## Combinações Recomendadas por Cenário

### 💻 Demonstração de Interação com Terminal

```
type (0.5s) → enter (0.5s) → command-execute (0.5s) → output-appear (0.6s)
```

Elemento de loop: `cursor-blink` como som ambiente em idle.

### 🃏 Fluxo de Seleção de Cartão

```
hover-subtle (0.5s, hover UI) → click-soft (0.5s, clique) → card-snap (0.5s, posicionamento)
```

Ou versão avançada: `card-flip` para troca frente/verso.

### 🤖 Fluxo Completo de Geração por IA

```
generate-start (0.8s, início) → ai-process (1.2s, processamento) → sparkle (0.8s, brilho) → complete-done (0.8s, conclusão)
```

Em caso de erro, usar `error-tone` no lugar de `complete-done`.

### 🎬 Logo Reveal (Momento da Marca)

```
whoosh-fast (0.6s, preparação) → logo-reveal-v2 (1.5s, ponto de impacto) → sparkle (0.8s, cauda)
```

Versão simplificada: `whoosh → logo-reveal` (diretamente o par v7b).

### 📱 Demonstração de Interação UI (Mobile)

```
tap-finger (0.5s, toque) → slide-in (0.6s, painel deslizando) → toggle-on (0.5s, interruptor)
```

Após conclusão: `success-chime` ou `notification-pop`.

### 📊 Visualização de Dados / Dashboard

```
loading-tick (0.5s, batida) × N → complete-done (0.8s, dados prontos) → achievement (1.5s, ponto de impacto impressionante)
```

### 🎯 Fluxo de Envio de Formulário

```
click-soft (0.5s) → loading-tick ×2 (1.0s) → success-chime (1.0s)
```

Ramificação de falha: `error-tone (0.7s)`.

### 🪄 Cenário de Transformação Mágica

```
whoosh-fast (0.6s) → transform (1.0s) → sparkle (0.8s)
```

Adequado para: transformação de elemento, comparação antes/depois, demonstração de "reescrita por IA".

---

## Normas de Uso

### Recomendações de Volume (do sistema de duas trilhas de áudio do apple-gallery-showcase.md)

- **Trilha principal SFX**: `1.0` (sem atenuação)
- **Trilha de fundo BGM**: `0.4 ~ 0.5` (SFX penetra claramente)
- **Múltiplos SFX sobrepostos**: usar `amix=inputs=N:duration=longest:normalize=0` para preservar faixa dinâmica

### Template de Montagem ffmpeg

```bash
# SFX único alinhado a um ponto no tempo:
ffmpeg -i video.mp4 -itsoffset 2.5 -i sfx/ui/click.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4

# Múltiplos SFX + BGM:
ffmpeg -i video.mp4 \
  -itsoffset 1.0 -i sfx/transition/whoosh-fast.mp3 \
  -itsoffset 1.6 -i sfx/impact/logo-reveal-v2.mp3 \
  -i bgm.mp3 \
  -filter_complex "[3:a]volume=0.4[bgm];[0:a][1:a][2:a][bgm]amix=inputs=4:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### Árvore de Decisão de Seleção

1. **Ação tátil** (digitar/clicar/deslizar) → `keyboard/` ou `ui/`
2. **Elemento entrando/saindo** → `transition/`
3. **Operação em camada de container** (cartão/modal) → `container/`
4. **Feedback de estado** (sucesso/falha/notificação) → `feedback/`
5. **Progresso/passagem de tempo** → `progress/`
6. **Ponto de impacto da marca/momento importante** → `impact/`
7. **Magia/transformação por IA** → `magic/`
8. **Linha de comando/demonstração de código** → `terminal/`

### Evitar Acúmulo de Sons Sobrepostos

- No mesmo ponto no tempo, `máximo 2 SFX` concorrentes
- Com BGM abaixo de 0.3, pode-se usar 3 SFX
- Em impacto de marca, limpar outros SFX (deixar 0.2s de espaço antes do ponto de impacto)

---

## Princípios de Redação de Prompt (Para Reutilização)

Estilo de referência: `apple keynote, tight, minimal, no reverb unless ambient, crisp, elegant`

**Três elementos de um bom prompt**:

1. **Descrição física do som**: qual objeto, qual ação ("mechanical keyboard single key press")
2. **Limitação de textura/estilo**: apple-style / ios-style / cinematic / retro
3. **Exclusão de contraexemplos**: no reverb / clean studio / minimal

❌ "click sound"
✅ "crisp ui button click, clean modern interface sound, apple-style, high pitched"

❌ "magic"
✅ "bright twinkling stars sound, high pitched glittery chime, fairy dust"

---

## Veja Também

- Sistema de duas trilhas de áudio e montagem ffmpeg: `apple-gallery-showcase.md`
- Script de geração original: `/tmp/gen_sfx_batch.sh` (gerador de lote único)
