# Hangfire em C# – Guia Definitivo de Implementação, Performance e Segurança (.NET 6/8/9)

Guia usado em produção por empresas de grande porte no Brasil (bancos, e-commerces, healthtechs, fintechs).

## 1. Configuração Ideal no Program.cs (.NET 8 Top-Level Statements)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// --------------------------
// HANGFIRE – CONFIGURAÇÃO PRODUÇÃO
// --------------------------
builder.Services.AddHangfire((sp, config) =>
{
    var connectionString = builder.Configuration.GetConnectionString("HangfireConnection");

    config.UseSqlServerStorage(connectionString, new SqlServerStorageOptions
    {
        PrepareSchemaIfNecessary = true,
        QueuePollInterval = TimeSpan.FromSeconds(15),
        UseRecommendedIsolationLevel = true,
        DisableGlobalLocks = true // importante para alta concorrência
    });

    // Serialização otimizada
    config.UseRecommendedSerializerSettings();

    // Filtros globais (ver seção completa abaixo)
    config.UseFilter(new AutomaticRetryAttribute { Attempts = 5, DelaysInSeconds = new[] { 60, 300, 900, 1800, 3600 } });
    config.UseFilter(new SerilogLoggingJobFilter());
    config.UseFilter(new OpenTelemetryJobFilter());
    config.UseFilter(new DisableConcurrentExecutionAttribute(1800));
    config.UseFilter(new ThrottlingJobFilter());
});

builder.Services.AddHangfireServer(options =>
{
    options.WorkerCount = Environment.ProcessorCount * 5; // padrão recomendado
    options.Queues = new[] { "critical", "default", "lowpriority" }; // ordem importa
    options.ServerName = $"{Environment.MachineName}:{AppDomain.CurrentDomain.FriendlyName}";
});

// App
var app = builder.Build();

// Dashboard com autenticação forte (exemplo com claims do Identity)
app.UseHangfireDashboard("/hangfire", new DashboardOptions
{
    Authorization = new[] { new HangfireDashboardAuthorizationFilter() },
    IgnoreAntiforgeryToken = true,
    StatsPollingInterval = 5000,
    DashboardTitle = "Jobs – Produção"
});

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();

// --------------------------
// AUTORIZAÇÃO DO DASHBOARD (exemplo com ASP.NET Identity)
// --------------------------
public class HangfireDashboardAuthorizationFilter : IDashboardAuthorizationFilter
{
    public bool Authorize(DashboardContext context)
    {
        var httpContext = context.GetHttpContext();
        return httpContext.User.Identity?.IsAuthenticated == true &&
               httpContext.User.IsInRole("Admin") ||
               httpContext.User.IsInRole("Hangfire.Viewer");
    }
}
```

## 2. Como Enfileirar Jobs (padrão recomendado)

```csharp
// Fire-and-forget
BackgroundJob.Enqueue<IEmailService>(x => x.EnviarConfirmacaoPedido(pedidoId));

// Delayed
BackgroundJob.Schedule<IProcessamentoJob>(x => x.ProcessarArquivos(), TimeSpan.FromHours(2));

// Recorrente (CRON + Timezone Brasil)
RecurringJob.AddOrUpdate<IResumoDiarioJob>(
    "resumo-diario-vendas",
    x => x.GerarResumoDoDia(),
    "0 3 * * *", // todo dia 03:00
    TimeZoneInfo.FindSystemTimeZoneById("America/Sao_Paulo"));

// Continuação
var parentId = BackgroundJob.Enqueue<IImportacaoJob>(x => x.Importar());
BackgroundJob.ContinueJobWith(parentId, () => new NotificarConclusaoJob().Executar(parentId));
```

## 3. Job Padrão de Alta Qualidade (com DI, Scope e Retry)

```csharp
public interface IProcessarPedidosJob
{
    Task ProcessarPendentes(CancellationToken ct = default);
}

[AutomaticRetry(Attempts = 7, DelaysInSeconds = new[] { 60, 300, 900, 1800, 3600, 7200, 14400 })]
[Queue("critical")]
public class ProcessarPedidosJob : IProcessarPedidosJob
{
    private readonly ILogger<ProcessarPedidosJob> _logger;
    private readonly IServiceProvider _provider;

    public ProcessarPedidosJob(ILogger<ProcessarPedidosJob> logger, IServiceProvider provider)
    {
        _logger = logger;
        _provider = provider;
    }

    public async Task ProcessarPendentes(CancellationToken ct = default)
    {
        using var scope = _provider.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        // seu código aqui
    }
}
```

## 4. Filtros Avançados (Production-Ready)

### 4.1 Log Rico com Serilog + LogContext

```csharp
public class SerilogLoggingJobFilter : JobFilterAttribute, IClientFilter, IServerFilter, IElectStateFilter, IApplyStateFilter
{
    // código completo do filtro (ver resposta anterior)
}
```

### 4.2 Bloqueio de Execução Concorrente

```csharp
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public class DisableConcurrentExecutionAttribute : JobFilterAttribute, IElectStateFilter, IApplyStateFilter
{
    // código completo do filtro (ver resposta anterior)
}
```

### 4.3 OpenTelemetry / Tracing Distribuído

```csharp
public class OpenTelemetryJobFilter : JobFilterAttribute, IServerFilter
{
    // código completo do filtro (ver resposta anterior)
}
```

### 4.4 Throttling por Tipo de Job

```csharp
public class ThrottlingJobFilter : JobFilterAttribute, IElectStateFilter
{
    // código completo do filtro (ver resposta anterior)
}

[Throttling(10, 60)] // máximo 10 execuções por minuto
public class EnviarPushJob { ... }
```

### 4.5 Registrar todos os filtros de uma vez

```csharp
GlobalJobFilters.Filters.Add(new AutomaticRetryAttribute { Attempts = 5, DelaysInSeconds = new[] { 60, 300, 900, 1800, 3600 } });
GlobalJobFilters.Filters.Add(new SerilogLoggingJobFilter());
GlobalJobFilters.Filters.Add(new OpenTelemetryJobFilter());
GlobalJobFilters.Filters.Add(new DisableConcurrentExecutionAttribute(1800));
GlobalJobFilters.Filters.Add(new ThrottlingJobFilter());
```

## 5. Dicas de Performance & Operação

| Item                  | Recomendação                                                           |
|-----------------------|------------------------------------------------------------------------|
| WorkerCount           | `Environment.ProcessorCount * 5` (padrão Hangfire)                     |
| QueuePollInterval     | 15 segundos (padrão) → reduzir para 5s se precisar de baixa latência   |
| DisableGlobalLocks    | `true` em SQL Server com alta concorrência                             |
| Filas separadas       | `critical`, `default`, `lowpriority` + servidor dedicado para critical |
| Retenção de histórico | 7 dias sucesso, 30–90 dias falhas                                      |
| Timezone              | Sempre `America/Sao_Paulo` em RecurringJob                             |
| Dashboard em produção | SEMPRE com autenticação forte + IP restrito                            |
| Monitoramento         | Grafana + Prometheus (hangfire_exporter) ou Zabbix                     |
