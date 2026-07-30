# Design System Inspirado no Webflow

## 1. Tema Visual e Atmosfera

O site do Webflow é uma plataforma visualmente rica e orientada a ferramentas, que comunica “design sem código” por meio de superfícies brancas limpas, do azul característico do Webflow (`#146ef5`) e de uma paleta secundária rica (roxo, rosa, verde, laranja, amarelo e vermelho). A fonte personalizada WF Visual Sans Variable cria um sistema tipográfico confiante e preciso, com peso 600 para títulos de destaque e 500 para corpo de texto.

**Características principais:**

- Tela branca com texto quase preto (`#080808`)
- Webflow Blue (`#146ef5`) como cor primária de marca e interação
- WF Visual Sans Variable — fonte variável personalizada com peso 500–600
- Paleta secundária rica: roxo `#7a3dff`, rosa `#ed52cb`, verde `#00d722`, laranja `#ff6b00`, amarelo `#ffae13`, vermelho `#ee1d36`
- Border-radius conservador de 4px–8px — visual mais nítido, menos arredondado
- Pilhas de sombra em múltiplas camadas (sombras em cascata com 5 camadas)
- Rótulos em caixa alta: 10px–15px, peso 500–600, espaçamento amplo entre letras (0.6px–1.5px)
- Animação de hover com `translate(6px)` em botões

## 2. Paleta de Cores e Papéis

### Primárias

- **Quase Preto** (`#080808`): texto principal
- **Webflow Blue** (`#146ef5`): `--_color---primary--webflow-blue`, CTA principal e links
- **Blue 400** (`#3b89ff`): `--_color---primary--blue-400`, azul interativo mais claro
- **Blue 300** (`#006acc`): `--_color---blue-300`, variação de azul mais escura
- **Button Hover Blue** (`#0055d4`): `--mkto-embed-color-button-hover`

### Acentos Secundários

- **Roxo** (`#7a3dff`): `--_color---secondary--purple`
- **Rosa** (`#ed52cb`): `--_color---secondary--pink`
- **Verde** (`#00d722`): `--_color---secondary--green`
- **Laranja** (`#ff6b00`): `--_color---secondary--orange`
- **Amarelo** (`#ffae13`): `--_color---secondary--yellow`
- **Vermelho** (`#ee1d36`): `--_color---secondary--red`

### Neutras

- **Cinza 800** (`#222222`): texto secundário escuro
- **Cinza 700** (`#363636`): texto intermediário
- **Cinza 300** (`#ababab`): texto discreto, placeholder
- **Cinza Médio** (`#5a5a5a`): texto de link
- **Cinza de Borda** (`#d8d8d8`): bordas e divisórias
- **Borda Hover** (`#898989`): borda no estado hover

### Sombras

- **Cascata em 5 camadas**: `rgba(0,0,0,0) 0px 84px 24px, rgba(0,0,0,0.01) 0px 54px 22px, rgba(0,0,0,0.04) 0px 30px 18px, rgba(0,0,0,0.08) 0px 13px 13px, rgba(0,0,0,0.09) 0px 3px 7px`

## 3. Regras de Tipografia

### Fonte: `WF Visual Sans Variable`, fallback: `Arial`

| Papel                                        | Tamanho | Peso    | Altura de Linha | Espaçamento entre Letras | Observações |
| -------------------------------------------- | ------- | ------- | --------------- | ------------------------ | ----------- |
| Hero de destaque                             | 80px    | 600     | 1.04            | -0.8px                   |             |
| Título de seção                              | 56px    | 600     | 1.04            | normal                   |             |
| Subtítulo                                    | 32px    | 500     | 1.30            | normal                   |             |
| Título de funcionalidade                     | 24px    | 500–600 | 1.30            | normal                   |             |
| Corpo                                        | 20px    | 400–500 | 1.40–1.50       | normal                   |             |
| Corpo padrão                                 | 16px    | 400–500 | 1.60            | -0.16px                  |             |
| Botão                                        | 16px    | 500     | 1.60            | -0.16px                  |             |
| Rótulo em caixa alta                         | 15px    | 500     | 1.30            | 1.5px                    | caixa alta  |
| Legenda                                      | 14px    | 400–500 | 1.40–1.60       | normal                   |             |
| Badge em caixa alta                          | 12.8px  | 550     | 1.20            | normal                   | caixa alta  |
| Micro em caixa alta                          | 10px    | 500–600 | 1.30            | 1px                      | caixa alta  |

Fonte de código: Inconsolata (fonte monoespaçada complementar).

## 4. Estilos de Componentes

### Botões

- Transparente: texto `#080808`, `translate(6px)` no hover
- Círculo branco: raio de 50%, fundo branco
- Badge azul: fundo `#146ef5`, raio de 4px, peso 550

### Cards: `1px solid #d8d8d8`, raio de 4px–8px

### Badges: fundo azulado com 10% de opacidade, raio de 4px

## 5. Layout

- Espaçamento: escala fracionada (1px, 2.4px, 3.2px, 4px, 5.6px, 6px, 7.2px, 8px, 9.6px, 12px, 16px, 24px)
- Raios: 2px, 4px, 8px, 50% — conservador e nítido
- Breakpoints: 479px, 768px, 992px

## 6. Profundidade: sistema de sombras em cascata com 5 camadas

## 7. Faça e Não Faça

- Faça: use WF Visual Sans Variable entre 500–600. Use azul (`#146ef5`) para CTAs. Raio de 4px. Hover com `translate(6px)`.
- Não faça: arredondar além de 8px em elementos funcionais. Usar cores secundárias em CTAs principais.

## 8. Responsivo: 479px, 768px, 992px

## 9. Guia de Prompt para Agente

- Texto: Quase Preto (`#080808`)
- CTA: Webflow Blue (`#146ef5`)
- Fundo: Branco (`#ffffff`)
- Borda: `#d8d8d8`
- Secundárias: Roxo `#7a3dff`, Rosa `#ed52cb`, Verde `#00d722`
