---
applyTo: '**/*.cs'
description: 'Best Practices for Implementing Unit Tests with xUnit in C# Projects'
---

# Best Practices for Implementing Unit Tests with xUnit in C# Projects

xUnit is an open-source unit testing framework for .NET, known for its simplicity, performance, and support for parallel tests. It is widely used in C# projects and replaces older frameworks like NUnit or MSTest. Below, we explain **how to configure**, **write tests**, and **apply best practices** based on official Microsoft documentation and xUnit guidelines.

## 1. Initial Configuration of a Test Project

Create a test project alongside your main project:

```bash
dotnet new classlib -n MyProject.Tests
cd MyProject.Tests
dotnet add reference ../MyProject/MyProject.csproj
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
dotnet add package coverlet.collector  # For coverage reports (optional)
```

- **Recommended structure**: Separate unit test projects from integration tests.
- In `MyProject.Tests.csproj`, add:
  ```xml
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.10.0" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.9.2" />
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
  </ItemGroup>
  ```

Run tests with:

```bash
dotnet test
```

## 2. Writing Basic Tests

### Simple Test with `[Fact]`

Tests that run once, without parameters.

```csharp
public class CalculatorTests
{
    [Fact(DisplayName = "Add two numbers returns their sum")]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        var calc = new Calculator();

        // Act
        var result = calc.Add(2, 3);

        // Assert
        Assert.Equal(5, result);
    }
}
```

### Parameterized Tests with `[Theory]` and `[InlineData]`

Ideal for multiple scenarios in one method.

```csharp
[Theory(DisplayName = "Add various cases returns correct sum")]
[InlineData(2, 3, 5)]
[InlineData(0, 0, 0)]
[InlineData(-1, 1, 0)]
public void Add_VariousCases_ReturnsCorrectSum(int a, int b, int expected)
{
    // Arrange
    var calc = new Calculator();

    // Act
    var result = calc.Add(a, b);

    // Assert
    Assert.Equal(expected, result);
}
```

**Common assertions**:

- `Assert.Equal(expected, actual)`
- `Assert.True(condition)`
- `Assert.Throws<Exception>(() => method())`
- `Assert.NotNull(object)`

## 3. AAA (Arrange-Act-Assert) Pattern

**Mandatory** for readability:

- **Arrange**: Set up objects and dependencies.
- **Act**: Execute the tested method (only once!).
- **Assert**: Verify the result.

## 4. Essential Best Practices

Use this table as a checklist:

| Practice                  | Description                                                                             | Example/Benefit                                                                                       |
|---------------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Clear Naming**          | `Method_Scenario_Expected`                                                              | `Add_PositiveNumbers_ReturnsSum` – Serves as documentation.                                           |
| **Isolated Tests**        | No external dependencies (DB, files). Use mocks.                                        | Avoids false negatives.                                                                               |
| **Fast**                  | < 1ms per test.                                                                         | Allows frequent execution.                                                                            |
| **Independent**           | Order doesn't matter; runs in parallel.                                                 | xUnit runs in parallel by default.                                                                    |
| **Focused**               | One behavior per test.                                                                  | Use `[Theory]` for variations.                                                                        |
| **No Logic**              | Avoid `if`, loops in tests.                                                             | Split into smaller tests.                                                                             |
| **No Magic Strings**      | Use `const string` or enums.                                                            | `const string AdminUser = "admin";`                                                                   |
| **Smart Coverage**        | Focus on critical paths, not 100%.                                                      | Use `dotnet test --collect:"XPlat Code Coverage"`.                                                    |
| **Async Tests**           | Use `async Task` with `[Fact]`.                                                         | `await Assert.ThrowsAsync<Exception>(...)`                                                            |
| **DisplayName Mandatory** | Include DisplayName with brief description of what is being tested and expected result. | `[Fact(DisplayName = "Add two numbers returns their sum")]` – Improves readability and documentation. |

### 4.1 Importance of Testing Success and Failures

It is important to make clear that it is crucial to test both success scenarios and failure cases to ensure all use cases are covered. This includes positive paths, edge cases, and error conditions, ensuring robustness and reliability of the code.

### 4.2 Generating Test Cases with Exploratory Method

When creating use cases, it is important to use an exploratory method to generate these tests. This involves brainstorming possible inputs, outputs, and edge cases based on the requirements, rather than just following a checklist, promoting more comprehensive and creative coverage.

## 5. Shared Contexts (Fixtures)

Avoid expensive setup in each test. Use **IClassFixture**, **ICollectionFixture**, or **AssemblyFixture**.

```csharp
public class DatabaseFixture : IDisposable
{
    public SqlConnection Db { get; }

    public DatabaseFixture()
    {
        Db = new SqlConnection("...");
        // Setup data
    }

    public void Dispose() => Db.Dispose();
}

[CollectionDefinition("Database")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("Database")]
public class UserTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public UserTests(DatabaseFixture fixture) => _fixture = fixture;

    [Fact] public void Test() { /* Use _fixture.Db */ }
}
```

## 6. Mocking with Moq (External Dependencies)

Add `dotnet add package Moq`.

```csharp
[Fact(DisplayName = "Calculate price with discount uses external service")]
public void Calculate_Price_WithDiscount_UsesExternalService()
{
    // Arrange
    var mockDiscount = new Mock<IDiscountService>();
    mockDiscount.Setup(x => x.GetDiscount(It.IsAny<decimal>())).Returns(0.1m);
    var calc = new Calculator(mockDiscount.Object);

    // Act
    var price = calc.CalculatePrice(100m);

    // Assert
    Assert.Equal(90m, price);
    mockDiscount.Verify(x => x.GetDiscount(100m), Times.Once);
}
```

## 7. Async Tests and DI

```csharp
[Fact(DisplayName = "GetDataAsync returns a list of items")]
public async Task GetDataAsync_ReturnsList()
{
    // Arrange
    var service = new MyService();

    // Act
    var result = await service.GetDataAsync();

    // Assert
    Assert.NotEmpty(result);
}
```

For Dependency Injection in tests:

```csharp
// Add Microsoft.Extensions.DependencyInjection
var services = new ServiceCollection();
services.AddScoped<IMyService, MyService>();
var provider = services.BuildServiceProvider();
var service = provider.GetRequiredService<IMyService>();
```

## 8. Execution and Analysis

- **VS Code / Rider / VS**: `dotnet test` or extension.
- **Coverage**: `dotnet test --collect:"XPlat Code Coverage"` → Open `coverage.cobertura`.
- **CI/CD**: Integrate into GitHub Actions / Azure DevOps.

## Final Tips

- **Write tests BEFORE code** (TDD) for better design.
- **Maintain >80% coverage**, but prioritize quality.
- **Refactor tests** like production code.
- Resources: [xunit.net](https://xunit.net/), [MS Docs](https://learn.microsoft.com/en-us/dotnet/core/testing/).

Following these practices, your tests will be **reliable, fast, and easy to maintain**! If you need specific examples from your project, provide the code.
