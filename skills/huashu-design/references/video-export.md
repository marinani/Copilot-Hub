# Video Export: Exportando Animação HTML para MP4/GIF

Após concluir uma animação HTML, os usuários frequentemente perguntam "consigo exportar como vídeo?". Este guia fornece o fluxo completo.

## Quando Exportar

**Momento de exportação**:

- A animação foi executada completamente e verificada visualmente (captura de tela do Playwright confirma estado correto em cada ponto no tempo)
- O usuário viu no navegador pelo menos uma vez e aprovou o resultado
- **Não** exporte enquanto houver bugs na animação — é mais caro corrigir depois de exportado para vídeo

**Gatilhos comuns que o usuário pode mencionar**:

- "Consegue exportar como vídeo?"
- "Converter para MP4"
- "Fazer um GIF"
- "60fps"

## Especificações de Saída

Por padrão, forneça três formatos para o usuário escolher:

| Formato   | Especificação                                          | Adequado para                                         | Tamanho típico (30s) |
| --------- | ------------------------------------------------------ | ----------------------------------------------------- | -------------------- |
| MP4 25fps | 1920×1080 · H.264 · CRF 18                             | Incorporação em WeChat, Video Accounts, YouTube       | 1-2 MB               |
| MP4 60fps | 1920×1080 · minterpolate interpolação · H.264 · CRF 18 | Exibição em alta taxa de quadros, Bilibili, portfólio | 1.5-3 MB             |
| GIF       | 960×540 · 15fps · palette otimizado                    | Twitter/X, README, pré-visualização Slack             | 2-4 MB               |

## Cadeia de Ferramentas

Dois scripts em `scripts/`:

### 1. `render-video.js` — HTML → MP4

Grava uma versão MP4 básica a 25fps. Depende do playwright global.

```bash
NODE_PATH=$(npm root -g) node /path/to/claude-design/scripts/render-video.js <arquivo_html>
```

Parâmetros opcionais:

- `--duration=30` duração da animação (segundos)
- `--width=1920 --height=1080` resolução
- `--trim=2.2` segundos a cortar do início do vídeo (remove tempo de recarregamento + carregamento de fontes)
- `--fontwait=1.5` tempo de espera para carregamento de fontes (segundos), aumentar quando houver muitas fontes

Saída: mesmo diretório do HTML, com mesmo nome `.mp4`.

### 2. `add-music.sh` — MP4 + BGM → MP4

Adiciona música de fundo a um MP4 sem áudio, selecionando da biblioteca interna de BGM por clima (mood), ou usando áudio próprio. Ajusta duração automaticamente, adiciona fade in/out.

```bash
bash add-music.sh <input.mp4> [--mood=<nome>] [--music=<caminho>] [--out=<caminho>]
```

**Biblioteca BGM interna** (em `assets/bgm-<mood>.mp3`):

| `--mood=`         | Estilo                                                          | Cenário adequado                                                         |
| ----------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `tech` (padrão)   | Apple Silicon / keynote Apple, sintetizador minimalista + piano | Lançamento de produto, ferramentas de IA, divulgação do Skill            |
| `ad`              | Eletrônico moderno upbeat, com build + drop                     | Anúncios em redes sociais, teasers de produto, vídeos promocionais       |
| `educational`     | Quente e brilhante, violão leve/piano elétrico, convidativo     | Divulgação científica, introdução a tutoriais, teasers de curso          |
| `educational-alt` | Alternativa similar, tente outra                                | Mesmo que acima                                                          |
| `tutorial`        | Lo-fi ambiente, quase imperceptível                             | Demonstração de software, tutoriais de programação, demonstrações longas |
| `tutorial-alt`    | Alternativa similar                                             | Mesmo que acima                                                          |

**Comportamento**:

- A música é cortada para a duração do vídeo
- 0.3s fade in + 1s fade out (evita cortes bruscos)
- Stream de vídeo `-c:v copy` sem reencodificação, áudio AAC 192k
- `--music=<caminho>` tem prioridade sobre `--mood`, permite especificar qualquer áudio externo
- Se o nome do mood estiver errado, lista todas as opções disponíveis, sem falhar silenciosamente

**Pipeline típico** (três etapas de exportação de animação + música):

```bash
node render-video.js animation.html                        # Gravação
bash convert-formats.sh animation.mp4                      # Deriva 60fps + GIF
bash add-music.sh animation-60fps.mp4                      # Adiciona BGM tech padrão
# Ou para diferentes cenários:
bash add-music.sh tutorial-demo.mp4 --mood=tutorial
bash add-music.sh product-promo.mp4 --mood=ad --out=promo-final.mp4
```

### 3. `convert-formats.sh` — MP4 → 60fps MP4 + GIF

Gera versão 60fps e GIF a partir de um MP4 existente.

```bash
bash /path/to/claude-design/scripts/convert-formats.sh <input.mp4> [gif_width] [--minterpolate]
```

Saída (mesmo diretório da entrada):

- `<nome>-60fps.mp4` — usa `fps=60` cópia de quadros por padrão (ampla compatibilidade); adicione `--minterpolate` para interpolação de alta qualidade
- `<nome>.gif` — GIF com palette otimizado (960 de largura padrão, ajustável)

**Seleção de modo 60fps**:

| Modo                      | Comando                                    | Compatibilidade                             | Cenário de uso                                                                                                 |
| ------------------------- | ------------------------------------------ | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Cópia de quadros (padrão) | `convert-formats.sh in.mp4`                | QuickTime/Safari/Chrome/VLC todos funcionam | Entrega geral, upload para plataformas, redes sociais                                                          |
| Interpolação minterpolate | `convert-formats.sh in.mp4 --minterpolate` | macOS QuickTime/Safari podem recusar        | Cenários de exibição que precisam de interpolação real, **testar localmente no player alvo antes de entregar** |

Por que o padrão mudou para cópia de quadros? O stream elementar H.264 gerado pelo minterpolate tem um bug de compatibilidade conhecido — antes, com minterpolate como padrão, encontramos várias vezes o problema "macOS QuickTime não abre". Veja `animation-pitfalls.md` §14.

Parâmetro `gif_width`:

- 960 (padrão) — uso geral em plataformas sociais
- 1280 — mais nítido, mas arquivo maior
- 600 — carregamento prioritário no Twitter/X

## Fluxo Completo (Recomendação Padrão)

Após o usuário dizer "exportar vídeo":

```bash
cd <diretório_do_projeto>

# Assumindo que $SKILL aponta para a raiz deste skill (substitua conforme local de instalação)

# 1. Gravar MP4 básico a 25fps
NODE_PATH=$(npm root -g) node "$SKILL/scripts/render-video.js" my-animation.html

# 2. Derivar MP4 60fps e GIF
bash "$SKILL/scripts/convert-formats.sh" my-animation.mp4

# Lista de saída:
# my-animation.mp4         (25fps · 1-2 MB)
# my-animation-60fps.mp4   (60fps · 1.5-3 MB)
# my-animation.gif         (15fps · 2-4 MB)
```

## Detalhes Técnicos (Para Solução de Problemas)

### Armadilhas do Playwright recordVideo

- Taxa de quadros fixa em 25fps, não é possível gravar diretamente em 60fps (limite do compositor do Chromium headless)
- Começa a gravar desde a criação do context, é necessário usar `trim` para cortar o tempo de carregamento inicial
- Formato webm padrão, precisa de ffmpeg para converter para H.264 MP4 para reprodução universal

O `render-video.js` já trata os problemas acima.

### Parâmetros ffmpeg minterpolate

Configuração atual: `minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`

- `mi_mode=mci` — motion compensation interpolation (compensação de movimento)
- `mc_mode=aobmc` — adaptive overlapped block motion compensation
- `me_mode=bidir` — estimativa de movimento bidirecional
- `vsbmc=1` — variable size block motion compensation

Funciona bem com animações CSS **transform** (translate/scale/rotate).
Pode produzir leve ghosting em **fade puro** — se o usuário reclamar, degrade para cópia simples de quadros:

```bash
ffmpeg -i input.mp4 -r 60 -c:v libx264 ... output.mp4
```

### Por que o palette GIF precisa de duas etapas

GIF suporta apenas 256 cores. Um GIF de passagem única comprime todas as cores da animação em um palette genérico de 256 cores, o que resulta em perda de qualidade para combinações de cores sutis como bege + laranja.

Duas etapas:

1. `palettegen=stats_mode=diff` — escaneia todo o vídeo, gera **palette ótimo para esta animação**
2. `paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle` — codifica com este palette, rectangle diff atualiza apenas áreas de mudança, reduzindo significativamente o tamanho do arquivo

Para transições fade, usar `dither=bayer` é mais suave que `none`, mas o arquivo fica um pouco maior.

## Pre-flight Check (Antes de Exportar)

Auto-verificação de 30 segundos antes de exportar:

- [ ] HTML executado completamente no navegador, sem erros no console
- [ ] Quadro 0 da animação é o estado inicial completo (não está carregando em branco)
- [ ] Último quadro da animação é um estado final estável (não está no meio)
- [ ] Fontes/imagens/emoji renderizados corretamente (consulte `animation-pitfalls.md`)
- [ ] Parâmetro Duration corresponde à duração real da animação no HTML
- [ ] No HTML, Stage detecta `window.__recording` e força loop=false (obrigatório para Stage escrito manualmente; ao usar `assets/animations.jsx` já vem incluso)
- [ ] Sprite final com `fadeOut={0}` (último quadro do vídeo não desvanece)
- [ ] Incluir marca d'água "Created by Huashu-Design" (obrigatório apenas para animações; para trabalhos de terceiros, adicionar prefixo "Não oficial · ". Veja SKILL.md § "Marca d'água de divulgação do Skill")

## Instruções Anexadas na Entrega

Formato padrão de instruções ao usuário após exportação concluída:

```
**Entrega Completa**

| Arquivo | Formato | Especificação | Tamanho |
|---|---|---|---|
| foo.mp4 | MP4 | 1920×1080 · 25fps · H.264 | X MB |
| foo-60fps.mp4 | MP4 | 1920×1080 · 60fps (interpolação de movimento) · H.264 | X MB |
| foo.gif | GIF | 960×540 · 15fps · palette otimizado | X MB |

**Observações**
- 60fps usa minterpolate para interpolação de movimento, bom para animações transform
- GIF usa palette otimizado, animação de 30s pode ser comprimida para cerca de 3MB

Avise se precisar de tamanho ou taxa de quadros diferente.
```

## Demandas Adicionais Comuns dos Usuários

| Usuário diz                | Resposta                                                                            |
| -------------------------- | ----------------------------------------------------------------------------------- |
| "Muito grande"             | MP4: aumentar CRF para 23-28; GIF: reduzir resolução para 600 ou fps para 10        |
| "GIF muito borrado"        | Aumentar `gif_width` para 1280; ou sugerir usar MP4 (WeChat Moments também suporta) |
| "Quero vertical 9:16"      | Alterar `--width=1080 --height=1920` na fonte HTML, regravar                        |
| "Adicionar marca d'água"   | ffmpeg com `-vf "drawtext=..."` ou `overlay=` com PNG                               |
| "Quero fundo transparente" | MP4 não suporta alpha; usar WebM VP9 + alpha ou APNG                                |
| "Quero sem perdas"         | CRF alterar para 0 + preset veryslow (arquivo ficará 10x maior)                     |
