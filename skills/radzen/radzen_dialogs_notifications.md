# Diretrizes: Dialogs e Notifications

A biblioteca Radzen Blazor gerencia modais, popups e alertas exclusivamente através da injeção de serviços (`DialogService` e `NotificationService`).

**Regra de Ouro:** Nunca crie modais HTML/CSS manuais controlados por variáveis booleanas (ex: `@if(mostrarModal) {... }`). Confie sempre no despacho lógico desses serviços.

## 1. Radzen DialogService (Modais)

O `DialogService` deve ser injetado nas páginas (`@inject DialogService DialogService`) para lidar com interrupções visuais e popups.

* **Abertura de Componentes Assíncrona:** Para injetar uma página ou componente complexo no modal, utilize o método genérico `OpenAsync`:

```csharp
await DialogService.OpenAsync("Título do Modal", new Dictionary<string, object> { { "Id", 1 } });

```

Este é o método padrão que previne sobrecarga do arquivo raiz.

* **Alertas e Confirmações (Substitutos Nativos do JS):**
* Use `DialogService.Alert("Detalhes da mensagem", "Título", options)` para exibir falhas e avisos efêmeros.
* Use `DialogService.Confirm("Confirmar operação?", "Atenção", options)` para interceptar decisões. O retorno será um `bool?` indicando a escolha do usuário.

* **Controle de Fechamento Defensivo (`CanClose`):** Para formulários em edição, previna fechamentos acidentais (tecla Esc ou clique fora) injetando uma função no callback `CanClose` dentro de `DialogOptions`. Retorne `false` para bloquear a ação.
* **Side Dialogs:** Formulários ou detalhes adicionais podem deslizar das laterais usando os métodos nativos atrelados à classe `SideDialogOptions`, permitindo definir larguras e propriedades gráficas sem tocar em CSS.

## 2. Radzen NotificationService (Toasts/Avisos)

O `NotificationService` envia avisos flutuantes na tela sem interromper o fluxo do usuário.

* **Classificação Visual (`Severity`):** O agente deve sempre atrelar a propriedade principal ao enum `NotificationSeverity`, escolhendo entre `Info`, `Warning`, `Error` e `Success`.
* **Estrutura de Conteúdo:** O texto da notificação é obrigatoriamente particionado entre o título `Summary` e os detalhes subjacentes em `Detail`. (Se o conteúdo for complexo, pode-se usar `SummaryContent` e `DetailContent`).
* **Experiência de Usuário (UX):** Habilite barras de duração ativando a propriedade visual indicadora `ShowProgress` e, quando aplicável, orquestre callbacks de eventos através da propriedade iterativa `Click`.

**Exemplo de Invocação de Notificação a ser gerado pela IA:**

```csharp
NotificationService.Notify(new NotificationMessage
{
    Severity = NotificationSeverity.Success,
    Summary = "Registro Atualizado",
    Detail = "As configurações foram salvas com sucesso no banco de dados.",
    Duration = 4000,
    ShowProgress = true,
    CloseOnClick = true
});

```
