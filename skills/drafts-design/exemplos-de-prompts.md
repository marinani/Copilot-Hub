# Exemplos de Prompts — drafts-design

Cinco prompts que cobrem os modos de operação centrais da skill.

---

## 1. Protótipo Interativo de App com Marca Real

> **Contexto de uso**: Fluxo principal — marca definida, produto digital.

```
Preciso de um protótipo navegável para o novo módulo de "Extrato de Pontos"
do aplicativo do Programa de Fidelidade da Magazine Luiza.

O que tenho:
- Screenshot da home atual do app (em anexo)
- Logo da Magalu e paleta oficial: amarelo #FFE000, vermelho #E8000F
- Fonte: Nunito (já usada no app)

Quero ver três telas em sequência: resumo do saldo, histórico de transações
e tela de resgate. O usuário precisa conseguir clicar nos itens do histórico
para ver o detalhe. Dispositivo: iPhone 15 Pro.
```

**Por que a skill trata com facilidade**: tem design system fornecido, marca real com ativos disponíveis, escopo delimitado (3 telas + fluxo de clique), dispositivo especificado — a skill ativa o Protocolo de Ativos Centrais, confirma os assets, e entrega em modo Junior Designer (rascunho → confirmação → versão completa).

---

## 2. Deck de Apresentação para Diretoria

> **Contexto de uso**: Slide Designer — conteúdo técnico para audiência executiva.

```
Preciso de um deck em HTML (1920×1080) para apresentar à diretoria os
resultados do Q1 2026 do time de produto.

Conteúdo:
- 3 iniciativas entregues (nomes e métricas em anexo no CSV)
- 1 iniciativa atrasada (com causa-raiz e plano de recuperação)
- Próximos 90 dias: roadmap de 4 itens com status semáforo

Tom: profissional, dados em destaque, sem exagero visual. A empresa usa
o padrão de marca azul escuro (#1A2B4A) e branco, fonte Inter.
Quero speaker notes em cada slide com os pontos que devo falar.
```

**Por que a skill trata com facilidade**: entregável de apresentação é um dos cinco cenários explícitos da skill; o tom pedido ("dados em destaque, sem exagero visual") está alinhado à filosofia anti-slop; speaker notes fazem parte do repertório nativo.

---

## 3. Exploração de Direção de Design (Fallback Consultivo)

> **Contexto de uso**: Consultor de Direção de Design — projeto sem referência definida.

```
Estou criando um produto SaaS de gestão de contratos para escritórios de
advocacia. Ainda não tenho marca, paleta, nem referência de estilo — estou
na fase de decidir a identidade visual.

O público são advogados sêniores (40-60 anos), acostumados a interfaces
conservadoras, mas o produto precisa parecer moderno e diferenciado dos
rivais (Jusbrasil, Projuris).

Me mostra três direções de design completamente diferentes para eu escolher
uma e aprofundar.
```

**Por que a skill trata com facilidade**: a ausência de contexto e o pedido explícito de direções ativam o Modo Consultor — a skill percorre as 5 escolas (Arquitetura da Informação, Minimalismo, Filosofia Oriental, etc.), escolhe 3 de escolas distintas, explica por que cada uma serve ao perfil do público, e pode gerar demos visuais dos três caminhos em paralelo para o usuário comparar.

---

## 4. Animação de Lançamento de Produto com Vídeo Exportado

> **Contexto de uso**: Animador + pipeline de exportação MP4/GIF.

```
Preciso de uma animação de lançamento para o novo modelo de headphone
Bluetooth da JBL, o JBL Tour Pro 3.

Duração: 15 segundos.
Estilo: fundo preto, produto em destaque com luz lateral suave, entrada do
logo no final com tagline "Ouve cada detalhe".
Formato de entrega: GIF para usar em e-mail marketing + MP4 60fps para
o Instagram Stories.

O logo da JBL está neste link: [URL] . O render oficial do produto está
neste link: [URL].
```

**Por que a skill trata com facilidade**: animação baseada em timeline é um dos cinco cenários explícitos; a skill recebe os assets reais (logo + render), segue o Protocolo de Ativos Centrais sem precisar pesquisar, e entrega o pipeline completo — HTML animado → conversão MP4 25fps → interpolação 60fps → GIF com palette otimizada.

---

## 5. Revisão Heurística de Interface Existente

> **Contexto de uso**: Pós-entrega — avaliação 5D de um protótipo ou tela real.

```
Aqui está o protótipo HTML do módulo de emissão de NF-e que meu time
desenvolveu (arquivo em anexo).

Quero uma revisão completa antes de apresentar para o cliente. Avalie em
cinco dimensões: consistência filosófica, hierarquia visual, execução de
detalhes, funcionalidade e inovação. Para cada dimensão, dê uma nota de
0 a 10 e liste os pontos a corrigir em ordem de prioridade.
```

**Por que a skill trata com facilidade**: a Revisão 5D é uma capacidade nativa de pós-entrega — a skill já tem as cinco dimensões definidas, os critérios de pontuação 0-10 estabelecidos, e o formato de saída (nota + lista de correções priorizadas) é parte do protocolo padrão.

---

## Padrão Comum nos Cinco Prompts

Todos os prompts que a skill trata bem têm uma ou mais dessas características:

- **Escopo de entrega visual** (protótipo, slide, animação, infográfico) — não uma web app de produção
- **Contexto fornecido ou solicitável** (marca, assets, referência) — a skill sabe como buscá-los quando ausentes
- **Critério de sucesso claro** (fluxo de clique, duração, dimensões, notas) — a skill não precisa adivinhar o "done"
