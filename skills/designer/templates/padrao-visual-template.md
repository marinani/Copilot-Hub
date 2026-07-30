# Padrão Visual — [Nome do Produto/Projeto]

## 1. Metadados

- **Projeto:** [nome]
- **Versão do padrão:** v0.1.0
- **Data da última atualização:** [AAAA-MM-DD]
- **Responsável:** [nome/time]
- **Status:** Rascunho | Em validação | Aprovado

---

## 2. Objetivo e escopo

### 2.1 Objetivo

[Descrever o objetivo de UX/UI e resultado esperado]

### 2.2 Escopo

- Inclui: [telas/fluxos/componentes]
- Não inclui: [fora de escopo]

---

## 3. Público, contexto e jornada

### 3.1 Público-alvo

- Perfil principal: [descrição]
- Perfil secundário: [descrição]

### 3.2 Contexto de uso

- Ambientes: [desktop, mobile, campo, etc.]
- Restrições: [tempo, rede, iluminação, acessibilidade]

### 3.3 Jornadas críticas

1. [Jornada A]
2. [Jornada B]
3. [Jornada C]

---

## 4. Princípios visuais e de UX

- [Princípio 1]
- [Princípio 2]
- [Princípio 3]
- [Princípio 4]

Aplicações obrigatórias:

- Hierarquia visual clara
- Consistência de padrões
- Clareza de estados e feedback
- Legibilidade acima de ornamentação

---

## 5. Direção estética

### 5.1 Território visual

- Estilo predominante: [minimalista/editorial/premium/etc.]
- Tom da interface: [formal, amigável, técnico, etc.]
- Referências: [links/exemplos]

### 5.2 Do / Don’t

### Do

- [item]
- [item]

### Don’t

- [item]
- [item]

---

## 6. Sistema de cores

### 6.1 Estratégia

- Distribuição sugerida: 60-30-10 (quando aplicável)
- Restrições do projeto: [ex.: evitar fundos quentes saturados]

### 6.2 Tokens

- `--color-primary:` [hex]
- `--color-secondary:` [hex]
- `--color-accent:` [hex]
- `--color-success:` [hex]
- `--color-warning:` [hex]
- `--color-error:` [hex]
- `--color-neutral-50..900:` [escala]

### 6.3 Contraste e acessibilidade

- Texto normal: mínimo 4.5:1
- Texto grande: mínimo 3:1
- Componentes críticos: mínimo 3:1

---

## 7. Tipografia

### 7.1 Famílias e fallback

- Primária: [fonte]
- Secundária: [fonte]
- Fallback: [stack]

### 7.2 Escala tipográfica

- Display:
- H1:
- H2:
- H3:
- Body:
- Small:
- Caption:

### 7.3 Regras

- Máximo de famílias: [2]
- Máximo de pesos principais: [3-4]
- Line-height base: [1.4-1.6]
- Comprimento de linha recomendado: [45-75 caracteres]

---

## 8. Espaçamento, grid e layout

- Unidade base: [4px/8px]
- Escala: [4, 8, 12, 16, 24, 32, 48, 64...]
- Grid desktop: [12 colunas]
- Breakpoints: [mobile/tablet/desktop/wide]
- Max-width de conteúdo: [valor]

---

## 9. Componentes e estados

### 9.1 Componentes essenciais

- Botão
- Input
- Select
- Card
- Modal
- Tabela/Lista
- Navegação

### 9.2 Estados obrigatórios

- Default
- Hover (web)
- Focus (web + teclado)
- Active
- Disabled
- Loading
- Error
- Success

### 9.3 Regras de toque (mobile)

- Alvo mínimo: iOS 44pt / Android 48dp
- Distância mínima entre alvos: 8px

---

## 10. Motion e microinterações

- Princípios: feedback, orientação, continuidade
- Intensidade: [baixa/média/alta]
- Durações por categoria: [micro/transição/entrada]
- Easing padrão: [definir]
- Redução de movimento: suporte obrigatório (`prefers-reduced-motion` e equivalentes)

---

## 11. Navegação e arquitetura de informação

- Padrão principal: [top nav/sidebar/tab bar/drawer/stack]
- Profundidade máxima recomendada: [valor]
- Rotulagem: [regras de nomenclatura]
- Deep links (quando aplicável): [estratégia]

---

## 12. Acessibilidade

- Nível-alvo: WCAG 2.1 AA (mínimo)
- Navegação por teclado (web): obrigatória
- Semântica e ARIA: obrigatórias
- Texto alternativo de mídia: obrigatório
- Não depender só de cor para significado

---

## 13. Responsividade e plataformas

### 13.1 Web

- Viewports alvo: 375 / 768 / 1280 / 1920
- Estratégia: mobile-first

### 13.2 Mobile

- iOS: [guidelines-chave]
- Android: [guidelines-chave]
- Diferenças intencionais por plataforma: [listar]

---

## 14. Implementação e handoff

- Ferramenta de design: Penpot/Figma
- Estrutura de componentes: [padrão]
- Variantes: [padrão]
- Tokens exportáveis: [sim/não]
- Convenções de nomes: [padrão]

---

## 15. QA visual e testes

Checklist mínimo:

- [ ] Verificação de layout
- [ ] Verificação tipográfica
- [ ] Verificação de contraste
- [ ] Verificação de estados
- [ ] Verificação de responsividade
- [ ] Verificação de acessibilidade

Fluxos críticos testados:

1. [fluxo]
2. [fluxo]
3. [fluxo]

---

## 16. Decisões pendentes

1. [decisão] — responsável: [nome] — prazo: [data]
2. [decisão] — responsável: [nome] — prazo: [data]

---

## 17. Histórico de alterações

- Data: [AAAA-MM-DD]
- Seção: [seção]
- Alteração: [descrição]
- Motivo: [motivo]
- Impacto: [impacto]
- Aprovado por: [nome]

---

## 18. Resumo aprovado para o usuário

> [Resumo executivo do padrão visual atual em linguagem objetiva e não técnica, para validação com o usuário.]
