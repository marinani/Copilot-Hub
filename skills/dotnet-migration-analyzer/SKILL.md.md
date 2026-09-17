# Skill: .NET Migration Analyzer & Plano de Migração do ERP

Este documento contém o código-fonte da skill criada e o plano de ação passo a passo para a migração do ERP (projeto EGSAPI e bibliotecas associadas).

---

## Parte 1: Código-fonte da Skill (SKILL.md)

Para referência ou para recriar a skill em outro ambiente, este é o arquivo base que define o comportamento do assistente:

```yaml
---
name: dotnet-migration-analyzer
description: Analisa projetos legados em .NET Framework (.csproj, packages.config, estruturas de pasta) para avaliar impacto, esforço e estratégias de migração para o .NET 8+.
---
```
### .NET Migration Analyzer

Você atua como um Arquiteto de Software Especialista em .NET, focado em modernização de aplicações legadas (.NET Framework 4.x) para o ecossistema moderno (.NET 8+ LTS).

#### Quando Usar
Use esta skill sempre que o usuário fornecer estruturas de projeto (via texto ou imagens), arquivos `.csproj`, `packages.config`, ou pedir uma avaliação de esforço de migração de um sistema .NET.

#### Passos da Análise

1. **Identificar o Stack Legado:**
   - Procure por marcadores legados: `Web.config`, `packages.config`, `Global.asax`, `App_Start/`, `ApiControllers/`, `OdataControllers/`, `Hubs/`.
   - Determine os frameworks utilizados (ASP.NET Web API 2, MVC, SignalR, WCF, Entity Framework 6, OWIN, etc.).

2. **Mapeamento para Padrões Modernos (.NET 8):**
   - `Web.config` -> `appsettings.json` / Configuration API.
   - `packages.config` -> `<PackageReference>` no `.csproj` (SDK-style).
   - `Startup.cs` (OWIN) / `Global.asax` -> `Program.cs` (Minimal hosting model e Injeção de Dependência nativa).
   - ASP.NET Web API (`ApiController`) -> ASP.NET Core Web API (`ControllerBase`).
   - SignalR Legado -> ASP.NET Core SignalR.

3. **Avaliação de Impacto e Esforço:**
   - **Alto Impacto (Reescrita Severa):** WCF para gRPC/Web API, OData v3/v4 para ASP.NET Core OData, Web Forms, SignalR antigo (exige alteração pesada no client/frontend também).
   - **Médio Impacto:** EF6 para EF Core (ajustes em DbContext, Lazy Loading e queries LINQ complexas), migração de middlewares OWIN.
   - **Baixo Impacto:** Regras de negócio puras e Class Libraries (podem ser atualizadas para SDK-style e convertidas para `net8.0` com pouco ou nenhum ajuste no código C#).

4. **Gerar Plano de Ação Estratégico:**
   - Recomende o padrão de migração mais adequado (ex: Big Bang para projetos pequenos; **Padrão Strangler Fig / YARP proxy** para APIs grandes).

#### Formato de Saída (Markdown)
Gere um relatório técnico estruturado com as seguintes seções:
- **Diagnóstico da Arquitetura Atual** (O que foi identificado)
- **Mapa de Migração (De -> Para)** (Tabela de tecnologias)
- **Nível de Esforço e Retrabalho** (Classificado por projeto/camada)
- **Plano de Ação Sugerido** (Fases de execução)

---

## Parte 2: Passo a Passo da Migração (ERP EGS)

Com base na estrutura de projetos identificada (EGSAPI, EGSCORE, EGSFISCAL, EGSINTEGRACOES, etc.), aplique a estratégia **Strangler Fig** utilizando um Proxy Reverso para não interromper a operação do sistema.

### Fase 1: Atualização das Fundações (Bibliotecas de Domínio)
O objetivo desta fase é fazer as bibliotecas de regras de negócio serem consumíveis tanto pela API antiga (4.8) quanto pela nova (8.0).
1. **Converter para SDK-Style:** Utilize a ferramenta `upgrade-assistant` da Microsoft para converter os arquivos `.csproj` antigos dos projetos `EGSCORE`, `EGSFISCAL`, `EGSINTEGRACOES` e `EGSREPORT` para o novo formato `.csproj` enxuto.
2. **Alterar Target Framework:** Mude o `<TargetFramework>` dessas bibliotecas para `netstandard2.0` (se possível) ou para *multi-targeting* (`<TargetFrameworks>net48;net8.0</TargetFrameworks>`).
3. **Substituir packages.config:** O assistente de upgrade trocará o `packages.config` para `<PackageReference>` em todos eles. Resolva conflitos de pacotes de terceiros (como bibliotecas fiscais ou de geração de PDF que não tenham suporte e precisem de substituição).

### Fase 2: Criação do Novo Hub e Proxy (YARP)
1. **Nova Solução/Projeto:** Crie um projeto novo em .NET 8 (ex: `EGSAPI.Core`).
2. **Configuração do Proxy Reverso (YARP):** Instale o pacote `Yarp.ReverseProxy` no novo projeto.
3. **Roteamento:** Configure o `appsettings.json` do YARP. Defina que:
   - Qualquer rota já migrada (ex: `/api/v2/fiscal`) é resolvida na nova API.
   - Qualquer rota desconhecida/antiga (ex: `/api/clientes`, `/odata/...`) faça o proxy pass (redirecionamento silencioso) para o IIS onde roda a `EGSAPI` original em .NET 4.8.
4. **Deploy:** Coloque o novo proxy na frente da infraestrutura atual. A partir deste momento, todas as requisições do frontend batem no .NET 8.

### Fase 3: Migração Cirúrgica das Controllers
1. **Extração de Middlewares:** Migre o código customizado do `Startup.cs` (OWIN) para a pipeline do `Program.cs` moderna.
2. **Controllers Padrão:** Traga um a um os controllers da pasta `ApiControllers` do projeto antigo para o novo.
   - Troque `[RoutePrefix]` por `[Route]`.
   - Troque `ApiController` por `ControllerBase`.
   - Substitua retornos `IHttpActionResult` por `IActionResult`.
3. **Testes de Rota:** Assim que um endpoint estiver funcional no projeto .NET 8, adicione a rota no YARP para que ele intercepte a chamada, removendo a necessidade de ir até o legado.

### Fase 4: Refatoração Complexa (OData e Banco de Dados)
1. **Migração do OData:** Os `OdataControllers` precisam ser ajustados para a sintaxe do ASP.NET Core OData (versão 8+). O `EdmModel` (que provavelmente está no `App_Start` ou `Startup.cs`) deve ser recriado no formato atual.
2. **Entity Framework:** Se você utiliza Entity Framework 6 (EF6), você pode mantê-lo rodando no .NET 8 temporariamente. No entanto, agende a conversão para o Entity Framework Core, o que envolverá adaptar as classes de `DbContext`, `DbSet` e possivelmente reescrever consultas LINQ que dependiam de *Lazy Loading* automático (que não é recomendado no Core).

### Fase 5: WebSockets (SignalR)
1. **Reescrita do Hub:** Os arquivos na pasta `Hubs` devem ser reescritos usando ASP.NET Core SignalR. A sintaxe muda (os pacotes são diferentes).
2. **Atualização do Frontend:** O ASP.NET Core SignalR **exige um cliente novo**. Isso significa que as aplicações web ou desktop que se conectam aos Hubs do seu ERP precisarão ter a biblioteca do cliente (ex: `@microsoft/signalr` no npm) atualizada, forçando uma subida de versão simultânea entre a API e o Client para este módulo específico.

### Fase 6: Descomissionamento
1. Quando o projeto `EGSAPI` original não estiver mais recebendo nenhuma requisição via YARP e todos os testes validarem que o `EGSAPI.Core` (.NET 8) suporta a operação completa.
2. Exclua as pastas `App_Start`, `ApiControllers`, `Hubs`, `OdataControllers` e o projeto original `.NET 4.8` da solução.
3. Desative o modo *multi-targeting* das Class Libraries e deixe tudo como `<TargetFramework>net8.0</TargetFramework>`.
