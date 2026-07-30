# TOC — Software Documentation

This document is the root index of the documentation structure and must be kept up to date whenever a new artifact is created, renamed, or removed.

## Official Structure

- `documentacao/matriz-risco-sistema.md`
- `documentacao/processo_unificado/artefatos_aprovados/documentacao_api/`
- `documentacao/processo_unificado/artefatos_aprovados/visao/`
- `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/`
- `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/wireframes/`
- `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/criterios/`
- `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/regras/`
- `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/estimativas/`
- `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_classes/`
- `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_integracao_de_sistemas/`
- `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_entidades_e_relacionamento/`
- `documentacao/processo_unificado/artefatos_aprovados/dicionario_de_dados/`
- `documentacao/processo_unificado/artefatos_aprovados/documentos_de_apoio/`

## Index by Artifact Type

### 1) API Documentation (`api-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/documentacao_api/`

- [`api-template.md`](./processo_unificado/artefatos_aprovados/documentacao_api/api-template.md) — base template for technical documentation of endpoints and services.

### 2) Vision (`vis-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/visao/`

- [`vis-template.md`](./processo_unificado/artefatos_aprovados/visao/vis-template.md) — base template for business vision, scope, and stakeholders.

### 3) Requirements (`req-`, `apf-req-`, and `apr_req-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/detalhamento_requisitos/`

- [`req-template.md`](./processo_unificado/artefatos_aprovados/detalhamento_requisitos/req-template.md) — base template for detailed requirement specification in a **single file**, with mandatory wireframe section for interfaces.
- [`tec-req-template.md`](./processo_unificado/artefatos_aprovados/detalhamento_requisitos/tec-req-template.md) — base template for the complete technical requirement document.
- [`apr_req-template.md`](./processo_unificado/artefatos_aprovados/detalhamento_requisitos/apr_req-template.md) — base template for formalizing requirement approval.

- For each requirement `req-XXXX-...md`, the following mandatory artifacts must exist:
  - `apf-req-XXXX.md` — function point analysis.
  - `tec/tec-req-XXXX-...md` — technical document.
  - `criterios/cri-req-XXXX-...md` — all Gherkin acceptance scenarios.
  - `estimativas/estimativa-req-XXXX-{YYYY-MM-DD-HHmmSS}.md` — change estimate.
- The **Functional Requirements** and **Business Rules** master documents reside in `regras/`:
  - [`regras/requisitos-funcionais.md`](./processo_unificado/artefatos_aprovados/detalhamento_requisitos/regras/requisitos-funcionais.md) — single source of truth for all FR (continuous global numbering).
  - [`regras/regras-negocios.md`](./processo_unificado/artefatos_aprovados/detalhamento_requisitos/regras/regras-negocios.md) — single source of truth for all BR (continuous global numbering).
- For interface requirements, wireframe images must be stored in `wireframes/`.

### 3.1) Global System Risk Matrix

- [`matriz-risco-sistema.md`](./matriz-risco-sistema.md) — unique system risk matrix. Must be updated with every requirement inclusion/change.

### 4) Class Diagram (`dcl-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_classes/`

- [`dcl-template.md`](./processo_unificado/artefatos_aprovados/diagrama_de_classes/dcl-template.md) — base template for class modeling and documentation.

### 5) System Integration (`min-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_integracao_de_sistemas/`

- [`min-template.md`](./processo_unificado/artefatos_aprovados/diagrama_de_integracao_de_sistemas/min-template.md) — base template for system integration flows.

### 6) DER (`der-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/diagrama_de_entidades_e_relacionamento/`

- [`der-template.md`](./processo_unificado/artefatos_aprovados/diagrama_de_entidades_e_relacionamento/der-template.md) — base template for entity-relationship model.

### 7) Data Dictionary (`did-`)

Directory: `documentacao/processo_unificado/artefatos_aprovados/dicionario_de_dados/`

- [`did-template.md`](./processo_unificado/artefatos_aprovados/dicionario_de_dados/did-template.md) — base template for field and data rule catalog.

## Naming Convention

| Document Type                             | Prefix         |
| ----------------------------------------- | -------------- |
| API Documentation                         | `api-`         |
| Vision Document                           | `vis-`         |
| Requirement Specification (business)      | `req-`         |
| Technical Requirement Document            | `tec-req-`     |
| Requirement FPA                           | `apf-req-`     |
| Complete Acceptance Criteria              | `cri-req-`     |
| Change Estimate                           | `estimativa-req-` |
| Requirement Approval                      | `apr_req-`     |
| Class Diagram                             | `dcl-`         |
| System Integration Diagram                | `min-`         |
| Entity Relationship Diagram (DER)         | `der-`         |
| Data Dictionary                           | `did-`         |

## Control

- **Last TOC update:** 06/01/2026
- **Responsible:** Documentation Team
- **Status:** Active
