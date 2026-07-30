# Copilot Hub — Referência de Skills

Este documento lista todas as GitHub Copilot Agent Skills disponíveis neste repositório, com uma breve descrição de cada uma e um exemplo de como invocá-las.

---

## Índice por Categoria

- [🗂️ Planejamento](#️-planejamento)
- [🔍 Análise & Discovery](#-análise--discovery)
- [💻 Desenvolvimento](#-desenvolvimento)
- [🗄️ Banco de Dados & Tuning](#️-banco-de-dados--tuning)
- [🧪 Testes](#-testes)
- [📝 Documentação](#-documentação)
- [🤖 IA & Agentes](#-ia--agentes)
- [☁️ Infraestrutura & Cloud](#️-infraestrutura--cloud)
- [🔧 DevOps & Git](#-devops--git)
- [⚙️ Workflow & Produtividade](#️-workflow--produtividade)

---

## 🗂️ Planejamento

### architecture

Framework para tomada de decisão arquitetural cobrindo análise de requisitos, avaliação de trade-offs, seleção de padrões e documentação de ADRs. Use ao definir ou documentar decisões de design de sistemas.

**Como usar:**
> Me ajude a decidir a arquitetura para uma nova plataforma SaaS multi-tenant e documente a decisão.

---

### architecture-blueprint-generator

Analisa uma codebase e gera um documento abrangente `Project_Architecture_Blueprint.md` com stack tecnológica auto-detectada, padrões arquiteturais, diagramas C4/UML e padrões de implementação.

**Como usar:**
> Gere um blueprint de arquitetura para esta codebase .NET Clean Architecture.

---

### behavioral-modes

Define modos operacionais distintos para a IA (`BRAINSTORM`, `IMPLEMENT`, `DEBUG`, `REVIEW`, `TEACH`, `SHIP`, `ORCHESTRATE`) que adaptam o comportamento, o estilo de comunicação e as prioridades conforme o tipo de tarefa.

**Como usar:**
> Entre no modo BRAINSTORM para explorar opções de arquitetura para o meu novo microsserviço.

---

### brainstorming

Protocolo socrático que exige perguntas de esclarecimento antes de implementar requisitos complexos ou vagos. Garante pelo menos 3 perguntas sobre propósito, usuários e escopo antes de escrever qualquer código.

**Como usar:**
> Quero construir um sistema de notificações — me ajude a pensar nos requisitos primeiro.

---

### copilot-planning

Planejamento de execução estruturado usando waves (macro-fases), batches (ações incrementais) e fluxo waveless para tarefas pequenas. Inclui histórico persistente no diretório `planning/`, checklists e checkpoints anti-alucinação.

**Como usar:**
> Planeje a implementação do novo módulo de pagamentos usando waves e batches.

---

### gen-specs-as-issues

Guia um fluxo sistemático para identificar funcionalidades ausentes via análise de gap, priorizá-las com uma matriz de pontuação e criar GitHub Issues detalhadas com especificações para implementação.

**Como usar:**
> Analise este projeto, encontre funcionalidades faltantes e crie GitHub Issues com especificações.

---

### tdd-workflow

Fluxo de Desenvolvimento Orientado a Testes seguindo o ciclo RED-GREEN-REFACTOR e as três leis do TDD, com princípios para cada fase, convenções de nomenclatura de testes e anti-padrões a evitar.

**Como usar:**
> Me guie pela implementação de uma nova funcionalidade usando o fluxo TDD.

---

## 🔍 Análise & Discovery

### agentic-eval

Padrões para avaliar e melhorar iterativamente as saídas de agentes de IA por meio de autocrítica, loops de reflexão, pipelines avaliador-otimizador e rubricas LLM-as-judge. Vai além da geração única para refinamento iterativo.

**Como usar:**
> Configure um loop avaliador-otimizador para melhorar a qualidade do código gerado pelo meu agente.

---

### autoresearch

Loop de experimentação iterativa autônoma para qualquer tarefa de programação. Define metas e métricas mensuráveis e executa um ciclo autônomo de alterações de código, testes, medições e aceitação ou descarte dos resultados — inspirado no autoresearch do Karpathy.

**Como usar:**
> Otimize autonomamente o tempo de execução do meu pipeline de processamento de dados usando autoresearch.

---

### code-archeologist

Realiza investigação e documentação profunda de uma codebase existente, produzindo um artefato de conhecimento estruturado cobrindo arquitetura, fluxos de dados, validações, integrações e padrões de design — detalhado o suficiente para reproduzir o sistema do zero.

**Como usar:**
> Mapeie esta codebase legada e documente como o fluxo de autenticação funciona de ponta a ponta.

---

### code-exemplars-blueprint-generator

Gera um prompt que escaneia a codebase para identificar exemplos de código de alta qualidade e produz um arquivo `exemplars.md`. Suporta .NET, Java, JavaScript, TypeScript, React, Angular e Python com profundidade e categorização configuráveis.

**Como usar:**
> Gere um exemplars.md identificando os melhores padrões de código neste projeto .NET.

---

### datanalysis-credit-risk

Pipeline de limpeza de dados e triagem de variáveis para modelagem de risco de crédito pré-empréstimo. Cobre análise de valores ausentes, filtragem IV/PSI, denoising por Null Importance, remoção de alta correlação e geração de relatório de limpeza.

**Como usar:**
> Execute o pipeline de limpeza de dados de risco de crédito no meu dataset de empréstimos e gere o relatório.

---

### dotnet-design-pattern-review

Revisa código C#/.NET quanto à implementação de padrões de design (Command, Factory, DI, Repository, Provider) e fornece sugestões de melhoria sem modificar o código.

**Como usar:**
> Revise esta camada de serviços C# quanto à aderência a padrões de design e violações de SOLID.

---

### eval-driven-dev

Instrumenta aplicações Python com LLM, constrói datasets dourados, escreve testes baseados em avaliação, os executa e identifica a causa raiz das falhas — cobrindo o ciclo completo de desenvolvimento orientado a avaliação para apps de IA.

**Como usar:**
> Configure um pipeline de avaliação para o meu chatbot Python para medir e acompanhar a qualidade das respostas.

---

### folder-structure-blueprint-generator

Analisa um projeto e gera um `Project_Folders_Structure_Blueprint.md` abrangente documentando organização de pastas, convenções de nomenclatura, padrões de posicionamento de arquivos e templates de extensão. Auto-detecta .NET, Java, React, Angular, Python, Node.js e Flutter.

**Como usar:**
> Gere um blueprint de estrutura de pastas para este projeto React/TypeScript.

---

### performance-profiling

Princípios de profiling de performance com um fluxo de 4 etapas (baseline, identificar, corrigir, validar), metas de Core Web Vitals (LCP, INP, CLS) e auditoria automatizada via Lighthouse.

**Como usar:**
> Faça o profiling de performance da minha aplicação web em <https://localhost:3000> e identifique gargalos.

---

### project-workflow-analysis-blueprint-generator

Gera documentação detalhada para fluxos de aplicação de ponta a ponta, auto-detectando arquitetura e stack tecnológica, produzindo diagramas de sequência, fluxos de camada de serviço e padrões de testes como templates de implementação.

**Como usar:**
> Documente o fluxo de ponta a ponta do endpoint de criação de pedido neste projeto .NET.

---

### technology-stack-blueprint-generator

Analisa uma codebase para gerar um `Technology_Stack_Blueprint.md` abrangente documentando todas as tecnologias com versões, licenças, padrões de uso, convenções de codificação e diagramas de arquitetura. Suporta .NET, Java, React, Angular e Python.

**Como usar:**
> Gere um blueprint da stack tecnológica para este projeto React/Node.js.

---

### discoverytoolkit

Pacote de discovery em múltiplas etapas para sistemas legados, organizado em roteadores por domínio: fundação, banco, fluxos, pendências, interface, backend EJB, consolidação e exportação. O objetivo é produzir documentação rastreável e navegável do sistema (telas, fluxos, regras, dados e artefatos de apoio).

Módulos do pacote:

- discovery-01-fundacao (planejamento, índice e bootstrap)
- discovery-10-banco e discovery-12-banco-rotinas (schema, status/enums, rotinas e SPs)
- discovery-40-interface (catálogo e documentação de telas)
- discovery-50-backend-ejb (catálogo e documentação de EJBs)
- discovery-20-fluxos (catálogo e documentação industrial de fluxos)
- discovery-80-consolidacao (matriz cruzada entre fluxos, telas, endpoints e tabelas)
- discovery-30-pendencias e discovery-99-exportacao (pendências e exportações)

**Como usar:**
> Execute o discoverytoolkit completo em sequência: fundação, banco, interface/backend, fluxos, consolidação e exportação.

Exemplos rápidos:

- executar a fundação
- executar o discovery banco
- executar os fluxos
- Rode o pipeline discovery-99-exportacao completo

---

## 💻 Desenvolvimento

### api-patterns

Princípios e tomada de decisão de design de API cobrindo seleção de REST vs GraphQL vs tRPC, formatos de resposta, versionamento, paginação, autenticação, rate limiting e testes de segurança (OWASP API Top 10).

**Como usar:**
> Me ajude a decidir entre REST e GraphQL para minha nova API backend e desenhe o formato de resposta.

---

### app-builder

Orquestrador principal de construção de aplicações que cria aplicações full-stack a partir de requisições em linguagem natural. Detecta o tipo de projeto, seleciona a stack tecnológica adequada e coordena agentes usando um dos 12 templates de projeto disponíveis.

**Como usar:**
> Construa uma aplicação web SaaS com Next.js e pagamentos com Stripe.

---

### aspnet-minimal-api-openapi

Guia a criação de endpoints ASP.NET Minimal API bem estruturados com documentação OpenAPI/Swagger adequada usando o suporte nativo do .NET 9, typed results e validação.

**Como usar:**
> Crie um endpoint Minimal API para gerenciamento de produtos com documentação OpenAPI completa.

---

### clean-code

Padrões de codificação pragmáticos enfatizando código conciso, direto e focado em soluções. Cobre SRP, DRY, KISS, YAGNI, convenções de nomenclatura, regras de funções e anti-padrões para evitar over-engineering.

**Como usar:**
> Revise meu código em busca de violações de clean code e sugira melhorias.

---

### containerize-aspnet-framework

Cria um Dockerfile personalizado para containerizar uma aplicação ASP.NET .NET Framework em um container Windows Docker. Gerencia configuração do IIS, seleção de SKU do Windows Server e etapas de build.

**Como usar:**
> Containerize minha aplicação ASP.NET 4.8 usando Windows Server Core 2022.

---

### containerize-aspnetcore

Cria um Dockerfile personalizado para containerizar uma aplicação ASP.NET Core (.NET) em um container Linux Docker seguindo boas práticas de segurança e performance.

**Como usar:**
> Containerize minha aplicação ASP.NET Core 8 usando uma imagem base Alpine Linux.

---

### csharp-async

Boas práticas para programação assíncrona em C# incluindo convenções de nomenclatura, tipos de retorno, tratamento de exceções, padrões de performance (`Task.WhenAll`, cancellation tokens) e armadilhas comuns a evitar.

**Como usar:**
> Revise meu código C# em busca de anti-padrões de async/await e sugira melhorias.

---

### csharp-docs

Garante que tipos e membros C# estejam documentados com comentários XML corretos seguindo os padrões de documentação da Microsoft, cobrindo summaries, params, returns, exceptions e examples.

**Como usar:**
> Adicione comentários de documentação XML a todos os membros públicos desta classe C#.

---

### csharp-mcp-server-generator

Gera um projeto MCP server completo em C# com tools, prompts, configuração de DI via Host builder, logging em stderr e atributos MCP adequados usando o pacote NuGet `ModelContextProtocol`.

**Como usar:**
> Gere um MCP server em C# com tools para leitura e escrita de arquivos.

---

### designer

Orquestrador sênior de UX/UI para design web e mobile completo cobrindo design systems, protótipos, componentes de layout, auditorias de acessibilidade e handoff Penpot/Figma, com perguntas sequenciais interativas e auditoria visual contínua.

**Como usar:**
> Revise e melhore o design de UI da minha página de dashboard para acessibilidade e consistência.

---

### huashu-design

**花叔Design** — Skill de design profissional com HTML para criar protótipos hi-fi, demonstrações interativas, animações, slides de apresentação, infográficos e exploração de variações de design. HTML é ferramenta, não o meio final — a skill adapta a abordagem conforme a tarefa, incorporando especialistas diferentes (UX Designer / Animador / Designer de Slides / Prototipador) e evitando clichês de AI slop.

**Principais capacidades**:

- **Protótipos Interativos**: mockups de alta fidelidade onde usuários podem clicar, navegar e sentir o fluxo real
- **Exploração de Variações**: comparar múltiplas direções de design lado a lado, com tweaks em tempo real para ajustar parâmetros
- **Demos de Animação**: motion design baseado em timeline para material de vídeo ou apresentações conceituais (exportação MP4/GIF otimizada)
- **Slides HTML**: decks em 1920×1080 de alta qualidade que funcionam como PPT
- **Consultor de Direção**: quando o usuário é indeciso, recomenda 3 direções diferenciadas de 20 filosofias de design (Pentagram, Kenya Hara, Field.io, Sagmeister, etc.)
- **Protocolo de Ativos**: busca e integra logo, imagens do produto, screenshots de UI, cores e fontes reais de marcas para evitar design genérico
- **Anti-AI Slop**: cria design reconhecível e profissional, não a "média do corpus de treinamento"

**Quando usar**: protótipos de produtos, exploração de variações visuais, animações de lançamento, decks de apresentação, infográficos, mockups de app iOS/Android, demonstrações conceituais. **Quando NÃO usar**: web apps de produção com backend dinâmico, sites de SEO, sistemas que precisam de servidor.

**Como usar (Protótipo Interativo):**
> Faça um protótipo hi-fi de um app de gestão de tarefas tipo Todoist. Use tons de azul e branco, com interações de clique entre telas. Quero poder clicar em "Adicionar tarefa" e ver uma modal aparecer.

**Como usar (Exploração de Variações):**
> Me mostre 3 variações visuais para a página inicial de um marketplace de cursos online: uma clean/minimalista, outra moderna/ousada com gradientes, e outra com mais tipografia e cores quentes.

**Como usar (Animação):**
> Crie uma animação de lançamento de 10 segundos para o novo iPhone 16 Pro. Use o logotipo da Apple, imagens do produto em rotação 3D estilizada, e transições suaves com música cinética de fundo. Exporte como MP4 60fps.

**Como usar (Consultor de Direção):**
> Não tenho certeza do estilo visual para minha marca pessoal de design. Me recomenda 3 direções bem diferentes — mostre exemplos em paralelo para eu escolher.

**Como usar (Apresentação em Slides):**
> Crie 5 slides de apresentação sobre "Tendências de Design 2026". Cada slide com layout profissional, tipografia clara, dados/gráficos visuais. Estilo corporativo moderno com paleta azul + branco + accent laranja.

---

### dotnet-best-practices

Garante que o código .NET/C# atenda às boas práticas do projeto incluindo documentação XML, DI com primary constructor, padrão Command Handler, `ResourceManager`, async/await, MSTest com FluentAssertions e Moq.

**Como usar:**
> Revise este código C# e garanta que ele segue as boas práticas .NET para este projeto.

---

### dotnet-upgrade

Fornece prompts prontos para análise e execução abrangente de upgrade de .NET Framework, cobrindo classificação de projetos, compatibilidade de dependências, sequenciamento de upgrade, modernização de código, gestão de NuGet e atualização de pipelines CI/CD.

**Como usar:**
> Analise minha solução .NET Framework 4.8 e planeje o upgrade para .NET 8.

---

### ef-core

Boas práticas para Entity Framework Core cobrindo design do DbContext, relacionamentos entre entidades, performance (`AsNoTracking`, eager loading, compiled queries), migrations, padrões de consulta e como evitar problemas N+1.

**Como usar:**
> Revise meu DbContext e queries EF Core em busca de anti-padrões de performance.

---

### fluentui-blazor

Guia para usar corretamente o pacote NuGet `Microsoft.FluentUI.AspNetCore.Components` (v4) em aplicações Blazor, cobrindo providers obrigatórios, registro de serviços, uso de componentes, theming e JS interop.

**Como usar:**
> Me ajude a configurar o Fluent UI Blazor na minha aplicação Blazor Server com FluentDialog e FluentToast.

---

### i18n-localization

Padrões de internacionalização e localização cobrindo detecção de strings hardcoded, gerenciamento de traduções, arquivos de locale, suporte a RTL e padrões de implementação para React (react-i18next) e Next.js (next-intl).

**Como usar:**
> Adicione suporte a i18n na minha aplicação React e detecte todas as strings hardcoded que precisam de tradução.

---

### microsoft-agent-framework

Cria, atualiza, refatora e revisa soluções Microsoft Agent Framework em .NET ou Python. Fornece orientação sobre agentes, workflows, uso de tools, integração com MCP e migração a partir do Semantic Kernel ou AutoGen.

**Como usar:**
> Crie um workflow .NET com Microsoft Agent Framework com uma etapa de aprovação human-in-the-loop.

---

### microsoft-code-reference

Consulta referências de API da Microsoft, encontra exemplos de código funcionais e verifica a correção do código SDK usando o Microsoft Learn MCP Server. Detecta métodos alucinados, assinaturas erradas e padrões deprecados.

**Como usar:**
> Encontre a assinatura correta do método para fazer upload de blob com managed identity em Azure.Storage.Blobs.

---

### refactor

Refatoração cirúrgica de código para melhorar a manutenibilidade sem alterar o comportamento externo. Cobre extração de funções, renomeação de variáveis, decomposição de god functions, eliminação de code smells e aplicação incremental de padrões de design.

**Como usar:**
> Refatore esta classe controller grande para melhorar legibilidade e separação de responsabilidades.

---

### review-and-refactor

Revisa todas as diretrizes de codificação em `.github/instructions/*.md` e `.github/copilot-instructions.md`, e refatora o código para que seja limpo e manutenível seguindo os padrões definidos no projeto.

**Como usar:**
> Revise e refatore toda a codebase de acordo com nossas diretrizes de codificação.

---

### web-coder

Engenheiro de desenvolvimento web expert com conhecimento abrangente de HTML, CSS, JavaScript, Web APIs, HTTP/HTTPS, segurança, performance e acessibilidade em todas as camadas da stack web.

**Como usar:**
> Me ajude a implementar uma política de CORS segura e Content Security Policy para minha aplicação web.

---

### web-design-reviewer

Realiza inspeção visual de sites rodando localmente ou remotamente usando automação de browser para detectar e corrigir problemas de design incluindo quebras de layout responsivo, violações de acessibilidade e inconsistências visuais.

**Como usar:**
> Revise o design da minha aplicação em <http://localhost:3000> e corrija problemas de layout ou acessibilidade.

---

## 🗄️ Banco de Dados & Tuning

### database-design

Princípios e tomada de decisão de design de banco de dados cobrindo design de schema, estratégia de indexação, seleção de ORM (Drizzle vs Prisma vs Kysely), seleção de banco (PostgreSQL vs Neon vs SQLite) e migrations seguras.

**Como usar:**
> Me ajude a desenhar o schema de banco de dados para uma aplicação SaaS multi-tenant.

---

### database-mcp

MCP server para exploração interativa, análise e documentação de bancos PostgreSQL e SQL Server. Gera diagramas ER, mapas de dados, catálogos de funções e mantém um índice `discovery-database.yml` sincronizado.

**Como usar:**
> Explore meu banco PostgreSQL e gere um diagrama ER e catálogo de dados.

---

### ef-core (tuning)

> Ver seção [Desenvolvimento → ef-core](#ef-core) — também abrange tuning de queries, migrations e padrões de consulta no contexto .NET.

---

### postgresql-code-review

Assistente de revisão de código específico para PostgreSQL com foco em operações JSONB, uso de arrays, tipos customizados, design de schema, otimização de funções, Row Level Security (RLS) e boas práticas exclusivas do PostgreSQL.

**Como usar:**
> Revise meu schema e queries PostgreSQL em busca de anti-padrões e boas práticas de RLS.

---

### postgresql-optimization

Assistente de desenvolvimento específico para PostgreSQL cobrindo recursos avançados: índices JSONB/GIN, operações com arrays, tipos range/geométricos, busca full-text, window functions e o ecossistema de extensões.

**Como usar:**
> Me ajude a otimizar esta query PostgreSQL que usa verificações de containment em JSONB.

---

### sql-code-review

Assistente universal de revisão de código SQL para todos os bancos (MySQL, PostgreSQL, SQL Server, Oracle) com foco em prevenção de SQL injection, controle de acesso, anti-padrões, padrões de código e proteção de dados.

**Como usar:**
> Revise minhas stored procedures SQL em busca de vulnerabilidades de segurança e problemas de manutenibilidade.

---

### sql-optimization

Assistente universal de otimização de performance SQL cobrindo ajuste de queries, estratégias de indexação, análise de plano de execução, paginação, operações em batch e monitoramento de performance em todos os principais bancos SQL.

**Como usar:**
> Otimize estas queries SQL lentas e sugira a estratégia de indexação adequada.

---

## 🧪 Testes

### csharp-mstest

Boas práticas para testes unitários com MSTest 3.x/4.x incluindo APIs de assertion modernas, testes parametrizados, classes de teste seladas, lifecycle hooks e o padrão Arrange-Act-Assert.

**Como usar:**
> Escreva testes unitários MSTest para minha classe Calculator seguindo boas práticas.

---

### csharp-nunit

Boas práticas para testes unitários com NUnit cobrindo testes padrão, testes parametrizados com `TestCase`/`TestCaseSource`, assertions com o modelo de constraints, setup/teardown e o padrão AAA.

**Como usar:**
> Escreva testes parametrizados NUnit para o serviço de processamento de pedidos.

---

### csharp-tunit

Boas práticas para testes unitários com TUnit (.NET 8+) incluindo testes parametrizados baseados em Arguments, assertions assíncronas fluentes, lifecycle hooks e gerenciamento de dependências com `DependsOn`.

**Como usar:**
> Escreva testes TUnit para meu módulo de processamento de pagamentos.

---

### csharp-xunit

Boas práticas para testes unitários com xUnit incluindo testes Fact/Theory, `InlineData`/`MemberData`/`ClassData` para cenários parametrizados, `IClassFixture` para contexto compartilhado e Fluent Assertions.

**Como usar:**
> Escreva testes xUnit para minha classe UserService usando Theory e InlineData.

---

### playwright

Automação de browser de propósito geral empacotada como Claude Code Plugin. Permite escrever e executar qualquer automação Playwright on-the-fly — de testes simples de página a fluxos complexos de múltiplas etapas. Usa browser visível por padrão para inspeção em tempo real.

**Como usar:**
> Automatize um fluxo de login e tire um screenshot do dashboard.

---

### playwright-automation-fill-in-form

Automatiza o preenchimento de um formulário Microsoft Forms específico usando o Playwright MCP server, navegando para a URL, preenchendo os campos e solicitando revisão do usuário antes de enviar.

**Como usar:**
> Automatize o preenchimento do formulário de inscrição em evento em <https://forms.microsoft.com/>... com os dados de hoje.

---

### playwright-explore-website

Explora um site usando o Playwright MCP server para identificar 3–5 funcionalidades ou fluxos principais, documenta elementos de UI e seus locators e propõe casos de teste baseados na exploração.

**Como usar:**
> Explore <https://meuapp.com> e identifique os principais fluxos de usuário para testar.

---

### playwright-generate-test

Gera um teste Playwright TypeScript baseado em um cenário fornecido executando as etapas uma a uma via Playwright MCP, salva o arquivo de teste e itera até que ele passe.

**Como usar:**
> Gere um teste Playwright para o fluxo de login e checkout no meu e-commerce.

---

### testing-patterns

Padrões e princípios de testes cobrindo a pirâmide de testes (unitário/integração/E2E), padrão AAA, estratégias de mock, isolamento de testes e quando usar cada tipo de teste.

**Como usar:**
> Quais padrões de teste devo usar para esta camada de integração com API?

---

### webapp-testing

Kit de ferramentas para testar e depurar aplicações web locais usando Playwright MCP ou ambiente Node.js local. Suporta verificação de UI, interação com formulários, captura de screenshots, inspeção de logs do console e verificações de design responsivo.

**Como usar:**
> Teste o formulário de login na minha aplicação em <http://localhost:3000> e verifique se ele trata credenciais inválidas corretamente.

---

## 📝 Documentação

### convert-plaintext-to-md

Converte arquivos de documentação em texto puro para Markdown formatado adequadamente. Suporta instruções explícitas, procedimentos de opção documentados ou um arquivo de referência convertido como guia.

**Como usar:**
> Converta este arquivo de release notes em texto puro para Markdown bem formatado.

---

### copilot-instructions-blueprint-generator

Gera um arquivo `copilot-instructions.md` abrangente analisando padrões reais da codebase para guiar o GitHub Copilot a produzir código consistente com as versões exatas de tecnologia, estilo arquitetural e padrões de qualidade do projeto.

**Como usar:**
> Gere um copilot-instructions.md para este projeto TypeScript/React.

---

### create-agentsmd

Cria um arquivo `AGENTS.md` completo e preciso na raiz do repositório seguindo a especificação pública agents.md, fornecendo aos agentes de codificação IA o contexto e as instruções necessárias sobre o projeto.

**Como usar:**
> Crie um arquivo AGENTS.md para este repositório.

---

### create-architectural-decision-record

Cria um documento ADR (Architectural Decision Record) estruturado com front matter, contexto, decisão, consequências, alternativas e partes interessadas, salvo no diretório `/docs/adr/`.

**Como usar:**
> Crie um ADR para nossa decisão de usar PostgreSQL em vez de MongoDB para o novo serviço.

---

### create-llms

Cria um novo arquivo `llms.txt` do zero na raiz do repositório seguindo a [especificação oficial llms.txt](https://llmstxt.org/), fornecendo aos LLMs um ponto de entrada estruturado para entender e navegar pelo repositório.

**Como usar:**
> Crie um arquivo llms.txt para este projeto seguindo a especificação llmstxt.org.

---

### create-readme

Cria um arquivo `README.md` abrangente e bem estruturado revisando todo o projeto, seguindo boas práticas de projetos open source, usando formatação GFM e admonitions do GitHub.

**Como usar:**
> Crie um README.md para este projeto.

---

### create-tldr-page

Cria páginas tldr concisas e acionáveis seguindo os padrões do projeto tldr-pages, buscando documentação autorizada e extraindo os padrões de comandos mais comuns.

**Como usar:**
> /create-tldr-page <https://docs.exemplo.com/cli> minha-ferramenta-cli

---

### documentacao-de-software

Especialista unificado em documentação de software (requisitos + técnica + governança) com investigação profunda de código, rastreabilidade entre artefatos, matriz de riscos, APF por requisito e validação cruzada. Produz documentação completa e sem ambiguidades.

**Como usar:**
> Documente os requisitos de software e a arquitetura técnica deste sistema.

---

### markdown-to-html

Converte arquivos Markdown para HTML usando marked.js ou scripts customizados, suportando arquivos únicos, conversões em lote, GFM/CommonMark e integração com sistemas de templates como Jekyll ou Hugo.

**Como usar:**
> Converta todos os meus arquivos de documentação Markdown para HTML usando marked.js.

---

### mkdocs-translations

Traduz toda a documentação MkDocs da pasta fonte em inglês para um idioma de destino especificado, preservando a estrutura de pastas e a formatação Markdown, com rastreamento automático de progresso.

**Como usar:**
> Traduza toda a documentação MkDocs para português brasileiro (pt-BR).

---

### oo-component-documentation

Cria ou atualiza documentação padronizada de componentes orientados a objetos usando um template compartilhado seguindo os padrões C4 Model, Arc42 e IEEE 1016, com diagramas Mermaid e referências de API baseadas no código real.

**Como usar:**
> Crie documentação para o componente OrderService a partir do seu código-fonte.

---

### readme-blueprint-generator

Gera um `README.md` abrangente escaneando arquivos do diretório `.github/copilot` (arquitetura, stack tecnológica, estrutura de pastas, etc.) e `copilot-instructions.md` para produzir documentação bem estruturada focada no desenvolvedor.

**Como usar:**
> Gere um README.md para este repositório baseado nos arquivos de documentação em .github/copilot.

---

### tldr-prompt

Cria resumos tldr concisos para arquivos de customização do GitHub Copilot (`.prompt.md`, `.agent.md`, `.instructions.md`), documentação de MCP server ou URLs, renderizando o resultado diretamente no chat no formato tldr-pages.

**Como usar:**
> Crie um resumo tldr para este arquivo .prompt.md para que eu saiba como usá-lo rapidamente.

---

## 🤖 IA & Agentes

### agent-governance

Padrões e técnicas para adicionar controles de governança, segurança e confiança a sistemas de agentes de IA. Cobre controles de acesso baseados em políticas, classificação semântica de intenções, trilhas de auditoria, rate limits e filtros de conteúdo para qualquer framework de agentes (PydanticAI, CrewAI, LangChain, AutoGen, etc.).

**Como usar:**
> Adicione controles de governança e segurança ao meu agente PydanticAI que chama APIs externas.

---

### agentic-eval

Padrões para avaliar e melhorar iterativamente as saídas de agentes de IA por meio de autocrítica, loops de reflexão, pipelines avaliador-otimizador e rubricas LLM-as-judge. Vai além da geração única para refinamento iterativo.

**Como usar:**
> Configure um loop avaliador-otimizador para melhorar a qualidade do código gerado pelo meu agente.

---

### copilot-sdk

Guia a construção de aplicações agênticas integrando o GitHub Copilot SDK em apps Python, TypeScript, Go ou .NET. Cobre tools customizadas, respostas em streaming, gerenciamento de sessão, conexões com MCP server e agentes customizados.

**Como usar:**
> Crie uma aplicação TypeScript que integra o Copilot como agente com tools customizadas.

---

### declarative-agents

Kit completo de desenvolvimento para agentes declarativos do Microsoft 365 Copilot com três fluxos (criação básica, design enterprise avançado, validação/otimização), suporte a TypeSpec e integração com o Microsoft 365 Agents Toolkit.

**Como usar:**
> Crie um agente declarativo básico do Microsoft 365 para suporte de helpdesk de TI.

---

### mcp-builder

Fornece princípios para construção de servidores MCP (Model Context Protocol), cobrindo design de tools, padrões de recursos, tipos de transporte (stdio, SSE, WebSocket) e boas práticas para servidores baseados em TypeScript.

**Como usar:**
> Me ajude a desenhar e construir um novo MCP server com tools para consultar nossa API interna.

---

### mcp-cli

Interface CLI para descoberta e chamada de tools de MCP server pela linha de comando. Fornece comandos para listar servidores, explorar tools com parâmetros, obter schemas JSON e executar chamadas de tools.

**Como usar:**
> mcp-cli filesystem — mostre todas as tools MCP de filesystem disponíveis e seus parâmetros.

---

### mcp-configure

Configura um MCP server Dataverse para o GitHub Copilot, verificando servidores existentes, interpretando URLs de ambiente e gravando a configuração no arquivo de config MCP global ou com escopo de projeto.

**Como usar:**
> Configure o MCP server Dataverse para minha org em <https://minhaorg.crm.dynamics.com> globalmente.

---

### mcp-copilot-studio-server-generator

Gera uma implementação completa de MCP server otimizada para integração com Microsoft Copilot Studio, seguindo os padrões de connector do Power Platform com HTTP streamable, conformidade de schema e JSON-RPC 2.0.

**Como usar:**
> Gere um MCP server compatível com Copilot Studio para consultar a API do nosso catálogo de produtos.

---

### mcp-create-adaptive-cards

Adiciona templates de resposta com Adaptive Cards (estáticos ou dinâmicos) a plugins de API baseados em MCP para apresentação visual de dados no Microsoft 365 Copilot.

**Como usar:**
> Adicione templates de Adaptive Card à resposta da tool GetBudgets do meu plugin MCP.

---

### mcp-create-declarative-agent

Cria um agente declarativo completo para o Microsoft 365 Copilot integrando um MCP server com autenticação, seleção de tools e configuração usando o Microsoft 365 Agents Toolkit.

**Como usar:**
> Crie um agente declarativo M365 Copilot conectado ao meu MCP server com autenticação OAuth 2.0.

---

### mcp-deploy-manage-agents

Guia o deploy e o gerenciamento de agentes declarativos baseados em MCP no centro de administração do Microsoft 365, com governança, atribuições de usuários/grupos, controles de conformidade e distribuição organizacional.

**Como usar:**
> Me ajude a fazer o deploy e governar meu agente Copilot declarativo em toda a organização.

---

### parallel-agents

Padrões de orquestração multi-agente para executar múltiplos agentes especializados em paralelo (segurança, performance, qualidade) ou em cadeias sequenciais quando as tarefas requerem diferentes expertises de domínio ou análise abrangente.

**Como usar:**
> Use agentes paralelos para analisar esta codebase em busca de segurança, performance e cobertura de testes simultaneamente.

---

## ☁️ Infraestrutura & Cloud

### appinsights-instrumentation

Instrumenta uma aplicação web ASP.NET Core ou Node.js para enviar dados de telemetria ao Azure Application Insights para melhor observabilidade. Cobre auto-instrumentação e instrumentação manual via Bicep ou Azure CLI.

**Como usar:**
> Adicione telemetria do Azure Application Insights à minha aplicação ASP.NET Core hospedada no Azure App Service.

---

### microsoft-docs

Skill de pesquisa para o ecossistema de tecnologias Microsoft que consulta a documentação oficial via Microsoft Learn MCP, Context7 e Aspire MCP, cobrindo Azure, .NET, M365, Agent Framework, VS Code, GitHub e muito mais.

**Como usar:**
> Encontre a documentação oficial para configurar o Azure Service Bus com Managed Identity em .NET.

---

## 🔧 DevOps & Git

### editorconfig

Gera um arquivo .editorconfig abrangente e orientado a boas práticas analisando as linguagens e tipos de arquivos do projeto, com uma explicação regra a regra para cada configuração.

**Como usar:**
> Gere um arquivo .editorconfig para meu monorepo TypeScript e C#.

---

### generate-custom-instructions-from-codebase

Analisa diferenças entre dois estados de projeto (branches, commits ou releases) para gerar instruções precisas de migração/evolução para o GitHub Copilot, permitindo aplicação consistente de padrões de transformação durante upgrades ou refatorações.

**Como usar:**
> Gere instruções de migração para o Copilot comparando os branches v1 e v2 deste projeto.

---

### gh-cli

Referência abrangente para o GitHub CLI (gh) cobrindo repositórios, issues, pull requests, Actions, projects, releases, gists, codespaces, organizações e extensões — todas as operações do GitHub pela linha de comando.

**Como usar:**
> Como eu crio um pull request e o vinculo a uma issue usando o GitHub CLI?

---

### git-commit

Analisa as mudanças staged e gera uma mensagem de commit padronizada no formato Conventional Commits com detecção automática de tipo/escopo, staging inteligente de arquivos e suporte a breaking changes e footers.

**Como usar:**
> /commit — crie um conventional commit para minhas mudanças staged.

---

### git-flow-branch-creator

Analisa o status e o diff do git para determinar inteligentemente o tipo de branch Git Flow adequado (feature, release, hotfix, etc.) e cria um nome de branch semântico seguindo o modelo Git Flow do nvie.

**Como usar:**
> Analise minhas mudanças e crie o branch Git Flow adequado para esta correção de bug.

---

### github-copilot-starter

Configura uma configuração completa e pronta para produção do GitHub Copilot para um novo projeto com base em sua stack tecnológica, criando copilot-instructions.md, arquivos de instrução de linguagem/testes/segurança e opcionalmente um copilot-setup-steps.yml.

**Como usar:**
> Configure uma configuração completa do GitHub Copilot para meu projeto Python/FastAPI.

---

### lint-and-validate

Procedimento automático de controle de qualidade que exige a execução de linting, verificação de tipos e auditorias de segurança após cada alteração de código. Cobre Node.js/TypeScript (ESLint, tsc) e Python (Ruff, Bandit, MyPy).

**Como usar:**
> Faça o lint e valide todos os meus arquivos TypeScript e corrija os erros.

---

### nuget-manager

Gerencia pacotes NuGet em projetos .NET usando dotnet CLI, aplicando fluxos de trabalho seguros para adicionar/remover pacotes e verificar a existência de versões antes de atualizar, incluindo suporte a gerenciamento centralizado de pacotes.

**Como usar:**
> Adicione Newtonsoft.Json 13.0.3 ao meu projeto e verifique primeiro se a versão existe no NuGet.

---

## ⚙️ Workflow & Produtividade

### copilot-cli-quickstart

Tutorial interativo passo a passo para aprender o GitHub Copilot CLI do zero. Oferece trilhas separadas para Desenvolvedor e Não-Desenvolvedor, além de Q&A sob demanda com uma persona de tutor encorajador.

**Como usar:**
> Inicie o tutorial do Copilot CLI — sou um desenvolvedor que não conhece a ferramenta.

---

### copilot-spaces

Aproveita o Copilot Spaces para trazer contexto específico do projeto (repositórios, arquivos, documentação, instruções) para as conversas. Suporta listar, carregar, criar, atualizar e gerenciar spaces via MCP tools ou REST API.

**Como usar:**
> Carregue o Copilot Space de arquitetura do meu time e responda perguntas baseadas em nossa documentação.

---

### copilot-usage-metrics

Recupera e exibe métricas de uso do GitHub Copilot (taxas de aceitação, usuários ativos, uso do chat) para organizações e empresas usando o GitHub CLI e a REST API, com suporte a datas específicas.

**Como usar:**
> Mostre as métricas de uso do Copilot na minha organização da semana passada.

---

### make-skill-template

Meta-skill para criar novas GitHub Copilot Agent Skills por meio de scaffold de pasta de skill, geração do SKILL.md com frontmatter adequado e adição opcional de diretórios de scripts, referências, assets e templates.

**Como usar:**
> Crie uma nova skill chamada kubernetes-helper para ajudar com deployments Kubernetes.

---

### memory-merger

Mescla lições maduras de um arquivo de memória de domínio em seu arquivo de instrução correspondente, garantindo preservação do conhecimento com redundância mínima em escopos globais ou de workspace.

**Como usar:**
> /memory-merger >prompt-engineering — mescle a memória de engenharia de prompts nas instruções.

---

### mentoring-juniors

Persona de mentoria socrática (Sensei) para desenvolvedores juniores e iniciantes em IA que guia por perguntas em vez de dar respostas diretas, usando dicas progressivas, técnicas de ensino e celebração de conquistas.

**Como usar:**
> Estou travado entendendo por que minha função async não retorna o valor correto — me ajude a entender.

---

### microsoft-skill-creator

Cria hybrid agent skills para tecnologias Microsoft pesquisando profundamente os tópicos via ferramentas Learn MCP e gerando uma skill que armazena o conhecimento essencial localmente enquanto habilita buscas dinâmicas mais profundas.

**Como usar:**
> Crie uma nova skill para Azure Container Apps usando a documentação mais recente do Microsoft Learn.

---

### notebooklm

Interage com notebooks do Google NotebookLM via automação de browser para consultar documentação com respostas baseadas em fontes e citações do Gemini, e gerenciar a biblioteca de notebooks.

**Como usar:**
> Pergunte ao meu NotebookLM em <https://notebooklm.google.com/notebook/abc123> — quais são os limites de rate da API?


---
