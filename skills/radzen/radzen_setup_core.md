# Diretrizes de Setup: Radzen Blazor

Quando o usuário pedir para configurar o Radzen em um projeto novo ou existente, execute os seguintes passos obrigatórios:

1. **Pacote NuGet:**
   Instale o pacote: `dotnet add package Radzen.Blazor`
2. **Imports Globais (`_Imports.razor`):**
   Adicione as seguintes linhas:razor

```razor
@using Radzen
@using Radzen.Blazor

```

1. **Injeção de Dependência (`Program.cs`):**
   Registre os serviços requeridos antes do `builder.Build()`:

```csharp
builder.Services.AddRadzenComponents();

```

1. **Tema e Scripts (`App.razor` ou `_Layout.cshtml`):**
   No `<head>`, adicione o tema (ex: material):
   `<link rel="stylesheet" href="_content/Radzen.Blazor/css/material-base.css">`
   No final do `<body>`, injete o script:
   `<script src="_content/Radzen.Blazor/Radzen.Blazor.js?v=@(typeof(Radzen.Colors).Assembly.GetName().Version)"></script>`
2. **Provedor de Componentes Globais (`MainLayout.razor`):**
   Envolva seu `@Body` ou adicione no topo do layout:

```razor
<RadzenComponents @rendermode="InteractiveAuto" />

```
