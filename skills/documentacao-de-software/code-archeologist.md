# Code Archeologist

A deep-investigation skill for producing rich, structured knowledge from an existing codebase. The output must be so thorough that, armed only with it, a developer could fully recreate the system — including every validation rule, data flow, integration point, UI behavior, and design decision.

---

## When to Use This Skill

- User wants to "understand how the system works" before modifying it
- User needs to onboard a new developer with no prior knowledge
- User is refactoring and needs a complete map before touching code
- User needs to document a legacy or undocumented codebase
- User wants to reproduce or migrate a system to another stack
- User mentions MVC, REST API, monolith, microservices, SPA, or any app pattern

---

## Guiding Principle

> "Leave no stone unturned. Every file, every line of configuration, every hidden validation, every implicit convention is evidence. The goal is not to summarize — it is to reconstruct."

The artifact produced by this skill must enable **full reproduction** of the system. Vague statements like "handles authentication" are insufficient. The output must state _how_ (JWT? sessions? OAuth? what claims? what middleware? what errors are returned?).

---

## Phase 1 — Workspace Reconnaissance

Before reading any code, map the terrain.

### 1.1 Directory Structure

- List the full directory tree (at least 3 levels deep)
- Identify the architectural pattern: MVC, layered, hexagonal, microservices, monorepo, etc.
- Note any unusual or non-standard folder names
- Detect co-location patterns (e.g., tests next to source, styles next to components)

### 1.2 Technology Stack Identification

Scan for all configuration and manifest files:

| File                                                                                                                     | What it reveals                                              |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| `package.json` / `composer.json` / `pom.xml` / `*.csproj` / `go.mod` / `Gemfile` / `requirements.txt` / `pyproject.toml` | Runtime, framework, all dependencies and their versions      |
| `.env` / `.env.example` / `appsettings.json` / `config/`                                                                 | Environment variables, feature flags, external service names |
| `Dockerfile` / `docker-compose.yml`                                                                                      | Runtime environment, exposed ports, service topology         |
| `Makefile` / `justfile` / `taskfile.yml`                                                                                 | Build, test, and deploy commands                             |
| `*.config.js` / `vite.config.*` / `webpack.config.*` / `tsconfig.json`                                                   | Bundler, transpiler, alias paths, build targets              |
| `eslint*` / `.stylelintrc` / `prettier*` / `.editorconfig`                                                               | Code style and linting rules                                 |
| `*.sql` / `migrations/` / `schema.*`                                                                                     | Database schema and migration history                        |
| `openapi.yaml` / `swagger.*` / `graphql/*.graphql`                                                                       | API contracts                                                |
| `README.md` / `CONTRIBUTING.md` / `ARCHITECTURE.md`                                                                      | Human-written context — read these first                     |

### 1.3 Entry Points

Identify every entry point into the system:

- Web server bootstrapping (`main.go`, `index.js`, `Program.cs`, `manage.py`, `app.rb`, etc.)
- CLI commands
- Background jobs / cron / workers
- Event consumers (queues, pub/sub, webhooks)
- Exported modules (if a library)

---

## Phase 2 — Architecture Mapping

### 2.1 Layered Architecture Decomposition

For each identified layer, document its purpose, files, and responsibilities:

```
Presentation Layer    → controllers, views, templates, components, pages
Application Layer     → services, use cases, orchestrators, DTOs
Domain Layer          → models, entities, value objects, domain events, business rules
Infrastructure Layer  → repositories, adapters, ORM configs, external clients, cache, queues
Cross-cutting         → middlewares, guards, interceptors, logging, error handlers, auth
```

### 2.2 Module / Feature Decomposition

- List every business domain / feature module
- For each module: what data does it own? what does it expose? what does it depend on?
- Draw module dependency direction (which module imports which)

### 2.3 Configuration & Bootstrapping Flow

Document the startup sequence:

1. What is loaded first? (config, DI container, logger)
2. What middleware is registered and in what order?
3. What database connections are established?
4. What background workers are started?
5. What is the shutdown sequence?

---

## Phase 3 — Backend Investigation

### 3.1 Routing

For every route, capture:

| Method | Path            | Controller / Handler  | Auth required? | Roles / Permissions |
| ------ | --------------- | --------------------- | -------------- | ------------------- |
| GET    | /api/users      | UsersController#index | Yes            | admin               |
| POST   | /api/auth/login | AuthController#login  | No             | —                   |

- Include route parameter names and types
- Note any route-level middleware (rate limiting, CORS, caching)
- Note any route prefix conventions (versioning, subdomains)

### 3.2 Controllers / Handlers

For each controller, document:

- Injected dependencies
- Every action method: what it receives, what it validates, what service it calls, what it returns
- Response formats and status codes for success and every error case
- Authorization checks (which guard, which policy, which role)

### 3.3 Services / Use Cases

For each service, document:

- Constructor dependencies
- Every public method: business rule name, preconditions, steps, postconditions
- Complex business logic expressed in prose + pseudo-code
- Side effects (emails sent, events published, cache invalidated, files written)
- Transactional boundaries (what is atomic, what is eventual)

### 3.4 Data Access Layer

- ORM / query builder in use (Prisma, TypeORM, Eloquent, GORM, Entity Framework, SQLAlchemy, ActiveRecord, etc.)
- Every repository / DAO: what queries it runs, what indexes it relies on
- N+1 queries detected? Eager loading patterns?
- Raw SQL files or stored procedures

### 3.5 Database Schema (Full)

For every table/collection:

```
Table: orders
  id          UUID         PK, auto-generated
  user_id     UUID         FK → users.id, NOT NULL, indexed
  status      ENUM         ('pending','paid','shipped','cancelled')
  total_cents INT          NOT NULL, CHECK (total_cents > 0)
  created_at  TIMESTAMP    DEFAULT NOW()

Indexes: idx_orders_user_id, idx_orders_status_created_at
```

Include all constraints, foreign keys, default values, check constraints, and unique constraints.

### 3.6 Validations (Backend)

For every input object (DTO, form, request body, command):

- Every field: type, required/optional, min/max/length, regex, enum values, custom rules
- Cross-field rules (e.g., `end_date > start_date`)
- Database-level constraints (unique, FK integrity)
- Error messages returned for each rule violation (exact string if hardcoded)

### 3.7 Authentication & Authorization

- Auth mechanism: JWT, sessions, OAuth2, API keys, mTLS
- Token structure: claims, expiry, refresh strategy
- Session storage: in-memory, Redis, cookie, DB
- Every permission/role defined and what it allows
- How auth is enforced: middleware, decorator, policy, guard
- Token revocation strategy

### 3.8 External Integrations

For each external service / API:

- Service name and purpose
- SDK or HTTP client used
- Credentials source (env var name)
- Endpoints called, payloads sent, responses expected
- Error handling and retry policy
- Webhooks received (path, verification method, event types)

### 3.9 Background Jobs & Queues

For every job / worker:

- Name and purpose
- Trigger: cron schedule, event, queue
- Payload structure
- Steps executed
- Retry policy and failure handling
- Idempotency considerations

### 3.10 Caching Strategy

- Cache technology (Redis, Memcached, in-memory)
- What is cached (key pattern, TTL, invalidation trigger)
- Cache-aside vs write-through vs read-through

### 3.11 Error Handling

- Global error handler behavior
- Error types / exception hierarchy
- HTTP status codes per error type
- Error response format (schema)
- Logging strategy per error severity

---

## Phase 4 — Frontend Investigation

### 4.1 Framework & Rendering Strategy

- Framework: React, Vue, Angular, Svelte, Blade, Thymeleaf, ERB, etc.
- Rendering: SPA, SSR, SSG, MPA, islands architecture
- Routing: client-side (React Router, Vue Router) or server-side
- State management: Redux, Zustand, Pinia, Context API, NgRx, none

### 4.2 Page / Screen Inventory

For every page / route:

| Path       | Component / View | Purpose           | Auth required? | Data fetched   |
| ---------- | ---------------- | ----------------- | -------------- | -------------- |
| /login     | LoginPage        | Authenticate user | No             | —              |
| /dashboard | DashboardPage    | Show KPIs         | Yes            | GET /api/stats |

### 4.3 Component Architecture

- Component hierarchy for key screens (tree format)
- Smart vs dumb components distinction
- Shared / reusable components and their props/slots/events
- Layout components and slot structure

### 4.4 Data Fetching & API Communication

- HTTP client used (fetch, axios, react-query, SWR, Apollo, etc.)
- Base URL configuration
- Authentication header injection (interceptors, auth headers)
- Request/response interceptors for error handling
- Loading, error, and empty states per page
- Optimistic updates (if any)

### 4.5 Forms & Client-Side Validations

For every form:

- Library: react-hook-form, Formik, VeeValidate, Angular Reactive Forms, plain HTML5, etc.
- Every field: type, label, placeholder, required?, client-side rules
- Cross-field validations
- Submit behavior: endpoint called, method, payload mapped from form
- Error display strategy (inline, toast, modal)
- Success behavior (redirect, message, state update)

### 4.6 JavaScript / TypeScript Deep Dive

- Utility functions: purpose, inputs, outputs, edge cases
- Custom hooks / composables: what state or side-effects they manage
- Event handling: DOM events, custom events, global event bus
- Browser APIs used (localStorage, sessionStorage, IndexedDB, geolocation, etc.)
- Third-party scripts or SDKs loaded (analytics, chat, payments, maps)

### 4.7 State Management Details

For each piece of global state:

- Shape of the state (schema)
- Actions / mutations / reducers that modify it
- Which components subscribe to it
- Persistence strategy (survives page reload?)

### 4.8 Routing & Navigation

- Route definitions (path, component, guards, lazy-loaded?)
- Route guards: condition checked, redirect target
- Navigation after login/logout
- 404 and error boundary handling

---

## Phase 5 — Design & UI Layer

### 5.1 Design System / Styling

- CSS approach: plain CSS, CSS Modules, Tailwind, BEM, styled-components, SCSS
- Design tokens: color palette (all named colors + hex), spacing scale, typography scale
- Breakpoints and responsive strategy
- Dark/light mode support

### 5.2 Component Library

- Third-party UI library (MUI, Ant Design, Shadcn, Bootstrap, Vuetify, etc.)
- Version in use
- Customization approach (theme, CSS overrides)
- Custom components built on top

### 5.3 Layout Structure

- Grid system used
- Persistent navigation: topbar, sidebar, tabs
- Header/footer presence per layout
- Modal / drawer / overlay patterns

### 5.4 Accessibility (a11y)

- ARIA attributes used
- Keyboard navigation support
- Screen reader considerations
- Color contrast compliance notes

---

## Phase 6 — Infrastructure & DevOps

### 6.1 CI/CD Pipeline

- Platform: GitHub Actions, GitLab CI, Jenkins, CircleCI, etc.
- Stages: lint → test → build → deploy
- Environments: development, staging, production
- Deployment targets: Kubernetes, ECS, App Service, bare VM, Vercel, Netlify

### 6.2 Infrastructure as Code

- Terraform / Bicep / CloudFormation resources declared
- Key infrastructure: databases, queues, storage buckets, VPCs, CDN

### 6.3 Observability

- Logging library and log levels in use
- Metrics (Prometheus, CloudWatch, Datadog)
- Tracing (OpenTelemetry, Jaeger)
- Error tracking (Sentry, Rollbar)

---

## Phase 7 — Test Coverage Analysis

### 7.1 Test Inventory

| Type        | Framework                  | Location           | Coverage notes   |
| ----------- | -------------------------- | ------------------ | ---------------- |
| Unit        | Jest / pytest / xUnit      | src/\*_/_.test.ts  | Service layer    |
| Integration | Supertest / testcontainers | tests/integration/ | API routes       |
| E2E         | Playwright / Cypress       | e2e/               | Happy paths only |

### 7.2 Test Patterns

- Test data builders / factories
- Mocking strategy (jest.mock, unittest.mock, WireMock)
- Database reset strategy between tests
- Key test scenarios covered (happy path + main error paths)

---

## Phase 8 — Knowledge Artifact Output Format

After completing all phases, produce **one consolidated document** called `SYSTEM_KNOWLEDGE.md` (or present inline in chat for smaller systems) structured as:

```markdown
# System: <Name>

## 1. Technology Stack Summary

...

## 2. Architecture Overview

...

## 3. Module Map

...

## 4. Database Schema

...

## 5. API Endpoints (Full Reference)

...

## 6. Business Rules & Validations

...

## 7. Frontend: Screens, Components, Forms

...

## 8. State Management

...

## 9. Authentication & Authorization

...

## 10. External Integrations

...

## 11. Background Jobs

...

## 12. Infrastructure & Deployment

...

## 13. Test Coverage Summary

...

## 14. Design System

...

## 15. Known Gaps / Ambiguities

...
```

Every section must contain **specifics**, not generalities:

- ✅ "The `POST /api/orders` endpoint validates that `quantity` is an integer between 1 and 999, and that `product_id` references an existing non-archived product. Returns 422 with `{ error: 'INVALID_QUANTITY' }` if out of range."
- ❌ "Orders are validated before saving."

---

## Investigation Workflow (Step by Step)

```
1. Read README.md and any architecture docs first
2. Run Phase 1 (reconnaissance) — full directory tree + manifest files
3. Run Phase 2 (architecture) — identify layers and modules
4. Run Phase 3 (backend) — route by route, service by service
5. Run Phase 4 (frontend) — page by page, form by form
6. Run Phase 5 (design) — styling, components, layout
7. Run Phase 6 (infra) — CI/CD, cloud, observability
8. Run Phase 7 (tests) — what is tested and how
9. Compile Phase 8 output artifact
10. List all gaps or assumptions that require clarification
```

For large codebases, use parallel subagents per layer (backend agent, frontend agent, infra agent) and merge results.

---

## Quality Checklist (Before Delivering the Artifact)

- [ ] Every API endpoint documented with verbs, paths, auth, validations, and response shapes
- [ ] Every database table documented with columns, types, constraints, and indexes
- [ ] Every form documented with field-level validation rules
- [ ] Every external integration documented with credentials source, endpoints, and error handling
- [ ] Authentication and authorization rules fully described
- [ ] Business rules stated in plain language and traceable to code
- [ ] Component hierarchy of key screens documented
- [ ] State management shape and mutations documented
- [ ] Infrastructure and deployment pipeline documented
- [ ] All gaps and assumptions listed in "Known Gaps" section

---

## Tips for Hard-to-Read Codebases

- If there are no comments, read the tests — they are living documentation
- If there are no tests, read the database migrations — they reveal the domain's evolution
- If variable names are cryptic, check git history for the original intent
- Configuration files often contain feature flags and dead code indicators
- Look for `TODO`, `FIXME`, `HACK`, `DEPRECATED` comments — they reveal technical debt
- Check `package-lock.json` or `yarn.lock` for exact dependency versions used in production
- `.env.example` reveals every external service the system depends on
- Seed files and fixtures reveal what "normal" data looks like

---

## References

- [The Feynman Technique applied to code](https://en.wikipedia.org/wiki/Feynman_Technique) — if you can't explain it simply, you don't understand it yet
- [Architecture Decision Records (ADR)](https://adr.github.io/) — look for these in `docs/adr/` or `decisions/`
- [C4 Model](https://c4model.com/) — reference for structuring architecture diagrams in the output
