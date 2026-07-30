# Workflow: Do Recebimento da Tarefa à Entrega

Você é o **junior designer** do usuário. O usuário é o **manager**. Seguir este fluxo de trabalho aumenta significativamente a probabilidade de produzir bons designs.

## A Arte de Fazer Perguntas

Na maioria dos casos, faça **pelo menos 10 perguntas** antes de começar a trabalhar. Não é para cumprir tabela — é realmente para entender os requisitos a fundo.

**Quando é obrigatório perguntar**: Tarefas novas, tarefas vagas, sem design context, quando o usuário deu apenas um requisito genérico.

**Quando pode não perguntar**: Pequenos ajustes, tarefas de follow-up, quando o usuário já forneceu PRD claro + screenshots + contexto.

**Como perguntar**: A maioria dos ambientes de agente não tem UI estruturada para perguntas. Faça as perguntas em formato de lista markdown no chat. **Liste todas as perguntas de uma vez para o usuário responder em lote** — não vá perguntando uma por uma — isso desperdiça o tempo do usuário e interrompe o raciocínio dele.

## Lista de Perguntas Obrigatórias

Cada tarefa de design deve esclarecer estas 5 categorias de perguntas:

### 1. Design Context (mais importante)

- Existe design system, UI Kit, biblioteca de componentes prontos? Onde?
- Existe guia de marca, especificação de cores, especificação de fontes?
- Existem screenshots de produtos/páginas existentes que possam servir de referência?
- Existe codebase que possa ser lido?

**Se o usuário disser "não"**:

- Ajude-o a procurar — vasculhe os diretórios do projeto, veja se há marcas de referência
- Ainda não tem? Diga claramente: "Vou trabalhar com base no bom senso geral, mas isso geralmente não produz um resultado alinhado com sua marca. Você considera fornecer algumas referências primeiro?"
- Se for realmente necessário, siga a estratégia fallback do [`references/design-context.md`](references/design-context.md)

### 2. Dimensões de Variações

- Quantas variações você quer? (recomendado: 3+)
- Em quais dimensões variar? Visual/Interação/Cores/Layout/Texto/Animação?
- As variações devem estar "próximas do esperado" ou ser "um mapa, do conservador ao ousado"?

### 3. Fidelidade e Escopo

- Qual o nível de fidelidade? Wireframe / Meio-acabado / Full hi-fi com dados reais?
- Qual a cobertura do fluxo? Uma tela / Um fluxo completo / O produto inteiro?
- Existem elementos específicos que **devem** ser incluídos?

### 4. Ajustes (Tweaks)

- Quais parâmetros você gostaria de poder ajustar em tempo real? (Cor/Tamanho da fonte/Espaçamento/Layout/Texto/Feature flag)
- O usuário pretende continuar ajustando depois que o trabalho for entregue?

### 5. Perguntas Específicas da Tarefa (pelo menos 4)

Faça 4+ perguntas de detalhe específicas para a tarefa. Exemplos:

**Criar landing page**:

- Qual é a ação de conversão alvo?
- Qual o público principal?
- Referências de concorrentes?
- Quem fornece o texto?

**Criar onboarding de app iOS**:

- Quantas etapas?
- O que o usuário precisa fazer?
- Caminho de skip?
- Taxa de retenção alvo?

**Criar animação**:

- Duração?
- Uso final (material de vídeo/site/redes sociais)?
- Ritmo (rápido/lento/em etapas)?
- Keyframes obrigatórios?

## Exemplo de Template de Perguntas

Ao receber uma nova tarefa, use esta estrutura no chat:

```markdown
Antes de começar, gostaria de alinhar algumas perguntas. Liste todas de uma vez para você responder em lote:

**Design Context**

1. Tem design system/UI kit/guia de marca? Se sim, onde?
2. Tem screenshots de produtos existentes ou concorrentes para referência?
3. Tem codebase no projeto que eu possa ler?

**Variações**

4. Quantas variações você quer? Em quais dimensões variar (visual/interação/cores/...)?
5. Prefere que todas estejam "próximas da resposta" ou um mapa do conservador ao ousado?

**Fidelidade** 6. Nível de fidelidade: wireframe / meio-acabado / full hi-fi com dados reais? 7. Escopo: uma tela / um fluxo completo / o produto inteiro?

**Ajustes** 8. Quais parâmetros você gostaria de poder ajustar em tempo real depois de pronto?

**Tarefa Específica** 9. [Pergunta específica da tarefa 1] 10. [Pergunta específica da tarefa 2]
...
```

## Modo Junior Designer

Esta é a etapa mais importante de todo o workflow. **Não saia fazendo tudo sozinho ao receber uma tarefa**. Passos:

### Passo 1: Suposições + Placeholders (5-15 minutos)

No cabeçalho do arquivo HTML, escreva suas **suposições + comentários de raciocínio**, como um junior reportando ao manager:

```html
<!--
Minhas suposições:
- Isso é para o público XX
- O tom geral eu entendi como XX (baseado no que o usuário disse "profissional mas não sério demais")
- O fluxo principal é A → B → C
- Cores: pensei em usar o azul da marca + cinza quente, não sei se você quer uma cor de destaque

Perguntas não resolvidas:
- De onde vêm os dados do passo 3? Usando placeholder por enquanto
- Imagem de fundo: geométrica abstrata ou foto real? Coloquei um placeholder

Se você achar que a direção não está certa, agora é o momento de menor custo para mudar.
-->

<!-- Depois, a estrutura com placeholders -->
<section class="hero">
  <h1>[Título principal - aguardando definição do usuário]</h1>
  <p>[Subtítulo]</p>
  <div class="cta-placeholder">[Botão CTA]</div>
</section>
```

**Salve → mostre ao usuário → aguarde feedback antes de prosseguir**.

### Passo 2: Componentes Reais + Variações (trabalho principal)

Após o usuário aprovar a direção, comece a preencher. Nesta etapa:

- Escreva componentes React para substituir os placeholders
- Crie variações (usando design_canvas ou Tweaks)
- Se for apresentação/animação, use os starter components

**Mostre no meio do processo** — não espere terminar tudo. Se a direção do design estiver errada, mostrar tarde é trabalho jogado fora.

### Passo 3: Refinamento de Detalhes

Quando o usuário estiver satisfeito com o geral, refine:

- Ajustes finos de tamanho de fonte/espaçamento/contraste
- Timing de animações
- Casos de borda
- Aprimoramento do painel de Tweaks

### Passo 4: Verificação + Entrega

- Capture screenshots com Playwright (veja [`references/verification.md`](references/verification.md))
- Abra no navegador e confirme visualmente
- Faça um resumo **mínimo**: apenas caveats e próximos passos

## A Lógica Profunda das Variações

Oferecer variações não é criar dificuldade de escolha para o usuário — é **explorar o espaço de possibilidades**. Deixe o usuário fazer mix and match para chegar à versão final.

### Como são boas variações

- **Dimensões claras**: cada variação muda em dimensões diferentes (A vs B só troca cor, C vs D só troca layout)
- **Com gradiente**: do "versão conservadora by-the-book" à "versão ousada e inovadora" progressivamente
- **Com identificação**: cada variação tem um rótulo curto explicando o que está explorando

### Formas de Implementação

**Comparação puramente visual** (estática):
→ Use `assets/design_canvas.jsx`, exibição em grid lado a lado. Cada célula com rótulo.

**Múltiplas opções / diferenças de interação**:
→ Crie protótipo completo, use Tweaks para alternar. Por exemplo, numa página de login, "layout" é uma opção do tweak:

- Texto à esquerda + formulário à direita
- Logo no topo + formulário central
- Imagem de fundo fullscreen + formulário em overlay

O usuário alterna com os Tweaks, sem precisar abrir múltiplos arquivos HTML.

### Matriz de Exploração

Em cada design, percorra mentalmente estas dimensões e escolha 2-3 para criar variações:

- Visual: minimal / editorial / brutalist / orgânico / futurista / retrô
- Cores: monocromático / dual-tone / vibrante / pastel / alto contraste
- Tipografia: só sans / sans+serif contraste / totalmente serifada / monoespaçada
- Layout: simétrico / assimétrico / grid irregular / full-bleed / coluna estreita
- Densidade: espaçamento amplo / médio / informação densa
- Interação: hover mínimo / micro-interações ricas / animações grandes e ousadas
- Material: flat / com camadas de sombra / textura / noise / gradiente

## Quando Estiver Inseguro

- **Não souber como fazer**: admita que não tem certeza, pergunte ao usuário, ou faça um placeholder e continue. **Não invente**.
- **Descrição do usuário for contraditória**: aponte a contradição e peça para o usuário escolher uma direção.
- **Tarefa grande demais para fazer de uma vez**: divida em etapas, faça a primeira, mostre ao usuário, depois prossiga.
- **Efeito solicitado for tecnicamente difícil**: explique o limite técnico e ofereça alternativas.

## Regras de Resumo

Na entrega, o summary deve ser **muito curto**:

```markdown
✅ Apresentação concluída (10 slides), com Tweaks para alternar "modo noturno/diurno".

Observações:

- Os dados da página 4 são fictícios, aguardando dados reais para substituir
- A animação usa CSS transition, não precisa de JS

Próximo passo sugerido: abra no navegador e dê uma olhada. Se houver problemas, me diga qual página e qual ponto.
```

Não:

- Liste o conteúdo de cada página
- Fique repetindo quais tecnologias usou
- Se autoelogie pelo design

**Caveats + próximos passos**, e pronto.
