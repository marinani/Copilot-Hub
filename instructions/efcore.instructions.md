---
description: 'Guidelines for use C# EF Core applications'
applyTo: '**/*.cs'
---

# EF Core Development

O **Entity Framework (EF) Core** é uma versão leve, extensível, de código aberto e multiplataforma da popular tecnologia de acesso a dados Entity Framework da Microsoft. Ele atua como um **Object-Relational Mapper (O/RM)**, que é uma ferramenta crucial para desenvolvedores .NET.

---

## 🗺️ O que faz o EF Core como O/RM?

A função principal do EF Core como O/RM é permitir que desenvolvedores **.NET** trabalhem com um banco de dados usando **objetos .NET** (classes e propriedades), em vez de escrever a maior parte do código de acesso a dados em **SQL** ou outro idioma específico do banco de dados.

* **Mapeamento Objeto-Relacional:** O EF Core lida com o mapeamento entre as classes (que são as "entidades" na sua aplicação) e as tabelas do banco de dados relacional. Por exemplo, uma classe `Cliente` pode ser mapeada para uma tabela `Clientes`.
* **Consultas LINQ:** Você pode consultar o banco de dados usando **LINQ** (Language-Integrated Query) em C#, que o EF Core traduz internamente para o SQL apropriado do banco de dados.
* **Controle de Alterações e Persistência:** Ele rastreia as alterações feitas nos objetos .NET e gera automaticamente os comandos `INSERT`, `UPDATE` e `DELETE` necessários para persistir essas alterações no banco de dados.
* **Migrations:** O recurso de *Migrations* permite que você evolua o esquema do seu banco de dados conforme o seu modelo de classes .NET muda, gerenciando as alterações de forma controlada.
* **Suporte Multiplataforma e a Vários Bancos de Dados:** Como faz parte do ecossistema .NET Core/.NET, é multiplataforma (Windows, macOS, Linux) e suporta diversos provedores de banco de dados, como SQL Server, SQLite, PostgreSQL, MySQL e Azure Cosmos DB.

Em essência, o EF Core **simplifica e acelera** o desenvolvimento ao abstrair grande parte das complexidades de interagir diretamente com o banco de dados, permitindo que o desenvolvedor se concentre mais na lógica de negócios da aplicação.

A utilização básica do Entity Framework (EF) Core envolve quatro etapas principais:

1. **Instalação** dos pacotes NuGet.
2. **Criação** das classes de modelo (entidades).
3. **Definição** do `DbContext`.
4. **Configuração** e uso do contexto para interagir com o banco de dados.

-----

## 🛠️ 1. Instalação (Pacotes NuGet)

Você precisa instalar os pacotes NuGet apropriados no seu projeto .NET. Os dois pacotes essenciais são:

* **`Microsoft.EntityFrameworkCore`**: O núcleo do EF Core.
* **Um provedor de banco de dados**: Escolha o pacote para o banco de dados que você usará (por exemplo, SQL Server, SQLite, MySQL).

| Banco de Dados | Pacote NuGet de Exemplo                   |
|:---------------|:------------------------------------------|
| **SQL Server** | `Microsoft.EntityFrameworkCore.SqlServer` |
| **SQLite**     | `Microsoft.EntityFrameworkCore.Sqlite`    |
| **PostgreSQL** | `Npgsql.EntityFrameworkCore.PostgreSQL`   |

Você pode instalá-los usando o gerenciador de pacotes NuGet ou a CLI do .NET:

```bash
# Exemplo para SQL Server
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
```

-----

## 👩‍💻 2. Criação das Entidades (Modelos)

As **Entidades** são classes .NET que representam as tabelas do seu banco de dados.

```csharp
// Exemplo de uma classe de Entidade (Tabela no BD)
public class Aluno
{
    // A propriedade 'Id' é convencionalmente reconhecida como a Chave Primária
    public int Id { get; set; }
    public string Nome { get; set; }
    public int Idade { get; set; }
}
```

-----

## 🧠 3. Definição do DbContext

O **`DbContext`** é a classe principal no EF Core. Ele representa uma **sessão** com o banco de dados e é responsável por:

* Gerenciar as conexões.
* Consultar e salvar dados.
* Mapear suas entidades para o banco de dados.

Você deve herdar de `Microsoft.EntityFrameworkCore.DbContext` e definir uma propriedade `DbSet<TEntity>` para cada entidade que deseja mapear.

```csharp
using Microsoft.EntityFrameworkCore;

public class EscolaContexto : DbContext
{
    // O DbSet mapeia a classe Aluno para uma tabela 'Alunos' no BD
    public DbSet<Aluno> Alunos { get; set; }

    // Construtor que recebe as opções de configuração
    public EscolaContexto(DbContextOptions<EscolaContexto> options)
        : base(options)
    {
    }
}
```

-----

## ⚙️ 4. Configuração e Interação

### A. Configuração da Conexão

A maneira mais comum de configurar a string de conexão é passá-la para o `DbContext` através de injeção de dependência no arquivo `Program.cs` (em aplicações web/serviços):

```csharp
builder.Services.AddDbContext<EscolaContexto>(options =>
    // Substitua a string de conexão apropriada
    ````instructions
    ---
    description: "Guidelines for using C# EF Core applications"
    applyTo: '**/*.cs'
    ---

    # EF Core Development

    Entity Framework (EF) Core is a lightweight, extensible, open-source, and cross-platform version of Microsoft's popular data access technology. It acts as an Object-Relational Mapper (ORM), which is an essential tool for .NET developers.

    ---

    ## What EF Core does as an ORM

    EF Core allows .NET developers to work with a database using .NET objects (classes and properties) instead of writing most of the data access code in SQL or another database-specific language.

    - Object-relational mapping: EF Core maps your classes (entities) to database tables (for example, a `Customer` class to a `Customers` table).
    - LINQ queries: You can query the database using LINQ (Language Integrated Query) in C#, which EF Core translates into the appropriate SQL for the selected provider.
    - Change tracking and persistence: EF Core tracks changes made to .NET objects and generates the appropriate `INSERT`, `UPDATE`, and `DELETE` commands to persist those changes.
    - Migrations: The Migrations feature allows you to evolve your database schema as your .NET model classes change.
    - Cross-platform and multi-database support: EF Core runs on Windows, macOS, and Linux, and supports multiple database providers including SQL Server, SQLite, PostgreSQL, MySQL and Azure Cosmos DB.

    In short, EF Core simplifies and speeds up development by abstracting a lot of the complexity of interacting with the database, letting developers focus more on business logic.

    Core steps to using EF Core:

    1. Install NuGet packages.
    2. Create model classes (entities).
    3. Define a `DbContext`.
    4. Configure and use the context to interact with the database.

    -----

    ## 1. Installation (NuGet packages)

    Install the appropriate NuGet packages for your .NET project. The two core packages are:

    - `Microsoft.EntityFrameworkCore`: the EF Core runtime.
    - A database provider package for your chosen database (e.g., SQL Server, SQLite, PostgreSQL).

    Examples:

    | Database       | Example NuGet package                             |
    |:---------------|:--------------------------------------------------|
    | SQL Server     | `Microsoft.EntityFrameworkCore.SqlServer`         |
    | SQLite         | `Microsoft.EntityFrameworkCore.Sqlite`            |
    | PostgreSQL     | `Npgsql.EntityFrameworkCore.PostgreSQL`           |

    Install via the .NET CLI:

    ```bash
    dotnet add package Microsoft.EntityFrameworkCore.SqlServer
    dotnet add package Microsoft.EntityFrameworkCore.Tools
    ```

    -----

    ## 2. Creating entities (models)

    Entities are plain .NET classes that represent database tables.

    ```csharp
    // Example entity class mapped to a database table
    public class Student
    {
        // The 'Id' property is conventionally recognized as the primary key
        public int Id { get; set; }
        public string Name { get; set; }
        public int Age { get; set; }
    }
    ```

    -----

    ## 3. Defining the DbContext

    The `DbContext` is the primary class for EF Core. It represents a session with the database and is responsible for:

    - Managing connections
    - Querying and saving data
    - Mapping your entities to database objects

    Create a class that inherits from `Microsoft.EntityFrameworkCore.DbContext` and expose `DbSet<TEntity>` properties for each entity.

    ```csharp
    using Microsoft.EntityFrameworkCore;

    public class SchoolContext : DbContext
    {
        // The DbSet maps the Student class to the Students table
        public DbSet<Student> Students { get; set; }

        public SchoolContext(DbContextOptions<SchoolContext> options)
            : base(options)
        {
        }
    }
    ```

    -----

    ## 4. Configuration and interaction

    ### A. Connection configuration

    The most common way to configure the connection string is to pass it to the `DbContext` via dependency injection in `Program.cs` (web applications):

    ```csharp
    builder.Services.AddDbContext<SchoolContext>(options =>
        options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
    ```

    ### B. Using the DbContext for CRUD operations

    With a configured `DbContext`, inject it into services or controllers and use it for CRUD operations.

    #### Querying data (LINQ)

    EF Core translates LINQ expressions to SQL.

    ```csharp
    // Query example returning all students
    var allStudents = await context.Students.ToListAsync();

    // Filtered query example
    var adultStudents = await context.Students
        .Where(s => s.Age >= 18)
        .OrderBy(s => s.Name)
        .ToListAsync();
    ```

    #### Create, Update and Delete

    Modify objects and call `SaveChanges()` or `SaveChangesAsync()` to persist changes.

    ```csharp
    // CREATE
    var newStudent = new Student { Name = "Maria", Age = 20 };
    context.Students.Add(newStudent);
    await context.SaveChangesAsync();

    // UPDATE
    var studentToUpdate = await context.Students.FindAsync(1);
    if (studentToUpdate != null)
    {
        studentToUpdate.Name = "Maria Silva";
        await context.SaveChangesAsync();
    }

    // DELETE
    var studentToDelete = await context.Students.FindAsync(2);
    if (studentToDelete != null)
    {
        context.Students.Remove(studentToDelete);
        await context.SaveChangesAsync();
    }
    ```

    -----

    ## Migrations

    Use EF Core Migrations to create and update the database schema based on your entity classes.

    1. Add a new migration:
    ```bash
    dotnet ef migrations add InitialCreate
    ```
    2. Apply migrations to the database:
    ```bash
    dotnet ef database update
    ```

    -----

    The following are best practices for using EF Core to ensure performance, maintainability and scalability.

    -----

    ## Performance and queries

    ### 1. Use `AsNoTracking()` for read-only queries

    If you only read data and do not intend to update it, use `AsNoTracking()`.

    Why: EF Core does not need to track changes for read-only entities, which reduces CPU and memory usage and makes queries faster.

    ```csharp
    // Good: faster for read-only scenarios
    var students = await context.Students.AsNoTracking().ToListAsync();

    // Bad: unnecessary tracking when not updating
    // var students = await context.Students.ToListAsync();
    ```

    ### 2. Use `Where()` and `Select()` for filtering and projection

    Always filter (`Where`) and project (`Select`) the data you need before executing the query.

    - Filter on the server: apply `Where`, `OrderBy`, etc. before calling terminal operations like `ToList()` or `FirstOrDefault()` so filtering happens in the database.
    - Project only required columns with `Select` to reduce network traffic and memory usage.

    ```csharp
    // Good: fetch only Name and Id for students aged 18 or older
    var names = await context.Students
        .Where(s => s.Age >= 18)
        .Select(s => new { s.Name, s.Id })
        .ToListAsync();

    // Bad: loads all columns then filters in memory
    // var all = await context.Students.ToListAsync();
    // var names = all.Where(s => s.Age >= 18).Select(s => s.Name);
    ```

    ### Separating `Where()` clauses (AND vs OR)

    Every `Where` clause should be separated except when conditions are joined by OR (`||`). For conditions combined with AND prefer chaining multiple `.Where(...)` — this improves readability and avoids complex expressions inside a single lambda. When conditions are joined by OR, keep them in a single `Where` call.

    Examples:

    ```csharp
    // BAD
    var result = context.Entities
        .Where(x => x.Name == "name" && x.Date > DateTime.Now);

    // GOOD
    var result = context.Entities
        .Where(x => x.Name == "name")
        .Where(x => x.Date > DateTime.Now);

    // GOOD
    var result = context.Entities
        .Where(x => x.Name == "name" || x.Date > DateTime.Now);
    ```

    ### 3. Eager loading for relationships (`Include`)

    Use `Include()` to load related navigation properties in the same query and avoid accidental N+1 query problems.

    N+1 query problem: when you load a list of entities and then access a related property in a loop, EF Core may execute an additional query per entity, resulting in N+1 total queries.

    ```csharp
    // Good: load students and their courses in a single JOIN
    var studentsWithCourses = await context.Students
        .Include(s => s.Courses)
        .ToListAsync();
    ```

    You can chain `Include` and `ThenInclude` for deeper relationships.

    -----

    ## Design and architecture

    ### 4. Register and dispose the `DbContext` correctly

    In ASP.NET Core apps, register the `DbContext` as Scoped using `services.AddDbContext`. A Scoped lifetime creates one `DbContext` per request and disposes it at the end of the request.

    Rule of thumb: a `DbContext` instance should represent a single unit of work (a single business transaction or HTTP request). Do not register `DbContext` as Singleton — it is not thread-safe.

    ### 5. Repository and Unit of Work patterns (optional)

    Although `DbContext` already provides repository and unit-of-work behavior, some teams still implement explicit repository and unit-of-work layers to isolate data access logic and improve testability (e.g., by mocking repositories).

    ### 6. Owned types

    Use owned types to model value objects that do not need their own table (for example, an Address owned by a Person). This keeps the domain model clean while persisting values in the same table as the owner entity.

    -----

    ## Mapping and configuration

    ### 7. Explicit configuration (Fluent API)

    EF Core relies on conventions and data annotations but for complex mappings prefer using the Fluent API in `OnModelCreating`.

    Why: it centralizes mapping configuration in one place and keeps entity classes focused on domain logic.

    ```csharp
    // Inside DbContext.OnModelCreating
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure a composite primary key
        modelBuilder.Entity<OrderDetail>()
            .HasKey(od => new { od.OrderId, od.ProductId });

        // Specify the exact table name
        modelBuilder.Entity<Student>().ToTable("StudentsTable");
    }
    ```

    ### 8. Manage migrations carefully

    - Review generated SQL: always inspect migration SQL before applying to production.
    - Separate migrations if you have multiple `DbContext` instances (store each context's migrations in its own folder).

    -----

    ## Understanding and resolving N+1 queries

    The N+1 problem occurs when you load a list of N primary entities and then issue N additional queries (one per entity) to load related data.

    The usual solutions are:

    - Use eager loading (`Include`) to fetch related data in the same query.
    - Disable lazy loading if you do not need it and prefer explicit loading.
    - Use projection via `Select` to fetch only the fields you need from related entities.

    ```csharp
    // Eager loading example
    var orders = await context.Orders
        .Include(o => o.OrderItems)
        .ToListAsync();

    // Use ThenInclude for nested navigation properties
    var ordersWithCustomerAddress = await context.Orders
        .Include(o => o.Customer)
            .ThenInclude(c => c.Address)
        .ToListAsync();
    ```

    -----

    ## Efficient projection with `Select()`

    `Include` still selects all columns from involved tables. If you only need a subset of columns, prefer projection with `Select` to create a DTO or anonymous type with only the required fields.

    ```csharp
    var productSummaries = await context.Products
        .Where(p => p.IsActive)
        .Select(p => new ProductSummaryDto
        {
            ProductName = p.Name,
            CategoryName = p.Category.Name
        })
        .ToListAsync();
    ```

    -----

    ## AsNoTracking() — essential optimization for reads

    Use `AsNoTracking()` for queries where returned entities will not be updated. It disables the change tracker and reduces memory and CPU overhead.

    Recommended patterns:

    | Scenario                         | Recommended usage                                   |
    |:---------------------------------|:----------------------------------------------------|
    | Read only                        | `context.Entities.AsNoTracking().ToList()`          |
    | Read with related data           | `context.Entities.Include(...).AsNoTracking().ToList()` |
    | Read with projection             | `context.Entities.AsNoTracking().Select(...).ToList()` |

    ---

    ## Final notes

    Use logging to inspect the SQL generated by EF Core in development. Properly index columns used in `Where` and `OrderBy` clauses. Group multiple changes and call `SaveChanges()` once to reduce round-trips for write operations.

    Happy coding!

    ````
      modelBuilder.Entity<Cliente>()
          .HasIndex(c => c.Nome);
  }
  ```

---

O uso do Entity Framework (EF) Core com **Injeção de Dependência (ID)** é a forma mais recomendada e padrão em aplicações .NET Core e ASP.NET Core. Ele garante que o seu `DbContext` seja gerenciado corretamente quanto ao seu ciclo de vida (lifetime) e facilita a arquitetura desacoplada.

## ⚙️ 1. Configuração no `Program.cs`

A configuração é feita no arquivo `Program.cs` (ou `Startup.cs` em versões anteriores), utilizando o método de extensão `AddDbContext`.

### ➡️ 1.1. Instalação Necessária

Certifique-se de que tem o pacote correto para a sua base de dados, por exemplo:

```csharp
Microsoft.EntityFrameworkCore.SqlServer // Para SQL Server
Microsoft.EntityFrameworkCore.Sqlite    // Para SQLite
```

### ➡️ 1.2. Registo do Serviço

Utilize `AddDbContext` no contentor de serviços (Service Container). O EF Core cuida de tudo, incluindo o ciclo de vida e a injeção do contexto.

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// 1. Obter a string de conexão do arquivo appsettings.json
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// 2. Registar o DbContext como um serviço Scoped
builder.Services.AddDbContext<SeuContexto>(options =>
    // 3. Configurar o provedor de banco de dados e a string de conexão
    options.UseSqlServer(connectionString)
);

var app = builder.Build();
// ...
```

-----

## ⏳ 2. Ciclo de Vida do `DbContext` (Lifetime)

Ao usar o `AddDbContext`, o EF Core regista o seu contexto por padrão com o ciclo de vida **Scoped** (Escopo).

| Ciclo de Vida       | Descrição                                                                                                                                                                                                                                             |
|:--------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Scoped** (Padrão) | Uma nova instância do `DbContext` é criada para **cada pedido HTTP** (request) em aplicações web. É a opção ideal para a maioria das aplicações, pois garante que o contexto seja isolado por transação de negócio e é descartado ao final do pedido. |
| **Transient**       | Uma nova instância é criada **sempre que é injetada**. Raro de usar para `DbContext`.                                                                                                                                                                 |
| **Singleton**       | Uma única instância é usada durante **toda a vida** da aplicação. **Nunca use** este ciclo de vida para `DbContext`, pois ele não é thread-safe e pode causar problemas de concorrência e rastreamento de alterações.                                 |

### ⚠️ Regra de Ouro

Um `DbContext` deve ser usado para uma **única unidade de trabalho** (ou seja, uma única transação ou pedido) e, em seguida, **descartado**. A injeção de dependência (`Scoped`) lida com este descarte automaticamente, o que evita problemas de concorrência e vazamento de memória.

-----

## 🏗️ 3. Utilização em Classes (Injeção)

Para usar o seu `DbContext` em qualquer classe (como Repositórios, Serviços ou Controladores), basta pedi-lo no construtor. O *Service Container* tratará de fornecer a instância correta (Scoped).

### Exemplo em um Controlador (Controller):

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("[controller]")]
public class AlunosController : ControllerBase
{
    private readonly SeuContexto _contexto;

    // A injeção de dependência fornece a instância do SeuContexto
    public AlunosController(SeuContexto contexto)
    {
        _contexto = contexto;
    }

    [HttpGet]
    public async Task<IActionResult> Get()
    {
        // Uso do DbContext injetado
        var alunos = await _contexto.Alunos
            .AsNoTracking()
            .ToListAsync();

        return Ok(alunos);
    }
}
```

### Exemplo em um Serviço ou Repositório:

Se você usa o padrão Repositório, a injeção acontece de forma semelhante, garantindo que o seu repositório (e o `DbContext` interno) também tenha o ciclo de vida Scoped:

```csharp
// Repositório
public class AlunoRepository : IAlunoRepository
{
    private readonly SeuContexto _contexto;

    public AlunoRepository(SeuContexto contexto) // Injeção aqui
    {
        _contexto = contexto;
    }

    public async Task<List<Aluno>> ObterTodos()
    {
        return await _contexto.Alunos.ToListAsync();
    }
}
```

Ao seguir este método, você garante que o seu código esteja **desacoplado**, **testável** e que o `DbContext` seja gerenciado de forma **eficiente e segura** em termos de concorrência.
