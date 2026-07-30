# Diretrizes: RadzenDataGrid

Quando solicitado a criar uma tabela de dados (Grid), aplique estas regras rigorosas:

1. **Sempre priorize Server-Side Paging/Filtering para grandes volumes:**
   Nunca faça `IQueryable.ToList()` antes de passar para o Grid se os dados forem dinâmicos.

2. **Propriedades Obrigatórias para Alta Performance:**
   - Use o evento `LoadData` mapeado para um método C# assíncrono.
   - Defina `AllowPaging="true"`, `AllowSorting="true"` e `AllowFiltering="true"`.
   - Adicione a propriedade `Count="@count"` para manter o paginador sincronizado.
   - Adicione `IsLoading="@isLoading"` para feedback visual.

3. **Exemplo de Estrutura Padrão:**

```razor

   <RadzenDataGrid Data="@dados" Count="@count" LoadData="@CarregarDados" IsLoading="@isLoading"
                   AllowPaging="true" PageSize="10" AllowSorting="true" AllowFiltering="true">
       <Columns>
           <RadzenDataGridColumn Property="Id" Title="ID" />
           <RadzenDataGridColumn Property="Nome" Title="Nome do Cliente" />
       </Columns>
   </RadzenDataGrid>

```

1. **Tratamento de Argumentos (`LoadDataArgs`):**
   No método C#, use `args.Skip`, `args.Top` e `args.Filter` para injetar no repositório do Entity Framework Core.
