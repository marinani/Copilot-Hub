# Guia Avançado de Revisão de Design

> Referência detalhada da Fase 7. Fornece critérios de pontuação, ênfases por cenário e lista de problemas comuns.

---

## Critérios de Pontuação Detalhados

### 1. Consistência Filosófica (Philosophy Alignment)

| Pontuação | Critério                                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------------------ |
| 9-10      | O design incorpora perfeitamente o espírito central da filosofia escolhida, cada detalhe tem fundamento filosófico |
| 7-8       | Direção geral correta, características centrais adequadas, alguns detalhes pontuais desviados                      |
| 5-6       | É possível perceber a intenção, mas na execução misturou elementos de outros estilos, falta pureza                 |
| 3-4       | Apenas imitação superficial, não compreendeu o núcleo da filosofia                                                 |
| 1-2       | Basicamente sem relação com a filosofia escolhida                                                                  |

**Pontos de avaliação**:

- Utiliza os métodos característicos do designer/instituição de referência?
- Cores, tipografia, layout estão alinhados com o sistema filosófico?
- Existem elementos "contraditórios"? (ex: escolheu Kenya Hara mas preencheu com conteúdo excessivo)

### 2. Hierarquia Visual (Visual Hierarchy)

| Pontuação | Critério                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------- |
| 9-10      | O olhar do usuário flui naturalmente conforme a intenção do designer, obtenção de informação sem atrito |
| 7-8       | Relação de hierarquia clara, ocasionalmente 1-2 pontos de hierarquia confusa                            |
| 5-6       | Consegue distinguir título e corpo, mas níveis intermediários confusos                                  |
| 3-4       | Informação planificada, sem ponto de entrada visual claro                                               |
| 1-2       | Confuso, o usuário não sabe para onde olhar primeiro                                                    |

**Pontos de avaliação**:

- O contraste de tamanho entre título e corpo é suficiente? (pelo menos 2,5x)
- Cor/peso/tamanho estabelecem 3-4 níveis hierárquicos claros?
- O espaçamento está guiando o olhar?
- "Teste do olho semicerrado": ao semicerrar os olhos, a hierarquia ainda está clara?

### 3. Execução de Detalhes (Craft Quality)

| Pontuação | Critério                                                                          |
| --------- | --------------------------------------------------------------------------------- |
| 9-10      | Precisão a nível de pixel, alinhamento, espaçamento, cores sem qualquer falha     |
| 7-8       | Globalmente refinado, 1-2 pequenos problemas de alinhamento/espaçamento           |
| 5-6       | Alinhamento básico ok, mas espaçamento não uniforme, uso de cores não sistemático |
| 3-4       | Erros evidentes de alinhamento, espaçamento confuso, cores em excesso             |
| 1-2       | Grosseiro, parece rascunho                                                        |

**Pontos de avaliação**:

- Utiliza um sistema de espaçamento unificado (ex: grid de 8pt)?
- O espaçamento entre elementos do mesmo tipo é consistente?
- A quantidade de cores é controlada? (geralmente não mais que 3-4)
- A família tipográfica é unificada? (geralmente não mais que 2)
- O alinhamento das bordas é preciso?

### 4. Funcionalidade (Functionality)

| Pontuação | Critério                                                                         |
| --------- | -------------------------------------------------------------------------------- |
| 9-10      | Cada elemento de design serve ao objetivo, zero redundância                      |
| 7-8       | Orientação funcional clara, com poucos elementos decorativos removíveis          |
| 5-6       | Basicamente funcional, mas com elementos decorativos evidentes que distraem      |
| 3-4       | Forma sobrepuja função, o usuário precisa se esforçar para encontrar informação  |
| 1-2       | Completamente submerso em decoração, perdeu a capacidade de comunicar informação |

**Pontos de avaliação**:

- Se remover qualquer elemento, o design fica pior? (Se não, deve remover)
- O CTA/informação crítica está na posição mais visível?
- Existem elementos adicionados "porque ficam bonitos"?
- A densidade de informação é compatível com o meio? (PPT não deve ser muito denso, PDF pode ser mais denso)

### 5. Originalidade (Originality)

| Pontuação | Critério                                                                               |
| --------- | -------------------------------------------------------------------------------------- |
| 9-10      | Surpreendente e refrescante, encontrou uma expressão única dentro do quadro filosófico |
| 7-8       | Tem ideias próprias, não é simples aplicação de template                               |
| 5-6       | Mediano, parece template                                                               |
| 3-4       | Uso excessivo de clichês (ex: esfera gradiente representando IA)                       |
| 1-2       | Totalmente composto de templates ou materiais de terceiros                                                |

**Pontos de avaliação**:

- Evita clichês comuns? (veja "Lista de Problemas Comuns" abaixo)
- Há expressão pessoal dentro da filosofia de design escolhida?
- Existem decisões de design "inesperadas mas muito adequadas"?

---

## Ênfase por Cenário de Revisão

Diferentes tipos de saída têm diferentes focos de avaliação:

| Cenário                      | Dimensão Mais Importante             | Secundária              | Pode Relaxar                                        |
| ---------------------------- | ------------------------------------ | ----------------------- | --------------------------------------------------- |
| Capa/Imagem de conta pública | Originalidade, Hierarquia Visual     | Consistência Filosófica | Funcionalidade (imagem única não envolve interação) |
| Infográfico                  | Funcionalidade, Hierarquia Visual    | Execução de Detalhes    | Originalidade (precisão primeiro)                   |
| PPT/Keynote                  | Hierarquia Visual, Funcionalidade    | Execução de Detalhes    | Originalidade (clareza primeiro)                    |
| PDF/White Paper              | Execução de Detalhes, Funcionalidade | Hierarquia Visual       | Originalidade (profissionalismo primeiro)           |
| Landing Page/Site            | Funcionalidade, Hierarquia Visual    | Originalidade           | — (exigência completa)                              |
| App UI                       | Funcionalidade, Execução de Detalhes | Hierarquia Visual       | Consistência Filosófica (usabilidade primeiro)      |
| Imagem para Xiaohongshu      | Originalidade, Hierarquia Visual     | Consistência Filosófica | Execução de Detalhes (atmosfera primeiro)           |

---

## Top 10 Problemas Comuns de Design

### 1. Clichê de tecnologia AI

**Problema**: Esfera gradiente, chuva digital, placa de circuito azul, rosto de robô
**Por que é problema**: Os usuários já estão fatigados visualmente, não conseguem diferenciar você dos outros
**Correção**: Use metáforas abstratas em vez de símbolos literais (ex: use a metáfora do "diálogo" em vez do ícone de balão de chat)

### 2. Hierarquia de tamanho de fonte insuficiente

**Problema**: Diferença muito pequena entre título e corpo (<2,5x)
**Por que é problema**: O usuário não consegue localizar rapidamente a informação crítica
**Correção**: Título deve ser pelo menos 3x o corpo (ex: corpo 16px → título 48-64px)

### 3. Cores em excesso

**Problema**: Uso de mais de 5 cores, sem hierarquia
**Por que é problema**: Confusão visual, sensação de marca fraca
**Correção**: Limite a 1 cor principal + 1 cor secundária + 1 cor de destaque + tons de cinza

### 4. Espaçamento não uniforme

**Problema**: Espaçamento entre elementos aleatório, sem sistema
**Por que é problema**: Parece não profissional, ritmo visual confuso
**Correção**: Estabeleça um sistema de grid de 8pt (espaçamento use apenas 8/16/24/32/48/64px)

### 5. Espaço em branco insuficiente

**Problema**: Todo espaço preenchido com conteúdo
**Por que é problema**: Informação congestionada causa fadiga de leitura, reduzindo a eficiência da comunicação
**Correção**: Espaço em branco deve ocupar pelo menos 40% da área total (estilo minimalista 60%+)

### 6. Fontes em excesso

**Problema**: Uso de mais de 3 fontes
**Por que é problema**: Ruído visual, enfraquece a sensação de unidade
**Correção**: No máximo 2 fontes (1 para título + 1 para corpo), use peso e tamanho para criar variação

### 7. Alinhamento inconsistente

**Problema**: Alguns elementos alinhados à esquerda, outros centralizados, outros à direita
**Por que é problema**: Destrói a sensação de ordem visual
**Correção**: Escolha um modo de alinhamento (recomendado: alinhamento à esquerda) e mantenha globalmente

### 8. Decoração sobrepujando conteúdo

**Problema**: Padrões de fundo/gradientes/sombras roubam a atenção do conteúdo principal
**Por que é problema**: Inversão de prioridades — o usuário veio para ver informação, não decoração
**Correção**: "Se eu remover esta decoração, o design fica pior?" Se não, remova

### 9. Abuso de neon cyberpunk

**Problema**: Fundo azul escuro (#0D1117) + efeito de brilho neon
**Por que é problema**: Zona de conforto estética padrão (linha de base de bom gosto deste skill), e já se tornou um dos maiores clichês — o usuário pode sobrescrever conforme sua marca
**Correção**: Escolha um esquema de cores mais distinto (consulte o sistema de cores dos 20 estilos)

### 10. Incompatibilidade entre densidade de informação e meio

**Problema**: PPT com uma página inteira de texto / imagem de capa com 10 elementos
**Por que é problema**: Diferentes meios têm diferentes densidades ideais de informação
**Correção**:

- PPT: 1 ideia central por slide
- Imagem de capa: 1 foco visual
- Infográfico: exibição em camadas
- PDF: pode ser mais denso, mas precisa de navegação clara

---

## Template de Relatório de Revisão

```
## Relatório de Revisão de Design

**Pontuação Geral**: X.X/10 [Excelente (8+)/Bom (6-7,9)/Precisa Melhorar (4-5,9)/Insuficiente (<4)]

**Pontuação por Item**:
- Consistência Filosófica: X/10 [explicação em uma frase]
- Hierarquia Visual: X/10 [explicação em uma frase]
- Execução de Detalhes: X/10 [explicação em uma frase]
- Funcionalidade: X/10 [explicação em uma frase]
- Originalidade: X/10 [explicação em uma frase]

### Pontos Fortes (Keep)
- [Aponte especificamente o que foi bem feito, usando linguagem de design]

### Problemas (Fix)
[Ordenados por gravidade]

**1. [Nome do Problema]** — ⚠️Crítico / ⚡Importante / 💡Otimização
- Atual: [Descreva a situação atual]
- Problema: [Por que isso é um problema]
- Correção: [Ação específica, incluindo valores]

### Lista de Correções Rápidas (Quick Wins)
Se tiver apenas 5 minutos, priorize estas 3 coisas:
- [ ] [Correção de maior impacto]
- [ ] [Segunda correção mais importante]
- [ ] [Terceira correção mais importante]
```

---

**Versão**: v1.0
**Data de atualização**: 2026-02-13
