
# Diretrizes: Formulários e Validação

Para criar formulários de inserção ou edição:

1. **Uso Mandatório:** Utilize SEMPRE `<RadzenTemplateForm>` no lugar de `EditForm` nativo.
2. **Vinculação de Dados:**
   Use o parâmetro `Data` se quiser submissões automáticas baseadas em um modelo:
   `<RadzenTemplateForm Data="@meuModelo" TItem="MeuModelo" Submit="@OnSubmit">`

3. **Validadores Radzen:**
   A propriedade `Name` do componente de input DEVE ser idêntica à propriedade `Component` do validador.

```razor
   *Exemplo correto:*razor
   <RadzenTextBox Name="PrimeiroNome" @bind-Value="meuModelo.Nome" />
   <RadzenRequiredValidator Component="PrimeiroNome" Text="O nome é obrigatório" />

```

1. **Tipos de Validadores a Explorar:**

- `RadzenEmailValidator` (Para e-mails)
- `RadzenNumericRangeValidator` (Min/Max numérico)
- `RadzenLengthValidator` (Tamanho de strings)
