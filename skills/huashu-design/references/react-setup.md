# React + Babel — Normas do Projeto

Regras técnicas obrigatórias ao fazer protótipos com HTML+React+Babel. Não seguir quebra tudo.

## Script Tags Fixos (use estas versões)

No `<head>` do HTML, coloque estas três script tags com **versão fixa + integrity hash**:

```html
<script
  src="https://unpkg.com/react@18.3.1/umd/react.development.js"
  integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
  crossorigin="anonymous"
></script>
<script
  src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
  integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
  crossorigin="anonymous"
></script>
<script
  src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
  integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
  crossorigin="anonymous"
></script>
```

**Não** use versões sem fixação como `react@18` ou `react@latest` — isso causa desvios de versão / problemas de cache.

**Não** omita `integrity` — é a linha de defesa caso a CDN seja sequestrada ou adulterada.

## Estrutura de Arquivos

```
NomeDoProjeto/
├── index.html               # HTML principal
├── components.jsx           # Arquivo de componentes (carregado com type="text/babel")
├── data.js                  # Arquivo de dados
└── styles.css               # CSS adicional (opcional)
```

Modo de carregamento no HTML:

```html
<!-- Primeiro React + Babel -->
<script src="https://unpkg.com/react@18.3.1/..."></script>
<script src="https://unpkg.com/react-dom@18.3.1/..."></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/..."></script>

<!-- Depois seus arquivos de componente -->
<script type="text/babel" src="components.jsx"></script>
<script type="text/babel" src="pages.jsx"></script>

<!-- Por fim, a entrada principal -->
<script type="text/babel">
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(<App />);
</script>
```

**Não** use `type="module"` — entra em conflito com o Babel.

## Três Regras Inquebráveis

### Regra 1: Objetos styles devem ter nomes únicos

**Errado** (quebra com múltiplos componentes):

```jsx
// components.jsx
const styles = { button: {...}, card: {...} };

// pages.jsx  ← sobrescrita do mesmo nome!
const styles = { container: {...}, header: {...} };
```

**Correto**: use prefixos únicos para styles de cada arquivo de componente.

```jsx
// terminal.jsx
const terminalStyles = {
  screen: {...},
  line: {...}
};

// sidebar.jsx
const sidebarStyles = {
  container: {...},
  item: {...}
};
```

**Ou use inline styles** (recomendado para componentes pequenos):

```jsx
<div style={{ padding: 16, background: "#111" }}>...</div>
```

Esta regra é **innegociável**. Toda vez que escrever `const styles = {...}` deve substituir por um nome específico, senão o carregamento de múltiplos componentes causará erro em toda a pilha.

### Regra 2: Escopos não são compartilhados — exporte manualmente

**Entendimento crítico**: cada `<script type="text/babel">` é compilado independentemente pelo Babel, e os **escopos não se comunicam**. O componente `Terminal` definido em `components.jsx` será **undefined** em `pages.jsx`.

**Solução**: no final de cada arquivo de componente, exporte para `window` os componentes/utilitários que deseja compartilhar:

```jsx
// Final de components.jsx
function Terminal(props) { ... }
function Line(props) { ... }
const colors = { green: '#...', red: '#...' };

Object.assign(window, {
  Terminal, Line, colors,
  // Liste aqui tudo que for usar em outros lugares
});
```

Assim `pages.jsx` pode usar `<Terminal />` diretamente, pois o JSX buscará em `window.Terminal`.

### Regra 3: Não use scrollIntoView

`scrollIntoView` empurra todo o contêiner HTML para cima, quebrando o layout do web harness. **Nunca use**.

Alternativas:

```js
// Rolar até uma posição dentro do contêiner
container.scrollTop = targetElement.offsetTop;

// Ou use element.scrollTo
container.scrollTo({
  top: targetElement.offsetTop - 100,
  behavior: "smooth",
});
```

## Chamar a API Claude (dentro do HTML)

Alguns ambientes nativos de design-agent (como Artifacts do Claude.ai) têm `window.claude.complete` sem configuração, mas a maioria dos ambientes de agente (Claude Code / Codex / Cursor / Trae / etc.) **não têm** localmente.

Se seu protótipo HTML precisar chamar um LLM para demonstração (ex.: fazer uma interface de chat), duas opções:

### Opção A: Não chamar de verdade, usar mock

Recomendado para cenários de demonstração. Crie um helper falso que retorna respostas pré-definidas:

```jsx
window.claude = {
  async complete(prompt) {
    await new Promise((r) => setTimeout(r, 800)); // simula latência
    return "Esta é uma resposta mock. Substitua pela API real ao implantar.";
  },
};
```

### Opção B: Chamar a Anthropic API de verdade

Requer uma chave de API — o usuário deve inserir a própria chave no HTML para executar. **Nunca codifique a chave diretamente no HTML**.

```html
<input id="api-key" placeholder="Cole sua chave da Anthropic API" />
<script>
  window.claude = {
    async complete(prompt) {
      const key = document.getElementById("api-key").value;
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "x-api-key": key,
          "anthropic-version": "2023-06-01",
          "content-type": "application/json",
        },
        body: JSON.stringify({
          model: "claude-haiku-4-5",
          max_tokens: 1024,
          messages: [{ role: "user", content: prompt }],
        }),
      });
      const data = await res.json();
      return data.content[0].text;
    },
  };
</script>
```

**Nota**: chamar a Anthropic API diretamente do navegador encontra problemas de CORS. Se o ambiente de pré-visualização do usuário não suportar bypass de CORS, este caminho não funciona. Nesse caso, use a Opção A (mock) ou informe que é necessário um backend proxy.

### Opção C: Usar a capacidade LLM do lado do agente para gerar dados mock

Se for apenas para demonstração local, você pode chamar temporariamente a capacidade LLM do agente atual (ou uma skill multi-modelo instalada pelo usuário) para gerar dados de resposta mock, e então codificá-los diretamente no HTML. Assim o HTML em execução não dependerá de nenhuma API.

## Template HTML Inicial Típico

Copie este template como esqueleto para protótipos React:

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Nome do Seu Protótipo</title>

    <!-- React + Babel com versões fixas -->
    <script
      src="https://unpkg.com/react@18.3.1/umd/react.development.js"
      integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
      integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
      integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
      crossorigin="anonymous"
    ></script>

    <style>
      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }
      html,
      body {
        height: 100%;
        width: 100%;
      }
      body {
        font-family: -apple-system, "SF Pro Text", sans-serif;
        background: #fafafa;
        color: #1a1a1a;
      }
      #root {
        min-height: 100vh;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>

    <!-- Seus arquivos de componente -->
    <script type="text/babel" src="components.jsx"></script>

    <!-- Entrada principal -->
    <script type="text/babel">
      const { useState, useEffect } = React;

      function App() {
        return (
          <div style={{ padding: 40 }}>
            <h1>Olá</h1>
          </div>
        );
      }

      const root = ReactDOM.createRoot(document.getElementById("root"));
      root.render(<App />);
    </script>
  </body>
</html>
```

## Erros Comuns e Soluções

**`styles is not defined` ou `Cannot read property 'button' of undefined`**
→ Você definiu `const styles` em um arquivo e outro arquivo sobrescreveu. Renomeie cada um com nomes específicos.

**`Terminal is not defined`**
→ Ao referenciar entre arquivos, os escopos não se comunicam. Adicione `Object.assign(window, {Terminal})` ao final do arquivo onde Terminal é definido.

**Página toda branca, sem erros no console**
→ Provavelmente erro de sintaxe JSX que o Babel não reportou no console. Substitua temporariamente `babel.min.js` pela versão não minificada `babel.js` para mensagens de erro mais claras.

**ReactDOM.createRoot is not a function**
→ Versão incorreta. Confirme que está usando react-dom@18.3.1 (não 17 ou outra).

**`Objects are not valid as a React child`**
→ Você está renderizando um objeto em vez de JSX/string. Geralmente é `{someObj}` escrito onde deveria ser `{someObj.name}`.

## Como Dividir Arquivos em Projetos Grandes

**Arquivo único >1000 linhas** é difícil de manter. Estratégia de divisão:

```
Projeto/
├── index.html
├── src/
│   ├── primitives.jsx      # Elementos base: Button, Card, Badge...
│   ├── components.jsx      # Componentes de negócio: UserCard, PostList...
│   ├── pages/
│   │   ├── home.jsx        # Página inicial
│   │   ├── detail.jsx      # Página de detalhes
│   │   └── settings.jsx    # Página de configurações
│   ├── router.jsx          # Roteamento simples (troca de estado React)
│   └── app.jsx             # Componente de entrada
└── data.js                 # Dados mock
```

Carregamento no HTML em ordem:

```html
<script type="text/babel" src="src/primitives.jsx"></script>
<script type="text/babel" src="src/components.jsx"></script>
<script type="text/babel" src="src/pages/home.jsx"></script>
<script type="text/babel" src="src/pages/detail.jsx"></script>
<script type="text/babel" src="src/pages/settings.jsx"></script>
<script type="text/babel" src="src/router.jsx"></script>
<script type="text/babel" src="src/app.jsx"></script>
```

**Ao final de cada arquivo**, use `Object.assign(window, {...})` para exportar o que for compartilhado.
