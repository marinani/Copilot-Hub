---
description: API Documentation for swagger.
---

# Swagger/OpenAPI Documentation

## Summary

This document explains what Swagger/OpenAPI is, how to configure it in ASP.NET Core projects (Controllers and Minimal APIs), how to secure the API with JWT Bearer, and how to integrate Swagger UI for interactive testing. It includes practical examples, advanced configurations, and a new section with Best Practices for team usage and CI.

**Quick Overview**

- Swagger = a set of tools for working with the OpenAPI specification.
- OpenAPI = a specification (YAML/JSON) that describes your API (endpoints, parameters, responses).
- Swagger UI = an interactive interface that consumes the OpenAPI document.

---

## 1. Installation (Swashbuckle)

The recommended package for ASP.NET Core is `Swashbuckle.AspNetCore`.

Install it with:

```bash
dotnet add package Swashbuckle.AspNetCore
```

---

## 2. Basic Configuration (Controllers)

In `Program.cs` (apps .NET 6+), register the services before `builder.Build()` and configure the middleware in the pipeline.

Minimal example:

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "My Example API",
        Version = "v1",
        Description = "A demonstration API using ASP.NET Core and Swagger."
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "My API v1");
        c.RoutePrefix = string.Empty; // Serve at /
    });
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();
```

> Tip: Avoid exposing Swagger UI in production without authentication.

---

## 3. Configuration for Minimal APIs

Minimal APIs concentrate configuration in `Program.cs`. Ensure you call `.WithOpenApi()` for each endpoint you want to document.

Example:

```csharp
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "Task Minimal API", Version = "v1", Description = "Simple task management." });
});

var app = builder.Build();
if (app.Environment.IsDevelopment()) { app.UseSwagger(); app.UseSwaggerUI(c => { c.SwaggerEndpoint("/swagger/v1/swagger.json", "Minimal API v1"); c.RoutePrefix = string.Empty; }); }

app.UseHttpsRedirection();

app.MapGet("/tasks", () => Results.Ok(new[] { new Task(1, "Configure Swagger", true) }))
   .WithName("GetAllTasks")
   .WithOpenApi();

app.MapGet("/tasks/{id}", (int id) => id == 0 ? Results.NotFound() : Results.Ok(new Task(id, $"Task {id}", true)))
   .WithName("GetTaskById")
   .WithOpenApi(operation =>
   {
       operation.Summary = "Fetch a specific task by ID.";
       operation.Responses.Add("404", new Microsoft.OpenApi.Models.OpenApiResponse { Description = "Task not found." });
       return operation;
   });

app.Run();

public record Task(int Id, string Name, bool Completed);
```

---

## 4. XML Comments and Model Documentation

Enable XML file generation in `.csproj` so that Swashbuckle includes `///` comments in the spec:

```xml
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
```

In `Program.cs` (inside `AddSwaggerGen`), load the generated XML file:

```csharp
var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
if (File.Exists(xmlPath)) c.IncludeXmlComments(xmlPath);
```

Example usage in controllers and models (`///` comments and attributes like `<example>` are reflected in the spec):

```csharp
/// <summary>
/// Represents a product in the system.
/// </summary>
public class Product
{
    /// <summary>Unique identifier.</summary>
    public int Id { get; set; }

    /// <summary>Product name.</summary>
    /// <example>Laptop X</example>
    public required string Name { get; set; }

    /// <summary>Unit price.</summary>
    /// <example>1999.99</example>
    public decimal Price { get; set; }
}
```

---

## 5. Documenting Responses (Controllers)

Use `[ProducesResponseType]` to describe HTTP status codes and returned types:

```csharp
[HttpGet("{id}")]
[ProducesResponseType(StatusCodes.Status200OK, Type = typeof(Product))]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public ActionResult<Product> Get(int id)
{
    if (id == 0) return NotFound();
    return Ok(new Product { Id = id, Name = "Example", Price = 0 });
}
```

---

## 6. Securing the API with JWT Bearer and Integrating with Swagger UI

Install the authentication package:

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

Add authentication configuration in `Program.cs`:

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Jwt:Audience"],
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"] ?? throw new InvalidOperationException("Jwt:Key not configured.")))
        };
    });
builder.Services.AddAuthorization();

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
```

To enable the `Authorize` field in Swagger UI, add the following to `AddSwaggerGen`:

```csharp
using Microsoft.OpenApi.Models;

builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "My Protected API", Version = "v1" });

    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        In = ParameterLocation.Header,
        Description = "Enter JWT in the format: Bearer {token}",
        Name = "Authorization",
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" },
                Scheme = "oauth2",
                Name = "Bearer",
                In = ParameterLocation.Header,
            }, new List<string>()
        }
    });
});
```

After this, the "Authorize" button will appear in Swagger UI.

---

## 7. Quick Practical Examples

- Controllers: use `AddSwaggerGen`, `UseSwagger`, `UseSwaggerUI`, XML comments, and `[ProducesResponseType]`.
- Minimal APIs: ensure `.WithOpenApi()` and use `operation` to add extra descriptions and responses.

---

## 8. Best Practices for Using Swagger/OpenAPI

- **API Versioning:** Always version the document (`/swagger/v1/swagger.json`) and use consistent `operationId` to facilitate tracking and client generation.
- **Do not expose in production without protection:** Block Swagger UI in public environments or require authentication/ACL for the documentation environment.
- **Keep the spec under version control:** Generate and validate the OpenAPI file from code and commit the resulting YAML/JSON when appropriate.
- **Lint and CI:** Use tools like `spectral` to validate rules (naming, descriptions, examples) and run as a CI step.
- **Real examples:** Include examples (`example`/`examples`) in request/response to facilitate testing and mock generation.
- **Avoid sensitive data:** Do not include secrets, credentials, or sensitive data samples in descriptions or examples.
- **Document errors:** Provide schemas and examples for error responses (400/401/403/500) so consumers know how to handle failures.
- **Consistency:** Standardize parameter names, status codes, and model structures; create style guides for your organization.
- **Generate clients/servers carefully:** When using codegen, review the generated code and maintain explicit type mappings when necessary.
- **Use `tags` to group endpoints:** Helps navigate Swagger UI and organize the contract.
- **Monitor changes and compatibility:** Have a process to manage breaking changes—use semver and changelogs for the schema.
- **Support OAuth2/OpenID Connect:** When using OAuth2 flows, properly configure `AddSecurityDefinition` to allow authenticated tests in the UI.

---

## 9. Quick References

- Swashbuckle: https://github.com/domaindrivendev/Swashbuckle.AspNetCore
- OpenAPI Spec: https://spec.openapis.org
- Spectral (lint): https://github.com/stoplightio/spectral

---

## 10. Suggested Next Steps

- Add a CI step to validate the spec with `spectral`.
- Generate real examples from integrated tests and attach them to the OpenAPI document.

```csharp
// Example POST
app.MapPost("/tasks", (Task newTask) =>
{
    // Logic to save the task...
    return Results.Created($"/tasks/{newTask.Id}", newTask);
})
.WithName("CreateTask")
.WithOpenApi();

app.Run();

// Data Model
public record Task(int Id, string Name, bool Completed);
```

### Key Details for Minimal APIs

1.  **`AddEndpointsApiExplorer()`**: This service must be registered for the application to know how to expose the endpoints defined by the `Map*` method.
2.  **`.WithOpenApi()`**: This is the magic method for Minimal APIs. It is an extension that instructs Swashbuckle to generate the OpenAPI (Swagger) document information for that specific endpoint. **Without it, the endpoint will not appear in the Swagger documentation.**
3.  **`.WithName()`**: Although not strictly required for Swagger to function, it provides a friendlier operation name, which is useful for documentation and code generation.

### How to Document Responses and Types in Minimal APIs

Since we are not in controller classes with attributes like `[ProducesResponseType]`, we use extension methods in the endpoint definition:

```csharp
// Example of GET with documented HTTP responses
app.MapGet("/tasks/{id}", (int id) =>
{
    if (id == 0)
    {
        return Results.NotFound();
    }
    return Results.Ok(new Task(id, $"Task {id}", true));
})
.WithName("GetTaskById")
.WithOpenApi(operation =>
{
    // Add a summary for the endpoint
    operation.Summary = "Fetch a specific task by ID.";

    // Configure specific HTTP responses
    var response200 = operation.Responses["200"]; // Get the default 200 response
    response200.Description = "Task found successfully.";

    // Adds a new response (404)
    operation.Responses.Add("404", new OpenApiResponse { Description = "Task not found." });

    return operation;
});
```

## Adding JWT (JSON Web Token) Bearer Authentication to Protect RESTful APIs.

This involves two main parts:

1.  **Configuring the API:** Telling ASP.NET Core how to validate and accept a JWT.
2.  **Configuring the Swagger UI:** Adding a field in the documentation interface for the user to enter the token and test the protected endpoints.

---

### 🔑 1. API Configuration (Both Types)

The main authentication configuration is the same for Controllers and Minimal APIs. You will need to install a package and configure `Program.cs`.

### Step 1: Install the Package

You will need the package to enable JWT Bearer authentication:

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

### Step 2: Configure `Program.cs`

In your `Program.cs` file, add the necessary configuration before `builder.Build()`.

```csharp
// Program.cs

using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// ... (Other services like AddControllers or AddEndpointsApiExplorer) ...

// 1. ADD AUTHENTICATION AND AUTHORIZATION SERVICES
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            // The server (API) that issued the token
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],

            // The client (Application) that can consume the token
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Jwt:Audience"],

            // The security key
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"] ??
                throw new InvalidOperationException("Jwt:Key not configured."))
            )
        };
    });

builder.Services.AddAuthorization();

var app = builder.Build();

// ... (Swagger middleware) ...

// 2. USE AUTHENTICATION AND AUTHORIZATION MIDDLEWARES
// Must come before app.MapControllers() or app.Map*
app.UseAuthentication();
app.UseAuthorization();

// ... (Endpoint mapping) ...

app.Run();
```

> **Note:** Make sure to have the `Jwt:Issuer`, `Jwt:Audience`, and `Jwt:Key` settings in your `appsettings.json` file (or environment variables).

## 🚀 2. Swagger UI Configuration (Both Types)

To have Swagger UI display a field to enter the token, you need to configure `AddSwaggerGen` to describe the security scheme.

### Step 1: Configure `AddSwaggerGen`

Add the security logic inside `AddSwaggerGen` in `Program.cs`:

```csharp
// Program.cs

// ... (usings) ...
using Microsoft.OpenApi.Models; // Necessary for OpenApiSecurityScheme

// ... (inside builder.Services.AddSwaggerGen) ...

builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "My Protected API", Version = "v1" });

    // 🔑 SECURITY CONFIGURATION IN SWAGGER
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        In = ParameterLocation.Header,
        Description = "Enter JWT in the format: Bearer {token}",
        Name = "Authorization",
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                },
                Scheme = "oauth2",
                Name = "Bearer",
                In = ParameterLocation.Header,
            },
            new List<string>()
        }
    });
});
```

With this configuration, Swagger UI will have an **"Authorize"** button in the top right corner, where the user can paste the JWT token.

---

## 🎯 3. Applying Protection to Endpoints

Finally, you need to apply the `[Authorize]` attribute to the endpoints you want to protect.

### Example 1: Web API (Controllers)

Use the `[Authorize]` attribute on the controller class or specific methods:

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

[Route("api/[controller]")]
[ApiController]
[Authorize] // 🔒 Protects all endpoints in this controller
public class ValuesController : ControllerBase
{
    // This endpoint will require a valid token
    [HttpGet]
    public IEnumerable<string> Get()
    {
        return new string[] { "value1", "value2", "protected" };
    }

    // You can have public endpoints in the same class by removing [Authorize] from the controller
    [HttpGet("public")]
    [AllowAnonymous] // Allows access without authentication
    public string GetPublic()
    {
        return "This endpoint is public.";
    }
}
```

### Example 2: Minimal API

Use the `.RequireAuthorization()` extension method:

```csharp
// Program.cs

// ... (after app.UseAuthorization()) ...

// 🔒 Protected Endpoint
app.MapGet("/protecteddata", () =>
{
    return "This is data accessed via JWT Bearer.";
})
.RequireAuthorization() // 🔒 Requires the request to be authenticated
.WithOpenApi();

// Public Endpoint
app.MapGet("/publicdata", () =>
{
    return "This is public data.";
})
.WithOpenApi();
```
