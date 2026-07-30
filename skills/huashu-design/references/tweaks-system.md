# Tweaks: Ajuste em Tempo Real de Variações de Design

Tweaks é uma capacidade central deste skill — permite que o usuário alterne variações/ajuste parâmetros em tempo real sem modificar o código.

**Adaptação entre ambientes de agente**: alguns ambientes nativos de design-agent (como Claude.ai Artifacts) dependem de `postMessage` do host para reescrever os valores dos tweaks no código-fonte para persistência. Este skill adota uma **abordagem puramente front-end com `localStorage`** — o efeito é o mesmo (estado preservado após refresh), mas a persistência ocorre no `localStorage` do navegador, não no arquivo de código-fonte. Esta abordagem funciona em qualquer ambiente de agente (Claude Code / Codex / Cursor / Trae / etc.).

## Quando Adicionar Tweaks

- Quando o usuário solicita explicitamente "poder ajustar parâmetros" / "alternar entre versões"
- Quando o design tem múltiplas variações que precisam ser comparadas
- Quando o usuário não pediu, mas você julga que **adicionar alguns tweaks instigantes pode ajudar o usuário a enxergar possibilidades**

Recomendação padrão: **adicione 2-3 tweaks em cada design** (tema de cor/tamanho de fonte/variação de layout) mesmo que o usuário não peça — mostrar o espaço de possibilidades faz parte do serviço de design.

## Implementação (Versão Puramente Front-end)

### Estrutura Básica

```jsx
const TWEAK_DEFAULTS = {
  primaryColor: "#D97757",
  fontSize: 16,
  density: "comfortable",
  dark: false,
};

function useTweaks() {
  const [tweaks, setTweaks] = React.useState(() => {
    try {
      const stored = localStorage.getItem("design-tweaks");
      return stored
        ? { ...TWEAK_DEFAULTS, ...JSON.parse(stored) }
        : TWEAK_DEFAULTS;
    } catch {
      return TWEAK_DEFAULTS;
    }
  });

  const update = (patch) => {
    const next = { ...tweaks, ...patch };
    setTweaks(next);
    try {
      localStorage.setItem("design-tweaks", JSON.stringify(next));
    } catch {}
  };

  const reset = () => {
    setTweaks(TWEAK_DEFAULTS);
    try {
      localStorage.removeItem("design-tweaks");
    } catch {}
  };

  return { tweaks, update, reset };
}
```

### Painel UI de Tweaks

Painel flutuante no canto inferior direito. Recolhível:

```jsx
function TweaksPanel() {
  const { tweaks, update, reset } = useTweaks();
  const [open, setOpen] = React.useState(false);

  return (
    <div
      style={{
        position: "fixed",
        bottom: 20,
        right: 20,
        zIndex: 9999,
      }}
    >
      {open ? (
        <div
          style={{
            background: "white",
            border: "1px solid #e5e5e5",
            borderRadius: 12,
            padding: 20,
            boxShadow: "0 10px 40px rgba(0,0,0,0.12)",
            width: 280,
            fontFamily: "system-ui",
            fontSize: 13,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 16,
            }}
          >
            <strong>Tweaks</strong>
            <button
              onClick={() => setOpen(false)}
              style={{
                border: "none",
                background: "none",
                cursor: "pointer",
                fontSize: 16,
              }}
            >
              ×
            </button>
          </div>

          {/* Cor */}
          <label style={{ display: "block", marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: "#666" }}>Cor Principal</div>
            <input
              type="color"
              value={tweaks.primaryColor}
              onChange={(e) => update({ primaryColor: e.target.value })}
              style={{ width: "100%", height: 32 }}
            />
          </label>

          {/* Slider de tamanho de fonte */}
          <label style={{ display: "block", marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: "#666" }}>
              Tamanho da Fonte ({tweaks.fontSize}px)
            </div>
            <input
              type="range"
              min={12}
              max={24}
              step={1}
              value={tweaks.fontSize}
              onChange={(e) => update({ fontSize: +e.target.value })}
              style={{ width: "100%" }}
            />
          </label>

          {/* Opção de densidade */}
          <label style={{ display: "block", marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: "#666" }}>Densidade</div>
            <select
              value={tweaks.density}
              onChange={(e) => update({ density: e.target.value })}
              style={{ width: "100%", padding: 6 }}
            >
              <option value="compact">Compacto</option>
              <option value="comfortable">Confortável</option>
              <option value="spacious">Espaçoso</option>
            </select>
          </label>

          {/* Alternância de modo escuro */}
          <label
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              marginBottom: 16,
            }}
          >
            <input
              type="checkbox"
              checked={tweaks.dark}
              onChange={(e) => update({ dark: e.target.checked })}
            />
            <span>Modo Escuro</span>
          </label>

          <button
            onClick={reset}
            style={{
              width: "100%",
              padding: "8px 12px",
              background: "#f5f5f5",
              border: "none",
              borderRadius: 6,
              cursor: "pointer",
              fontSize: 12,
            }}
          >
            Redefinir
          </button>
        </div>
      ) : (
        <button
          onClick={() => setOpen(true)}
          style={{
            background: "#1A1A1A",
            color: "white",
            border: "none",
            borderRadius: 999,
            padding: "10px 16px",
            fontSize: 12,
            cursor: "pointer",
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
          }}
        >
          ⚙ Tweaks
        </button>
      )}
    </div>
  );
}
```

### Aplicando Tweaks

Usando Tweaks no componente principal:

```jsx
function App() {
  const { tweaks } = useTweaks();

  return (
    <div
      style={{
        "--primary": tweaks.primaryColor,
        "--font-size": `${tweaks.fontSize}px`,
        background: tweaks.dark ? "#0A0A0A" : "#FAFAFA",
        color: tweaks.dark ? "#FAFAFA" : "#1A1A1A",
      }}
    >
      {/* Seu conteúdo */}
      <TweaksPanel />
    </div>
  );
}
```

Usando variáveis no CSS:

```css
button.cta {
  background: var(--primary);
  color: white;
  font-size: var(--font-size);
}
```

## Opções Típicas de Tweak

Quais tweaks adicionar para diferentes tipos de design:

### Geral

- Cor principal (color picker)
- Tamanho da fonte (slider 12-24px)
- Tipo de fonte (select: fonte de display vs fonte de corpo)
- Modo escuro (toggle)

### Deck de Slides

- Tema (light/dark/brand)
- Estilo de fundo (solid/gradient/image)
- Contraste de fonte (mais decorativo vs mais contido)
- Densidade de informação (minimal/standard/dense)

### Protótipo de Produto

- Variação de layout (layout A / B / C)
- Velocidade de interação (animation speed 0.5x-2x)
- Volume de dados (quantidade de dados mock 5/20/100)
- Estado (empty/loading/success/error)

### Animação

- Velocidade (0.5x-2x)
- Loop (once/loop/ping-pong)
- Easing (linear/easeOut/spring)

### Landing Page

- Estilo do Hero (image/gradient/pattern/solid)
- Texto do CTA (várias variações)
- Estrutura (single column / two column / sidebar)

## Princípios de Design de Tweaks

### 1. Opções Significativas, Não Apenas para Encher

Cada tweak deve expor **opções de design reais**. Não adicione tweaks que ninguém realmente usaria (como um slider de border-radius de 0-50px — o usuário ajusta e descobre que todos os valores intermediários são feios).

Bons tweaks expõem **variações discretas e pensadas**:

- "Estilo de borda": sem borda / borda sutil / borda arredondada (três opções)
- Não: "Borda": slider 0-50px

### 2. Menos é Mais

O painel de Tweaks de um design deve ter **no máximo 5-6 opções**. Mais que isso vira uma "página de configuração", perdendo o propósito de explorar variações rapidamente.

### 3. O Valor Padrão é o Design Finalizado

Tweaks são **a cereja do bolo**. O valor padrão deve ser, por si só, um design completo e publicável. O que o usuário vê ao fechar o painel de Tweaks é o resultado final.

### 4. Agrupamento Lógico

Quando houver muitas opções, exiba em grupos:

```
---- Visual ----
Cor Principal | Tamanho da Fonte | Modo Escuro

---- Layout ----
Densidade | Posição da Barra Lateral

---- Conteúdo ----
Volume de Dados | Estado
```

## Compatibilidade Retroativa com Host de Persistência em Nível de Código

Se você quiser que o design também funcione em ambientes que suportam tweaks em nível de código-fonte (como Claude.ai Artifacts), mantenha o **bloco de marcação EDITMODE**:

```jsx
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/ {
  primaryColor: "#D97757",
  fontSize: 16,
  density: "comfortable",
  dark: false,
}; /*EDITMODE-END*/
```

O bloco de marcação **não tem efeito** na abordagem com `localStorage` (é apenas um comentário comum), mas em hosts que suportam reescrita de código-fonte, ele será lido para persistência em nível de código. Adicionar isso não causa danos ao ambiente atual, mantendo compatibilidade retroativa.

## Perguntas Frequentes

**O painel Tweaks está cobrindo o conteúdo do design**
→ Torne-o fechável. Fechado por padrão, exibe apenas um pequeno botão, expande quando o usuário clica.

**O usuário precisa reconfigurar após alternar tweaks**
→ Já está usando `localStorage`. Se não persistir após refresh, verifique se o `localStorage` está disponível (modo anônimo pode falhar, use `catch`).

**Múltiplas páginas HTML querem compartilhar tweaks**
→ Adicione um nome de projeto à chave do `localStorage`: `design-tweaks-[projectName]`.

**Quero que tweaks tenham relações de interdependência**
→ Adicione lógica no `update`:

```jsx
const update = (patch) => {
  let next = { ...tweaks, ...patch };
  // Interdependência: ao selecionar modo escuro, alternar automaticamente a cor do texto
  if (patch.dark === true && !patch.textColor) {
    next.textColor = '#F0EEE6';
  }
  setTweaks(next);
  localStorage.setItem(...);
};
```
