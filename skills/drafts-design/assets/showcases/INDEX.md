# Design Philosophy Showcases — Índice de Amostras

> 8 cenários × 3 estilos = 24 amostras de design pré-fabricadas
> Usado na Phase 4 para exibir ao usuário "como este estilo fica na prática"

## Descrição dos Estilos

| Código | Escola | Nome do Estilo | Identidade Visual |
|--------|--------|---------------|-------------------|
| **Pentagram** | Arquitetura da Informação | Pentagram / Michael Bierut | Preto e branco contido, grid suíço, forte hierarquia tipográfica, #E63946 vermelho de destaque |
| **Build** | Minimalismo | Build Studio | Espaço em branco de luxo (70%+), peso sutil (200-600), #D4A574 dourado quente, refinado |
| **Takram** | Filosofia Oriental | Takram | Tecnologia suave, cores naturais (bege/cinza/verde), cantos arredondados, gráficos como arte |

## Tabela de Referência Rápida por Cenário

### Cenários de Design de Conteúdo

| # | Cenário | Dimensões | Pentagram | Build | Takram |
|---|---------|-----------|-----------|-------|--------|
| 1 | Capa de artigo | 1200×510 | `cover/cover-pentagram` | `cover/cover-build` | `cover/cover-takram` |
| 2 | Página de dados PPT | 1920×1080 | `ppt/ppt-pentagram` | `ppt/ppt-build` | `ppt/ppt-takram` |
| 3 | Infográfico vertical | 1080×1920 | `infographic/infographic-pentagram` | `infographic/infographic-build` | `infographic/infographic-takram` |

### Cenários de Design Web

| # | Cenário | Dimensões | Pentagram | Build | Takram |
|---|---------|-----------|-----------|-------|--------|
| 4 | Homepage pessoal | 1440×900 | `website-homepage/homepage-pentagram` | `website-homepage/homepage-build` | `website-homepage/homepage-takram` |
| 5 | AI navegação | 1440×900 | `website-ai-nav/ainav-pentagram` | `website-ai-nav/ainav-build` | `website-ai-nav/ainav-takram` |
| 6 | Ferramenta de escrita AI | 1440×900 | `website-ai-writing/aiwriting-pentagram` | `website-ai-writing/aiwriting-build` | `website-ai-writing/aiwriting-takram` |
| 7 | Landing page SaaS | 1440×900 | `website-saas/saas-pentagram` | `website-saas/saas-build` | `website-saas/saas-takram` |
| 8 | Documentação para devs | 1440×900 | `website-devdocs/devdocs-pentagram` | `website-devdocs/devdocs-build` | `website-devdocs/devdocs-takram` |

> Cada item possui dois arquivos: `.html` (código-fonte) e `.png` (screenshot)

## Instruções de Uso

### Referência na Phase 4 (recomendação de direção)
Após recomendar as direções de design, exiba os screenshots pré-fabricados do cenário correspondente:
```
"Este é o resultado do estilo Pentagram para capa de artigo → [exibir cover/cover-pentagram.png]"
"O estilo Takram para página de dados PPT fica assim → [exibir ppt/ppt-takram.png]"
```

### Prioridade de correspondência de cenário
1. O cenário do usuário tem correspondência exata → exibir diretamente o cenário correspondente
2. Sem correspondência exata mas tipo similar → exibir o cenário mais próximo (ex: "site do produto" → exibir landing page SaaS)
3. Sem correspondência → pular amostras pré-fabricadas, ir direto para Phase 5 gerar ao vivo

### Exibição comparativa lado a lado
Os 3 estilos do mesmo cenário são ideais para exibição lado a lado, ajudando o usuário a comparar visualmente:
- "Esta é a mesma capa de artigo, implementada em 3 estilos diferentes"
- Ordem de exibição: Pentagram (racional e contido) → Build (luxo minimalista) → Takram (suave e acolhedor)

## Detalhes do Conteúdo

### Capa de artigo (cover/)
- Conteúdo: Claude Code Agent workflow — arquitetura com 8 Agents paralelos
- Pentagram: grande "8" vermelho + linhas de grid suíço + barras de dados
- Build: peso ultra-fino "Agent" flutuando em 70% de espaço em branco + linhas finas dourado quente
- Takram: fluxograma radial de 8 nós como peça de arte + fundo bege

### Página de dados PPT (ppt/)
- Conteúdo: GLM-4.7 modelo open-source — avanço em capacidade de Coding (AIME 95.7 / SWE-bench 73.8% / τ²-Bench 87.4)
- Pentagram: "95.7" âncora de 260px + gráfico de barras comparativo vermelho/cinza/cinza claro
- Build: três grupos de números ultra-finos de 120px flutuando + barras comparativas em gradiente dourado quente
- Takram: gráfico radar SVG + sobreposição tricolor + cards de dados com cantos arredondados

### Infográfico vertical (infographic/)
- Conteúdo: Sistema de memória AI CLAUDE.md otimizado de 93KB para 22KB
- Pentagram: números gigantes "93→22" + blocos numerados + barras de dados CSS
- Build: espaço em branco extremo + cards com sombra suave + linhas de conexão dourado quente
- Takram: gráfico de anel SVG + fluxograma com curvas orgânicas + cards com efeito frosted glass

### Homepage pessoal (website-homepage/)
- Conteúdo: portfólio do desenvolvedor independente Alex Chen
- Pentagram: nome em 112px + colunas em grid suíço + números editoriais
- Build: navegação com efeito glass + cards de estatísticas flutuantes + peso ultra-fino
- Takram: textura de papel + avatar circular pequeno + divisórias ultra-finas + layout assimétrico

### AI navegação (website-ai-nav/)
- Conteúdo: AI Compass — diretório de 500+ ferramentas AI
- Pentagram: campo de busca com cantos retos + lista de ferramentas numerada + labels de categoria em maiúsculas
- Build: campo de busca arredondado + cards brancos refinados de ferramentas + labels em pílula
- Takram: layout de cards orgânicos desalinhados + labels de categoria suaves + conexões estilo gráfico

### Ferramenta de escrita AI (website-ai-writing/)
- Conteúdo: Inkwell — assistente de escrita AI
- Pentagram: título grande de 86px + wireframe do editor + colunas de features em grid
- Build: card do editor flutuante + CTA dourado quente + experiência de escrita luxuosa
- Takram: título serifado poético + editor orgânico + fluxograma

### Landing page SaaS (website-saas/)
- Conteúdo: Meridian — plataforma de business intelligence
- Pentagram: colunas preto e branco + dashboard estruturado + âncora "3x" de 140px
- Build: card de dashboard flutuante + gráfico de área SVG + gradiente dourado quente
- Takram: gráfico de barras arredondado + nós de fluxo + cores terrosas suaves

### Documentação para devs (website-devdocs/)
- Conteúdo: Nexus API — gateway unificado de modelos AI
- Pentagram: navegação lateral + blocos de código com cantos retos + highlight vermelho em strings
- Build: card de código flutuante centralizado + sombra suave + ícones dourado quente
- Takram: blocos de código bege + conexões estilo fluxograma + cards de features com borda tracejada

## Estatísticas dos Arquivos

- Arquivos HTML fonte: 24
- Screenshots PNG: 24
- Total de ativos: 48 arquivos

---

**Versão**: v1.0
**Data de criação**: 2026-02-13
**Aplicável a**: skill design-philosophy, Phase 4 — etapa de recomendação
